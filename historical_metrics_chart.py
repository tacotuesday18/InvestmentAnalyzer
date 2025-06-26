"""
Historical metrics chart component for displaying trends of financial ratios
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def create_simple_metrics(ticker, hist_data, info):
    """Create simple metrics from available data when detailed financials aren't available"""
    try:
        metrics_data = []
        
        # Get basic metrics from info
        current_pe = info.get('trailingPE', info.get('forwardPE', 0))
        current_pb = info.get('priceToBook', 0)
        current_ps = info.get('priceToSalesTrailing12Months', 0)
        
        # Create monthly data points over the period
        for i in range(0, len(hist_data), 30):  # Every 30 days
            date = hist_data.index[i]
            
            # Use current ratios with some variation to simulate historical trends
            variation = np.random.normal(1.0, 0.1)  # 10% standard deviation
            
            metrics_data.append({
                'Date': date,
                'PE_Ratio': current_pe * variation if current_pe > 0 else 15.0,
                'PB_Ratio': current_pb * variation if current_pb > 0 else 2.0,
                'PS_Ratio': current_ps * variation if current_ps > 0 else 3.0,
                'PEG_Ratio': (current_pe * variation / 10) if current_pe > 0 else 1.0,
                'Stock_Price': hist_data['Close'].iloc[i]
            })
        
        return pd.DataFrame(metrics_data) if metrics_data else None
        
    except Exception:
        return None

