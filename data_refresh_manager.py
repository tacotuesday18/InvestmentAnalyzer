import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class DataRefreshManager:
    """Manages real-time data refreshing across the application"""
    
    def __init__(self):
        self.cache_duration = 300  # 5 minutes cache
        
    def get_live_stock_price(self, ticker):
        """Get current stock price using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                return float(hist['Close'][-1])
        except Exception as e:
            st.error(f"Error fetching price for {ticker}: {e}")
        return None
    
    def get_comprehensive_stock_data(self, ticker):
        """Get comprehensive stock data including financials"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get financial statements
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            
            # Extract key metrics
            data = {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'revenue': info.get('totalRevenue', 0),
                'net_income': 0,
                'eps': info.get('trailingEps', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'industry': info.get('industry', 'Unknown'),
                'sector': info.get('sector', 'Unknown'),
                'last_updated': datetime.now().isoformat()
            }
            
            # Calculate additional metrics from financial statements
            if not financials.empty and 'Net Income' in financials.index:
                data['net_income'] = financials.loc['Net Income'].iloc[0]
            
            if not financials.empty and 'Total Revenue' in financials.index:
                data['revenue'] = financials.loc['Total Revenue'].iloc[0]
            
            # Calculate PS ratio
            if data['market_cap'] > 0 and data['revenue'] > 0:
                data['ps_ratio'] = data['market_cap'] / data['revenue']
            else:
                data['ps_ratio'] = 0
            
            return data
            
        except Exception as e:
            st.error(f"Error fetching comprehensive data for {ticker}: {e}")
            return None
    
    def refresh_all_prices(self, tickers):
        """Refresh prices for multiple tickers"""
        updated_prices = {}
        progress_bar = st.progress(0)
        
        for i, ticker in enumerate(tickers):
            price = self.get_live_stock_price(ticker)
            if price:
                updated_prices[ticker] = price
            progress_bar.progress((i + 1) / len(tickers))
        
        progress_bar.empty()
        return updated_prices
    
    def show_market_status(self):
        """Show current market status"""
        now = datetime.now()
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        if market_open <= now <= market_close and now.weekday() < 5:
            st.success("🟢 Market is OPEN - Live data available")
        else:
            st.info("🔴 Market is CLOSED - Showing last available prices")

# Global instance
data_manager = DataRefreshManager()