import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys
import os

# フォーマット用ヘルパー関数
from format_helpers import format_currency, format_large_number, format_ja_number

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# stock_dataモジュールをインポート
from stock_data import get_stock_data, update_stock_price, fetch_tradingview_price
from real_time_fetcher import fetch_current_stock_price, fetch_comprehensive_data, show_live_price_indicator, display_market_status
from comprehensive_stock_data import search_stocks_by_name, get_all_tickers, get_stock_info, get_stocks_by_category, get_all_categories

# ページ設定は main app.py で処理済み

# Modern design CSS consistent with homepage
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #222222;
    }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        margin: -2rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cards */
    .analysis-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }
    
    .card-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #222222;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Metrics */
    .metric-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #717171;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #5a67d8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Input fields */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div {
        border-radius: 10px;
    }
    
    /* Charts */
    .plotly-chart {
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Recommendation badges */
    .recommendation-box {
        border-radius: 50px;
        padding: 1rem 2rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .recommendation-buy {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .recommendation-hold {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    .recommendation-sell {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
    }
    
    /* Navigation */
    .nav-pills {
        display: flex;
        background: #f8f9fa;
        border-radius: 50px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .nav-pill {
        flex: 1;
        text-align: center;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        background: transparent;
        color: #717171;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-pill.active {
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">📊 ビジネスモデル分析</div>
    <div class="page-subtitle">財務データとファンダメンタルズ分析で企業の本質的価値を見極める</div>
</div>
""", unsafe_allow_html=True)

# 分析手法の説明を追加
with st.expander("🔍 分析手法について詳しく"):
    st.markdown("""
    <h3>このページの分析手法</h3>
    <p>このページでは以下の分析手法を組み合わせて、総合的な企業分析を行います。</p>
    
    <h4>1. ファンダメンタル分析</h4>
    <p>企業の財務データや事業内容を定量的・定性的に分析し、企業の価値や成長性を評価します。</p>
    <ul>
        <li>財務諸表の分析（売上高、利益、成長率など）</li>
        <li>財務比率の評価（PER、PBR、PSR、ROEなど）</li>
        <li>市場シェアと業界内ポジションの分析</li>
        <li>経営陣の質と経営戦略の評価</li>
    </ul>
    
    <h4>2. SWOT分析</h4>
    <p>企業の内部・外部環境を4つの視点から分析します。</p>
    <ul>
        <li><strong>S</strong>trengths（強み）：企業の内部的な長所</li>
        <li><strong>W</strong>eaknesses（弱み）：企業の内部的な短所</li>
        <li><strong>O</strong>pportunities（機会）：外部環境からの好機</li>
        <li><strong>T</strong>hreats（脅威）：外部環境からの脅威</li>
    </ul>
    
    <h4>3. 競争優位性（モート）分析</h4>
    <p>企業が長期的に競争優位性を維持できる「堀（モート）」を評価します。</p>
    <ul>
        <li>ブランド力</li>
        <li>ネットワーク効果</li>
        <li>コスト優位性</li>
        <li>切替コスト</li>
        <li>特許・知的財産</li>
    </ul>
    
    <h4>4. 最新の注目ポイント分析</h4>
    <p>企業の最新の決算発表や重要イベント、市場トレンドなどを分析し、投資判断に重要な最新情報を提供します。</p>
    <ul>
        <li>決算発表のハイライト</li>
        <li>経営陣のコメントと将来見通し</li>
        <li>新製品・サービスの展開状況</li>
        <li>業界トレンドとの整合性</li>
        <li>市場の反応と専門家の意見</li>
    </ul>
    """, unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("### 企業分析ツール")
    st.markdown("企業のファンダメンタルズを分析し、最新の注目ポイントを提供することで投資判断をサポートします。")
    
    st.markdown("---")
    
    # ナビゲーション
    st.markdown("### ナビゲーション")
    if st.button("ホームに戻る", key="home_btn"):
        st.switch_page("app.py")
    
    if st.button("銘柄比較", key="compare_btn"):
        st.switch_page("pages/02_銘柄比較.py")
        
    if st.button("DCF価値計算機", key="dcf_btn"):
        st.switch_page("pages/04_DCF価値計算機.py")

# Enhanced stock selection with fundamental analysis filter
st.markdown("<div class='form-section mobile-card'>", unsafe_allow_html=True)
st.markdown("<h2>📊 企業を選択</h2>", unsafe_allow_html=True)

# Import fundamental analysis data
from fundamental_analysis_data import get_supported_tickers, display_fundamental_analysis

# Only show companies with comprehensive fundamental analysis data
available_tickers = get_supported_tickers()

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("企業名またはティッカーで検索", placeholder="例: Apple, Microsoft, AAPL, MSFT")
    if search_query:
        # Filter supported tickers based on search
        search_results = [ticker for ticker in available_tickers 
                         if search_query.upper() in ticker or 
                         search_query.lower() in get_stock_info(ticker)['name'].lower()]
        if search_results:
            available_tickers = search_results
        else:
            st.warning(f"'{search_query}' に一致する銘柄が見つかりません")

with col2:
    st.info(f"分析対象: {len(available_tickers)}社")

# Create options with company names for better UX
ticker_options = {}
for ticker in available_tickers:
    stock_info = get_stock_info(ticker)
    ticker_options[ticker] = f"{ticker} - {stock_info['name']}"

selected_ticker = st.selectbox(
    "ファンダメンタル分析対象企業を選択",
    options=available_tickers,
    index=0,
    format_func=lambda x: ticker_options.get(x, x),
    key="fundamental_ticker_selection"
)

st.markdown("</div>", unsafe_allow_html=True)

# Execute comprehensive fundamental analysis
if selected_ticker:
    analysis_success = display_fundamental_analysis(selected_ticker)
    
    if not analysis_success:
        st.error("選択された企業の詳細分析データが利用できません。")
else:
    st.info("企業を選択してファンダメンタル分析を開始してください。")
