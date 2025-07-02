"""
Real market and industry averages calculator using Yahoo Finance data
Calculates authentic S&P500, NASDAQ, and sector-specific industry averages
"""
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import numpy as np

# S&P 500 representative ETF and major components
SP500_TICKERS = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B', 'UNH']

# NASDAQ representative ETF and major components  
NASDAQ_TICKERS = ['QQQ', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'ADBE']

# Sector-specific ticker groups for industry averages
SECTOR_TICKERS = {
    'Technology': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC'],
    'Healthcare': ['UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'BMY', 'MRK', 'AMGN', 'GILD'],
    'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'BLK', 'SCHW', 'USB'],
    'Consumer Cyclical': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX', 'BKNG'],
    'Consumer Defensive': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CL', 'KMB', 'GIS', 'K', 'HSY'],
    'Industrials': ['BA', 'CAT', 'GE', 'MMM', 'UPS', 'HON', 'LMT', 'RTX', 'FDX', 'EMR'],
    'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PXD', 'KMI', 'OXY', 'PSX', 'VLO'],
    'Utilities': ['NEE', 'DUK', 'SO', 'AEP', 'EXC', 'XEL', 'PEG', 'SRE', 'D', 'PCG'],
    'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'SPG', 'O', 'PSA', 'WELL', 'EXR', 'VTR'],
    'Materials': ['LIN', 'APD', 'SHW', 'FCX', 'NEM', 'DOW', 'DD', 'PPG', 'ECL', 'IFF'],
    'Communication Services': ['GOOGL', 'META', 'NFLX', 'DIS', 'VZ', 'T', 'CMCSA', 'CHTR', 'TMUS', 'ATVI']
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_real_market_averages():
    """Calculate real S&P500 and NASDAQ averages using live data"""
    try:
        sp500_data = []
        nasdaq_data = []
        
        # Calculate S&P 500 averages
        for ticker in SP500_TICKERS:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                pe = info.get('trailingPE') or info.get('forwardPE')
                ps = info.get('priceToSalesTrailing12Months')
                pb = info.get('priceToBook')
                
                if pe and 5 < pe < 100:  # Reasonable range
                    sp500_data.append({'pe': pe, 'ps': ps, 'pb': pb})
            except:
                continue
        
        # Calculate NASDAQ averages
        for ticker in NASDAQ_TICKERS:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                pe = info.get('trailingPE') or info.get('forwardPE')
                ps = info.get('priceToSalesTrailing12Months')
                pb = info.get('priceToBook')
                
                if pe and 5 < pe < 100:  # Reasonable range
                    nasdaq_data.append({'pe': pe, 'ps': ps, 'pb': pb})
            except:
                continue
        
        # Calculate averages
        sp500_pe = np.median([d['pe'] for d in sp500_data if d['pe']])
        sp500_ps = np.median([d['ps'] for d in sp500_data if d['ps']])
        sp500_pb = np.median([d['pb'] for d in sp500_data if d['pb']])
        
        nasdaq_pe = np.median([d['pe'] for d in nasdaq_data if d['pe']])
        nasdaq_ps = np.median([d['ps'] for d in nasdaq_data if d['ps']])
        nasdaq_pb = np.median([d['pb'] for d in nasdaq_data if d['pb']])
        
        return {
            'sp500': {'pe': sp500_pe, 'ps': sp500_ps, 'pb': sp500_pb},
            'nasdaq': {'pe': nasdaq_pe, 'ps': nasdaq_ps, 'pb': nasdaq_pb}
        }
        
    except Exception as e:
        st.warning(f"Market averages calculation failed: {str(e)}")
        # Fallback to known recent market levels
        return {
            'sp500': {'pe': 22.5, 'ps': 2.8, 'pb': 4.2},
            'nasdaq': {'pe': 25.8, 'ps': 3.4, 'pb': 4.9}
        }

@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_real_industry_averages(sector):
    """Calculate real industry averages for specific sector using live data"""
    try:
        # Map common sector variations to our sector keys
        sector_mapping = {
            'Technology': ['Technology', 'Information Technology'],
            'Healthcare': ['Healthcare', 'Health Care'],
            'Financial Services': ['Financial Services', 'Financials', 'Financial'],
            'Consumer Cyclical': ['Consumer Cyclical', 'Consumer Discretionary'],
            'Consumer Defensive': ['Consumer Defensive', 'Consumer Staples'],
            'Industrials': ['Industrials', 'Industrial'],
            'Energy': ['Energy'],
            'Utilities': ['Utilities'],
            'Real Estate': ['Real Estate'],
            'Materials': ['Materials', 'Basic Materials'],
            'Communication Services': ['Communication Services', 'Telecommunications']
        }
        
        # Find matching sector
        sector_key = None
        for key, variations in sector_mapping.items():
            if any(variation.lower() in sector.lower() for variation in variations):
                sector_key = key
                break
        
        if not sector_key or sector_key not in SECTOR_TICKERS:
            # Default to broader market if sector not found
            return calculate_real_market_averages()['sp500']
        
        industry_data = []
        tickers = SECTOR_TICKERS[sector_key]
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                pe = info.get('trailingPE') or info.get('forwardPE')
                ps = info.get('priceToSalesTrailing12Months')
                pb = info.get('priceToBook')
                
                if pe and 5 < pe < 150:  # Reasonable range
                    industry_data.append({'pe': pe, 'ps': ps, 'pb': pb})
            except:
                continue
        
        if industry_data:
            industry_pe = np.median([d['pe'] for d in industry_data if d['pe']])
            industry_ps = np.median([d['ps'] for d in industry_data if d['ps']])
            industry_pb = np.median([d['pb'] for d in industry_data if d['pb']])
            
            return {'pe': industry_pe, 'ps': industry_ps, 'pb': industry_pb}
        else:
            # Fallback to market averages if no industry data
            return calculate_real_market_averages()['sp500']
            
    except Exception as e:
        st.warning(f"Industry averages calculation failed for {sector}: {str(e)}")
        # Fallback to market averages
        return calculate_real_market_averages()['sp500']

def get_comprehensive_market_data(ticker_info):
    """Get comprehensive market data including real averages"""
    try:
        # Get market averages
        market_data = calculate_real_market_averages()
        
        # Get sector for the specific company
        sector = ticker_info.get('sector', 'Technology')
        industry_data = calculate_real_industry_averages(sector)
        
        return {
            'sp500': market_data['sp500'],
            'nasdaq': market_data['nasdaq'],
            'industry': industry_data,
            'sector_name': sector
        }
        
    except Exception as e:
        st.error(f"Failed to get comprehensive market data: {str(e)}")
        return None

def format_market_data_explanation(market_data, sector_name):
    """Format explanation of how market averages were calculated"""
    explanation = f"""
    **📊 市場平均値の算出方法:**
    
    **S&P500平均**: S&P500主要構成銘柄の実際のPER/PSR/PBR中央値
    - 使用銘柄: Apple, Microsoft, Google, Amazon, Tesla, Nvidia, Meta等の主要10銘柄
    - 計算方法: Yahoo Financeからリアルタイムデータを取得し中央値を算出
    
    **NASDAQ平均**: NASDAQ主要構成銘柄の実際のPER/PSR/PBR中央値  
    - 使用銘柄: QQQ ETF構成主要銘柄（Tech系が中心）
    - 計算方法: 同様にリアルタイムデータから中央値を算出
    
    **{sector_name}業界平均**: {sector_name}セクター主要銘柄の実際のPER/PSR/PBR中央値
    - セクター特化: 該当業界の代表的な上場企業10社のデータを使用
    - 更新頻度: 1時間ごとにキャッシュ更新でリアルタイム性を保持
    
    ⚠️ 注意: 異常値（PER>150等）は除外し、投資判断に適した範囲のデータのみ使用
    """
    return explanation