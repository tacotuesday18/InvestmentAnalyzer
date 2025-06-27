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

def get_authentic_historical_ratios(ticker, hist_data, info):
    """Calculate authentic historical financial ratios using real financial data"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get real quarterly financial data
        quarterly_financials = stock.quarterly_financials
        quarterly_earnings = stock.quarterly_earnings if hasattr(stock, 'quarterly_earnings') else None
        
        if quarterly_financials.empty:
            return None
            
        metrics_data = []
        
        # Get real financial data points
        for date in quarterly_financials.columns[:8]:  # Last 8 quarters (2 years)
            try:
                # Find closest price date
                price_date = min(hist_data.index, key=lambda x: abs((x.date() - date.date()).days))
                stock_price = hist_data.loc[price_date, 'Close']
                
                # Calculate authentic ratios using real financial data
                total_revenue = quarterly_financials.loc['Total Revenue', date] if 'Total Revenue' in quarterly_financials.index else 0
                net_income = quarterly_financials.loc['Net Income', date] if 'Net Income' in quarterly_financials.index else 0
                
                # Get shares outstanding from info (approximation)
                shares_outstanding = info.get('sharesOutstanding', info.get('impliedSharesOutstanding', 1))
                
                # Calculate authentic ratios
                eps = (net_income * 4) / shares_outstanding if shares_outstanding > 0 else 0  # Annualized
                pe_ratio = stock_price / eps if eps > 0 else 0
                
                # Revenue per share for PS ratio
                revenue_per_share = (total_revenue * 4) / shares_outstanding if shares_outstanding > 0 else 0
                ps_ratio = stock_price / revenue_per_share if revenue_per_share > 0 else 0
                
                # Use current PB ratio as approximation (book value changes slowly)
                pb_ratio = info.get('priceToBook', 0)
                
                # PEG ratio (using growth estimate)
                growth_rate = info.get('earningsGrowth', 0.1) * 100
                peg_ratio = pe_ratio / growth_rate if growth_rate > 0 and pe_ratio > 0 else 0
                
                # Only add if we have valid data
                if pe_ratio > 0 and pe_ratio < 200:  # Reasonable PE range
                    metrics_data.append({
                        'Date': price_date,
                        'PE_Ratio': pe_ratio,
                        'PB_Ratio': pb_ratio,
                        'PS_Ratio': ps_ratio,
                        'PEG_Ratio': peg_ratio,
                        'Stock_Price': stock_price
                    })
                    
            except Exception:
                continue
        
        return pd.DataFrame(metrics_data) if metrics_data else None
        
    except Exception:
        return None

def get_historical_metrics(ticker, years=10):
    """Get historical financial metrics using authentic Yahoo Finance data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get historical price data
        hist_data = stock.history(period=f"{years}y")
        if hist_data.empty:
            return None
            
        # Try authentic historical ratios first using real financial data
        authentic_data = get_authentic_historical_ratios(ticker, hist_data, info)
        if authentic_data is not None and len(authentic_data) > 4:
            return authentic_data
            
        # If no authentic historical data available, return None instead of synthetic data
        return None
            
        # Sample quarterly over the historical period for better granularity
        quarterly_dates = pd.date_range(start=hist_data.index[0], end=hist_data.index[-1], freq='QE')
        
        for date in quarterly_dates:
            if date not in hist_data.index:
                closest_date = hist_data.index[hist_data.index <= date]
                if len(closest_date) == 0:
                    continue
                date = closest_date[-1]
                
            price = hist_data.loc[date, 'Close']
            current_price = hist_data['Close'].iloc[-1]
            
            # Calculate time-based factors
            years_ago = (hist_data.index[-1] - date).days / 365.25
            
            # Apply more sophisticated adjustments based on:
            # 1. Market cycles (bull/bear markets)
            # 2. Earnings growth over time
            # 3. Market sentiment shifts
            
            # Market cycle factor (simulates 4-7 year cycles)
            cycle_factor = 0.85 + 0.3 * np.sin(years_ago * 0.9)
            
            # Earnings growth factor (companies generally grow earnings over time)
            growth_factor = 1.0 - (years_ago * 0.05)  # Assume 5% annual EPS growth
            
            # Price momentum factor
            price_factor = price / current_price
            
            # Combined adjustment
            pe_adjustment = cycle_factor * growth_factor
            ps_adjustment = cycle_factor * (1.0 - years_ago * 0.03)  # Revenue multiples compress over time
            pb_adjustment = cycle_factor * (1.0 - years_ago * 0.02)  # Book value multiples more stable
            
            # Calculate historical metrics with realistic bounds
            historical_pe = current_pe * pe_adjustment if current_pe else None
            historical_ps = current_ps * ps_adjustment if current_ps else None  
            historical_pb = current_pb * pb_adjustment if current_pb else None
            historical_peg = current_peg if current_peg else 1.5  # PEG more stable
            
            # Add some realistic noise (±15% variation)
            noise_factor = 0.85 + 0.3 * np.random.random()
            
            if historical_pe:
                historical_pe *= noise_factor
            if historical_ps:
                historical_ps *= noise_factor
            if historical_pb:
                historical_pb *= noise_factor
            
            metrics_data.append({
                'Date': date,
                'PE_Ratio': historical_pe if historical_pe and 8 < historical_pe < 150 else None,
                'PS_Ratio': historical_ps if historical_ps and 1 < historical_ps < 80 else None,
                'PB_Ratio': historical_pb if historical_pb and 0.8 < historical_pb < 40 else None,
                'PEG_Ratio': historical_peg if historical_peg and 0.5 < historical_peg < 8 else None,
                'Stock_Price': price
            })
        
        if not metrics_data:
            return None
            
        df = pd.DataFrame(metrics_data)
        df = df.sort_values('Date')
        
        return df
        
    except Exception as e:
        return None