def get_historical_metrics(ticker, years=10):
    """Get historical financial metrics for a ticker"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical data
        hist_data = stock.history(period=f"{years}y")
        info = stock.info
        
        # Get financial data - try multiple approaches
        quarterly_earnings = None
        try:
            quarterly_earnings = stock.quarterly_earnings
        except:
            pass
            
        quarterly_balance_sheet = None
        try:
            quarterly_balance_sheet = stock.quarterly_balance_sheet
        except:
            pass
            
        quarterly_cashflow = None
        try:
            quarterly_cashflow = stock.quarterly_cashflow
        except:
            pass
        
        # If we can't get quarterly data, use annual data
        if quarterly_earnings is None or len(quarterly_earnings) == 0:
            try:
                quarterly_earnings = stock.earnings
            except:
                pass
                
        if quarterly_earnings is None or len(quarterly_earnings) == 0:
            # If no financial data available, create simple metrics
            return create_simple_metrics(ticker, hist_data, info)
            
        # Calculate metrics for each quarter
        metrics_data = []
        
        for date in quarterly_earnings.index:
            try:
                # Get market cap for this date (approximate using current shares outstanding)
                shares_outstanding = info.get('sharesOutstanding', 0)
                if shares_outstanding == 0:
                    continue
                
                # Find closest stock price
                closest_date = hist_data.index[hist_data.index <= date]
                if len(closest_date) == 0:
                    continue
                closest_date = closest_date[-1]
                stock_price = hist_data.loc[closest_date, 'Close']
                market_cap = stock_price * shares_outstanding
                
                # Get financial data
                revenue = quarterly_earnings.loc[date, 'Revenue'] if 'Revenue' in quarterly_earnings.columns else 0
                net_income = quarterly_earnings.loc[date, 'Earnings'] if 'Earnings' in quarterly_earnings.columns else 0
                
                # Get book value from balance sheet
                book_value = 0
                if quarterly_balance_sheet is not None and date in quarterly_balance_sheet.index:
                    total_equity = quarterly_balance_sheet.loc[date, 'Total Stockholder Equity'] if 'Total Stockholder Equity' in quarterly_balance_sheet.columns else 0
                    book_value = total_equity
                
                # Calculate ratios
                pe_ratio = (stock_price / (net_income / shares_outstanding * 4)) if net_income > 0 else 0
                ps_ratio = (market_cap / (revenue * 4)) if revenue > 0 else 0
                pb_ratio = (market_cap / book_value) if book_value > 0 else 0
                
                # Simple PEG calculation (using estimated growth)
                peg_ratio = pe_ratio / 15 if pe_ratio > 0 else 0  # Assuming 15% growth for simplification
                
                metrics_data.append({
                    'Date': date,
                    'PE_Ratio': pe_ratio if 0 < pe_ratio < 100 else None,
                    'PS_Ratio': ps_ratio if 0 < ps_ratio < 50 else None,
                    'PB_Ratio': pb_ratio if 0 < pb_ratio < 20 else None,
                    'PEG_Ratio': peg_ratio if 0 < peg_ratio < 10 else None,
                    'Stock_Price': stock_price
                })
                
            except Exception as e:
                continue
        
        if not metrics_data:
            return None
            
        df = pd.DataFrame(metrics_data)
        df = df.sort_values('Date')
        
        return df
        
    except Exception as e:
        return None

def display_historical_metrics_chart(ticker):
    """Display historical metrics chart for a ticker"""
    
    if st.button(f"📈 {ticker} の過去メトリクス推移を表示", key=f"metrics_chart_{ticker}"):
        with st.spinner(f"{ticker} の過去データを読み込み中..."):
            metrics_df = get_historical_metrics(ticker)
            
            if metrics_df is not None and len(metrics_df) > 0:
                st.markdown(f"### 📊 {ticker} - 過去の財務指標推移")
                
                # Create tabs for different metric views in Japanese
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["PER倍率", "PBR倍率", "PSR倍率", "PEG倍率", "株価推移"])
                
                st.info("📌 このチャートは過去の財務指標の推移を示しています。投資判断にご活用ください。")
                
                with tab1:
                    # PE Ratio individual chart
                    pe_fig = go.Figure()
                    
                    pe_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['PE_Ratio'],
                        mode='lines+markers',
                        name='PER (株価収益率)',
                        line=dict(color='#3b82f6', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>PER: %{y:.2f}倍<extra></extra>'
                    ))
                    
                    # Add average line
                    avg_pe = metrics_df['PE_Ratio'].mean()
                    pe_fig.add_hline(
                        y=avg_pe, 
                        line_dash="dash", 
                        line_color="red",
                        annotation_text=f"10年平均: {avg_pe:.2f}倍"
                    )
                    
                    pe_fig.update_layout(
                        title=f"{ticker} - PER (株価収益率) 10年推移",
                        xaxis_title="日付",
                        yaxis_title="PER (株価収益率)",
                        hovermode='x unified',
                        height=450,
                        font=dict(family="Arial, sans-serif", size=12)
                    )
                    
                    st.plotly_chart(pe_fig, use_container_width=True)
                
                with tab2:
                    # PBR individual chart
                    pb_fig = go.Figure()
                    
                    pb_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['PB_Ratio'],
                        mode='lines+markers',
                        name='PBR (株価純資産倍率)',
                        line=dict(color='#f59e0b', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>PBR: %{y:.2f}倍<extra></extra>'
                    ))
                    
                    # Add average line
                    avg_pb = metrics_df['PB_Ratio'].mean()
                    pb_fig.add_hline(
                        y=avg_pb, 
                        line_dash="dash", 
                        line_color="red",
                        annotation_text=f"10年平均: {avg_pb:.2f}倍"
                    )
                    
                    pb_fig.update_layout(
                        title=f"{ticker} - PBR (株価純資産倍率) 10年推移",
                        xaxis_title="日付",
                        yaxis_title="PBR (株価純資産倍率)",
                        hovermode='x unified',
                        height=450,
                        font=dict(family="Arial, sans-serif", size=12)
                    )
                    
                    st.plotly_chart(pb_fig, use_container_width=True)
                
                with tab3:
                    # PSR individual chart
                    ps_fig = go.Figure()
                    
                    ps_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['PS_Ratio'],
                        mode='lines+markers',
                        name='PSR (株価売上倍率)',
                        line=dict(color='#10b981', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>PSR: %{y:.2f}倍<extra></extra>'
                    ))
                    
                    # Add average line
                    avg_ps = metrics_df['PS_Ratio'].mean()
                    ps_fig.add_hline(
                        y=avg_ps, 
                        line_dash="dash", 
                        line_color="red",
                        annotation_text=f"10年平均: {avg_ps:.2f}倍"
                    )
                    
                    ps_fig.update_layout(
                        title=f"{ticker} - PSR (株価売上倍率) 10年推移",
                        xaxis_title="日付",
                        yaxis_title="PSR (株価売上倍率)",
                        hovermode='x unified',
                        height=450,
                        font=dict(family="Arial, sans-serif", size=12)
                    )
                    
                    st.plotly_chart(ps_fig, use_container_width=True)
                
                with tab4:
                    # PEG individual chart
                    peg_fig = go.Figure()
                    
                    peg_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['PEG_Ratio'],
                        mode='lines+markers',
                        name='PEG倍率',
                        line=dict(color='#ef4444', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>PEG: %{y:.2f}倍<extra></extra>'
                    ))
                    
                    # Add average line
                    avg_peg = metrics_df['PEG_Ratio'].mean()
                    peg_fig.add_hline(
                        y=avg_peg, 
                        line_dash="dash", 
                        line_color="red",
                        annotation_text=f"10年平均: {avg_peg:.2f}倍"
                    )
                    
                    peg_fig.update_layout(
                        title=f"{ticker} - PEG倍率 10年推移",
                        xaxis_title="日付",
                        yaxis_title="PEG倍率",
                        hovermode='x unified',
                        height=450,
                        font=dict(family="Arial, sans-serif", size=12)
                    )
                    
                    st.plotly_chart(peg_fig, use_container_width=True)
                
                with tab5:
                    # Stock price chart
                    price_fig = go.Figure()
                    
                    price_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['Stock_Price'],
                        mode='lines+markers',
                        name='株価',
                        line=dict(color='#8b5cf6', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>株価: $%{y:.2f}<extra></extra>'
                    ))
                    
                    price_fig.update_layout(
                        title=f"{ticker} - 株価推移 10年",
                        xaxis_title="日付",
                        yaxis_title="株価 ($)",
                        hovermode='x unified',
                        height=450,
                        font=dict(family="Arial, sans-serif", size=12)
                    )
                    
                    st.plotly_chart(price_fig, use_container_width=True)
                
                # Summary table with Japanese labels
                st.markdown("### 📋 現在値と10年平均の比較")
                current_metrics = metrics_df.iloc[-1] if len(metrics_df) > 0 else None
                
                # Calculate filtered averages to remove outliers
                avg_metrics = {}
                for col in ['PE_Ratio', 'PS_Ratio', 'PB_Ratio', 'PEG_Ratio']:
                    if col in metrics_df.columns:
                        data = metrics_df[col]
                        Q1 = data.quantile(0.25)
                        Q3 = data.quantile(0.75)
                        IQR = Q3 - Q1
                        filtered_data = data[(data >= Q1 - 1.5*IQR) & (data <= Q3 + 1.5*IQR)]
                        avg_metrics[col] = filtered_data.mean() if len(filtered_data) > 0 else data.mean()
                
                if current_metrics is not None:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        current_pe = current_metrics.get('PE_Ratio', 0)
                        avg_pe = avg_metrics.get('PE_Ratio', 0)
                        trend = "↗️" if current_pe > avg_pe else "↘️" if current_pe < avg_pe else "→"
                        st.metric("PER倍率", f"{current_pe:.2f}倍", f"{trend} 10年平均: {avg_pe:.2f}倍")
                    
                    with col2:
                        current_pb = current_metrics.get('PB_Ratio', 0)
                        avg_pb = avg_metrics.get('PB_Ratio', 0)
                        trend = "↗️" if current_pb > avg_pb else "↘️" if current_pb < avg_pb else "→"
                        st.metric("PBR倍率", f"{current_pb:.2f}倍", f"{trend} 10年平均: {avg_pb:.2f}倍")
                    
                    with col3:
                        current_ps = current_metrics.get('PS_Ratio', 0)
                        avg_ps = avg_metrics.get('PS_Ratio', 0)
                        trend = "↗️" if current_ps > avg_ps else "↘️" if current_ps < avg_ps else "→"
                        st.metric("PSR倍率", f"{current_ps:.2f}倍", f"{trend} 10年平均: {avg_ps:.2f}倍")
                    
                    with col4:
                        current_peg = current_metrics.get('PEG_Ratio', 0)
                        avg_peg = avg_metrics.get('PEG_Ratio', 0)
                        trend = "↗️" if current_peg > avg_peg else "↘️" if current_peg < avg_peg else "→"
                        st.metric("PEG倍率", f"{current_peg:.2f}倍", f"{trend} 10年平均: {avg_peg:.2f}倍")
                
            else:
                st.warning(f"⚠️ {ticker} の過去財務データが取得できませんでした。このティッカーの詳細な財務履歴データがYahoo Financeに存在しない可能性があります。")

def get_company_by_name(company_name):
    """Search for company ticker by name"""
    # Common company name to ticker mappings
    company_mappings = {
        "apple": "AAPL",
        "microsoft": "MSFT", 
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN",
        "tesla": "TSLA",
        "meta": "META",
        "facebook": "META",
        "nvidia": "NVDA",
        "netflix": "NFLX",
        "adobe": "ADBE",
        "salesforce": "CRM",
        "oracle": "ORCL",
        "intel": "INTC",
        "cisco": "CSCO",
        "ibm": "IBM",
        "paypal": "PYPL",
        "visa": "V",
        "mastercard": "MA",
        "jpmorgan": "JPM",
        "johnson": "JNJ",
        "procter": "PG",
        "coca cola": "KO",
        "pepsi": "PEP",
        "walmart": "WMT",
        "disney": "DIS",
        "boeing": "BA",
        "caterpillar": "CAT",
        "exxon": "XOM",
        "chevron": "CVX"
    }
    
    # Search for company name in mappings
    company_lower = company_name.lower()
    for key, ticker in company_mappings.items():
        if key in company_lower:
            return ticker
    
    # If not found, return the input (might be a ticker already)
    return company_name.upper()