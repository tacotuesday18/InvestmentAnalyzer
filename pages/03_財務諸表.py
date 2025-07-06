import streamlit as st
import pandas as pd
import yfinance as yf
from auto_financial_data import get_auto_financial_data
from format_helpers import format_currency, format_large_number
from earnings_scraper import get_website_text_content, analyze_earnings_call
from gemini_historical_metrics import create_historical_metrics_table_with_ai
import numpy as np
import requests
import trafilatura
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# ページ設定は main app.py で処理済み

def format_japanese_number(value):
    """Format numbers for Japanese users (billions = 億, millions = 百万)"""
    if abs(value) >= 1000:  # Billions
        return f"{value/1000:.1f}億"
    elif abs(value) >= 1:  # Millions  
        return f"{value:.0f}百万"
    else:
        return f"{value:.1f}百万"

def format_market_cap_japanese(market_cap_usd):
    """Format market cap for Japanese users with proper scale"""
    if market_cap_usd >= 1_000_000_000_000:  # Trillion USD
        return f"{market_cap_usd/1_000_000_000_000:.2f}兆ドル"
    elif market_cap_usd >= 1_000_000_000:  # Billion USD  
        return f"{market_cap_usd/1_000_000_000:.1f}億ドル"
    elif market_cap_usd >= 1_000_000:  # Million USD
        return f"{market_cap_usd/1_000_000:.0f}百万ドル"
    else:
        return f"${market_cap_usd:,.0f}"

def calculate_yoy_growth(current_val, previous_val):
    """Calculate year-over-year growth percentage"""
    if previous_val == 0 or pd.isna(previous_val) or pd.isna(current_val):
        return 0
    return ((current_val - previous_val) / abs(previous_val)) * 100