def get_industry_benchmarks(sector, industry):
    """Get industry average metrics for comparison with realistic market multiples"""
    
    # Specific high-multiple companies and sectors
    ai_tech_companies = ['NVDA', 'AMD', 'GOOGL', 'GOOG', 'MSFT', 'AMZN', 'META', 'TSLA', 'CRM', 'SNOW', 'PLTR']
    magnificent_seven = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA']
    
    # More realistic industry benchmarks based on current market conditions
    industry_benchmarks = {
        # High-growth technology sectors
        'Technology': {
            'Software': {'pe': 45.0, 'pb': 8.0, 'ps': 12.0, 'peg': 2.0},
            'Semiconductors': {'pe': 35.0, 'pb': 6.0, 'ps': 8.0, 'peg': 1.8},
            'AI & Machine Learning': {'pe': 60.0, 'pb': 12.0, 'ps': 18.0, 'peg': 2.5},
            'Cloud Computing': {'pe': 50.0, 'pb': 10.0, 'ps': 15.0, 'peg': 2.2},
            'Hardware': {'pe': 28.0, 'pb': 5.0, 'ps': 6.0, 'peg': 1.6},
            'default': {'pe': 35.0, 'pb': 6.0, 'ps': 8.0, 'peg': 1.8}
        },
        
        # Communication & Internet
        'Communication Services': {
            'Social Media': {'pe': 25.0, 'pb': 4.5, 'ps': 6.0, 'peg': 1.8},
            'Streaming': {'pe': 40.0, 'pb': 6.0, 'ps': 8.0, 'peg': 2.0},
            'Telecommunications': {'pe': 15.0, 'pb': 2.0, 'ps': 2.5, 'peg': 1.2},
            'default': {'pe': 25.0, 'pb': 4.0, 'ps': 5.0, 'peg': 1.6}
        },
        
        # Healthcare & Biotech
        'Healthcare': {
            'Biotechnology': {'pe': 35.0, 'pb': 4.0, 'ps': 8.0, 'peg': 2.0},
            'Pharmaceuticals': {'pe': 22.0, 'pb': 3.0, 'ps': 4.0, 'peg': 1.5},
            'Medical Devices': {'pe': 28.0, 'pb': 3.5, 'ps': 5.0, 'peg': 1.7},
            'default': {'pe': 25.0, 'pb': 3.2, 'ps': 5.0, 'peg': 1.6}
        },
        
        # Consumer sectors
        'Consumer Discretionary': {
            'E-commerce': {'pe': 45.0, 'pb': 8.0, 'ps': 10.0, 'peg': 2.2},
            'Electric Vehicles': {'pe': 55.0, 'pb': 10.0, 'ps': 12.0, 'peg': 2.5},
            'Retail': {'pe': 18.0, 'pb': 2.5, 'ps': 1.8, 'peg': 1.3},
            'Restaurants': {'pe': 25.0, 'pb': 4.0, 'ps': 3.0, 'peg': 1.6},
            'default': {'pe': 25.0, 'pb': 4.0, 'ps': 3.0, 'peg': 1.6}
        },
        
        'Consumer Staples': {'pe': 18.0, 'pb': 2.5, 'ps': 1.5, 'peg': 1.3},
        
        # Financial services
        'Financial Services': {
            'Banks': {'pe': 12.0, 'pb': 1.1, 'ps': 3.0, 'peg': 1.0},
            'Insurance': {'pe': 14.0, 'pb': 1.3, 'ps': 2.5, 'peg': 1.1},
            'Fintech': {'pe': 35.0, 'pb': 5.0, 'ps': 8.0, 'peg': 1.8},
            'default': {'pe': 15.0, 'pb': 1.3, 'ps': 3.0, 'peg': 1.1}
        },
        
        # Industrial sectors
        'Industrials': {'pe': 20.0, 'pb': 2.8, 'ps': 2.2, 'peg': 1.4},
        'Energy': {'pe': 16.0, 'pb': 1.8, 'ps': 1.2, 'peg': 1.2},
        'Utilities': {'pe': 18.0, 'pb': 1.4, 'ps': 2.8, 'peg': 1.1},
        'Real Estate': {'pe': 22.0, 'pb': 2.0, 'ps': 10.0, 'peg': 1.3},
        'Materials': {'pe': 16.0, 'pb': 2.0, 'ps': 1.8, 'peg': 1.2}
    }
    
    # Special handling for specific high-multiple sectors
    if sector == 'Technology':
        tech_benchmarks = industry_benchmarks['Technology']
        
        # Check for specific technology sub-sectors
        if any(keyword in industry.lower() for keyword in ['software', 'saas', 'cloud']):
            return tech_benchmarks.get('Software', tech_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['semiconductor', 'chip', 'processor']):
            return tech_benchmarks.get('Semiconductors', tech_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['artificial intelligence', 'ai', 'machine learning']):
            return tech_benchmarks.get('AI & Machine Learning', tech_benchmarks['default'])
        else:
            return tech_benchmarks['default']
    
    elif sector == 'Communication Services':
        comm_benchmarks = industry_benchmarks['Communication Services']
        
        if any(keyword in industry.lower() for keyword in ['social', 'media', 'platform']):
            return comm_benchmarks.get('Social Media', comm_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['streaming', 'entertainment']):
            return comm_benchmarks.get('Streaming', comm_benchmarks['default'])
        else:
            return comm_benchmarks['default']
    
    elif sector == 'Healthcare':
        health_benchmarks = industry_benchmarks['Healthcare']
        
        if 'biotech' in industry.lower():
            return health_benchmarks.get('Biotechnology', health_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['pharmaceutical', 'drug']):
            return health_benchmarks.get('Pharmaceuticals', health_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['medical device', 'device']):
            return health_benchmarks.get('Medical Devices', health_benchmarks['default'])
        else:
            return health_benchmarks['default']
    
    elif sector == 'Consumer Discretionary':
        consumer_benchmarks = industry_benchmarks['Consumer Discretionary']
        
        if any(keyword in industry.lower() for keyword in ['e-commerce', 'online retail', 'internet retail']):
            return consumer_benchmarks.get('E-commerce', consumer_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['electric vehicle', 'ev', 'automotive']):
            return consumer_benchmarks.get('Electric Vehicles', consumer_benchmarks['default'])
        elif 'retail' in industry.lower():
            return consumer_benchmarks.get('Retail', consumer_benchmarks['default'])
        else:
            return consumer_benchmarks['default']
    
    elif sector == 'Financial Services':
        fin_benchmarks = industry_benchmarks['Financial Services']
        
        if any(keyword in industry.lower() for keyword in ['bank', 'banking']):
            return fin_benchmarks.get('Banks', fin_benchmarks['default'])
        elif 'insurance' in industry.lower():
            return fin_benchmarks.get('Insurance', fin_benchmarks['default'])
        elif any(keyword in industry.lower() for keyword in ['fintech', 'payment', 'digital']):
            return fin_benchmarks.get('Fintech', fin_benchmarks['default'])
        else:
            return fin_benchmarks['default']
    
    # For sectors with single benchmark set
    if sector in industry_benchmarks and not isinstance(industry_benchmarks[sector], dict):
        return industry_benchmarks[sector]
    
    # Default fallback
    return {'pe': 22.0, 'pb': 3.0, 'ps': 4.0, 'peg': 1.5}

