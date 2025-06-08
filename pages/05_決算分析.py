import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

from auto_financial_data import get_auto_financial_data, calculate_growth_rate
from comprehensive_stock_data import search_stocks_by_name, get_all_tickers, get_stock_info, get_stocks_by_category, get_all_categories
from format_helpers import format_currency, format_large_number
from revenue_streams_analyzer import display_revenue_streams_analysis
from real_time_data import financial_chatbot

# Page configuration
st.set_page_config(page_title="決算分析", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #f0f0f0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1.5rem;
    }
    
    .feature-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .earnings-highlight {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .growth-positive {
        color: #10b981;
        font-weight: bold;
    }
    
    .growth-negative {
        color: #ef4444;
        font-weight: bold;
    }
    
    .growth-neutral {
        color: #6b7280;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📈 決算分析</div>
    <div class="hero-subtitle">
        企業の最新決算データから事業セグメント別売上、成長性、収益性を包括的に分析
    </div>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <div class="feature-badge">🏢 事業セグメント分析</div>
        <div class="feature-badge">📊 売上構成可視化</div>
        <div class="feature-badge">📈 成長トレンド分析</div>
        <div class="feature-badge">💡 戦略的インサイト</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Company selection
available_tickers = get_all_tickers()

st.markdown("### 📊 企業選択")

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("企業名またはティッカーで検索", placeholder="企業名またはティッカーシンボルを入力 (例: Apple, Tesla, AAPL)")
    if search_query:
        search_results = search_stocks_by_name(search_query)
        if search_results:
            available_tickers = search_results[:30]
        else:
            st.warning(f"'{search_query}' に一致する銘柄が見つかりません")

with col2:
    categories = ["All"] + get_all_categories()
    selected_category = st.selectbox("カテゴリー", categories)
    if selected_category != "All":
        available_tickers = get_stocks_by_category(selected_category)

st.info(f"選択可能銘柄数: {len(available_tickers)} | 包括的な株式データベース")

# Create options with company names
ticker_options = {}
for ticker in available_tickers:
    stock_info = get_stock_info(ticker)
    ticker_options[ticker] = f"{ticker} - {stock_info['name']}"

selected_ticker = st.selectbox(
    "企業を選択してください",
    options=available_tickers,
    index=0,
    format_func=lambda x: ticker_options.get(x, x),
    key="earnings_ticker_selection"
)

if st.button("🔄 データ更新", use_container_width=True):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("データを更新しました")
    st.rerun()

if selected_ticker:
    with st.spinner("最新の決算データを取得・分析中..."):
        # Get comprehensive financial data
        auto_data = get_auto_financial_data(selected_ticker)
        
        if auto_data:
            # Company overview section
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"### 🏢 {auto_data['name']} - 企業概要")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("現在株価", f"${auto_data['current_price']:.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                st.metric("時価総額", format_currency(market_cap, "$"))
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("年間売上", format_currency(auto_data['revenue'], "$"))
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("純利益", format_currency(auto_data['net_income'], "$"))
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col5:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                try:
                    stock = yf.Ticker(selected_ticker)
                    revenue_growth = calculate_growth_rate(stock)
                    growth_class = "growth-positive" if revenue_growth > 0 else "growth-negative" if revenue_growth < 0 else "growth-neutral"
                    st.markdown(f"<div class='metric-card'><div style='color: #6b7280; font-size: 0.9rem;'>売上成長率</div><div class='{growth_class}' style='font-size: 1.5rem;'>{revenue_growth:.1f}%</div></div>", unsafe_allow_html=True)
                except:
                    st.metric("売上成長率", "N/A")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Revenue streams analysis (main feature)
            display_revenue_streams_analysis(selected_ticker)
            
            # Quarterly earnings trend
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 📊 四半期決算トレンド")
            
            try:
                stock = yf.Ticker(selected_ticker)
                quarterly_financials = stock.quarterly_financials
                
                if not quarterly_financials.empty and len(quarterly_financials.columns) >= 4:
                    # Extract quarterly revenue data
                    revenue_data = []
                    if 'Total Revenue' in quarterly_financials.index:
                        for col in quarterly_financials.columns[:8]:  # Last 8 quarters
                            quarter = col.strftime('%Y Q%m') if hasattr(col, 'strftime') else str(col)
                            revenue = quarterly_financials.loc['Total Revenue', col]
                            if pd.notna(revenue):
                                revenue_data.append({
                                    'Quarter': quarter,
                                    'Revenue': revenue / 1e9,  # Convert to billions
                                    'YoY_Growth': 0  # Will calculate below
                                })
                    
                    if len(revenue_data) >= 4:
                        # Calculate YoY growth
                        for i in range(len(revenue_data)):
                            if i >= 4:  # Compare with same quarter last year
                                current_revenue = revenue_data[i]['Revenue']
                                prev_year_revenue = revenue_data[i-4]['Revenue']
                                if prev_year_revenue > 0:
                                    yoy_growth = ((current_revenue - prev_year_revenue) / prev_year_revenue) * 100
                                    revenue_data[i]['YoY_Growth'] = yoy_growth
                        
                        # Create visualization
                        df = pd.DataFrame(revenue_data)
                        
                        fig = go.Figure()
                        
                        # Revenue bars
                        fig.add_trace(go.Bar(
                            x=df['Quarter'],
                            y=df['Revenue'],
                            name='四半期売上 (B$)',
                            marker_color='#667eea',
                            yaxis='y'
                        ))
                        
                        # YoY growth line
                        fig.add_trace(go.Scatter(
                            x=df['Quarter'],
                            y=df['YoY_Growth'],
                            mode='lines+markers',
                            name='前年同期比成長率 (%)',
                            line=dict(color='#10b981', width=3),
                            marker=dict(size=8),
                            yaxis='y2'
                        ))
                        
                        fig.update_layout(
                            title=f"{auto_data['name']} - 四半期売上トレンド",
                            xaxis_title="四半期",
                            yaxis=dict(title="売上 (億ドル)", side="left"),
                            yaxis2=dict(title="前年同期比成長率 (%)", side="right", overlaying="y"),
                            height=500,
                            legend=dict(x=0.01, y=0.99)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Recent performance summary
                        latest_quarter = revenue_data[0] if revenue_data else None
                        if latest_quarter:
                            st.markdown(f"""
                            <div class="earnings-highlight">
                                <h4>📈 最新四半期ハイライト</h4>
                                <p><strong>売上:</strong> ${latest_quarter['Revenue']:.1f}B</p>
                                <p><strong>前年同期比成長率:</strong> 
                                <span class="{'growth-positive' if latest_quarter['YoY_Growth'] > 0 else 'growth-negative'}">{latest_quarter['YoY_Growth']:.1f}%</span></p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("四半期データが不足しているため、トレンド分析を表示できません")
                else:
                    st.info("四半期財務データが利用できません")
            except Exception as e:
                st.warning("四半期データの取得に失敗しました")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Profitability analysis
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 💰 収益性分析")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                if auto_data['revenue'] > 0:
                    gross_margin = (auto_data['net_income'] / auto_data['revenue']) * 100
                    st.metric("純利益率", f"{gross_margin:.1f}%")
                else:
                    st.metric("純利益率", "N/A")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("ROE", f"{auto_data.get('roe', 0):.1f}%")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                if auto_data['eps'] > 0:
                    pe_ratio = auto_data['current_price'] / auto_data['eps']
                    st.metric("PER", f"{pe_ratio:.1f}倍")
                else:
                    st.metric("PER", "N/A")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                if auto_data['revenue'] > 0:
                    market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                    ps_ratio = market_cap / auto_data['revenue']
                    st.metric("PSR", f"{ps_ratio:.1f}倍")
                else:
                    st.metric("PSR", "N/A")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # AI-powered earnings analysis
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🤖 AI決算分析レポート")
            
            with st.spinner("AIが最新決算を分析中..."):
                try:
                    analysis_query = f"""
                    {selected_ticker} ({auto_data['name']})の最新決算について、以下の観点から包括的な分析を日本語で提供してください：
                    
                    1. **業績ハイライト**: 売上・利益の前年同期比変化
                    2. **事業セグメント別動向**: 各事業の成長状況
                    3. **収益性分析**: マージンや効率性の変化
                    4. **将来見通し**: ガイダンスや戦略的方向性
                    5. **投資家への影響**: 株価への潜在的インパクト
                    
                    現在の財務データ:
                    - 売上: ${auto_data['revenue']:.1f}M
                    - 純利益: ${auto_data['net_income']:.1f}M
                    - 売上成長率: {revenue_growth:.1f}%
                    - 純利益率: {(auto_data['net_income']/auto_data['revenue']*100 if auto_data['revenue'] > 0 else 0):.1f}%
                    
                    簡潔で読みやすい形式で分析してください。
                    """
                    
                    ai_analysis = financial_chatbot(analysis_query)
                    
                    if ai_analysis and "API key" not in ai_analysis and "quota" not in ai_analysis:
                        formatted_analysis = ai_analysis.replace('\n', '<br>')
                        st.markdown(f"""
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #667eea;">
                        {formatted_analysis}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("AI分析を実行するには、OpenAI APIキーが必要です。")
                        
                        # Fallback to basic analysis
                        st.markdown(f"""
                        <div class="earnings-highlight">
                        <h4>📊 基本分析サマリー</h4>
                        <p><strong>売上規模:</strong> {format_currency(auto_data['revenue'], '$')}</p>
                        <p><strong>収益性:</strong> 純利益率 {(auto_data['net_income']/auto_data['revenue']*100 if auto_data['revenue'] > 0 else 0):.1f}%</p>
                        <p><strong>成長性:</strong> 売上成長率 <span class="{'growth-positive' if revenue_growth > 0 else 'growth-negative'}">{revenue_growth:.1f}%</span></p>
                        <p><strong>バリュエーション:</strong> PER {pe_ratio:.1f}倍 (業界平均との比較推奨)</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error("AI分析の実行中にエラーが発生しました")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            st.error("選択された企業の財務データを取得できませんでした")