def create_financial_chart(income_stmt, balance_sheet, cash_flow, chart_type, is_quarterly=False):
    """Create financial charts based on the selected type"""
    fig = go.Figure()
    
    try:
        if chart_type == "revenue_income":
            # Revenue and Net Income chart
            revenue_data = []
            income_data = []
            revenue_growth = []
            income_growth = []
            dates = []
            
            # Get revenue data
            revenue_key = None
            for key in ['Total Revenue', 'Revenue']:
                if key in income_stmt.index:
                    revenue_key = key
                    break
            
            # Get net income data
            income_key = None
            for key in ['Net Income', 'Net Income Common Stockholders']:
                if key in income_stmt.index:
                    income_key = key
                    break
            
            if revenue_key and income_key:
                columns = list(income_stmt.columns)
                for i, col in enumerate(columns):
                    if is_quarterly:
                        # Format quarterly dates in Japanese
                        quarter = (col.month - 1) // 3 + 1
                        dates.append(f"{col.year}年Q{quarter}")
                    else:
                        dates.append(f"{col.year}年")
                    
                    revenue_val = income_stmt.loc[revenue_key, col] if not pd.isna(income_stmt.loc[revenue_key, col]) else 0
                    income_val = income_stmt.loc[income_key, col] if not pd.isna(income_stmt.loc[income_key, col]) else 0
                    
                    revenue_data.append(revenue_val / 1e6)  # Convert to millions
                    income_data.append(income_val / 1e6)   # Convert to millions
                    
                    # Calculate YoY growth
                    if is_quarterly and i >= 4:  # Compare with same quarter previous year
                        prev_revenue = income_stmt.loc[revenue_key, columns[i-4]] if not pd.isna(income_stmt.loc[revenue_key, columns[i-4]]) else 0
                        prev_income = income_stmt.loc[income_key, columns[i-4]] if not pd.isna(income_stmt.loc[income_key, columns[i-4]]) else 0
                        revenue_growth.append(calculate_yoy_growth(revenue_val, prev_revenue))
                        income_growth.append(calculate_yoy_growth(income_val, prev_income))
                    elif not is_quarterly and i >= 1:  # Compare with previous year
                        prev_revenue = income_stmt.loc[revenue_key, columns[i-1]] if not pd.isna(income_stmt.loc[revenue_key, columns[i-1]]) else 0
                        prev_income = income_stmt.loc[income_key, columns[i-1]] if not pd.isna(income_stmt.loc[income_key, columns[i-1]]) else 0
                        revenue_growth.append(calculate_yoy_growth(revenue_val, prev_revenue))
                        income_growth.append(calculate_yoy_growth(income_val, prev_income))
                    else:
                        revenue_growth.append(0)
                        income_growth.append(0)
                
                # Reverse to show chronological order
                dates.reverse()
                revenue_data.reverse()
                income_data.reverse()
                revenue_growth.reverse()
                income_growth.reverse()
                
                # Create growth text labels
                revenue_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in revenue_growth]
                income_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in income_growth]
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=revenue_data,
                    name='売上高',
                    marker_color='orange',
                    text=revenue_text,
                    textposition='outside',
                    textfont=dict(size=10, color='orange'),
                    yaxis='y'
                ))
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=income_data,
                    name='純利益',
                    marker_color='black',
                    text=income_text,
                    textposition='outside',
                    textfont=dict(size=10, color='black'),
                    yaxis='y'
                ))
                
                fig.update_layout(
                    title="売上高と純利益",
                    xaxis_title="期間",
                    yaxis_title="金額 (百万USD)",
                    height=400,
                    barmode='group'
                )
        
        elif chart_type == "assets_liabilities":
            # Assets and Liabilities chart
            assets_data = []
            liabilities_data = []
            assets_growth = []
            liabilities_growth = []
            dates = []
            
            assets_key = None
            for key in ['Total Assets']:
                if key in balance_sheet.index:
                    assets_key = key
                    break
                    
            liabilities_key = None
            for key in ['Total Liabilities Net Minority Interest', 'Total Liabilities', 'Total Liab']:
                if key in balance_sheet.index:
                    liabilities_key = key
                    break
            
            if assets_key and liabilities_key:
                columns = list(balance_sheet.columns)
                for i, col in enumerate(columns):
                    if is_quarterly:
                        quarter = (col.month - 1) // 3 + 1
                        dates.append(f"{col.year}年Q{quarter}")
                    else:
                        dates.append(f"{col.year}年")
                    
                    assets_val = balance_sheet.loc[assets_key, col] if not pd.isna(balance_sheet.loc[assets_key, col]) else 0
                    liabilities_val = balance_sheet.loc[liabilities_key, col] if not pd.isna(balance_sheet.loc[liabilities_key, col]) else 0
                    
                    assets_data.append(assets_val / 1e6)
                    liabilities_data.append(liabilities_val / 1e6)
                    
                    # Calculate YoY growth
                    if is_quarterly and i >= 4:
                        prev_assets = balance_sheet.loc[assets_key, columns[i-4]] if not pd.isna(balance_sheet.loc[assets_key, columns[i-4]]) else 0
                        prev_liabilities = balance_sheet.loc[liabilities_key, columns[i-4]] if not pd.isna(balance_sheet.loc[liabilities_key, columns[i-4]]) else 0
                        assets_growth.append(calculate_yoy_growth(assets_val, prev_assets))
                        liabilities_growth.append(calculate_yoy_growth(liabilities_val, prev_liabilities))
                    elif not is_quarterly and i >= 1:
                        prev_assets = balance_sheet.loc[assets_key, columns[i-1]] if not pd.isna(balance_sheet.loc[assets_key, columns[i-1]]) else 0
                        prev_liabilities = balance_sheet.loc[liabilities_key, columns[i-1]] if not pd.isna(balance_sheet.loc[liabilities_key, columns[i-1]]) else 0
                        assets_growth.append(calculate_yoy_growth(assets_val, prev_assets))
                        liabilities_growth.append(calculate_yoy_growth(liabilities_val, prev_liabilities))
                    else:
                        assets_growth.append(0)
                        liabilities_growth.append(0)
                
                dates.reverse()
                assets_data.reverse()
                liabilities_data.reverse()
                assets_growth.reverse()
                liabilities_growth.reverse()
                
                # Create growth text labels
                assets_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in assets_growth]
                liabilities_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in liabilities_growth]
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=assets_data,
                    name='総資産',
                    marker_color='blue',
                    text=assets_text,
                    textposition='outside',
                    textfont=dict(size=10, color='blue')
                ))
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=liabilities_data,
                    name='総負債',
                    marker_color='red',
                    text=liabilities_text,
                    textposition='outside',
                    textfont=dict(size=10, color='red')
                ))
                
                fig.update_layout(
                    title="総資産と総負債",
                    xaxis_title="期間",
                    yaxis_title="金額 (百万USD)",
                    height=400,
                    barmode='group'
                )
        
        elif chart_type == "debt_to_assets":
            # Debt to Assets ratio chart
            debt_ratio_data = []
            ratio_growth = []
            dates = []
            
            assets_key = None
            for key in ['Total Assets']:
                if key in balance_sheet.index:
                    assets_key = key
                    break
                    
            liabilities_key = None
            for key in ['Total Liabilities Net Minority Interest', 'Total Liabilities', 'Total Liab']:
                if key in balance_sheet.index:
                    liabilities_key = key
                    break
            
            if assets_key and liabilities_key:
                columns = list(balance_sheet.columns)
                for i, col in enumerate(columns):
                    if is_quarterly:
                        quarter = (col.month - 1) // 3 + 1
                        dates.append(f"{col.year}年Q{quarter}")
                    else:
                        dates.append(f"{col.year}年")
                    
                    assets_val = balance_sheet.loc[assets_key, col] if not pd.isna(balance_sheet.loc[assets_key, col]) else 0
                    liabilities_val = balance_sheet.loc[liabilities_key, col] if not pd.isna(balance_sheet.loc[liabilities_key, col]) else 0
                    
                    if assets_val > 0:
                        ratio = (liabilities_val / assets_val) * 100
                    else:
                        ratio = 0
                    debt_ratio_data.append(ratio)
                    
                    # Calculate ratio change
                    if is_quarterly and i >= 4:
                        prev_assets = balance_sheet.loc[assets_key, columns[i-4]] if not pd.isna(balance_sheet.loc[assets_key, columns[i-4]]) else 0
                        prev_liabilities = balance_sheet.loc[liabilities_key, columns[i-4]] if not pd.isna(balance_sheet.loc[liabilities_key, columns[i-4]]) else 0
                        prev_ratio = (prev_liabilities / prev_assets) * 100 if prev_assets > 0 else 0
                        ratio_change = ratio - prev_ratio
                        ratio_growth.append(ratio_change)
                    elif not is_quarterly and i >= 1:
                        prev_assets = balance_sheet.loc[assets_key, columns[i-1]] if not pd.isna(balance_sheet.loc[assets_key, columns[i-1]]) else 0
                        prev_liabilities = balance_sheet.loc[liabilities_key, columns[i-1]] if not pd.isna(balance_sheet.loc[liabilities_key, columns[i-1]]) else 0
                        prev_ratio = (prev_liabilities / prev_assets) * 100 if prev_assets > 0 else 0
                        ratio_change = ratio - prev_ratio
                        ratio_growth.append(ratio_change)
                    else:
                        ratio_growth.append(0)
                
                dates.reverse()
                debt_ratio_data.reverse()
                ratio_growth.reverse()
                
                # Create change text labels
                ratio_text = [f"+{g:.1f}pt" if g > 0 else f"{g:.1f}pt" if g != 0 else "" for g in ratio_growth]
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=debt_ratio_data,
                    name='負債比率',
                    marker_color='purple',
                    text=ratio_text,
                    textposition='outside',
                    textfont=dict(size=10, color='purple')
                ))
                
                fig.update_layout(
                    title="負債比率",
                    xaxis_title="期間",
                    yaxis_title="比率 (%)",
                    height=400
                )
        
        elif chart_type == "cash_flow":
            # Cash Flow chart
            ocf_data = []
            icf_data = []
            fcf_data = []
            ocf_growth = []
            icf_growth = []
            fcf_growth = []
            dates = []
            
            # Find operating cash flow
            ocf_key = None
            for key in ['Operating Cash Flow', 'Total Cash From Operating Activities', 'Cash Flow From Operating Activities']:
                if key in cash_flow.index:
                    ocf_key = key
                    break
            
            # Find investing cash flow
            icf_key = None
            for key in ['Investing Cash Flow', 'Total Cash From Investing Activities', 'Cash Flow From Investing Activities']:
                if key in cash_flow.index:
                    icf_key = key
                    break
            
            # Find free cash flow
            fcf_key = None
            for key in ['Free Cash Flow']:
                if key in cash_flow.index:
                    fcf_key = key
                    break
            
            if ocf_key:
                columns = list(cash_flow.columns)
                for i, col in enumerate(columns):
                    if is_quarterly:
                        quarter = (col.month - 1) // 3 + 1
                        dates.append(f"{col.year}年Q{quarter}")
                    else:
                        dates.append(f"{col.year}年")
                    
                    ocf_val = cash_flow.loc[ocf_key, col] if not pd.isna(cash_flow.loc[ocf_key, col]) else 0
                    ocf_data.append(ocf_val / 1e6)
                    
                    # Calculate YoY growth for operating cash flow
                    if is_quarterly and i >= 4:
                        prev_ocf = cash_flow.loc[ocf_key, columns[i-4]] if not pd.isna(cash_flow.loc[ocf_key, columns[i-4]]) else 0
                        ocf_growth.append(calculate_yoy_growth(ocf_val, prev_ocf))
                    elif not is_quarterly and i >= 1:
                        prev_ocf = cash_flow.loc[ocf_key, columns[i-1]] if not pd.isna(cash_flow.loc[ocf_key, columns[i-1]]) else 0
                        ocf_growth.append(calculate_yoy_growth(ocf_val, prev_ocf))
                    else:
                        ocf_growth.append(0)
                    
                    if icf_key:
                        icf_val = cash_flow.loc[icf_key, col] if not pd.isna(cash_flow.loc[icf_key, col]) else 0
                        icf_data.append(icf_val / 1e6)
                        
                        # Calculate YoY growth for investing cash flow
                        if is_quarterly and i >= 4:
                            prev_icf = cash_flow.loc[icf_key, columns[i-4]] if not pd.isna(cash_flow.loc[icf_key, columns[i-4]]) else 0
                            icf_growth.append(calculate_yoy_growth(icf_val, prev_icf))
                        elif not is_quarterly and i >= 1:
                            prev_icf = cash_flow.loc[icf_key, columns[i-1]] if not pd.isna(cash_flow.loc[icf_key, columns[i-1]]) else 0
                            icf_growth.append(calculate_yoy_growth(icf_val, prev_icf))
                        else:
                            icf_growth.append(0)
                    
                    if fcf_key:
                        fcf_val = cash_flow.loc[fcf_key, col] if not pd.isna(cash_flow.loc[fcf_key, col]) else 0
                        fcf_data.append(fcf_val / 1e6)
                        
                        # Calculate YoY growth for free cash flow
                        if is_quarterly and i >= 4:
                            prev_fcf = cash_flow.loc[fcf_key, columns[i-4]] if not pd.isna(cash_flow.loc[fcf_key, columns[i-4]]) else 0
                            fcf_growth.append(calculate_yoy_growth(fcf_val, prev_fcf))
                        elif not is_quarterly and i >= 1:
                            prev_fcf = cash_flow.loc[fcf_key, columns[i-1]] if not pd.isna(cash_flow.loc[fcf_key, columns[i-1]]) else 0
                            fcf_growth.append(calculate_yoy_growth(fcf_val, prev_fcf))
                        else:
                            fcf_growth.append(0)
                
                dates.reverse()
                ocf_data.reverse()
                ocf_growth.reverse()
                
                # Create growth text labels
                ocf_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in ocf_growth]
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=ocf_data,
                    name='営業キャッシュフロー',
                    marker_color='green',
                    text=ocf_text,
                    textposition='outside',
                    textfont=dict(size=10, color='green')
                ))
                
                if icf_data:
                    icf_data.reverse()
                    icf_growth.reverse()
                    icf_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in icf_growth]
                    fig.add_trace(go.Bar(
                        x=dates,
                        y=icf_data,
                        name='投資キャッシュフロー',
                        marker_color='orange',
                        text=icf_text,
                        textposition='outside',
                        textfont=dict(size=10, color='orange')
                    ))
                
                if fcf_data:
                    fcf_data.reverse()
                    fcf_growth.reverse()
                    fcf_text = [f"+{g:.1f}%" if g > 0 else f"{g:.1f}%" if g != 0 else "" for g in fcf_growth]
                    fig.add_trace(go.Bar(
                        x=dates,
                        y=fcf_data,
                        name='フリーキャッシュフロー',
                        marker_color='blue',
                        text=fcf_text,
                        textposition='outside',
                        textfont=dict(size=10, color='blue')
                    ))
                
                fig.update_layout(
                    title="キャッシュフロー",
                    xaxis_title="期間",
                    yaxis_title="金額 (百万USD)",
                    height=400,
                    barmode='group'
                )
        
        fig.update_layout(
            template="plotly_white",
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"チャート作成エラー: {str(e)}")
        return None

