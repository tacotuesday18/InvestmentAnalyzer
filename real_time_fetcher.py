import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_current_stock_price(ticker):
    """Fetch current stock price from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            current_price = float(data['Close'].iloc[-1])
            return {
                'price': current_price,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
    except Exception as e:
        st.warning(f"Live data unavailable for {ticker}: {str(e)}")
    
    return {'success': False}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_comprehensive_data(ticker):
    """Fetch comprehensive financial data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get current price
        hist = stock.history(period="1d")
        current_price = float(hist['Close'].iloc[-1]) if not hist.empty else 0
        
        # Get financials
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        
        # Extract revenue and net income
        revenue = 0
        net_income = 0
        
        if not financials.empty:
            if 'Total Revenue' in financials.index:
                revenue = float(financials.loc['Total Revenue'].iloc[0])
            if 'Net Income' in financials.index:
                net_income = float(financials.loc['Net Income'].iloc[0])
        
        data = {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'current_price': current_price,
            'market_cap': info.get('marketCap', 0),
            'revenue': revenue,
            'net_income': net_income,
            'eps': info.get('trailingEps', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
            'roe': (info.get('returnOnEquity', 0) * 100) if info.get('returnOnEquity') else 0,
            'shares_outstanding': info.get('sharesOutstanding', 0),
            'industry': info.get('industry', 'Unknown'),
            'sector': info.get('sector', 'Unknown'),
            'last_updated': datetime.now().isoformat(),
            'is_live': True
        }
        
        return data
        
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def show_live_price_indicator(ticker, price_data):
    """Show live price with indicator"""
    if price_data.get('success'):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.metric(
                label=f"{ticker} Stock Price",
                value=f"${price_data['price']:.2f}",
                delta="Live"
            )
        with col2:
            st.success("🔴 LIVE")
        with col3:
            if st.button("🔄 Refresh", key=f"refresh_{ticker}"):
                st.cache_data.clear()
                st.rerun()
    else:
        st.warning(f"Live price unavailable for {ticker}")

def display_market_status():
    """Display current market status"""
    now = datetime.now()
    
    # US market hours (9:30 AM - 4:00 PM ET)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    if market_open <= now <= market_close and now.weekday() < 5:
        st.success("🟢 US Market OPEN - Live data streaming")
    else:
        st.info("🔴 US Market CLOSED - Showing last traded prices")