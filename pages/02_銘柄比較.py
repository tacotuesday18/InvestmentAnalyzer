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
from real_time_fetcher import fetch_current_stock_price, fetch_comprehensive_data, show_live_price_indicator, display_market_status
from auto_financial_data import get_auto_financial_data

# ページ設定
st.set_page_config(
    page_title="銘柄比較 - 企業価値分析プロ",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">🔍 銘柄比較</div>
    <div class="page-subtitle">複数企業の多角的な価値評価と投資判断の比較分析</div>
</div>
""", unsafe_allow_html=True)

# Display market status
display_market_status()

# 入力フォームエリア
st.markdown("""
<div class="analysis-card">
    <div class="card-header">比較する銘柄を選択</div>
</div>
""", unsafe_allow_html=True)

# 利用可能なティッカーシンボル（先に取得）
available_tickers = get_available_tickers()
ticker_options = {ticker: f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in available_tickers}

# Auto-refreshed live data display
st.markdown("### 📊 Live Financial Data - Auto Updated")
st.markdown("All financial data is automatically fetched from Yahoo Finance API. No manual input required.")

# Refresh all data button
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh All Data", key="refresh_all_data"):
        st.cache_data.clear()
        st.success("Data refreshed!")
        st.rerun()

# マルチセレクト用のオプション
ticker_select_options = [f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in available_tickers]

# 複数銘柄の同時比較機能を強化
st.markdown("<div class='mobile-card'>", unsafe_allow_html=True)
st.markdown("<h3>銘柄選択</h3>", unsafe_allow_html=True)

# 業界フィルター (モバイルフレンドリー)
industries = list(set([get_stock_data(ticker).get('industry', 'その他') for ticker in available_tickers]))
industries = ['すべて'] + sorted(industries)
selected_industry = st.selectbox("業界でフィルター", industries)

# フィルタリングされた銘柄リスト
filtered_tickers = available_tickers
if selected_industry != 'すべて':
    filtered_tickers = [t for t in available_tickers if get_stock_data(t).get('industry', 'その他') == selected_industry]

# フィルタリングされたマルチセレクト用のオプション
ticker_select_options = [f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in filtered_tickers]

# 銘柄検索 (モバイルフレンドリー)
search_term = st.text_input("銘柄を検索 (ティッカーまたは企業名)", "")
if search_term:
    search_term = search_term.lower()
    ticker_select_options = [
        option for option in ticker_select_options 
        if search_term in option.lower()
    ]

# 銘柄選択（最大8つまで - 複数企業の比較を強化）
selected_ticker_options = st.multiselect(
    "比較する銘柄を選択してください（最大8つ）",
    options=ticker_select_options,
    default=[ticker_select_options[0], ticker_select_options[1]] if len(ticker_select_options) >= 2 else []
)
st.markdown("</div>", unsafe_allow_html=True)

# 選択された銘柄からティッカーシンボルを抽出
selected_tickers = [option.split(" - ")[0] for option in selected_ticker_options]

# 評価方法の選択 (モバイルフレンドリー)
st.markdown("<div class='mobile-card'>", unsafe_allow_html=True)
st.markdown("<h3>評価方法</h3>", unsafe_allow_html=True)

# レスポンシブなレイアウト
# モバイル向けレイアウト（縦に並べる）
use_pe = st.checkbox("PER (株価収益率)", value=True)
use_pb = st.checkbox("PBR (株価純資産倍率)", value=True)
use_ps = st.checkbox("PSR (株価売上高倍率)", value=True)

# 評価方法を配列に格納
valuation_methods = []
if use_pe:
    valuation_methods.append("pe_ratio")
if use_pb:
    valuation_methods.append("pb_ratio")
if use_ps:
    valuation_methods.append("ps_ratio")

# 比較ボタン
if st.button("比較を実行", key="compare_btn", use_container_width=True):
    if len(selected_tickers) == 0:
        st.warning("少なくとも1つの銘柄を選択してください。")
    elif len(selected_tickers) > 8:
        st.warning("最大8つの銘柄までしか比較できません。")
    elif len(valuation_methods) == 0:
        st.warning("少なくとも1つの評価方法を選択してください。")
    else:
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
                    
                    # Calculate current trading multiples (no intrinsic value calculations)
                    if "pe_ratio" in valuation_methods and auto_data['eps'] > 0:
                        current_pe = auto_data['current_price'] / auto_data['eps']
                        result["valuation_methods"]["pe_ratio"] = {
                            "current_multiple": current_pe,
                            "eps": auto_data['eps'],
                            "revenue_growth": calculate_growth_rate(auto_data.get('ticker', ticker))
                        }
                    
                    if "pb_ratio" in valuation_methods and auto_data['book_value_per_share'] > 0:
                        current_pb = auto_data['current_price'] / auto_data['book_value_per_share']
                        result["valuation_methods"]["pb_ratio"] = {
                            "current_multiple": current_pb,
                            "book_value": auto_data['book_value_per_share'],
                            "revenue_growth": calculate_growth_rate(auto_data.get('ticker', ticker))
                        }
                    
                    if "ps_ratio" in valuation_methods and auto_data['revenue'] > 0:
                        market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                        current_ps = market_cap / auto_data['revenue']
                        result["valuation_methods"]["ps_ratio"] = {
                            "current_multiple": current_ps,
                            "revenue": auto_data['revenue'],
                            "revenue_growth": calculate_growth_rate(auto_data.get('ticker', ticker))
                        }
                    
                    comparison_results[ticker] = result
            
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
                    
                    # Add revenue growth rate
                    revenue_growth = None
                    for method_data in result["valuation_methods"].values():
                        if "revenue_growth" in method_data:
                            revenue_growth = method_data["revenue_growth"]
                            break
                    
                    if revenue_growth is not None:
                        row["売上成長率"] = f"{revenue_growth:.1f}%"
                    
                    # 各評価方法の結果を追加
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                                row["EPS"] = f"${method_result['eps']:.2f}"
                            elif method == "pb_ratio":
                                method_name = "PBR"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                                row["1株純資産"] = f"${method_result['book_value']:.2f}"
                            elif method == "ps_ratio":
                                method_name = "PSR"
                                row[f"{method_name}"] = f"{method_result['current_multiple']:.2f}倍"
                                row["売上高"] = f"${method_result['revenue']/1000000:.1f}B"
                    
                    summary_data.append(row)
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
                
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
                

                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 各銘柄の詳細情報
                for ticker, result in comparison_results.items():
                    stock_data = get_stock_data(ticker)
                    
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"<h2 class='card-title'>{ticker} - {result['name']} の詳細分析</h2>", unsafe_allow_html=True)
                    
                    # 企業の基本情報
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**業界**: {result['industry']}")
                        st.markdown(f"**現在の株価**: ${result['current_price']:.2f}")
                    
                    with col2:
                        st.markdown(f"**売上高 (百万USD)**: ${stock_data['revenue']:,.0f}")
                        st.markdown(f"**純利益 (百万USD)**: ${stock_data['net_income']:,.0f}")
                    
                    with col3:
                        st.markdown(f"**EPS (USD)**: ${stock_data['eps']:.2f}")
                        st.markdown(f"**発行済株式数 (百万株)**: {stock_data['shares_outstanding']:,.0f}")
                    
                    # 評価方法ごとの結果
                    st.markdown("<h3>評価結果</h3>", unsafe_allow_html=True)
                    
                    # 評価結果のデータ
                    valuation_data = []
                    
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER (株価収益率)"
                                current_ratio = f"{method_result['current_ratio']:.2f}倍"
                                industry_avg = f"{method_result['industry_avg']:.2f}倍"
                            elif method == "pb_ratio":
                                method_name = "PBR (株価純資産倍率)"
                                current_ratio = f"{method_result['current_ratio']:.2f}倍"
                                industry_avg = f"{method_result['industry_avg']:.2f}倍"
                            elif method == "ps_ratio":
                                method_name = "PSR (株価売上高倍率)"
                                current_ratio = f"{method_result['current_ratio']:.2f}倍"
                                industry_avg = f"{method_result['industry_avg']:.2f}倍"
                            else:  # dcf
                                method_name = "DCF (割引キャッシュフロー法)"
                                current_ratio = "N/A"
                                industry_avg = "N/A"
                            
                            valuation_data.append({
                                "評価方法": method_name,
                                "現在の比率": current_ratio,
                                "業界平均": industry_avg,
                                "相対的な評価": method_result["relative_value"],
                                "公正価値": f"${method_result['fair_value']:.2f}",
                                "上昇余地": f"{method_result['upside_potential']:.1f}%"
                            })
                    
                    # データフレームで表示
                    valuation_df = pd.DataFrame(valuation_data)
                    st.dataframe(valuation_df, use_container_width=True)
                    
                    # 財務指標の比較チャート（現在値と業界平均）
                    st.markdown("<h3>財務指標の比較</h3>", unsafe_allow_html=True)
                    
                    # チャートデータの準備
                    industry = result["industry"]
                    industry_avg = get_industry_average(industry)
                    
                    ratios = ["pe_ratio", "pb_ratio", "ps_ratio"]
                    ratio_names = ["PER", "PBR", "PSR"]
                    
                    ratio_data = []
                    
                    for i, ratio in enumerate(ratios):
                        if ratio in stock_data:
                            ratio_data.append({
                                "指標": ratio_names[i],
                                "企業値": stock_data[ratio],
                                "業界平均": industry_avg[ratio]
                            })
                    
                    ratio_df = pd.DataFrame(ratio_data)
                    
                    # 棒グラフの作成
                    if not ratio_df.empty:
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            x=ratio_df["指標"],
                            y=ratio_df["企業値"],
                            name=f"{ticker}の値",
                            marker_color="royalblue"
                        ))
                        
                        fig.add_trace(go.Bar(
                            x=ratio_df["指標"],
                            y=ratio_df["業界平均"],
                            name=f"{industry}業界平均",
                            marker_color="lightgray"
                        ))
                        
                        fig.update_layout(
                            barmode="group",
                            title=f"{ticker}の財務指標と{industry}業界平均の比較",
                            xaxis_title="財務指標",
                            yaxis_title="倍率",
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("比較結果の取得中にエラーが発生しました。")
else:
    st.markdown("</div>", unsafe_allow_html=True)

# Add floating chatbot component
try:
    from floating_chatbot import render_floating_chatbot
    render_floating_chatbot()
except ImportError:
    pass