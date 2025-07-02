import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from auto_financial_data import get_auto_financial_data
from comprehensive_stock_data import get_all_tickers, get_stock_info, get_stocks_by_category, get_all_categories
from comprehensive_market_stocks import get_all_market_stocks, get_stock_info_enhanced, search_stocks_comprehensive, get_stock_sector_mapping, get_market_categories
from format_helpers import format_currency, format_large_number

# Modern design CSS
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
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Cards */
    .filter-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .investment-style {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">🔍 銘柄発見</div>
    <div class="page-subtitle">米国株式800銘柄以上から投資スタイルに合った企業を発見</div>
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; border-radius: 8px; margin: 15px 0; font-size: 14px;">
        <strong>🇺🇸 検索対象:</strong> S&P500 • NASDAQ • ダウ30 • Russell2000 • 成長株 • バイオテック • フィンテック • クリーンエネルギー • 暗号通貨関連株など<br>
        <strong>📊 米国株式データベース:</strong> 主要取引所の800銘柄以上をリアルタイム分析 • 投資スタイル別検索 • 業界別検索 • 高速モード対応
    </div>
</div>
""", unsafe_allow_html=True)

# Investment style guide
with st.expander("💡 投資スタイルガイド - どの投資戦略があなたに合っているか？"):
    st.markdown("""
    <div class="investment-style">
    <h4>🚀 成長株投資</h4>
    <p><strong>特徴:</strong> 高い成長率を持つ企業に投資</p>
    <p><strong>適した方:</strong> リスクを取ってでも高いリターンを目指したい方</p>
    <p><strong>スクリーニング条件:</strong> 売上成長率 > 15%, ROE > 15%, PEG < 2</p>
    </div>
    
    <div class="investment-style">
    <h4>💰 バリュー株投資</h4>
    <p><strong>特徴:</strong> 割安で取引されている優良企業に投資</p>
    <p><strong>適した方:</strong> 安定性を重視し、長期的な値上がりを期待する方</p>
    <p><strong>スクリーニング条件:</strong> PER < 15, PBR < 2, 配当利回り > 2%</p>
    </div>
    
    <div class="investment-style">
    <h4>💵 配当株投資</h4>
    <p><strong>特徴:</strong> 安定した配当収入を重視</p>
    <p><strong>適した方:</strong> 定期的な収入を求める方、リタイア世代</p>
    <p><strong>スクリーニング条件:</strong> 配当利回り > 3%, 配当性向 < 60%</p>
    </div>
    
    <div class="investment-style">
    <h4>🛡️ 安定株投資</h4>
    <p><strong>特徴:</strong> 財務が安定した大型株中心</p>
    <p><strong>適した方:</strong> リスクを抑えて着実に資産を増やしたい方</p>
    <p><strong>スクリーニング条件:</strong> 時価総額 > 100億ドル, 負債比率 < 0.5, 流動比率 > 1.5</p>
    </div>
    """, unsafe_allow_html=True)

# Stock screening filters
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
st.markdown("### 🎯 スクリーニング条件を設定")

# Investment style presets
col1, col2 = st.columns([2, 1])

with col1:
    # Search method selection
    search_method = st.radio(
        "検索方法を選択",
        ["投資スタイル別", "業界別"],
        horizontal=True,
        help="投資スタイル別：成長株、バリュー株、配当株から選択 | 業界別：特定の業界から銘柄を探す"
    )
    
    if search_method == "投資スタイル別":
        st.markdown("**投資スタイルを選択 (プリセット条件)**")
        investment_style = st.selectbox(
            "投資スタイル選択",
            ["カスタム設定", "成長株投資", "バリュー株投資", "配当株投資", "安定株投資"],
            label_visibility="collapsed"
        )
    else:
        st.markdown("**業界を選択**")
        industry_options = [
            "すべての業界",
            "テクノロジー", 
            "ヘルスケア・バイオテック",
            "金融サービス",
            "消費者向けサービス", 
            "消費者向け日用品",
            "エネルギー・石油ガス",
            "クリーンエネルギー・再生可能エネルギー",
            "電気自動車・自動車",
            "不動産・REIT",
            "産業・製造業", 
            "素材・鉱業",
            "通信・メディア",
            "公益事業",
            "エンターテイメント・メディア",
            "ゲーミング・カジノ",
            "大麻・代替投資",
            "暗号通貨関連",
            "小売・Eコマース"
        ]
        selected_industry = st.selectbox(
            "業界選択",
            industry_options,
            label_visibility="collapsed"
        )

with col2:
    fast_mode = st.checkbox("⚡ 高速モード", value=True, help="500銘柄を約1-2分で検索（推奨）")
    if st.button("🔄 条件をリセット", use_container_width=True):
        st.rerun()

# Set default values based on search method
if search_method == "投資スタイル別":
    if investment_style == "成長株投資":
        default_revenue_growth = (15.0, 50.0)
        default_roe = (15.0, 100.0)
        default_per = (0.0, 30.0)
        default_market_cap = (1.0, 5000.0)
    elif investment_style == "バリュー株投資":
        default_revenue_growth = (0.0, 50.0)
        default_roe = (10.0, 100.0)
        default_per = (0.0, 15.0)
        default_market_cap = (10.0, 5000.0)
    elif investment_style == "配当株投資":
        default_revenue_growth = (0.0, 50.0)
        default_roe = (8.0, 100.0)
        default_per = (0.0, 25.0)
        default_market_cap = (5.0, 5000.0)
    elif investment_style == "安定株投資":
        default_revenue_growth = (0.0, 50.0)
        default_roe = (10.0, 100.0)
        default_per = (0.0, 20.0)
        default_market_cap = (100.0, 5000.0)
    else:  # カスタム設定
        default_revenue_growth = (0.0, 50.0)
        default_roe = (0.0, 100.0)
        default_per = (0.0, 50.0)
        default_market_cap = (0.1, 5000.0)
else:  # 業界別検索
    # Industry-based search uses more relaxed default criteria
    default_revenue_growth = (0.0, 50.0)
    default_roe = (0.0, 100.0)
    default_per = (0.0, 50.0)
    default_market_cap = (0.1, 5000.0)

# Screening criteria
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**財務指標**")
    
    revenue_growth_range = st.slider(
        "売上成長率 (%)",
        min_value=0.0,
        max_value=50.0,
        value=default_revenue_growth,
        step=0.5,
        help="過去の年間売上成長率"
    )
    
    roe_range = st.slider(
        "ROE (%)",
        min_value=0.0,
        max_value=100.0,
        value=default_roe,
        step=1.0,
        help="自己資本利益率"
    )
    
    roa_range = st.slider(
        "ROA (%)",
        min_value=0.0,
        max_value=30.0,
        value=(0.0, 30.0),
        step=0.5,
        help="総資産利益率"
    )

with col2:
    st.markdown("**バリュエーション**")
    
    per_range = st.slider(
        "PER",
        min_value=0.0,
        max_value=50.0,
        value=default_per,
        step=0.5,
        help="株価収益率"
    )
    
    pbr_range = st.slider(
        "PBR",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1,
        help="株価純資産倍率"
    )
    
    profit_margin_range = st.slider(
        "純利益率 (%)",
        min_value=0.0,
        max_value=50.0,
        value=(0.0, 50.0),
        step=1.0,
        help="売上に対する純利益の割合"
    )

with col3:
    st.markdown("**企業規模・安定性**")
    
    market_cap_range = st.slider(
        "時価総額 (億ドル)",
        min_value=0.1,
        max_value=5000.0,
        value=default_market_cap,
        step=0.1,
        help="企業の規模"
    )
    
    debt_ratio_range = st.slider(
        "負債比率",
        min_value=0.0,
        max_value=2.0,
        value=(0.0, 2.0),
        step=0.1,
        help="負債÷自己資本"
    )
    
    current_ratio_range = st.slider(
        "流動比率",
        min_value=0.0,
        max_value=5.0,
        value=(0.0, 5.0),
        step=0.1,
        help="流動資産÷流動負債"
    )

# Sector filter - use comprehensive market sectors
sectors = ["All"] + list(get_stock_sector_mapping().keys())
selected_sectors = st.multiselect(
    "業界・セクター",
    sectors,
    default=["All"],
    help="特定の業界に絞り込み"
)

st.markdown('</div>', unsafe_allow_html=True)

# Search button
if st.button("🔍 銘柄を検索", use_container_width=True, type="primary"):
    
    with st.spinner("条件に合う銘柄を検索中..."):
        # Get all market stocks for comprehensive screening
        if search_method == "業界別":
            # Industry-based filtering
            if selected_industry == "すべての業界":
                available_tickers = get_all_market_stocks()
            else:
                # Map Japanese industry names to sector keys
                industry_mapping = {
                    "テクノロジー": "Technology",
                    "ヘルスケア・バイオテック": "Healthcare", 
                    "金融サービス": "Financials",
                    "消費者向けサービス": "Consumer Discretionary",
                    "消費者向け日用品": "Consumer Staples",
                    "エネルギー・石油ガス": "Energy",
                    "クリーンエネルギー・再生可能エネルギー": "Clean Energy",
                    "電気自動車・自動車": "Automotive",
                    "不動産・REIT": "Real Estate",
                    "産業・製造業": "Industrial",
                    "素材・鉱業": "Materials", 
                    "通信・メディア": "Telecommunications",
                    "公益事業": "Utilities",
                    "エンターテイメント・メディア": "Entertainment",
                    "ゲーミング・カジノ": "Gaming",
                    "大麻・代替投資": "Cannabis",
                    "暗号通貨関連": "Crypto-Related",
                    "小売・Eコマース": "Retail"
                }
                
                sector_key = industry_mapping.get(selected_industry)
                sector_mapping = get_stock_sector_mapping()
                available_tickers = []
                
                if sector_key and sector_key in sector_mapping:
                    available_tickers = sector_mapping[sector_key]
                else:
                    available_tickers = get_all_market_stocks()
        else:
            # Original sector-based filtering for investment style search
            if "All" in selected_sectors or not selected_sectors:
                available_tickers = get_all_market_stocks()
            else:
                # Filter by sector from comprehensive market stocks
                sector_mapping = get_stock_sector_mapping()
                available_tickers = []
                for sector in selected_sectors:
                    if sector != "All" and sector in sector_mapping:
                        available_tickers.extend(sector_mapping[sector])
                available_tickers = list(set(available_tickers))
        
        # Use comprehensive market coverage - remove artificial limit
        # Now screening from thousands of stocks instead of just 200
        st.info(f"📊 {len(available_tickers):,}銘柄から条件に合致する企業を検索中...")
        
        # Optimize performance based on user selection
        if fast_mode:
            max_process = min(500, len(available_tickers))  # Fast mode: 500 stocks for 1-2 minute response
            st.info("⚡ 高速モード: 上位500銘柄を約1-2分で検索します")
        else:
            max_process = min(2000, len(available_tickers))  # Full mode: up to 2000 stocks (slower)
            st.info("🔍 フルモード: 最大2,000銘柄を検索します（5-10分程度）")
        
        available_tickers = available_tickers[:max_process]
        
        # Pre-filter out known delisted/problematic stocks to improve performance
        delisted_stocks = {
            'ALXN', 'APHA', 'ATVI', 'BBBY', 'NAKD', 'SNDL', 'EXPR', 'KOSS', 'BF.B',
            'BLUE', 'BOOKING', 'BRK.B', 'CERN', 'COUP', 'CTXS', 'CELG', 'MYL',
            'WORK', 'XLNX', 'MXIM', 'TCOM', 'PARA', 'WBD'
        }
        available_tickers = [t for t in available_tickers if t not in delisted_stocks]
        
        # Fix common ticker naming issues
        ticker_fixes = {
            'BRK.B': 'BRK-B',
            'BF.B': 'BF-B'
        }
        available_tickers = [ticker_fixes.get(t, t) for t in available_tickers]
        
        # Screen stocks
        matching_stocks = []
        processed_count = 0
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, ticker in enumerate(available_tickers):
            try:
                status_text.text(f"分析中: {ticker} ({i+1}/{len(available_tickers)})")
                progress_bar.progress((i + 1) / len(available_tickers))
                
                # Get financial data
                data = get_auto_financial_data(ticker)
                if not data:
                    continue
                
                processed_count += 1
                
                # Check screening criteria
                passes_screen = True
                
                # Revenue growth
                revenue_growth = data.get('historical_growth', 0) or 0
                if not (revenue_growth_range[0] <= revenue_growth <= revenue_growth_range[1]):
                    continue
                
                # ROE
                roe = data.get('roe', 0) or 0
                if not (roe_range[0] <= roe <= roe_range[1]):
                    continue
                
                # ROA
                roa = data.get('roa', 0) or 0
                if not (roa_range[0] <= roa <= roa_range[1]):
                    continue
                
                # PER
                per = data.get('pe_ratio', 0) or 0
                if per > 0 and not (per_range[0] <= per <= per_range[1]):
                    continue
                
                # PBR
                pbr = data.get('pb_ratio', 0) or 0
                if pbr > 0 and not (pbr_range[0] <= pbr <= pbr_range[1]):
                    continue
                
                # Profit margin
                profit_margin = data.get('profit_margin', 0) or 0
                if not (profit_margin_range[0] <= profit_margin <= profit_margin_range[1]):
                    continue
                
                # Market cap (convert to billions)
                market_cap_billions = (data.get('market_cap', 0) or 0) / 1000
                if not (market_cap_range[0] <= market_cap_billions <= market_cap_range[1]):
                    continue
                
                # Debt ratio
                debt_ratio = data.get('debt_to_equity', 0) or 0
                if not (debt_ratio_range[0] <= debt_ratio <= debt_ratio_range[1]):
                    continue
                
                # Current ratio
                current_ratio = data.get('current_ratio', 0) or 0
                if current_ratio > 0 and not (current_ratio_range[0] <= current_ratio <= current_ratio_range[1]):
                    continue
                
                # If all criteria pass, add to results
                matching_stocks.append({
                    'ticker': ticker,
                    'name': data.get('name', ticker),
                    'sector': data.get('sector', 'Unknown'),
                    'current_price': data.get('current_price', 0),
                    'market_cap': data.get('market_cap', 0),
                    'revenue_growth': revenue_growth,
                    'roe': roe,
                    'roa': roa,
                    'pe_ratio': per,
                    'pb_ratio': pbr,
                    'profit_margin': profit_margin,
                    'debt_ratio': debt_ratio,
                    'current_ratio': current_ratio,
                    'data': data
                })
                
            except Exception as e:
                continue
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        st.markdown(f"### 🎯 検索結果: {len(matching_stocks)}銘柄が条件に合致")
        st.markdown(f"<small>分析対象: {processed_count}銘柄 | 投資スタイル: {investment_style}</small>", unsafe_allow_html=True)
        
        if matching_stocks:
            # Sort by market cap descending
            matching_stocks.sort(key=lambda x: x['market_cap'], reverse=True)
            
            # Display results in cards
            for i, stock in enumerate(matching_stocks[:20]):  # Show top 20 results
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{stock['ticker']} - {stock['name']}**")
                    st.markdown(f"セクター: {stock['sector']}")
                    st.markdown(f"現在株価: ${stock['current_price']:.2f}")
                
                with col2:
                    # Key metrics
                    if stock['revenue_growth'] > 0:
                        st.markdown(f"<span class='metric-badge'>成長率 {stock['revenue_growth']:.1f}%</span>", unsafe_allow_html=True)
                    if stock['roe'] > 0:
                        st.markdown(f"<span class='metric-badge'>ROE {stock['roe']:.1f}%</span>", unsafe_allow_html=True)
                    if stock['pe_ratio'] > 0:
                        st.markdown(f"<span class='metric-badge'>PER {stock['pe_ratio']:.1f}</span>", unsafe_allow_html=True)
                
                with col3:
                    market_cap_billions = stock['market_cap'] / 1000
                    st.metric("時価総額", f"${market_cap_billions:.1f}B")
                
                # Detailed metrics in expandable section
                with st.expander(f"📊 {stock['ticker']} 詳細データ"):
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    
                    with metric_col1:
                        st.write(f"**売上成長率:** {stock['revenue_growth']:.1f}%")
                        st.write(f"**ROE:** {stock['roe']:.1f}%")
                        st.write(f"**ROA:** {stock['roa']:.1f}%")
                    
                    with metric_col2:
                        st.write(f"**PER:** {stock['pe_ratio']:.1f}")
                        st.write(f"**PBR:** {stock['pb_ratio']:.1f}")
                        st.write(f"**純利益率:** {stock['profit_margin']:.1f}%")
                    
                    with metric_col3:
                        st.write(f"**負債比率:** {stock['debt_ratio']:.2f}")
                        st.write(f"**流動比率:** {stock['current_ratio']:.2f}")
                        st.write(f"**時価総額:** ${market_cap_billions:.1f}B")
                
                st.markdown('</div>', unsafe_allow_html=True)
            

        
        else:
            st.warning("条件に合致する銘柄が見つかりませんでした。条件を緩和して再検索してください。")
            
            # Suggestions for better results
            st.markdown("""
            ### 💡 検索のコツ
            - 条件範囲を広げてみてください
            - 投資スタイルのプリセットを試してみてください
            - 特定のセクターに絞り込んでみてください
            - 時価総額の範囲を調整してみてください
            """)

# Investment tips
with st.expander("💡 投資のアドバイス"):
    st.markdown("""
    ### 銘柄選択のポイント
    
    **1. 分散投資を心がける**
    - 異なるセクターから複数の銘柄を選択
    - 時価総額の違う企業を組み合わせる
    
    **2. ファンダメンタルズを重視**
    - 財務の健全性（負債比率、流動比率）
    - 収益性（ROE、ROA、純利益率）
    - 成長性（売上成長率）
    
    **3. バリュエーションを確認**
    - PER、PBRが適正水準か
    - 同業他社との比較
    
    **4. 継続的なモニタリング**
    - 定期的な財務データの確認
    - 業界トレンドの把握
    - 経営陣の方針変更に注意
    
    **注意:** このツールは投資判断の参考情報です。実際の投資は自己責任で行ってください。
    """)