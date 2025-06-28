import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import json

# フォーマット用ヘルパー関数
from format_helpers import format_currency, format_large_number, format_ja_number

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# stock_dataモジュールをインポート
from stock_data import get_stock_data, get_available_tickers, compare_valuations, get_industry_average
from stock_data import update_stock_price, fetch_tradingview_price, refresh_stock_prices
from stock_data import load_sample_data, ensure_sample_data_dir, SAMPLE_DATA_DIR
from comprehensive_stock_data import search_stocks_by_name, get_all_tickers, get_stock_info, get_stocks_by_category, get_all_categories
from real_time_fetcher import fetch_current_stock_price, fetch_comprehensive_data, show_live_price_indicator, display_market_status
from auto_financial_data import get_auto_financial_data, calculate_growth_rate
from historical_metrics_chart import display_historical_metrics_chart
from market_comparison import display_stock_market_comparison, create_individual_stock_comparison_chart
from session_state_manager import init_session_state, reset_comparison_analysis, should_reset_comparison_analysis

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
        color: #0066cc;
    }
    
    .metric-box {
        border-radius: 10px;
        padding: 1rem;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0066cc;
    }
    
    .value-positive {
        color: #198754;
    }
    
    .value-negative {
        color: #dc3545;
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .comparison-table th, .comparison-table td {
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
    }
    
    .comparison-table th {
        background-color: #f8f9fa;
        font-weight: bold;
        color: #495057;
    }
    
    .comparison-table tr:hover {
        background-color: #f1f3f5;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# サイドバー
with st.sidebar:
    st.markdown("### 銘柄比較ツール")
    st.markdown("複数の株式を選択して様々な評価方法で比較します。")
    
    st.markdown("---")
    
    # ナビゲーション
    st.markdown("### ナビゲーション")
    if st.button("ホームに戻る", key="home_btn"):
        st.switch_page("app.py")
    
    if st.button("企業分析", key="analysis_btn"):
        st.switch_page("pages/01_企業分析.py")

# Hero section - TravelPerk style
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 3rem 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
    <div style="text-align: center;">
        <div style="font-size: 2.8rem; font-weight: 700; color: #1a202c; margin-bottom: 1rem;">
            🔍 企業価値比較分析
        </div>
        <div style="font-size: 1.3rem; color: #4a5568; margin-bottom: 2rem; max-width: 800px; margin-left: auto; margin-right: auto;">
            複数企業の財務指標をリアルタイムで比較し、データに基づいた投資判断をサポート
        </div>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <div style="background: white; padding: 1rem 1.5rem; border-radius: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <span style="color: #667eea; font-weight: 600;">📊 リアルタイム財務データ</span>
            </div>
            <div style="background: white; padding: 1rem 1.5rem; border-radius: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <span style="color: #764ba2; font-weight: 600;">⚡ 瞬時比較分析</span>
            </div>
            <div style="background: white; padding: 1rem 1.5rem; border-radius: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <span style="color: #10b981; font-weight: 600;">🎯 投資判断支援</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display market status
display_market_status()

# 入力フォームエリア
st.markdown("""
<div class="analysis-card">
    <div class="card-header">📊 企業選択・比較</div>
</div>
""", unsafe_allow_html=True)

# 利用可能なティッカーシンボル（数百銘柄）
available_tickers = get_all_tickers()

# データ更新ボタン
if st.button("🔄 データ更新", key="refresh_all_data"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("データを更新しました！")
    st.rerun()

# Search and filter interface
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "", 
        placeholder="企業名またはティッカーシンボルを入力 (例: Apple, Microsoft, AAPL, MSFT)", 
        help="企業名の一部またはティッカーシンボルで検索できます",
        label_visibility="collapsed"
    )

with col2:
    categories = ["All"] + get_all_categories()
    selected_category = st.selectbox("カテゴリー", categories)

# Apply search and category filters
if search_query:
    search_results = search_stocks_by_name(search_query)
    if search_results:
        available_tickers = search_results[:50]
    else:
        st.warning(f"'{search_query}' に一致する銘柄が見つかりません")
        available_tickers = get_all_tickers()[:50]
else:
    available_tickers = get_all_tickers()

if selected_category != "All":
    category_tickers = get_stocks_by_category(selected_category)
    if search_query:
        # Intersection of search results and category
        available_tickers = [t for t in available_tickers if t in category_tickers]
    else:
        available_tickers = category_tickers

# Create options with company names
ticker_options = {}
for ticker in available_tickers:
    stock_info = get_stock_info(ticker)
    ticker_options[ticker] = f"{ticker} - {stock_info['name']}"



# 統合された銘柄選択（最大8つまで）
st.markdown("**比較銘柄選択**")
selected_tickers = st.multiselect(
    "比較する銘柄を選択してください（最大8つ）",
    options=list(ticker_options.keys()),
    format_func=lambda x: ticker_options[x],
    default=list(ticker_options.keys())[:2] if len(ticker_options) >= 2 else [],
    help="複数の銘柄を選択して財務指標を比較できます"
)

# Continue with selected tickers for analysis

# 評価方法の選択とメトリクス表示
st.markdown("<div class='mobile-card'>", unsafe_allow_html=True)
st.markdown("<h3>表示する指標を選択</h3>", unsafe_allow_html=True)

# メトリクス選択用のチェックボックス
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**基本指標**")
    use_pe = st.checkbox("PER (株価収益率)", value=True)
    use_pb = st.checkbox("PBR (株価純資産倍率)", value=True)
    use_ps = st.checkbox("PSR (株価売上高倍率)", value=True)

with col2:
    st.markdown("**成長・効率指標**")
    show_revenue_growth = st.checkbox("売上成長率", value=True)
    show_peg = st.checkbox("PEG倍率", value=True)
    show_roe = st.checkbox("ROE (自己資本利益率)", value=True)
    show_roa = st.checkbox("ROA (総資産利益率)", value=True)
    show_profit_margin = st.checkbox("純利益率", value=True)
    show_gross_margin = st.checkbox("売上総利益率", value=False)
    show_operating_margin = st.checkbox("営業利益率", value=False)

with col3:
    st.markdown("**財務健全性指標**")
    show_dividend = st.checkbox("配当利回り", value=True)
    show_debt_ratio = st.checkbox("負債比率", value=True)
    show_current_ratio = st.checkbox("流動比率", value=True)
    show_asset_turnover = st.checkbox("総資産回転率", value=False)
    show_eps = st.checkbox("EPS (1株利益)", value=True)
    show_company_size = st.checkbox("企業規模", value=True)

# 評価方法を配列に格納
valuation_methods = []
if use_pe:
    valuation_methods.append("pe_ratio")
if use_pb:
    valuation_methods.append("pb_ratio")
if use_ps:
    valuation_methods.append("ps_ratio")

# Initialize session state for comparison data
if 'stored_comparison_results' not in st.session_state:
    st.session_state.stored_comparison_results = {}
if 'stored_comparison_tickers' not in st.session_state:
    st.session_state.stored_comparison_tickers = []
if 'stored_comparison_methods' not in st.session_state:
    st.session_state.stored_comparison_methods = []

# Check if we need to recompute comparison (only when tickers or methods change)
need_recompute = (
    set(selected_tickers) != set(st.session_state.stored_comparison_tickers) or
    set(valuation_methods) != set(st.session_state.stored_comparison_methods) or
    not st.session_state.stored_comparison_results
)

# 比較ボタン
comparison_button_clicked = False
if need_recompute:
    comparison_button_clicked = st.button("比較を実行", key="compare_btn", use_container_width=True)
else:
    # Show that comparison is already available
    st.success(f"比較済み: {len(st.session_state.stored_comparison_tickers)}銘柄 | 銘柄や指標を変更した場合は「比較を再実行」ボタンを押してください")
    comparison_button_clicked = st.button("比較を再実行", key="recompare_btn", use_container_width=True)
    if comparison_button_clicked:
        # Force recompute
        st.session_state.stored_comparison_results = {}

# Execute comparison if button was clicked and parameters are valid
if comparison_button_clicked:
    if len(selected_tickers) == 0:
        st.warning("少なくとも1つの銘柄を選択してください。")
    elif len(selected_tickers) > 8:
        st.warning("最大8つの銘柄までしか比較できません。")
    elif len(valuation_methods) == 0:
        st.warning("少なくとも1つの評価方法を選択してください。")
    else:
        # Store current selection
        st.session_state.stored_comparison_tickers = selected_tickers.copy()
        st.session_state.stored_comparison_methods = valuation_methods.copy()
        
        # Auto-fetch financial data for each selected ticker
        with st.spinner("Fetching live financial data and comparing stocks..."):
            comparison_results = {}
            
            for ticker in selected_tickers:
                auto_data = get_auto_financial_data(ticker)
                if auto_data:
                    # Calculate valuations using live data
                    result = {
                        "name": auto_data['name'],
                        "industry": auto_data['industry'],
                        "current_price": auto_data['current_price'],
                        "valuation_methods": {}
                    }
                    
                    # Use the enhanced auto_data which already contains accurate Yahoo Finance metrics
                    
                    # Calculate company size (more understandable than raw market cap)
                    market_cap_billion = auto_data.get('market_cap', 0) / 1000 if auto_data.get('market_cap') else 0
                    if market_cap_billion >= 100:
                        company_size = "超大型株"
                    elif market_cap_billion >= 10:
                        company_size = "大型株"
                    elif market_cap_billion >= 2:
                        company_size = "中型株"
                    else:
                        company_size = "小型株"
                    
                    # PEG ratio (PE / Growth rate) - only if both values are available
                    peg_ratio = None
                    if auto_data.get('pe_ratio') and auto_data.get('historical_growth') and auto_data['historical_growth'] > 0:
                        peg_ratio = auto_data['pe_ratio'] / auto_data['historical_growth']
                    
                    # Get dividend yield from Yahoo Finance
                    import yfinance as yf
                    stock_yf = yf.Ticker(ticker)
                    info = stock_yf.info
                    annual_dividend = info.get('dividendRate', 0)
                    dividend_yield = None
                    if annual_dividend and auto_data['current_price'] > 0:
                        dividend_yield = (annual_dividend / auto_data['current_price']) * 100
                    
                    # Store all metrics - use None for unavailable data instead of 0
                    result["financial_metrics"] = {
                        "revenue_growth": auto_data.get('historical_growth'),
                        "peg_ratio": peg_ratio,
                        "dividend_yield": dividend_yield,
                        "debt_to_equity": auto_data.get('debt_to_equity'),
                        "roe": auto_data.get('roe'),
                        "roa": auto_data.get('roa'),
                        "profit_margin": auto_data.get('profit_margin'),
                        "gross_margin": auto_data.get('gross_margin'),
                        "operating_margin": auto_data.get('operating_margin'),
                        "current_ratio": auto_data.get('current_ratio'),
                        "asset_turnover": auto_data.get('asset_turnover'),
                        "company_size": company_size,
                        "market_cap_billion": market_cap_billion
                    }
                    
                    # Calculate current trading multiples (no intrinsic value calculations)
                    if "pe_ratio" in valuation_methods and auto_data['eps'] > 0:
                        current_pe = auto_data['current_price'] / auto_data['eps']
                        result["valuation_methods"]["pe_ratio"] = {
                            "current_multiple": current_pe,
                            "eps": auto_data['eps']
                        }
                    
                    if "pb_ratio" in valuation_methods and auto_data['book_value_per_share'] > 0:
                        current_pb = auto_data['current_price'] / auto_data['book_value_per_share']
                        result["valuation_methods"]["pb_ratio"] = {
                            "current_multiple": current_pb,
                            "book_value": auto_data['book_value_per_share']
                        }
                    
                    if "ps_ratio" in valuation_methods and auto_data['revenue'] > 0:
                        market_cap_million = auto_data['current_price'] * auto_data['shares_outstanding']
                        current_ps = market_cap_million / auto_data['revenue']
                        result["valuation_methods"]["ps_ratio"] = {
                            "current_multiple": current_ps
                        }
                    
                    comparison_results[ticker] = result
            
            # Store results in session state for future use
            st.session_state.stored_comparison_results = comparison_results
            
            if comparison_results:
                # 比較結果の表示
                st.markdown("</div>", unsafe_allow_html=True)  # 入力カードを閉じる
                
                # 概要一覧表示
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h2 class='card-title'>比較結果の概要</h2>", unsafe_allow_html=True)
                
                # データフレームの作成
                summary_data = []
                
                for ticker, result in comparison_results.items():
                    row = {
                        "ティッカー": ticker,
                        "企業名": result["name"],
                        "業界": result["industry"],
                        "現在株価": f"${result['current_price']:.2f}"
                    }
                    
                    # Add financial metrics based on user selection
                    if "financial_metrics" in result:
                        metrics = result["financial_metrics"]
                        
                        if show_revenue_growth:
                            row["売上成長率"] = f"{metrics['revenue_growth']:.1f}%" if metrics['revenue_growth'] is not None else "N/A"
                        if show_peg:
                            row["PEG倍率"] = f"{metrics['peg_ratio']:.2f}" if metrics['peg_ratio'] is not None else "N/A"
                        if show_dividend:
                            row["配当利回り"] = f"{metrics['dividend_yield']:.2f}%" if metrics['dividend_yield'] is not None else "N/A"
                        if show_debt_ratio:
                            row["負債比率"] = f"{metrics['debt_to_equity']:.2f}" if metrics['debt_to_equity'] is not None else "N/A"
                        if show_roe:
                            row["ROE"] = f"{metrics['roe']:.1f}%" if metrics['roe'] is not None else "N/A"
                        if show_roa:
                            row["ROA"] = f"{metrics['roa']:.1f}%" if metrics['roa'] is not None else "N/A"
                        if show_profit_margin:
                            row["純利益率"] = f"{metrics['profit_margin']:.1f}%" if metrics['profit_margin'] is not None else "N/A"
                        if show_gross_margin:
                            row["売上総利益率"] = f"{metrics['gross_margin']:.1f}%" if metrics['gross_margin'] is not None else "N/A"
                        if show_operating_margin:
                            row["営業利益率"] = f"{metrics['operating_margin']:.1f}%" if metrics['operating_margin'] is not None else "N/A"
                        if show_current_ratio:
                            row["流動比率"] = f"{metrics['current_ratio']:.2f}" if metrics['current_ratio'] is not None else "N/A"
                        if show_asset_turnover:
                            row["総資産回転率"] = f"{metrics['asset_turnover']:.2f}" if metrics['asset_turnover'] is not None else "N/A"
                        if show_company_size:
                            row["企業規模"] = metrics['company_size']
                            row["時価総額"] = f"{metrics['market_cap_billion']:.0f}億ドル"
                    
                    # 各評価方法の結果を追加
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                                if show_eps:
                                    row["EPS"] = f"${method_result['eps']:.2f}"
                            elif method == "pb_ratio":
                                method_name = "PBR"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                                row["1株純資産"] = f"${method_result['book_value']:.2f}"
                            elif method == "ps_ratio":
                                method_name = "PSR"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                    
                    summary_data.append(row)
                
                summary_df = pd.DataFrame(summary_data)
                
                # Add metric explanations
                st.markdown("""
                <div style="margin-bottom: 10px;">
                <small>
                <b>指標説明:</b>
                <b>PER</b>: 株価収益率 (株価÷1株利益) |
                <b>PBR</b>: 株価純資産倍率 (株価÷1株純資産) |
                <b>PSR</b>: 株価売上高倍率 (株価÷1株売上高) |
                <b>PEG</b>: PER÷成長率 (1以下が割安) |
                <b>配当利回り</b>: 年間配当÷株価×100 |
                <b>負債比率</b>: 負債÷自己資本 |
                <b>ROE</b>: 自己資本利益率 (純利益÷自己資本×100) |
                <b>ROA</b>: 総資産利益率 (純利益÷総資産×100) |
                <b>純利益率</b>: 売上に対する純利益の割合 |
                <b>売上総利益率</b>: 売上総利益÷売上×100 |
                <b>営業利益率</b>: 営業利益÷売上×100 |
                <b>流動比率</b>: 流動資産÷流動負債 (2.0以上が理想) |
                <b>総資産回転率</b>: 売上÷総資産 (効率性指標)
                <br><i>※全データはYahoo Financeから取得した最新の財務諸表に基づきます</i>
                </small>
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(summary_df, use_container_width=True)
                
                # Financial Health Scorecard
                st.markdown("<h3>財務健全性指標</h3>", unsafe_allow_html=True)
                
                # Create financial health comparison
                health_cols = st.columns(len(selected_tickers))
                
                for i, ticker in enumerate(selected_tickers):
                    if ticker in comparison_results:
                        result = comparison_results[ticker]
                        metrics = result.get("financial_metrics", {})
                        
                        with health_cols[i]:
                            st.markdown(f"""
                            <div class="metric-container">
                                <h4 style="text-align: center; color: #667eea; margin-bottom: 15px;">{ticker}</h4>
                                <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            """, unsafe_allow_html=True)
                            
                            # Key financial health metrics
                            if metrics.get('debt_to_equity') is not None:
                                debt_color = "green" if metrics['debt_to_equity'] < 0.5 else "orange" if metrics['debt_to_equity'] < 1.0 else "red"
                                st.markdown(f"**負債比率:** <span style='color: {debt_color}'>{metrics['debt_to_equity']:.2f}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("**負債比率:** N/A")
                            
                            if metrics.get('current_ratio') is not None:
                                current_color = "green" if metrics['current_ratio'] >= 2.0 else "orange" if metrics['current_ratio'] >= 1.0 else "red"
                                st.markdown(f"**流動比率:** <span style='color: {current_color}'>{metrics['current_ratio']:.2f}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("**流動比率:** N/A")
                            
                            if metrics.get('roe') is not None:
                                roe_color = "green" if metrics['roe'] >= 15 else "orange" if metrics['roe'] >= 10 else "red"
                                st.markdown(f"**ROE:** <span style='color: {roe_color}'>{metrics['roe']:.1f}%</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("**ROE:** N/A")
                            
                            if metrics.get('roa') is not None:
                                roa_color = "green" if metrics['roa'] >= 5 else "orange" if metrics['roa'] >= 2 else "red"
                                st.markdown(f"**ROA:** <span style='color: {roa_color}'>{metrics['roa']:.1f}%</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("**ROA:** N/A")
                            
                            if metrics.get('profit_margin') is not None:
                                margin_color = "green" if metrics['profit_margin'] >= 20 else "orange" if metrics['profit_margin'] >= 10 else "red"
                                st.markdown(f"**純利益率:** <span style='color: {margin_color}'>{metrics['profit_margin']:.1f}%</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("**純利益率:** N/A")
                            
                            st.markdown("</div></div>", unsafe_allow_html=True)
                
                # 取引倍率チャート
                st.markdown("<h3>取引倍率の比較</h3>", unsafe_allow_html=True)
                
                # チャートデータの準備
                chart_data = []
                
                for ticker, result in comparison_results.items():
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER"
                            elif method == "pb_ratio":
                                method_name = "PBR"
                            elif method == "ps_ratio":
                                method_name = "PSR"
                            
                            chart_data.append({
                                "ティッカー": ticker,
                                "倍率種類": method_name,
                                "倍率": method_result["current_multiple"]
                            })
                
                if chart_data:
                    chart_df = pd.DataFrame(chart_data)
                    
                    # 棒グラフの作成
                    fig = px.bar(
                        chart_df,
                        x="ティッカー",
                        y="倍率",
                        color="倍率種類",
                        barmode="group",
                        title="各銘柄の取引倍率比較",
                        labels={"倍率": "倍率"},
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Financial metrics comparison chart
                st.markdown("<h3>財務指標の比較</h3>", unsafe_allow_html=True)
                
                # Prepare financial metrics chart data
                metrics_chart_data = []
                
                for ticker, result in comparison_results.items():
                    if "financial_metrics" in result:
                        metrics = result["financial_metrics"]
                        
                        if show_revenue_growth:
                            metrics_chart_data.append({
                                "ティッカー": ticker,
                                "指標": "売上成長率 (%)",
                                "値": metrics['revenue_growth']
                            })
                        
                        if show_profit_margin and metrics['profit_margin'] > 0:
                            metrics_chart_data.append({
                                "ティッカー": ticker,
                                "指標": "純利益率 (%)",
                                "値": metrics['profit_margin']
                            })
                        
                        if show_roe and metrics['roe'] > 0:
                            metrics_chart_data.append({
                                "ティッカー": ticker,
                                "指標": "ROE (%)",
                                "値": metrics['roe']
                            })
                        
                        if show_dividend and metrics.get('dividend_yield') and metrics['dividend_yield'] > 0:
                            metrics_chart_data.append({
                                "ティッカー": ticker,
                                "指標": "配当利回り (%)",
                                "値": metrics['dividend_yield']
                            })
                
                if metrics_chart_data:
                    metrics_df = pd.DataFrame(metrics_chart_data)
                    
                    # Create grouped bar chart for financial metrics
                    fig2 = px.bar(
                        metrics_df,
                        x="ティッカー",
                        y="値",
                        color="指標",
                        barmode="group",
                        title="財務指標の比較（%）",
                        labels={"値": "パーセンテージ (%)"},
                        height=500
                    )
                    
                    fig2.update_layout(
                        yaxis_title="パーセンテージ (%)",
                        xaxis_title="銘柄"
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)
                
                # Remove duplicate functionality - use dedicated pages for detailed analysis
                st.markdown("### 📌 詳細分析について")
                st.info("各銘柄の詳細な分析は以下のページをご利用ください：\n- 📊 ビジネスモデル分析: 個別企業の詳細分析と市場比較\n- 📈 決算分析: 最新の決算情報と業界比較")

# Also display stored comparison results even if button wasn't clicked this time
elif st.session_state.stored_comparison_results:
    # Display stored comparison results
    comparison_results = st.session_state.stored_comparison_results
    selected_tickers = st.session_state.stored_comparison_tickers
    valuation_methods = st.session_state.stored_comparison_methods
    
    st.markdown("</div>", unsafe_allow_html=True)  # 入力カードを閉じる
    
    # 概要一覧表示
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='card-title'>比較結果の概要</h2>", unsafe_allow_html=True)
    
    # Use same display logic as above but with stored results
    summary_data = []
    
    for ticker, result in comparison_results.items():
        row = {
            "ティッカー": ticker,
            "企業名": result["name"],
            "業界": result["industry"],
            "現在株価": f"${result['current_price']:.2f}"
        }
        
        # Add financial metrics based on stored selection
        if "financial_metrics" in result:
            metrics = result["financial_metrics"]
            
            # Use current UI state for what to show
            if show_revenue_growth:
                row["売上成長率"] = f"{metrics['revenue_growth']:.1f}%" if metrics['revenue_growth'] is not None else "N/A"
            if show_peg:
                row["PEG倍率"] = f"{metrics['peg_ratio']:.2f}" if metrics['peg_ratio'] is not None else "N/A"
            if show_dividend:
                row["配当利回り"] = f"{metrics['dividend_yield']:.2f}%" if metrics['dividend_yield'] is not None else "N/A"
            if show_debt_ratio:
                row["負債比率"] = f"{metrics['debt_to_equity']:.2f}" if metrics['debt_to_equity'] is not None else "N/A"
            if show_roe:
                row["ROE"] = f"{metrics['roe']:.1f}%" if metrics['roe'] is not None else "N/A"
            if show_roa:
                row["ROA"] = f"{metrics['roa']:.1f}%" if metrics['roa'] is not None else "N/A"
            if show_profit_margin:
                row["純利益率"] = f"{metrics['profit_margin']:.1f}%" if metrics['profit_margin'] is not None else "N/A"
            if show_gross_margin:
                row["売上総利益率"] = f"{metrics['gross_margin']:.1f}%" if metrics['gross_margin'] is not None else "N/A"
            if show_operating_margin:
                row["営業利益率"] = f"{metrics['operating_margin']:.1f}%" if metrics['operating_margin'] is not None else "N/A"
            if show_current_ratio:
                row["流動比率"] = f"{metrics['current_ratio']:.2f}" if metrics['current_ratio'] is not None else "N/A"
            if show_asset_turnover:
                row["総資産回転率"] = f"{metrics['asset_turnover']:.2f}" if metrics['asset_turnover'] is not None else "N/A"
            if show_company_size:
                row["企業規模"] = metrics['company_size']
                row["時価総額"] = f"{metrics['market_cap_billion']:.0f}億ドル"
        
        # 各評価方法の結果を追加
        for method in valuation_methods:
            if method in result["valuation_methods"]:
                method_result = result["valuation_methods"][method]
                
                # 方法に応じた表示名を設定
                if method == "pe_ratio":
                    method_name = "PER"
                    row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                    if show_eps:
                        row["EPS"] = f"${method_result['eps']:.2f}"
                elif method == "pb_ratio":
                    method_name = "PBR"
                    row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                    row["1株純資産"] = f"${method_result['book_value']:.2f}"
                elif method == "ps_ratio":
                    method_name = "PSR"
                    row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
        
        summary_data.append(row)
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 📌 詳細分析について")
    st.info("各銘柄の詳細な分析は以下のページをご利用ください：\n- 📊 ビジネスモデル分析: 個別企業の詳細分析と市場比較\n- 📈 決算分析: 最新の決算情報と業界比較")

# Display chart section for both new and stored comparison results
if st.session_state.stored_comparison_results:
    comparison_results = st.session_state.stored_comparison_results
    selected_tickers = st.session_state.stored_comparison_tickers
    
    # Individual stock comparison chart
    st.markdown("### 📊 個別銘柄株価パフォーマンス比較")
    st.markdown("選択した銘柄の株価パフォーマンスを比較チャートで表示します。")
    
    # Period selection for comparison chart
    comparison_period_options = {
        "1ヶ月": "1mo",
        "3ヶ月": "3mo", 
        "6ヶ月": "6mo",
        "1年": "1y",
        "2年": "2y",
        "5年": "5y"
    }
    
    # Initialize session state for comparison period if not exists
    if 'chart_period_selection' not in st.session_state:
        st.session_state.chart_period_selection = "1年"
    
    # Use radio buttons in columns for period selection to avoid page reload
    st.write("**比較期間を選択:**")
    
    cols = st.columns(6)
    period_keys = list(comparison_period_options.keys())
    
    for i, period in enumerate(period_keys):
        with cols[i]:
            if st.button(
                period, 
                key=f"period_btn_{period}",
                use_container_width=True,
                type="primary" if st.session_state.chart_period_selection == period else "secondary"
            ):
                st.session_state.chart_period_selection = period
                st.rerun()
    
    # Use the session state value for chart generation
    selected_comparison_period = comparison_period_options[st.session_state.chart_period_selection]
    
    # Display current selected period
    st.info(f"現在の表示期間: **{st.session_state.chart_period_selection}**")
    
    # Auto-generate individual stock comparison chart
    with st.spinner("個別銘柄比較チャートを作成中..."):
        comparison_chart = create_individual_stock_comparison_chart(
            selected_tickers, 
            selected_comparison_period
        )
        
        if comparison_chart:
            # Display chart with period-specific key
            st.plotly_chart(
                comparison_chart, 
                use_container_width=True,
                key=f"comparison_chart_{selected_comparison_period}_{hash(tuple(selected_tickers))}"
            )
                        
                        # Add performance summary for individual comparison
                        try:
                            import yfinance as yf
                            
                            st.markdown("#### パフォーマンス統計")
                            
                            # Calculate returns for each stock
                            returns_data = []
                            for ticker in selected_tickers:
                                try:
                                    stock = yf.Ticker(ticker)
                                    data = stock.history(period=selected_comparison_period)
                                    if not data.empty:
                                        period_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                                        returns_data.append({
                                            'Ticker': ticker,
                                            'Return (%)': f"{period_return:+.2f}%"
                                        })
                                except:
                                    continue
                            
                            if returns_data:
                                returns_df = pd.DataFrame(returns_data)
                                st.dataframe(returns_df, use_container_width=True)
                                
                        except Exception as e:
                            st.warning("パフォーマンス統計の計算中にエラーが発生しました")

            else:
                st.error("比較結果の取得中にエラーが発生しました。")
else:
    st.markdown("</div>", unsafe_allow_html=True)

