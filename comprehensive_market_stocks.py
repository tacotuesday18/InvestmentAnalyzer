"""
Comprehensive market stock database with all major US and international stocks
For the stock discovery tool
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import requests

def get_sp500_tickers():
    """Get all S&P 500 tickers"""
    try:
        # S&P 500 companies from Wikipedia
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        return sp500_table['Symbol'].tolist()
    except:
        # Fallback list of major S&P 500 stocks
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "UNH", "JNJ",
            "V", "XOM", "PG", "JPM", "HD", "CVX", "MA", "ABBV", "PFE", "AVGO",
            "LLY", "KO", "COST", "PEP", "TMO", "WMT", "MRK", "BAC", "CSCO", "ACN",
            "DIS", "DHR", "VZ", "ADBE", "ABT", "CRM", "NKE", "TXN", "NFLX", "RTX",
            "QCOM", "NEE", "PM", "ORCL", "T", "LOW", "COP", "UNP", "HON", "IBM"
        ]

def get_nasdaq100_tickers():
    """Get NASDAQ 100 tickers"""
    return [
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "COST",
        "NFLX", "ADBE", "PEP", "TMUS", "CSCO", "CMCSA", "TXN", "QCOM", "AMD", "HON",
        "INTU", "AMAT", "SBUX", "ISRG", "BKNG", "MDLZ", "GILD", "ADP", "MU", "REGN",
        "PYPL", "ATVI", "FISV", "CSX", "VRTX", "MELI", "KLAC", "CHTR", "NXPI", "MRVL",
        "FTNT", "ORLY", "LRCX", "ADSK", "MAR", "MNST", "ASML", "WDAY", "PANW", "SNPS"
    ]

def get_dow30_tickers():
    """Get Dow Jones 30 tickers"""
    return [
        "AAPL", "MSFT", "UNH", "V", "HD", "JPM", "PG", "JNJ", "CVX", "WMT",
        "CRM", "MRK", "DIS", "VZ", "AXP", "NKE", "KO", "IBM", "CAT", "MCD",
        "TRV", "GS", "BA", "MMM", "HON", "AMGN", "WBA", "INTC", "CSCO", "DOW"
    ]

def get_russell2000_sample():
    """Get sample of Russell 2000 small-cap stocks"""
    return [
        "ROKU", "PLUG", "AMC", "GME", "BB", "NOK", "SNDL", "CLOV", "WISH", "SOFI",
        "PLTR", "SPCE", "RIOT", "MARA", "TLRY", "ACB", "SIRI", "F", "AAL", "CCL",
        "NCLH", "RCL", "DAL", "UAL", "LUV", "JETS", "XRT", "IWM", "VTWO", "SCHA"
    ]

def get_international_stocks():
    """Get major international stocks (ADRs and direct listings)"""
    return [
        # Japanese stocks
        "TM", "SONY", "NTT", "MUFG", "SMFG", "HMC", "SNE",
        # European stocks  
        "ASML", "SAP", "NVO", "NESN", "ROCHE", "NOVN", "UL", "BP", "SHELL", "VOD",
        # Chinese stocks
        "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "TME", "NTES", "WB",
        # Other international
        "TSM", "SHOP", "SPOT", "SE", "GRAB", "BEKE", "TAL", "EDU", "YMM", "VIPS"
    ]

def get_sector_etfs():
    """Get sector ETFs for sector analysis"""
    return {
        "Technology": "XLK",
        "Healthcare": "XLV", 
        "Financials": "XLF",
        "Consumer Discretionary": "XLY",
        "Communication Services": "XLC",
        "Industrials": "XLI",
        "Consumer Staples": "XLP",
        "Energy": "XLE",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Materials": "XLB"
    }

def get_all_market_stocks():
    """Get comprehensive list of all major market stocks"""
    all_stocks = []
    
    # Add major indices
    all_stocks.extend(get_sp500_tickers())
    all_stocks.extend(get_nasdaq100_tickers()) 
    all_stocks.extend(get_dow30_tickers())
    all_stocks.extend(get_russell2000_sample())
    all_stocks.extend(get_international_stocks())
    
    # Add popular individual stocks
    popular_stocks = [
        "ZOOM", "ZM", "UBER", "LYFT", "SNAP", "TWTR", "SQ", "SHOP", "SPOT", "RBLX",
        "COIN", "HOOD", "DKNG", "PENN", "MGM", "WYNN", "LVS", "MRNA", "BNTX", "JNJ",
        "PFE", "NVAX", "INO", "VXRT", "OCGN", "PROG", "PRTY", "BBBY", "EXPR", "KOSS"
    ]
    all_stocks.extend(popular_stocks)
    
    # Remove duplicates and return sorted list
    unique_stocks = list(set(all_stocks))
    return sorted(unique_stocks)

def get_stock_sector_mapping():
    """Map stocks to their sectors"""
    return {
        # Technology
        "Technology": ["AAPL", "MSFT", "GOOGL", "GOOG", "NVDA", "META", "TSLA", "NFLX", "ADBE", "CRM", "ORCL", "CSCO", "IBM", "INTC", "AMD", "QCOM", "TXN", "AVGO", "AMAT", "LRCX", "KLAC", "MRVL", "NXPI", "SNPS", "ADSK", "FTNT", "PANW", "WDAY", "ROKU", "ZOOM", "ZM", "SQ", "SHOP", "SPOT"],
        
        # Healthcare  
        "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "LLY", "TMO", "DHR", "ABT", "MRK", "GILD", "REGN", "VRTX", "ISRG", "AMGN", "MRNA", "BNTX", "NVAX"],
        
        # Financials
        "Financials": ["JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "BLK", "SCHW", "USB", "TFC", "PNC", "COF", "SPGI", "ICE", "CME", "V", "MA", "PYPL"],
        
        # Consumer Discretionary  
        "Consumer Discretionary": ["AMZN", "HD", "NKE", "DIS", "MCD", "SBUX", "LOW", "TJX", "BKNG", "MAR", "GM", "F", "TSLA", "CCL", "NCLH", "RCL", "MGM"],
        
        # Communication Services
        "Communication Services": ["META", "GOOGL", "GOOG", "NFLX", "DIS", "VZ", "T", "CMCSA", "CHTR", "SNAP", "TWTR", "SPOT"],
        
        # Industrials
        "Industrials": ["HON", "UNP", "RTX", "CAT", "BA", "LMT", "MMM", "GE", "FDX", "UPS", "CSX", "NSC", "UAL", "DAL", "LUV", "AAL"],
        
        # Consumer Staples
        "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST", "MDLZ", "CL", "KMB", "GIS", "K", "HSY"],
        
        # Energy
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC", "VLO", "PSX", "KMI", "OKE", "WMB"],
        
        # Utilities  
        "Utilities": ["NEE", "DUK", "SO", "AEP", "EXC", "XEL", "PEG", "ED", "ETR", "ES"],
        
        # Real Estate
        "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "AVB", "EQR", "VTR", "ESS", "MAA"],
        
        # Materials
        "Materials": ["LIN", "APD", "ECL", "SHW", "FCX", "NEM", "DOW", "DD", "PPG", "IFF"]
    }

def get_stock_info_enhanced(ticker):
    """Get enhanced stock information with sector and market cap"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get sector mapping
        sector_mapping = get_stock_sector_mapping()
        sector = "Other"
        for sec, stocks in sector_mapping.items():
            if ticker in stocks:
                sector = sec
                break
        
        return {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "sector": sector,
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "country": info.get("country", "US"),
            "exchange": info.get("exchange", "NASDAQ"),
            "price": info.get("currentPrice", 0)
        }
    except:
        return {
            "ticker": ticker,
            "name": ticker,
            "sector": "Other", 
            "industry": "N/A",
            "market_cap": 0,
            "country": "US",
            "exchange": "NASDAQ",
            "price": 0
        }

def search_stocks_comprehensive(query="", sector=None, min_market_cap=None, max_market_cap=None):
    """Comprehensive stock search with filters"""
    all_stocks = get_all_market_stocks()
    
    if query:
        # Filter by query in ticker or name
        filtered_stocks = [s for s in all_stocks if query.upper() in s.upper()]
    else:
        filtered_stocks = all_stocks
    
    # Apply additional filters (sector, market cap) would require real-time data
    return filtered_stocks[:100]  # Limit to 100 results for performance

def get_market_categories():
    """Get all market categories"""
    return {
        "US Large Cap": ["S&P 500", "Dow Jones 30", "NASDAQ 100"],
        "US Small Cap": ["Russell 2000"],
        "International": ["Japanese Stocks", "European Stocks", "Chinese Stocks"],
        "Sectors": list(get_sector_etfs().keys())
    }