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

# メインコンテンツ
st.markdown("<h1 class='main-header'>🔍 銘柄比較</h1>", unsafe_allow_html=True)

# 入力フォームエリア
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>比較する銘柄を選択</h2>", unsafe_allow_html=True)

# 利用可能なティッカーシンボル（先に取得）
available_tickers = get_available_tickers()
ticker_options = {ticker: f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in available_tickers}

# 株価・財務データ更新セクション
with st.expander("データを手動で更新", expanded=True):
    st.markdown("### 株価・財務データ更新")
    st.markdown("最新データを入力して分析精度を向上させます。正確な企業価値評価には最新のデータが不可欠です。")
    
    # タブで株価更新と財務データ更新を分ける
    price_tab, financial_tab = st.tabs(["株価更新", "財務データ更新"])
    
    with price_tab:
        st.markdown("#### 株価データの更新")
        st.markdown("各銘柄の現在の株価を入力してください。")
        
        update_col1, update_col2 = st.columns([2, 1])
        
        with update_col1:
            # 利用可能なティッカーからドロップダウンで選択
            update_ticker = st.selectbox(
                "更新する銘柄",
                options=available_tickers,
                format_func=lambda x: f"{x} - {get_stock_data(x)['name']}"
            )
        
        with update_col2:
            if update_ticker:
                current_price = get_stock_data(update_ticker)["current_price"]
                new_price = st.number_input(
                    "最新の株価 (USD)",
                    min_value=0.01,
                    max_value=10000.0,
                    value=float(current_price),
                    step=0.01,
                    format="%.2f"
                )
                
                # 更新ボタン
                if st.button("株価を更新", key="update_price_btn", use_container_width=True):
                    if update_ticker and new_price > 0:
                        success = update_stock_price(update_ticker, new_price)
                        if success:
                            st.success(f"{update_ticker}の株価を${new_price:.2f}に更新しました。")
                            # 最新の情報を反映するためにページをリロード
                            st.rerun()
                        else:
                            st.error("株価の更新に失敗しました。")
        
        # 複数銘柄の一括更新セクション
        st.markdown("#### 複数銘柄の価格を一括更新")
        
        # 3列のレイアウトで表示
        cols = st.columns(3)
        price_updates = {}
        
        # マグニフィセント7の銘柄を優先表示
        magnificent7 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]
        display_tickers = [t for t in magnificent7 if t in available_tickers]
        
        for i, ticker in enumerate(display_tickers):
            with cols[i % 3]:
                current_data = get_stock_data(ticker)
                current_price = current_data.get('current_price', 0.0)
                ticker_name = current_data.get('name', ticker)
                new_price = st.number_input(
                    f"{ticker} - {ticker_name}",
                    min_value=0.01,
                    max_value=10000.0,
                    value=float(current_price),
                    step=0.01,
                    format="%.2f",
                    key=f"price_{ticker}"
                )
                price_updates[ticker] = new_price
        
        # 一括更新ボタン
        if st.button("選択した銘柄の価格を一括更新", use_container_width=True):
            with st.spinner("株価データを更新中..."):
                updated_count = 0
                for ticker, price in price_updates.items():
                    if update_stock_price(ticker, price):
                        updated_count += 1
                st.success(f"{updated_count}銘柄の株価を更新しました。")
                # 最新の情報を反映するためにページをリロード
                st.rerun()
    
    with financial_tab:
        st.markdown("#### 財務データの更新")
        st.markdown("最新の四半期/年次レポートに基づいて財務データを更新できます。")
        
        # 銘柄選択
        fin_update_ticker = st.selectbox(
            "更新する銘柄",
            options=available_tickers,
            format_func=lambda x: f"{x} - {get_stock_data(x)['name']}",
            key="fin_ticker"
        )
        
        if fin_update_ticker:
            stock_data = get_stock_data(fin_update_ticker)
            
            # 各種財務データを入力するためのフォーム
            with st.form("financial_update_form"):
                st.markdown(f"#### {fin_update_ticker} - {stock_data['name']} の財務データ更新")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    revenue = st.number_input(
                        "売上高（百万USD）",
                        min_value=0.0,
                        value=float(stock_data["revenue"]),
                        step=100.0
                    )
                    
                    net_income = st.number_input(
                        "純利益（百万USD）",
                        value=float(stock_data["net_income"]),
                        step=10.0
                    )
                    
                    eps = st.number_input(
                        "EPS（USD）",
                        value=float(stock_data["eps"]),
                        step=0.01,
                        format="%.2f"
                    )
                
                with col2:
                    book_value_per_share = st.number_input(
                        "1株あたり純資産（USD）",
                        min_value=0.01,
                        value=float(stock_data["book_value_per_share"]),
                        step=0.1,
                        format="%.2f"
                    )
                    
                    shares_outstanding = st.number_input(
                        "発行済株式数（百万株）",
                        min_value=0.1,
                        value=float(stock_data["shares_outstanding"]),
                        step=10.0
                    )
                    
                    # 業界の選択肢
                    industry_options = list(set([get_stock_data(t).get('industry', 'その他') for t in available_tickers]))
                    industry = st.selectbox(
                        "業界",
                        options=industry_options,
                        index=industry_options.index(stock_data["industry"]) if stock_data["industry"] in industry_options else 0
                    )
                
                # 更新ボタン
                submitted = st.form_submit_button("財務データを更新", use_container_width=True)
                if submitted:
                    try:
                        # 財務データを更新する処理を実装
                        # 実際の実装では、stock_data.pyに新しい関数を追加して処理
                        stocks_data, industry_data = load_sample_data()
                        if fin_update_ticker in stocks_data:
                            # データを更新
                            stocks_data[fin_update_ticker]["revenue"] = revenue
                            stocks_data[fin_update_ticker]["net_income"] = net_income
                            stocks_data[fin_update_ticker]["eps"] = eps
                            stocks_data[fin_update_ticker]["book_value_per_share"] = book_value_per_share
                            stocks_data[fin_update_ticker]["shares_outstanding"] = shares_outstanding
                            stocks_data[fin_update_ticker]["industry"] = industry
                            
                            # 財務指標も更新
                            current_price = stocks_data[fin_update_ticker]["current_price"]
                            stocks_data[fin_update_ticker]["pe_ratio"] = current_price / eps if eps > 0 else 0
                            stocks_data[fin_update_ticker]["pb_ratio"] = current_price / book_value_per_share
                            stocks_data[fin_update_ticker]["ps_ratio"] = (current_price * shares_outstanding) / revenue if revenue > 0 else 0
                            
                            # ファイルに保存
                            ensure_sample_data_dir()
                            file_path = os.path.join(SAMPLE_DATA_DIR, "sample_stocks.json")
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(stocks_data, f, ensure_ascii=False, indent=4)
                            
                            st.success(f"{fin_update_ticker}の財務データを更新しました。")
                            st.rerun()
                        else:
                            st.error("指定された銘柄が見つかりません。")
                    except Exception as e:
                        st.error(f"財務データの更新中にエラーが発生しました: {str(e)}")

    # 外部データソースへのリンク
    st.markdown("### 最新データ取得リソース")
    st.markdown("""
    以下のサイトから最新の株価と財務データを取得できます：
    - [Yahoo Finance](https://finance.yahoo.com/) - 株価、基本財務指標
    - [MarketWatch](https://www.marketwatch.com/) - 詳細な財務データ
    - [Finviz](https://finviz.com/) - スクリーニングと基本指標
    - [Macrotrends](https://www.macrotrends.net/) - 長期的な財務トレンド
    """)
    
    # データ自動取得についての注意
    st.info("注意: 現在のバージョンでは手動データ入力のみをサポートしています。将来のアップデートでは、APIを使用した自動データ取得機能を実装予定です。")

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
use_dcf = st.checkbox("DCF (割引キャッシュフロー法)", value=True)



