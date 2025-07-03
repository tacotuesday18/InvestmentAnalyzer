import yfinance as yf
import streamlit as st
from datetime import datetime
import pandas as pd

def get_yahoo_finance_data(ticker):
    """Fetch financial data exclusively from Yahoo Finance API"""
    try:
        # Ensure ticker is uppercase and clean
        ticker = ticker.upper().strip()
        
        # Create the yfinance Ticker object
        stock = yf.Ticker(ticker)
        
        # Get basic info and historical data
        info = stock.info
        history = stock.history(period="1d")
        
        # Validate that we have actual data
        if not info or info.get('symbol') is None:
            return {
                'ticker': ticker,
                'error': 'No data available from Yahoo Finance',
                'is_live': False
            }
        
        # Get current price
        current_price = None
        if not history.empty:
            current_price = float(history['Close'].iloc[-1])
        elif info.get('currentPrice'):
            current_price = float(info.get('currentPrice'))
        elif info.get('previousClose'):
            current_price = float(info.get('previousClose'))
        
        if current_price is None:
            return {
                'ticker': ticker,
                'error': 'No price data available',
                'is_live': False
            }
        
        # Get only actual Yahoo Finance data - no calculations or fallbacks
        return {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'industry': info.get('industry'),
            'sector': info.get('sector'),
            'country': info.get('country'),
            'current_price': current_price,
            'market_cap': info.get('marketCap'),
            'revenue': info.get('totalRevenue'),
            'net_income': info.get('netIncomeToCommon'),
            'eps': info.get('trailingEps'),
            'pe_ratio': info.get('trailingPE'),
            'pb_ratio': info.get('priceToBook'),
            'ps_ratio': info.get('priceToSalesTrailing12Months'),
            'peg_ratio': info.get('pegRatio'),
            'roe': (info.get('returnOnEquity') * 100) if info.get('returnOnEquity') else None,
            'roa': (info.get('returnOnAssets') * 100) if info.get('returnOnAssets') else None,
            'shares_outstanding': info.get('sharesOutstanding'),
            'book_value_per_share': info.get('bookValue'),
            'historical_growth': (info.get('revenueGrowth') * 100) if info.get('revenueGrowth') else None,
            'profit_margin': (info.get('profitMargins') * 100) if info.get('profitMargins') else None,
            'gross_margin': (info.get('grossMargins') * 100) if info.get('grossMargins') else None,
            'operating_margin': (info.get('operatingMargins') * 100) if info.get('operatingMargins') else None,
            'current_ratio': info.get('currentRatio'),
            'debt_to_equity': info.get('debtToEquity'),
            'asset_turnover': None,  # Not available from Yahoo Finance
            'dividend_yield': (info.get('dividendYield') * 100) if info.get('dividendYield') else 0,
            'dividend_rate': info.get('dividendRate'),
            'is_live': True,
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance data for {ticker}: {str(e)}")
        return {
            'ticker': ticker,
            'error': f'Failed to fetch data: {str(e)}',
            'is_live': False
        }

def calculate_growth_rate(stock):
    """Calculate historical revenue growth rate using Yahoo Finance data only"""
    try:
        financials = stock.financials
        if financials.empty:
            return None
        
        revenue_row = None
        for index in financials.index:
            if 'revenue' in index.lower() or 'total revenue' in index.lower():
                revenue_row = financials.loc[index]
                break
        
        if revenue_row is None or len(revenue_row) < 2:
            return None
        
        # Calculate year-over-year growth
        revenues = revenue_row.dropna().sort_index()
        if len(revenues) >= 2:
            recent_revenue = revenues.iloc[-1]
            previous_revenue = revenues.iloc[-2]
            
            if previous_revenue != 0:
                growth_rate = ((recent_revenue - previous_revenue) / previous_revenue) * 100
                return growth_rate
        
        return None
        
    except Exception as e:
        print(f"Error calculating growth rate: {str(e)}")
        return None

def get_revenue_growth_details(stock):
    """Get detailed information about revenue growth calculation"""
    try:
        financials = stock.financials
        if financials.empty:
            return {
                'status': 'No financial data available',
                'years_used': [],
                'revenues': [],
                'growth_rate': None
            }
        
        revenue_row = None
        for index in financials.index:
            if 'revenue' in index.lower() or 'total revenue' in index.lower():
                revenue_row = financials.loc[index]
                break
        
        if revenue_row is None:
            return {
                'status': 'No revenue data found',
                'years_used': [],
                'revenues': [],
                'growth_rate': None
            }
        
        revenues = revenue_row.dropna().sort_index()
        years = [str(year.year) for year in revenues.index]
        values = [float(val) for val in revenues.values]
        
        growth_rate = None
        if len(revenues) >= 2:
            recent_revenue = revenues.iloc[-1]
            previous_revenue = revenues.iloc[-2]
            
            if previous_revenue != 0:
                growth_rate = ((recent_revenue - previous_revenue) / previous_revenue) * 100
        
        return {
            'status': 'Success',
            'years_used': years,
            'revenues': values,
            'growth_rate': growth_rate
        }
        
    except Exception as e:
        return {
            'status': f'Error: {str(e)}',
            'years_used': [],
            'revenues': [],
            'growth_rate': None
        }