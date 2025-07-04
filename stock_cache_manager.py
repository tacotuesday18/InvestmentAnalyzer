"""
Enhanced stock data caching system for improved performance
"""
import streamlit as st
import pandas as pd
import pickle
import hashlib
from datetime import datetime, timedelta
import os

class StockDataCache:
    def __init__(self, cache_duration_hours=6):
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache_dir = "stock_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, ticker):
        """Generate cache key for ticker"""
        return hashlib.md5(ticker.encode()).hexdigest()
    
    def _get_cache_path(self, ticker):
        """Get cache file path for ticker"""
        cache_key = self._get_cache_key(ticker)
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    
    def get_cached_data(self, ticker):
        """Get cached stock data if available and fresh"""
        try:
            cache_path = self._get_cache_path(ticker)
            if not os.path.exists(cache_path):
                return None
            
            with open(cache_path, 'rb') as f:
                cached_item = pickle.load(f)
            
            # Check if cache is still valid
            if datetime.now() - cached_item['timestamp'] < self.cache_duration:
                return cached_item['data']
            else:
                # Remove expired cache
                os.remove(cache_path)
                return None
        except Exception:
            return None
    
    def cache_data(self, ticker, data):
        """Cache stock data"""
        try:
            cache_path = self._get_cache_path(ticker)
            cached_item = {
                'timestamp': datetime.now(),
                'data': data
            }
            with open(cache_path, 'wb') as f:
                pickle.dump(cached_item, f)
        except Exception:
            pass  # Fail silently if caching fails
    
    def clear_cache(self):
        """Clear all cached data"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.pkl'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except Exception:
            pass

# Global cache instance
stock_cache = StockDataCache()

def get_cached_financial_data(ticker):
    """Get financial data with caching support"""
    from auto_financial_data import get_auto_financial_data
    
    # Try cache first
    cached_data = stock_cache.get_cached_data(ticker)
    if cached_data:
        return cached_data
    
    # Fetch fresh data
    data = get_auto_financial_data(ticker)
    if data:
        # Cache the data
        stock_cache.cache_data(ticker, data)
    
    return data

def batch_process_stocks(tickers, callback=None, batch_size=20):
    """Process stocks in batches with progress callback"""
    results = []
    total_batches = len(tickers) // batch_size + (1 if len(tickers) % batch_size > 0 else 0)
    
    for batch_idx in range(total_batches):
        batch_start = batch_idx * batch_size
        batch_end = min((batch_idx + 1) * batch_size, len(tickers))
        batch_tickers = tickers[batch_start:batch_end]
        
        batch_results = []
        for ticker in batch_tickers:
            try:
                data = get_cached_financial_data(ticker)
                if data:
                    batch_results.append(data)
            except Exception:
                continue
        
        results.extend(batch_results)
        
        # Call progress callback if provided
        if callback:
            callback(batch_idx + 1, total_batches, len(results))
    
    return results