# 評価方法を配列に格納
valuation_methods = []
if use_pe:
    valuation_methods.append("pe_ratio")
if use_pb:
    valuation_methods.append("pb_ratio")
if use_ps:
    valuation_methods.append("ps_ratio")
if use_dcf:
    valuation_methods.append("dcf")

# DCF法のパラメータ（オプショナル）
if use_dcf:
    st.markdown("### DCF分析パラメータ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        revenue_growth_override = st.checkbox("売上高成長率を指定", value=False)
        if revenue_growth_override:
            growth_rate = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=10.0, step=0.5)
    
    with col2:
        discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5)
    
    with col3:
        terminal_multiple = st.slider("終末価値倍率（PE）", min_value=5.0, max_value=30.0, value=15.0, step=0.5)

# 比較ボタン
if st.button("比較を実行", key="compare_btn", use_container_width=True):
    if len(selected_tickers) == 0:
        st.warning("少なくとも1つの銘柄を選択してください。")
    elif len(selected_tickers) > 8:
        st.warning("最大8つの銘柄までしか比較できません。")
    elif len(valuation_methods) == 0:
        st.warning("少なくとも1つの評価方法を選択してください。")
    else:
        # 銘柄比較の実行
        with st.spinner("銘柄を比較中..."):
            comparison_results = compare_valuations(selected_tickers, valuation_methods)
            
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
                    
                    # 各評価方法の結果を追加
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER評価"
                            elif method == "pb_ratio":
                                method_name = "PBR評価"
                            elif method == "ps_ratio":
                                method_name = "PSR評価"
                            else:  # dcf
                                method_name = "DCF評価"
                            
                            row[f"{method_name} (公正価値)"] = f"${method_result['fair_value']:.2f}"
                            row[f"{method_name} (上昇余地)"] = f"{method_result['upside_potential']:.1f}%"
                    
                    summary_data.append(row)
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
                
                # 比較チャート
                st.markdown("<h3>公正価値の比較</h3>", unsafe_allow_html=True)
                
                # チャートデータの準備
                chart_data = []
                
                for ticker, result in comparison_results.items():
                    # 現在の株価
                    chart_data.append({
                        "ティッカー": ticker,
                        "評価方法": "現在株価",
                        "価格": result["current_price"]
                    })
                    
                    # 各評価方法の公正価値
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER評価"
                            elif method == "pb_ratio":
                                method_name = "PBR評価"
                            elif method == "ps_ratio":
                                method_name = "PSR評価"
                            else:  # dcf
                                method_name = "DCF評価"
                            
                            chart_data.append({
                                "ティッカー": ticker,
                                "評価方法": method_name,
                                "価格": method_result["fair_value"]
                            })
                
                chart_df = pd.DataFrame(chart_data)
                
                # 棒グラフの作成
                fig = px.bar(
                    chart_df,
                    x="ティッカー",
                    y="価格",
                    color="評価方法",
                    barmode="group",
                    title="各銘柄の評価方法別公正価値比較",
                    labels={"価格": "株価 ($)"},
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 上昇余地の比較チャート
                st.markdown("<h3>上昇余地の比較</h3>", unsafe_allow_html=True)
                
                # 上昇余地のチャートデータ準備
                upside_data = []
                
                for ticker, result in comparison_results.items():
                    for method in valuation_methods:
                        if method in result["valuation_methods"]:
                            method_result = result["valuation_methods"][method]
                            
                            # 方法に応じた表示名を設定
                            if method == "pe_ratio":
                                method_name = "PER評価"
                            elif method == "pb_ratio":
                                method_name = "PBR評価"
                            elif method == "ps_ratio":
                                method_name = "PSR評価"
                            else:  # dcf
                                method_name = "DCF評価"
                            
                            upside_data.append({
                                "ティッカー": ticker,
                                "評価方法": method_name,
                                "上昇余地": method_result["upside_potential"]
                            })
                
                upside_df = pd.DataFrame(upside_data)
                
                # 上昇余地の棒グラフの作成
                fig = px.bar(
                    upside_df,
                    x="ティッカー",
                    y="上昇余地",
                    color="評価方法",
                    barmode="group",
                    title="各銘柄の評価方法別上昇余地比較",
                    labels={"上昇余地": "上昇余地 (%)"},
                    height=500
                )
                
                # ゼロラインの追加
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=0,
                    x1=len(selected_tickers) - 0.5,
                    y1=0,
                    line=dict(color="gray", width=1, dash="dash")
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