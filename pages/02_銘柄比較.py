import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# stock_dataモジュールをインポート
from stock_data import get_stock_data, get_available_tickers, compare_valuations, get_industry_average, update_stock_price, fetch_tradingview_price, refresh_stock_prices

# ページ設定
st.set_page_config(
    page_title="銘柄比較 - 企業価値分析プロ",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
    }
    
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        font-size: 1.4rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
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

# 株価更新セクション
with st.expander("株価を手動で更新"):
    st.markdown("特定の銘柄の株価を更新します。これにより分析結果も変化します。")
    
    update_col1, update_col2, update_col3 = st.columns([2, 1, 1])
    
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
            # 現在の株価から±30%の範囲で新しい価格を入力可能に
            min_price = max(0.1, current_price * 0.7)
            max_price = current_price * 1.3
            new_price = st.number_input(
                "新しい株価 (USD)",
                min_value=float(min_price),
                max_value=float(max_price),
                value=float(current_price),
                step=0.01,
                format="%.2f"
            )
    
    with update_col3:
        # 更新ボタン
        if st.button("株価を更新", key="update_price_btn"):
            if update_ticker and new_price > 0:
                success = update_stock_price(update_ticker, new_price)
                if success:
                    st.success(f"{update_ticker}の株価を${new_price:.2f}に更新しました。")
                    # 最新の情報を反映するためにページをリロード
                    st.rerun()
                else:
                    st.error("株価の更新に失敗しました。")

    # TradingViewからのリアルタイム株価更新ボタン
    if st.button("TradingViewから全銘柄の最新株価を取得", key="fetch_tv_btn"):
        with st.spinner("TradingViewから全銘柄の最新株価データを取得しています..."):
            # 全銘柄の価格を更新
            updated_prices = refresh_stock_prices()
            if updated_prices:
                tickers_updated = len(updated_prices)
                st.success(f"{tickers_updated}銘柄の株価を更新しました。")
                # 最新の情報を反映するためにページをリロード
                st.rerun()
            else:
                st.error("株価の更新に失敗しました。")

# マルチセレクト用のオプション
ticker_select_options = [f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in available_tickers]

# 銘柄選択（最大5つまで）
selected_ticker_options = st.multiselect(
    "比較する銘柄を選択してください（最大5つ）",
    options=ticker_select_options,
    default=[ticker_select_options[0], ticker_select_options[1]] if len(ticker_select_options) >= 2 else []
)

# 選択された銘柄からティッカーシンボルを抽出
selected_tickers = [option.split(" - ")[0] for option in selected_ticker_options]

# 評価方法の選択
st.markdown("### 評価方法")
col1, col2, col3, col4 = st.columns(4)

with col1:
    use_pe = st.checkbox("PER (株価収益率)", value=True)

with col2:
    use_pb = st.checkbox("PBR (株価純資産倍率)", value=True)

with col3:
    use_ps = st.checkbox("PSR (株価売上高倍率)", value=True)

with col4:
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
    elif len(selected_tickers) > 5:
        st.warning("最大5つの銘柄までしか比較できません。")
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