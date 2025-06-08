import streamlit as st

def clear_all_caches():
    """Clear all Streamlit caches and session state to prevent data persistence issues"""
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        
        # Clear all session state except essential keys
        essential_keys = ['authentication_status', 'username', 'name']
        keys_to_delete = [key for key in st.session_state.keys() if key not in essential_keys]
        
        for key in keys_to_delete:
            del st.session_state[key]
            
        return True
    except Exception as e:
        st.error(f"Cache clearing error: {e}")
        return False

def get_cache_key(ticker, data_type):
    """Generate unique cache key for ticker-specific data"""
    return f"{ticker}_{data_type}_{hash(ticker + data_type)}"