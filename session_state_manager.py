"""
Centralized session state manager for maintaining analysis results across page interactions
"""

import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    # Fundamental analysis state
    if 'fundamental_analysis_completed' not in st.session_state:
        st.session_state.fundamental_analysis_completed = False
    if 'fundamental_current_ticker' not in st.session_state:
        st.session_state.fundamental_current_ticker = "AAPL"
    if 'fundamental_analysis_report' not in st.session_state:
        st.session_state.fundamental_analysis_report = ""
    if 'fundamental_company_info' not in st.session_state:
        st.session_state.fundamental_company_info = {}
    
    # Earnings analysis state
    if 'earnings_analysis_completed' not in st.session_state:
        st.session_state.earnings_analysis_completed = False
    if 'earnings_current_ticker' not in st.session_state:
        st.session_state.earnings_current_ticker = "AAPL"
    if 'earnings_data' not in st.session_state:
        st.session_state.earnings_data = {}
    
    # Comparison analysis state
    if 'comparison_analysis_completed' not in st.session_state:
        st.session_state.comparison_analysis_completed = False
    if 'comparison_selected_tickers' not in st.session_state:
        st.session_state.comparison_selected_tickers = []
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = {}

def reset_fundamental_analysis():
    """Reset fundamental analysis state"""
    st.session_state.fundamental_analysis_completed = False
    st.session_state.fundamental_analysis_report = ""
    st.session_state.fundamental_company_info = {}

def reset_earnings_analysis():
    """Reset earnings analysis state"""
    st.session_state.earnings_analysis_completed = False
    st.session_state.earnings_data = {}

def reset_comparison_analysis():
    """Reset comparison analysis state"""
    st.session_state.comparison_analysis_completed = False
    st.session_state.comparison_results = {}

def should_reset_fundamental_analysis(new_ticker):
    """Check if fundamental analysis should be reset for new ticker"""
    return new_ticker != st.session_state.fundamental_current_ticker

def should_reset_earnings_analysis(new_ticker):
    """Check if earnings analysis should be reset for new ticker"""
    return new_ticker != st.session_state.earnings_current_ticker

def should_reset_comparison_analysis(new_tickers):
    """Check if comparison analysis should be reset for new tickers"""
    return set(new_tickers) != set(st.session_state.comparison_selected_tickers)

def get_search_input_key(page_name):
    """Get unique search input key for each page"""
    return f"{page_name}_search_input"

def maintain_search_input(page_name, default_value=""):
    """Maintain search input across page interactions"""
    key = get_search_input_key(page_name)
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]

def update_search_input(page_name, value):
    """Update search input for a specific page"""
    key = get_search_input_key(page_name)
    st.session_state[key] = value