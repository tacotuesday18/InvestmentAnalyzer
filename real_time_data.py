import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from openai import OpenAI

# OpenAI client initialization
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_live_stock_data(ticker):
    """
    Fetch real-time stock data using yfinance
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
    --------
    dict
        Real-time stock data including price, financials, and key metrics
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get basic info
        info = stock.info
        
        # Get historical data for calculations
        hist = stock.history(period="5y")
        
        # Get financial statements
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        
        # Calculate key metrics
        current_price = info.get('currentPrice', 0)
        market_cap = info.get('marketCap', 0)
        shares_outstanding = info.get('sharesOutstanding', 0)
        
        # Calculate 5-year CAGR
        if len(hist) > 252 * 5:  # 5 years of trading days
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            years = 5
            cagr = ((end_price / start_price) ** (1/years) - 1) * 100
        else:
            cagr = None
            
        # Get revenue and earnings data
        revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else 0
        net_income = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else 0
        
        # Calculate financial ratios
        pe_ratio = info.get('trailingPE', 0)
        pb_ratio = info.get('priceToBook', 0)
        roe = info.get('returnOnEquity', 0)
        debt_to_equity = info.get('debtToEquity', 0)
        
        return {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'current_price': current_price,
            'market_cap': market_cap,
            'shares_outstanding': shares_outstanding,
            'revenue': revenue,
            'net_income': net_income,
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'roe': roe * 100 if roe else 0,  # Convert to percentage
            'debt_to_equity': debt_to_equity,
            'cagr_5y': cagr,
            'industry': info.get('industry', 'Unknown'),
            'sector': info.get('sector', 'Unknown'),
            'last_updated': datetime.now().isoformat(),
            'success': True
        }
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return {
            'ticker': ticker,
            'error': str(e),
            'success': False
        }

def get_industry_averages(industry_name):
    """
    Get industry average financial metrics
    
    Parameters:
    -----------
    industry_name : str
        Industry name
        
    Returns:
    --------
    dict
        Industry average metrics
    """
    # Common industry tickers mapping
    industry_tickers = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX'],
        'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'BMY'],
        'Financial': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'BLK'],
        'Consumer Goods': ['PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'NKE', 'SBUX'],
        'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'VLO', 'PSX'],
        'Industrial': ['BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS', 'LMT', 'RTX']
    }
    
    tickers = industry_tickers.get(industry_name, industry_tickers['Technology'])
    
    try:
        metrics = []
        for ticker in tickers[:5]:  # Use first 5 to avoid rate limits
            data = get_live_stock_data(ticker)
            if data.get('success'):
                metrics.append(data)
        
        if not metrics:
            return {'error': 'No data available for industry'}
        
        # Calculate averages
        avg_pe = sum([m['pe_ratio'] for m in metrics if m['pe_ratio'] > 0]) / len([m for m in metrics if m['pe_ratio'] > 0])
        avg_pb = sum([m['pb_ratio'] for m in metrics if m['pb_ratio'] > 0]) / len([m for m in metrics if m['pb_ratio'] > 0])
        avg_roe = sum([m['roe'] for m in metrics if m['roe'] > 0]) / len([m for m in metrics if m['roe'] > 0])
        avg_debt_equity = sum([m['debt_to_equity'] for m in metrics if m['debt_to_equity'] > 0]) / len([m for m in metrics if m['debt_to_equity'] > 0])
        
        return {
            'industry': industry_name,
            'average_pe': avg_pe,
            'average_pb': avg_pb,
            'average_roe': avg_roe,
            'average_debt_to_equity': avg_debt_equity,
            'sample_size': len(metrics)
        }
        
    except Exception as e:
        return {'error': str(e)}

def financial_chatbot(question, context_data=None):
    """
    AI-powered financial chatbot using OpenAI
    
    Parameters:
    -----------
    question : str
        User's financial question
    context_data : dict, optional
        Additional context data for the response
        
    Returns:
    --------
    str
        AI-generated response
    """
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        
        system_prompt = """You are a professional financial analyst assistant for a Japanese financial analysis platform. 
        You help users understand financial metrics, industry comparisons, and investment analysis.
        
        Key capabilities:
        - Calculate and explain financial ratios (PE, PB, ROE, debt-to-equity, etc.)
        - Provide industry average comparisons
        - Analyze company growth rates (CAGR)
        - Explain investment concepts in simple terms
        - Answer in Japanese when appropriate
        
        Always provide specific, actionable insights based on real financial data when available.
        If you need specific company data that isn't provided, mention what data would be helpful.
        """
        
        user_prompt = f"Question: {question}"
        if context_data:
            user_prompt += f"\nContext data: {json.dumps(context_data, indent=2)}"
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"申し訳ございません。エラーが発生しました: {str(e)}"

def get_company_cagr(ticker, years=5):
    """
    Calculate company's CAGR for specified years
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    years : int
        Number of years for CAGR calculation
        
    Returns:
    --------
    dict
        CAGR data including revenue, earnings, and stock price CAGR
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical price data
        hist = stock.history(period=f"{years}y")
        
        # Get financial statements
        financials = stock.financials
        
        result = {'ticker': ticker, 'years': years}
        
        # Stock price CAGR
        if len(hist) > 252 * years * 0.8:  # At least 80% of expected trading days
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            stock_cagr = ((end_price / start_price) ** (1/years) - 1) * 100
            result['stock_price_cagr'] = stock_cagr
        
        # Revenue CAGR
        if 'Total Revenue' in financials.index and len(financials.columns) >= years:
            revenues = financials.loc['Total Revenue'].dropna()
            if len(revenues) >= 2:
                start_revenue = revenues.iloc[-1]  # Oldest available
                end_revenue = revenues.iloc[0]     # Most recent
                revenue_years = len(revenues) - 1
                if revenue_years > 0 and start_revenue > 0:
                    revenue_cagr = ((end_revenue / start_revenue) ** (1/revenue_years) - 1) * 100
                    result['revenue_cagr'] = revenue_cagr
        
        # Net Income CAGR
        if 'Net Income' in financials.index and len(financials.columns) >= years:
            net_incomes = financials.loc['Net Income'].dropna()
            if len(net_incomes) >= 2:
                start_ni = net_incomes.iloc[-1]  # Oldest available
                end_ni = net_incomes.iloc[0]     # Most recent
                ni_years = len(net_incomes) - 1
                if ni_years > 0 and start_ni > 0:
                    ni_cagr = ((end_ni / start_ni) ** (1/ni_years) - 1) * 100
                    result['net_income_cagr'] = ni_cagr
        
        return result
        
    except Exception as e:
        return {'ticker': ticker, 'error': str(e)}