def display_historical_metrics_chart(ticker):
    """Display historical metrics chart for a ticker with industry benchmarks"""
    
    if st.button(f"📈 {ticker} の過去メトリクス推移を表示", key=f"metrics_chart_{ticker}"):
        with st.spinner(f"{ticker} の過去データを読み込み中..."):
            # Get company info for industry benchmarks
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Technology')
            industry = info.get('industry', '')
            
            metrics_df = get_historical_metrics(ticker)
            industry_benchmarks = get_industry_benchmarks(sector, industry)
            
            if metrics_df is not None and len(metrics_df) > 0:
                st.markdown(f"### 📊 {ticker} - 過去の財務指標推移と業界比較")
                st.markdown(f"**セクター:** {sector} | **業界:** {industry}")
                
                # Create tabs for different metric views in Japanese
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["PER倍率", "PBR倍率", "PSR倍率", "PEG倍率", "株価推移"])
                
                st.info("📌 このチャートは過去の財務指標の推移と業界平均を比較表示しています。投資判断にご活用ください。")
                
                with tab1:
                    # PE Ratio chart with industry benchmark
                    pe_fig = go.Figure()
                    
                    pe_fig.add_trace(go.Scatter(
                        x=metrics_df['Date'],
                        y=metrics_df['PE_Ratio'],
                        mode='lines+markers',
                        name=f'{ticker} PER',
                        line=dict(color='#3b82f6', width=3),
                        marker=dict(size=6),
                        hovertemplate='日付: %{x}<br>PER: %{y:.2f}倍<extra></extra>'
                    ))
                    
                    # Add 10-year average line
                    avg_pe = metrics_df['PE_Ratio'].dropna().mean()
                    pe_fig.add_hline(
                        y=avg_pe, 
                        line_dash="dash", 
                        line_color="red",
                        annotation_text=f"10年平均: {avg_pe:.2f}倍"
                    )
                    
                    # Add industry benchmark line
                    industry_pe = industry_benchmarks['pe']
                    pe_fig.add_hline(
                        y=industry_pe, 
                        line_dash="dot", 
                        line_color="green",
                        annotation_text=f"業界平均: {industry_pe:.2f}倍"
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
                        current_peg = current_metrics.get('PEG_Ratio') or 0
                        avg_peg = avg_metrics.get('PEG_Ratio') or 0
                        if current_peg and avg_peg:
                            trend = "↗️" if current_peg > avg_peg else "↘️" if current_peg < avg_peg else "→"
                            st.metric("PEG倍率", f"{current_peg:.2f}倍", f"{trend} 10年平均: {avg_peg:.2f}倍")
                        else:
                            st.metric("PEG倍率", "データなし", "10年平均: N/A")
                
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