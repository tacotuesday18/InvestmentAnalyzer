import streamlit as st
import yfinance as yf
import requests
from datetime import datetime
import json

def get_current_usd_jpy_rate():
    """
    Get current USD/JPY exchange rate from Yahoo Finance
    
    Returns:
    --------
    float
        Current USD/JPY exchange rate
    """
    try:
        # Get USD/JPY exchange rate using yfinance
        ticker = yf.Ticker("USDJPY=X")
        data = ticker.history(period="1d")
        if not data.empty:
            current_rate = data['Close'].iloc[-1]
            return current_rate
        else:
            # Fallback to approximate rate if data not available
            return 150.0
    except Exception as e:
        # Fallback rate
        return 150.0

def convert_usd_to_jpy(usd_amount, exchange_rate=None):
    """
    Convert USD amount to JPY
    
    Parameters:
    -----------
    usd_amount : float
        Amount in USD
    exchange_rate : float, optional
        USD/JPY exchange rate. If None, fetches current rate
        
    Returns:
    --------
    tuple
        (JPY amount, exchange rate used)
    """
    if exchange_rate is None:
        exchange_rate = get_current_usd_jpy_rate()
    
    jpy_amount = usd_amount * exchange_rate
    return jpy_amount, exchange_rate

def format_currency_jpy(amount):
    """
    Format JPY amount with Japanese formatting
    
    Parameters:
    -----------
    amount : float
        Amount in JPY
        
    Returns:
    --------
    str
        Formatted JPY string
    """
    if amount >= 100000000:  # 1億以上
        return f"¥{amount/100000000:.1f}億"
    elif amount >= 10000:  # 1万以上
        return f"¥{amount/10000:.1f}万"
    else:
        return f"¥{amount:,.0f}"

def display_currency_converter():
    """
    Display interactive USD/JPY currency converter widget
    """
    st.markdown("### 💱 USD/JPY 通貨コンバーター")
    
    # Get current exchange rate
    current_rate = get_current_usd_jpy_rate()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 8px; text-align: center;">
            <div style="font-size: 1.2rem; font-weight: 600;">現在のレート</div>
            <div style="font-size: 2rem; font-weight: 700;">¥{current_rate:.2f}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">1 USD = {current_rate:.2f} JPY</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Currency conversion calculator
        usd_input = st.number_input(
            "USD金額を入力:",
            min_value=0.0,
            value=100.0,
            step=10.0,
            format="%.2f"
        )
        
        if usd_input > 0:
            jpy_amount, rate_used = convert_usd_to_jpy(usd_input, current_rate)
            formatted_jpy = format_currency_jpy(jpy_amount)
            
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.1rem; color: #64748b;">変換結果</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1a202c;">{formatted_jpy}</div>
                <div style="font-size: 0.9rem; color: #64748b;">({jpy_amount:,.0f} JPY)</div>
            </div>
            """, unsafe_allow_html=True)

def display_stock_price_in_jpy(ticker, usd_price):
    """
    Display stock price converted to JPY
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    usd_price : float
        Stock price in USD
    """
    current_rate = get_current_usd_jpy_rate()
    jpy_price, _ = convert_usd_to_jpy(usd_price, current_rate)
    formatted_jpy = format_currency_jpy(jpy_price)
    
    st.markdown(f"""
    <div style="background: #f0f9ff; border: 1px solid #0369a1; padding: 0.75rem; 
                border-radius: 6px; margin: 0.5rem 0;">
        <div style="font-size: 0.9rem; color: #0369a1; font-weight: 600;">
            日本円換算価格 (1USD = ¥{current_rate:.2f})
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #1e40af;">
            {formatted_jpy} ({jpy_price:,.0f} JPY)
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_historical_usd_jpy_chart():
    """
    Get historical USD/JPY exchange rate chart
    
    Returns:
    --------
    plotly figure
        Chart showing USD/JPY historical rates
    """
    try:
        import plotly.graph_objects as go
        
        # Get USD/JPY historical data
        ticker = yf.Ticker("USDJPY=X")
        data = ticker.history(period="1y")
        
        if not data.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='USD/JPY',
                line=dict(color='#667eea', width=2)
            ))
            
            fig.update_layout(
                title="USD/JPY 為替レート推移 (過去1年)",
                xaxis_title="日付",
                yaxis_title="レート (JPY)",
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(family="Inter, sans-serif")
            )
            
            return fig
        else:
            return None
            
    except Exception as e:
        return None

def display_investment_impact_calculator():
    """
    Display calculator showing impact of exchange rate on investments
    """
    st.markdown("### 📊 為替変動の投資への影響計算")
    
    col1, col2 = st.columns(2)
    
    current_rate = get_current_usd_jpy_rate()
    
    with col1:
        investment_usd = st.number_input(
            "投資金額 (USD):",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            format="%.0f"
        )
        
        purchase_rate = st.number_input(
            "購入時のレート (JPY):",
            min_value=100.0,
            max_value=200.0,
            value=current_rate,
            step=0.1,
            format="%.2f"
        )
    
    with col2:
        current_rate_input = st.number_input(
            "現在のレート (JPY):",
            min_value=100.0,
            max_value=200.0,
            value=current_rate,
            step=0.1,
            format="%.2f"
        )
        
        # Calculate impact
        if investment_usd > 0:
            purchase_jpy = investment_usd * purchase_rate
            current_jpy = investment_usd * current_rate_input
            fx_impact = current_jpy - purchase_jpy
            fx_impact_percent = (fx_impact / purchase_jpy) * 100
            
            color = "#10b981" if fx_impact >= 0 else "#ef4444"
            symbol = "+" if fx_impact >= 0 else ""
            
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">為替損益</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {color};">
                    {symbol}{format_currency_jpy(fx_impact)}
                </div>
                <div style="font-size: 1rem; color: {color}; font-weight: 600;">
                    {symbol}{fx_impact_percent:.1f}%
                </div>
                <div style="font-size: 0.9rem; color: #64748b; margin-top: 0.5rem;">
                    購入時: {format_currency_jpy(purchase_jpy)}<br>
                    現在価値: {format_currency_jpy(current_jpy)}
                </div>
            </div>
            """, unsafe_allow_html=True)