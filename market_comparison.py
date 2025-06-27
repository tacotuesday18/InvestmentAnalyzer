"""
Market comparison utilities for comparing stocks with major indices
"""

import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

def get_market_indices_data(period="1y"):
    """Get historical data for major market indices"""
    try:
        # Fetch data for major indices
        nasdaq = yf.Ticker("^IXIC")  # NASDAQ Composite
        sp500 = yf.Ticker("^GSPC")   # S&P 500
        
        nasdaq_data = nasdaq.history(period=period)
        sp500_data = sp500.history(period=period)
        
        return {
            'nasdaq': nasdaq_data,
            'sp500': sp500_data
        }
    except Exception as e:
        st.error(f"市場指数データの取得エラー: {e}")
        return None

def normalize_price_data(data, base_date=None):
    """Normalize price data to percentage change from base date"""
    if base_date is None:
        base_date = data.index[0]
    
    base_price = data.loc[base_date, 'Close']
    normalized = ((data['Close'] - base_price) / base_price) * 100
    return normalized

def create_stock_vs_market_chart(ticker, period="1y"):
    """Create a comparison chart of stock vs major market indices"""
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period=period)
        stock_info = stock.info
        company_name = stock_info.get('longName', ticker)
        
        # Get market indices data
        indices_data = get_market_indices_data(period)
        
        if indices_data is None or stock_data.empty:
            st.error("データの取得に失敗しました")
            return None
        
        # Normalize all data to the same starting point
        start_date = max(
            stock_data.index[0],
            indices_data['nasdaq'].index[0],
            indices_data['sp500'].index[0]
        )
        
        # Filter data to common date range
        stock_filtered = stock_data[stock_data.index >= start_date]
        nasdaq_filtered = indices_data['nasdaq'][indices_data['nasdaq'].index >= start_date]
        sp500_filtered = indices_data['sp500'][indices_data['sp500'].index >= start_date]
        
        # Normalize data
        stock_normalized = normalize_price_data(stock_filtered, start_date)
        nasdaq_normalized = normalize_price_data(nasdaq_filtered, start_date)
        sp500_normalized = normalize_price_data(sp500_filtered, start_date)
        
        # Create comparison chart
        fig = go.Figure()
        
        # Add stock price
        fig.add_trace(go.Scatter(
            x=stock_normalized.index,
            y=stock_normalized.values,
            mode='lines',
            name=f'{ticker} ({company_name})',
            line=dict(color='#1f77b4', width=3),
            hovertemplate=f'{ticker}: %{{y:.2f}}%<extra></extra>'
        ))
        
        # Add NASDAQ
        fig.add_trace(go.Scatter(
            x=nasdaq_normalized.index,
            y=nasdaq_normalized.values,
            mode='lines',
            name='NASDAQ Composite',
            line=dict(color='#ff7f0e', width=2),
            hovertemplate='NASDAQ: %{y:.2f}%<extra></extra>'
        ))
        
        # Add S&P 500
        fig.add_trace(go.Scatter(
            x=sp500_normalized.index,
            y=sp500_normalized.values,
            mode='lines',
            name='S&P 500',
            line=dict(color='#2ca02c', width=2),
            hovertemplate='S&P 500: %{y:.2f}%<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=f'{company_name} ({ticker}) vs 主要市場指数 - パフォーマンス比較',
            xaxis_title='日付',
            yaxis_title='リターン (%)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
        
        return fig
        
    except Exception as e:
        st.error(f"チャート作成エラー: {e}")
        return None

def display_stock_market_comparison(ticker, period="1y"):
    """Display stock vs market comparison chart"""
    
    period_options = {
        "1ヶ月": "1mo",
        "3ヶ月": "3mo", 
        "6ヶ月": "6mo",
        "1年": "1y",
        "2年": "2y",
        "5年": "5y"
    }
    
    selected_period_jp = st.selectbox(
        "比較期間を選択:",
        options=list(period_options.keys()),
        index=3,  # Default to 1年
        key=f"market_comparison_period_{ticker}"
    )
    
    selected_period = period_options[selected_period_jp]
    
    with st.spinner(f"{ticker}と市場指数を比較中..."):
        chart = create_stock_vs_market_chart(ticker, selected_period)
        
        if chart:
            st.plotly_chart(chart, use_container_width=True)
            
            # Add performance summary
            try:
                stock = yf.Ticker(ticker)
                stock_data = stock.history(period=selected_period)
                indices_data = get_market_indices_data(selected_period)
                
                if not stock_data.empty and indices_data:
                    # Calculate returns
                    stock_return = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
                    nasdaq_return = ((indices_data['nasdaq']['Close'].iloc[-1] - indices_data['nasdaq']['Close'].iloc[0]) / indices_data['nasdaq']['Close'].iloc[0]) * 100
                    sp500_return = ((indices_data['sp500']['Close'].iloc[-1] - indices_data['sp500']['Close'].iloc[0]) / indices_data['sp500']['Close'].iloc[0]) * 100
                    
                    # Display performance summary
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            label=f"{ticker} リターン",
                            value=f"{stock_return:+.2f}%",
                            delta=None
                        )
                    
                    with col2:
                        st.metric(
                            label="NASDAQ リターン",
                            value=f"{nasdaq_return:+.2f}%",
                            delta=f"{stock_return - nasdaq_return:+.2f}% vs NASDAQ"
                        )
                    
                    with col3:
                        st.metric(
                            label="S&P 500 リターン", 
                            value=f"{sp500_return:+.2f}%",
                            delta=f"{stock_return - sp500_return:+.2f}% vs S&P 500"
                        )
                        
            except Exception as e:
                st.warning("パフォーマンス統計の計算中にエラーが発生しました")

def create_individual_stock_comparison_chart(tickers, period="1y"):
    """Create comparison chart for multiple individual stocks"""
    try:
        if not tickers or len(tickers) < 2:
            st.warning("比較には最低2つの銘柄が必要です")
            return None
            
        fig = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        # Get common date range
        start_dates = []
        stock_data = {}
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period=period)
                if not data.empty:
                    stock_data[ticker] = data
                    start_dates.append(data.index[0])
            except:
                continue
        
        if not stock_data:
            st.error("有効なデータを取得できませんでした")
            return None
            
        common_start = max(start_dates)
        
        # Normalize and plot each stock
        for i, (ticker, data) in enumerate(stock_data.items()):
            try:
                # Get company name
                stock_info = yf.Ticker(ticker).info
                company_name = stock_info.get('shortName', ticker)
                
                # Filter and normalize data
                filtered_data = data[data.index >= common_start]
                normalized = normalize_price_data(filtered_data, common_start)
                
                fig.add_trace(go.Scatter(
                    x=normalized.index,
                    y=normalized.values,
                    mode='lines',
                    name=f'{ticker} ({company_name})',
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate=f'{ticker}: %{{y:.2f}}%<extra></extra>'
                ))
            except:
                continue
        
        # Update layout
        fig.update_layout(
            title='個別銘柄パフォーマンス比較',
            xaxis_title='日付',
            yaxis_title='リターン (%)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left", 
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
        
        return fig
        
    except Exception as e:
        st.error(f"比較チャート作成エラー: {e}")
        return None