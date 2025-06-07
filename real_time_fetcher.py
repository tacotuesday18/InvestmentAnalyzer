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
        cashflow = stock.cashflow
        
        # Extract revenue and net income (in millions)
        revenue = 0
        net_income = 0
        
        if not financials.empty:
            try:
                if 'Total Revenue' in financials.index:
                    revenue = float(financials.loc['Total Revenue'].iloc[0]) / 1_000_000  # Convert to millions
                elif 'Revenue' in financials.index:
                    revenue = float(financials.loc['Revenue'].iloc[0]) / 1_000_000
                
                if 'Net Income' in financials.index:
                    net_income = float(financials.loc['Net Income'].iloc[0]) / 1_000_000  # Convert to millions
            except:
                pass
        
        # Get book value
        book_value = 0
        if not balance_sheet.empty:
            try:
                if 'Total Stockholder Equity' in balance_sheet.index:
                    book_value = float(balance_sheet.loc['Total Stockholder Equity'].iloc[0]) / 1_000_000
                elif 'Stockholders Equity' in balance_sheet.index:
                    book_value = float(balance_sheet.loc['Stockholders Equity'].iloc[0]) / 1_000_000
            except:
                pass
        
        # Calculate book value per share
        shares_outstanding = info.get('sharesOutstanding', 0)
        book_value_per_share = (book_value * 1_000_000) / shares_outstanding if shares_outstanding > 0 else 0
        
        data = {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'current_price': current_price,
            'market_cap': info.get('marketCap', 0) / 1_000_000 if info.get('marketCap') else 0,  # Convert to millions
            'revenue': revenue,  # Already in millions
            'net_income': net_income,  # Already in millions
            'eps': info.get('trailingEps', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
            'roe': (info.get('returnOnEquity', 0) * 100) if info.get('returnOnEquity') else 0,
            'shares_outstanding': shares_outstanding / 1_000_000 if shares_outstanding else 0,  # Convert to millions
            'book_value_per_share': book_value_per_share,
            'industry': info.get('industry', 'Unknown'),
            'sector': info.get('sector', 'Unknown'),
            'country': info.get('country', 'US'),
            'last_updated': datetime.now().isoformat(),
            'is_live': True,
            'historical_growth': calculate_revenue_growth(stock),
            'profit_margin': (net_income / revenue * 100) if revenue > 0 else 0
        }
        
        return data
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def calculate_revenue_growth(stock):
    """Calculate historical revenue growth rate"""
    try:
        financials = stock.financials
        if financials.empty or len(financials.columns) < 2:
            return 5.0  # Default growth rate
        
        # Get revenue data for last 2 years
        revenue_current = None
        revenue_previous = None
        
        for col_idx in range(min(2, len(financials.columns))):
            if 'Total Revenue' in financials.index:
                if col_idx == 0:
                    revenue_current = float(financials.loc['Total Revenue'].iloc[col_idx])
                elif col_idx == 1:
                    revenue_previous = float(financials.loc['Total Revenue'].iloc[col_idx])
        
        if revenue_current and revenue_previous and revenue_previous > 0:
            growth_rate = ((revenue_current - revenue_previous) / revenue_previous) * 100
            return max(-50, min(50, growth_rate))  # Cap between -50% and 50%
        
        return 5.0  # Default growth rate
        
    except Exception:
        return 5.0  # Default growth rate

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