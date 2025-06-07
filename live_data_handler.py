import streamlit as st
from real_time_data import get_live_stock_data, get_industry_averages, get_company_cagr, financial_chatbot
import stock_data

def get_enhanced_stock_data(ticker):
    """
    Get enhanced stock data with real-time information
    """
    try:
        # Try live data first
        live_data = get_live_stock_data(ticker)
        if live_data.get('success'):
            return {
                'name': live_data['name'],
                'industry': live_data['industry'],
                'current_price': live_data['current_price'],
                'market_cap': live_data['market_cap'],
                'shares_outstanding': live_data['shares_outstanding'],
                'revenue': live_data['revenue'],
                'net_income': live_data['net_income'],
                'eps': live_data['net_income'] / live_data['shares_outstanding'] if live_data['shares_outstanding'] > 0 else 0,
                'book_value_per_share': live_data['market_cap'] / live_data['shares_outstanding'] if live_data['shares_outstanding'] > 0 else 0,
                'pe_ratio': live_data['pe_ratio'],
                'pb_ratio': live_data['pb_ratio'],
                'ps_ratio': live_data['market_cap'] / live_data['revenue'] if live_data['revenue'] > 0 else 0,
                'roe': live_data['roe'],
                'debt_to_equity': live_data['debt_to_equity'],
                'historical_growth': live_data.get('cagr_5y', 0),
                'last_updated': live_data['last_updated'],
                'is_live': True
            }
    except Exception as e:
        st.warning(f"Live data unavailable for {ticker}: {str(e)}")
    
    # Fallback to existing data
    fallback_data = stock_data.get_stock_data(ticker, use_cached=True)
    if fallback_data:
        fallback_data['is_live'] = False
        return fallback_data
    
    return None

def show_data_freshness_indicator(data):
    """
    Show indicator of data freshness
    """
    if data and data.get('is_live'):
        st.success("🔴 Live Data - Real-time market information")
    else:
        st.info("📊 Sample Data - For demonstration purposes")

def add_real_time_update_button(ticker):
    """
    Add button to refresh real-time data
    """
    if st.button(f"🔄 Refresh {ticker} Data", key=f"refresh_{ticker}"):
        # Force refresh by clearing any cache
        st.cache_data.clear()
        return True
    return False