# TravelPerk-style CSS for consistent design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    
    /* Enhanced Navigation Styles */
    .stSidebar, section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 20px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stSidebar > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar content styling */
    .stSidebar .stMarkdown, .stSidebar .stButton, .stSidebar .stForm {
        color: white !important;
    }
    
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, .stSidebar .stMarkdown p {
        color: white !important;
    }
    
    .stSidebar .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 5px 0 !important;
    }
    
    .stSidebar .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Style Streamlit page navigation */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
        padding: 1rem 0 !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stSidebarNav"] li {
        margin: 8px 0 !important;
    }
    
    [data-testid="stSidebarNav"] a {
        display: block !important;
        padding: 12px 16px !important;
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        text-decoration: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 600 !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 100%;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #4a5568;
        margin-bottom: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 0.75rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a202c;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .financial-table {
        font-size: 0.95rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .feature-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        display: inline-block;
    }
    
    /* Research paper styling */
    .research-paper {
        background: white;
        padding: 3rem 2.5rem;
        margin: 2rem 0;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        font-family: 'Inter', serif;
    }
    
    .paper-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a202c;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .paper-subtitle {
        font-size: 1.3rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .author-info {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        font-size: 1rem;
        line-height: 1.6;
        color: #2d3748;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero section - TravelPerk style
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📊 財務諸表分析</div>
    <div class="hero-subtitle">
        企業の最新決算データから損益計算書、貸借対照表、キャッシュフローの詳細を分析
    </div>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <div class="feature-badge">💹 リアルタイム財務データ</div>
        <div class="feature-badge">📈 決算ハイライト分析</div>
        <div class="feature-badge">🤖 AI要約レポート</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced stock selection with company name search similar to business model page
st.markdown("### 📈 企業選択")

# Initialize session state for financial statements page
def init_financial_session_state():
    if 'financial_analysis_completed' not in st.session_state:
        st.session_state.financial_analysis_completed = False
    if 'financial_current_ticker' not in st.session_state:
        st.session_state.financial_current_ticker = None
    if 'financial_data' not in st.session_state:
        st.session_state.financial_data = None
    if 'financial_period' not in st.session_state:
        st.session_state.financial_period = "yearly"
    if 'stored_financial_period' not in st.session_state:
        st.session_state.stored_financial_period = "yearly"

def should_reset_financial_analysis(ticker):
    return (st.session_state.financial_current_ticker != ticker or 
            not st.session_state.financial_analysis_completed)

def reset_financial_analysis():
    st.session_state.financial_analysis_completed = False
    st.session_state.financial_data = None

col1, col2 = st.columns([3, 1])

# Initialize session state
init_financial_session_state()

with col1:
    search_input = st.text_input(
        "企業名またはティッカーシンボルを入力",
        placeholder="例: Apple, Microsoft, AAPL, MSFT",
        help="企業名（日本語・英語）またはティッカーシンボルで検索",
        value=st.session_state.get('financial_search_input', '')
    )
    
    if search_input:
        st.session_state.financial_search_input = search_input
        from comprehensive_stock_data import search_stocks_by_name
        results = search_stocks_by_name(search_input)
        if results:
            selected_ticker = results[0]['ticker']
        else:
            selected_ticker = search_input.upper()
    else:
        selected_ticker = st.session_state.get('financial_current_ticker', 'AAPL')

with col2:
    analyze_button = st.button("財務分析", type="primary", use_container_width=True)

# Check if we should run analysis
should_analyze = analyze_button and selected_ticker

# If ticker changed, reset analysis
if should_reset_financial_analysis(selected_ticker):
    reset_financial_analysis()
    st.session_state.financial_current_ticker = selected_ticker

if should_analyze or (st.session_state.financial_analysis_completed and st.session_state.financial_current_ticker == selected_ticker):
    # Run analysis if needed
    if should_analyze and not st.session_state.financial_analysis_completed:
        with st.spinner(f"{selected_ticker}の財務諸表データを取得・分析中..."):
            try:
                # Get comprehensive financial data using yfinance and Gemini
                stock = yf.Ticker(selected_ticker)
                info = stock.info
                
                company_name = info.get('longName', selected_ticker)
                sector = info.get('sector', 'Technology')
                industry = info.get('industry', 'Software')
                
                # Get financial statements based on period selection
                if st.session_state.financial_period == "quarterly":
                    # Get quarterly financial statements
                    income_stmt = stock.quarterly_financials
                    balance_sheet = stock.quarterly_balance_sheet
                    cash_flow = stock.quarterly_cashflow
                else:
                    # Get yearly financial statements
                    income_stmt = stock.financials
                    balance_sheet = stock.balance_sheet
                    cash_flow = stock.cashflow
                
                # Get comprehensive financial data
                auto_data = get_auto_financial_data(selected_ticker)
                
                # Store in session state
                st.session_state.financial_data = {
                    'auto_data': auto_data,
                    'income_stmt': income_stmt,
                    'balance_sheet': balance_sheet,
                    'cash_flow': cash_flow,
                    'company_info': {
                        'name': company_name,
                        'sector': sector,
                        'industry': industry,
                        'info': info
                    },
                    'ticker': selected_ticker
                }
                st.session_state.stored_financial_period = st.session_state.financial_period
                st.session_state.financial_analysis_completed = True
                
            except Exception as e:
                st.error(f"財務データの取得に失敗しました: {str(e)}")
                st.session_state.financial_analysis_completed = False
    
    # Display analysis results if available
    if st.session_state.financial_analysis_completed and st.session_state.financial_data:
        financial_data = st.session_state.financial_data
        auto_data = financial_data['auto_data']
        company_info = financial_data['company_info']
        
        if auto_data:
            # Display company header similar to business model page
            st.markdown(f"""
            <div class="research-paper">
                <h1 class="paper-title">{company_info['name']} ({selected_ticker})</h1>
                <h2 class="paper-subtitle">詳細財務諸表分析</h2>
                
                <div class="author-info">
                    <strong>分析日:</strong> {datetime.now().strftime('%Y年%m月%d日')}<br>
                    <strong>セクター:</strong> {company_info['sector']} | <strong>業界:</strong> {company_info['industry']}<br>
                    <strong>データ源:</strong> Yahoo Finance<br>
                    <strong>現在株価:</strong> ${auto_data['current_price']:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Basic company metrics
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("企業名", company_info['name'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("業界", company_info['industry'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("現在株価", f"${auto_data['current_price']:.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                st.metric("時価総額", format_market_cap_japanese(market_cap))
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            

            
            # Add period selection toggle
            st.markdown("### 📊 財務諸表期間選択")
            period_col1, period_col2 = st.columns(2)
            
            with period_col1:
                if st.button("📅 四半期データ", key="quarterly_btn", use_container_width=True):
                    st.session_state.financial_period = "quarterly"
            
            with period_col2:
                if st.button("📆 年次データ", key="yearly_btn", use_container_width=True):
                    st.session_state.financial_period = "yearly"
            

            
            # Display current selection
            period_display = "四半期" if st.session_state.financial_period == "quarterly" else "年次"
            st.info(f"現在の表示: {period_display}データ")
            
            # Get financial statements from session state or fetch if period changed
            try:
                # Check if period changed - if so, we need to refetch data
                current_period = st.session_state.financial_period
                stored_period = st.session_state.get('stored_financial_period', 'yearly')
                
                if current_period != stored_period:
                    # Period changed, fetch new data
                    stock = yf.Ticker(selected_ticker)
                    
                    if current_period == "quarterly":
                        income_stmt = stock.quarterly_financials
                        balance_sheet = stock.quarterly_balance_sheet
                        cash_flow = stock.quarterly_cashflow
                        period_label = "四半期"
                    else:
                        income_stmt = stock.financials
                        balance_sheet = stock.balance_sheet
                        cash_flow = stock.cashflow
                        period_label = "年次"
                    
                    # Update stored data and period
                    st.session_state.financial_data['income_stmt'] = income_stmt
                    st.session_state.financial_data['balance_sheet'] = balance_sheet
                    st.session_state.financial_data['cash_flow'] = cash_flow
                    st.session_state.stored_financial_period = current_period
                    st.rerun()  # Rerun to update display
                else:
                    # Use stored data
                    income_stmt = financial_data['income_stmt']
                    balance_sheet = financial_data['balance_sheet']
                    cash_flow = financial_data['cash_flow']
                    period_label = "四半期" if current_period == "quarterly" else "年次"
                
                # 損益計算書 (Income Statement)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"### 📈 損益計算書 (Income Statement) - {period_label}")
                
                # Use the selected period's income statement
                # income_stmt is already set above based on period selection
                if not income_stmt.empty:
                    # Convert to Japanese labels and format
                    income_data = []
                    
                    # Key income statement items
                    income_items = {
                        'Total Revenue': '売上高',
                        'Cost Of Revenue': '売上原価',
                        'Gross Profit': '売上総利益',
                        'Operating Income': '営業利益',
                        'Net Income': '純利益',
                        'Basic EPS': '基本的1株当たり利益'
                    }
                    
                    for eng_item, jp_item in income_items.items():
                        if eng_item in income_stmt.index:
                            row_data = {"項目": jp_item}
                            for col in income_stmt.columns[:4]:  # Latest 4 periods
                                # Format date based on period type
                                if current_period == "quarterly":
                                    quarter = (col.month - 1) // 3 + 1
                                    date_label = f"{col.year}年Q{quarter}"
                                else:
                                    date_label = col.strftime('%Y年')
                                
                                value = income_stmt.loc[eng_item, col]
                                if not pd.isna(value):
                                    if eng_item == 'Basic EPS':
                                        row_data[date_label] = f"${value:.2f}"
                                    else:
                                        # Format with Japanese currency style
                                        if abs(value) >= 1_000_000_000:
                                            row_data[date_label] = f"${value/1_000_000_000:.2f}億"
                                        elif abs(value) >= 1_000_000:
                                            row_data[date_label] = f"${value/1_000_000:.1f}百万"
                                        else:
                                            row_data[date_label] = f"${value:,.0f}"
                                else:
                                    row_data[date_label] = "N/A"
                            income_data.append(row_data)
                    
                    if income_data:
                        income_df = pd.DataFrame(income_data)
                        st.dataframe(income_df, use_container_width=True, hide_index=True)
                        

                    else:
                        st.warning("損益計算書データが利用できません")
                else:
                    st.warning("損益計算書データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 貸借対照表 (Balance Sheet)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"### 🏦 貸借対照表 (Balance Sheet) - {period_label}")
                
                # Use the period-selected balance sheet data
                if not balance_sheet.empty:
                    balance_data = []
                    
                    # Key balance sheet items
                    balance_items = {
                        'Total Assets': '総資産',
                        'Current Assets': '流動資産',
                        'Cash And Cash Equivalents': '現金及び現金同等物',
                        'Total Liabilities Net Minority Interest': '総負債',
                        'Current Liabilities': '流動負債',
                        'Total Equity Gross Minority Interest': '株主資本',
                        'Retained Earnings': '利益剰余金'
                    }
                    
                    for eng_item, jp_item in balance_items.items():
                        if eng_item in balance_sheet.index:
                            row_data = {"項目": jp_item}
                            for col in balance_sheet.columns[:4]:  # Latest 4 periods
                                # Format date based on period type
                                if current_period == "quarterly":
                                    quarter = (col.month - 1) // 3 + 1
                                    date_label = f"{col.year}年Q{quarter}"
                                else:
                                    date_label = col.strftime('%Y年')
                                
                                value = balance_sheet.loc[eng_item, col]
                                if not pd.isna(value):
                                    # Format with Japanese currency style
                                    if abs(value) >= 1_000_000_000:
                                        row_data[date_label] = f"${value/1_000_000_000:.2f}億"
                                    elif abs(value) >= 1_000_000:
                                        row_data[date_label] = f"${value/1_000_000:.1f}百万"
                                    else:
                                        row_data[date_label] = f"${value:,.0f}"
                                else:
                                    row_data[date_label] = "N/A"
                            balance_data.append(row_data)
                    
                    if balance_data:
                        balance_df = pd.DataFrame(balance_data)
                        st.dataframe(balance_df, use_container_width=True, hide_index=True)
                        

                    else:
                        st.warning("貸借対照表データが利用できません")
                else:
                    st.warning("貸借対照表データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # キャッシュフロー計算書 (Cash Flow Statement)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"### 💰 キャッシュフロー計算書 (Cash Flow Statement) - {period_label}")
                
                # Use the period-selected cash flow data
                if not cash_flow.empty:
                    cf_data = []
                    
                    # Key cash flow items
                    cf_items = {
                        'Operating Cash Flow': '営業キャッシュフロー',
                        'Investing Cash Flow': '投資キャッシュフロー',
                        'Financing Cash Flow': '財務キャッシュフロー',
                        'Free Cash Flow': 'フリーキャッシュフロー',
                        'Capital Expenditure': '設備投資'
                    }
                    
                    for eng_item, jp_item in cf_items.items():
                        if eng_item in cash_flow.index:
                            row_data = {"項目": jp_item}
                            for col in cash_flow.columns[:4]:  # Latest 4 periods
                                # Format date based on period type
                                if current_period == "quarterly":
                                    quarter = (col.month - 1) // 3 + 1
                                    date_label = f"{col.year}年Q{quarter}"
                                else:
                                    date_label = col.strftime('%Y年')
                                
                                value = cash_flow.loc[eng_item, col]
                                if not pd.isna(value):
                                    # Format with Japanese currency style
                                    if abs(value) >= 1_000_000_000:
                                        row_data[date_label] = f"${value/1_000_000_000:.2f}億"
                                    elif abs(value) >= 1_000_000:
                                        row_data[date_label] = f"${value/1_000_000:.1f}百万"
                                    else:
                                        row_data[date_label] = f"${value:,.0f}"
                                else:
                                    row_data[date_label] = "N/A"
                            cf_data.append(row_data)
                    
                    if cf_data:
                        cf_df = pd.DataFrame(cf_data)
                        st.dataframe(cf_df, use_container_width=True, hide_index=True)
                        

                    else:
                        st.warning("キャッシュフロー計算書データが利用できません")
                else:
                    st.warning("キャッシュフロー計算書データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Consolidated Chart Section
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📊 財務トレンドチャート")
                
                # Chart type selector
                chart_tabs = st.tabs(["売上高・純利益", "資産・負債", "負債比率", "キャッシュフロー"])
                
                is_quarterly = (st.session_state.financial_period == "quarterly")
                
                with chart_tabs[0]:
                    # Revenue and Net Income Chart
                    chart = create_financial_chart(income_stmt, balance_sheet, cash_flow, "revenue_income", is_quarterly)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    else:
                        st.info("売上高・純利益データが不足しています")
                
                with chart_tabs[1]:
                    # Assets and Liabilities Chart
                    chart = create_financial_chart(income_stmt, balance_sheet, cash_flow, "assets_liabilities", is_quarterly)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    else:
                        st.info("資産・負債データが不足しています")
                
                with chart_tabs[2]:
                    # Debt to Assets Ratio Chart
                    chart = create_financial_chart(income_stmt, balance_sheet, cash_flow, "debt_to_assets", is_quarterly)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    else:
                        st.info("負債比率データが不足しています")
                
                with chart_tabs[3]:
                    # Cash Flow Chart
                    chart = create_financial_chart(income_stmt, balance_sheet, cash_flow, "cash_flow", is_quarterly)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    else:
                        st.info("キャッシュフローデータが不足しています")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 主要財務指標
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📊 主要財務指標")
                
                # Add metric explanations
                st.markdown("""
                <div style="margin-bottom: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                <small>
                <b>指標説明:</b><br>
                <b>PER</b>: 株価収益率 (株価÷1株利益) - 株価が利益の何倍かを示す<br>
                <b>PBR</b>: 株価純資産倍率 (株価÷1株純資産) - 株価が純資産の何倍かを示す<br>
                <b>PSR</b>: 株価売上高倍率 (時価総額÷売上高) - 売上に対する株価の割高・割安を示す<br>
                <b>純利益率</b>: 売上に対する純利益の割合 - 企業の収益効率を示す
                </small>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['eps'] > 0:
                        pe_ratio = auto_data['current_price'] / auto_data['eps']
                        st.metric("PER", f"{pe_ratio:.2f}倍")
                    else:
                        st.metric("PER", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['book_value_per_share'] > 0:
                        pb_ratio = auto_data['current_price'] / auto_data['book_value_per_share']
                        st.metric("PBR", f"{pb_ratio:.2f}倍")
                    else:
                        st.metric("PBR", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['revenue'] > 0:
                        market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                        ps_ratio = market_cap / auto_data['revenue']
                        st.metric("PSR", f"{ps_ratio:.2f}倍")
                    else:
                        st.metric("PSR", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col4:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['revenue'] > 0 and auto_data['net_income'] > 0:
                        profit_margin = (auto_data['net_income'] / auto_data['revenue']) * 100
                        st.metric("純利益率", f"{profit_margin:.1f}%")
                    else:
                        st.metric("純利益率", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col5:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    # Calculate revenue growth rate
                    try:
                        import yfinance as yf
                        from auto_financial_data import calculate_growth_rate, get_revenue_growth_details
                        stock = yf.Ticker(selected_ticker)
                        revenue_growth = calculate_growth_rate(stock)
                        st.metric("売上成長率", f"{revenue_growth:.1f}%")
                        
                        # Get detailed breakdown for verification
                        growth_details = get_revenue_growth_details(stock)
                        if "error" not in growth_details:
                            with st.expander("計算詳細を表示"):
                                st.write(f"**使用年度:** {', '.join(map(str, growth_details['years_used']))}")
                                for i, (year, revenue) in enumerate(zip(growth_details['years_used'], growth_details['revenues_billions'])):
                                    st.write(f"**{year}年売上:** ${revenue:.1f}B")
                                st.write(f"**計算式:** {growth_details['calculation']}")
                                if growth_details['is_2024_data']:
                                    st.success("✓ 2024年データを使用")
                                else:
                                    st.info(f"最新データ: {growth_details['years_used'][0]}年")
                    except:
                        st.metric("売上成長率", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                

                
                # Earnings highlights section removed - use dedicated earnings analysis page instead
                
            except Exception as e:
                st.error(f"財務データの取得中にエラーが発生しました: {str(e)}")
        
        else:
            st.error("選択された企業の財務データを取得できませんでした。")

# Historical metrics table (financecharts.com style)
if selected_ticker:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📈 過去の財務指標推移と業界比較")
    st.markdown("主要バリュエーション指標の現在値と過去平均値を比較して投資判断にご活用ください。")
    
    # Get current financial metrics
    stock = yf.Ticker(selected_ticker)
    info = stock.info
    current_pe = info.get('trailingPE', info.get('forwardPE', None))
    current_pb = info.get('priceToBook', None)
    current_ps = info.get('priceToSalesTrailing12Months', None)
    
    # Display historical metrics table
    create_historical_metrics_table_with_ai(selected_ticker, current_pe, current_pb, current_ps)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**注意**: 表示されるデータは最新の決算発表に基づいていますが、投資判断の際は必ず最新の情報を確認してください。")