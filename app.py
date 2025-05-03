import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import trafilatura
import requests
import os
import time
from utils import generate_swot_analysis, generate_moat_analysis
from financial_models import calculate_intrinsic_value, calculate_financial_ratios
from database import get_companies, get_company_financial_data, save_analysis, update_user_subscription, setup_database

# データベースのセットアップ
try:
    setup_database()
except Exception as e:
    st.error(f"データベース初期化エラー: {e}")

# メモリキャッシュ
@st.cache_data(ttl=300)  # 5分間キャッシュ
def cached_get_companies():
    """企業リストを取得し、結果をキャッシュする"""
    try:
        companies = get_companies()
        if not companies:
            # エラーが発生した場合はダミーデータを返す
            return [
                {"id": 1, "name": "Apple Inc.", "symbol": "AAPL", "industry": "テクノロジー"},
                {"id": 2, "name": "Microsoft Corporation", "symbol": "MSFT", "industry": "テクノロジー"},
                {"id": 3, "name": "Amazon.com, Inc.", "symbol": "AMZN", "industry": "消費財"},
                {"id": 4, "name": "JPMorgan Chase & Co.", "symbol": "JPM", "industry": "金融"},
                {"id": 5, "name": "Johnson & Johnson", "symbol": "JNJ", "industry": "ヘルスケア"}
            ]
        return companies
    except Exception as e:
        st.error(f"企業データ取得エラー: {e}")
        # エラーが発生した場合は空のリストを返す
        return []

# ページ設定
st.set_page_config(
    page_title="企業価値分析ツール",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem !important;
        color: #0066cc;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .subtitle {
        font-size: 1.2rem !important;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        font-size: 1.4rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
    }
    
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    
    /* プラン選択ボタンのスタイル */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* ダークモードサポート */
    @media (prefers-color-scheme: dark) {
        .card {
            background-color: #262730;
        }
        
        .metric-container {
            background-color: #1e1e1e;
        }
    }
</style>
""", unsafe_allow_html=True)

# アプリケーションタイトル
st.markdown("<h1 class='main-title'>💰 企業価値分析プロ</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>収益成長率と割引率から企業の本質的価値を計算し、投資判断をサポートする高度な分析ツール</p>", unsafe_allow_html=True)

# サブスクリプションプラン機能
def show_subscription_plans():
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='text-align: center; color: #0066cc;'>📊 サブスクリプションプラン</h3>", unsafe_allow_html=True)
    
    # プランのカード表示スタイル
    plan_style = """
    <div style="padding: 15px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="text-align: center; margin-bottom: 10px;">%s</h4>
        <p style="text-align: center; font-weight: bold; font-size: 1.2rem; margin-bottom: 12px; color: #0066cc;">%s</p>
        <ul style="list-style-type: none; padding-left: 5px;">
            %s
        </ul>
    </div>
    """
    
    # Free プラン
    free_features = "<li>✓ 基本的な企業分析</li><li>✓ 月3社まで分析可能</li><li>✓ シンプルなレポート</li>"
    st.sidebar.markdown(plan_style % ("🆓 無料プラン", "¥0", free_features), unsafe_allow_html=True)
    if st.sidebar.button("選択", key="free_plan", help="無料プランを選択"):
        st.session_state.subscription = "free"
        st.sidebar.success("✅ 無料プランが選択されました")
    
    st.sidebar.markdown("<hr style='margin: 20px 0'>", unsafe_allow_html=True)
    
    # Basic プラン
    basic_features = "<li>✓ 全ての無料機能</li><li>✓ 月20社まで分析可能</li><li>✓ 詳細SWOT分析</li><li>✓ 財務指標の比較</li>"
    st.sidebar.markdown(plan_style % ("🔹 ベーシックプラン", "¥2,500/月", basic_features), unsafe_allow_html=True)
    if st.sidebar.button("選択", key="basic_plan", help="ベーシックプランを選択"):
        st.session_state.subscription = "basic"
        st.sidebar.success("✅ ベーシックプランが選択されました")
    
    st.sidebar.markdown("<hr style='margin: 20px 0'>", unsafe_allow_html=True)
    
    # Premium プラン
    premium_features = "<li>✓ 全てのベーシック機能</li><li>✓ 無制限の企業分析</li><li>✓ 決算情報の詳細分析</li><li>✓ 業界詳細レポート</li><li>✓ カスタマーサポート</li>"
    st.sidebar.markdown(plan_style % ("💎 プレミアムプラン", "¥4,900/月", premium_features), unsafe_allow_html=True)
    if st.sidebar.button("選択", key="premium_plan", help="プレミアムプランを選択"):
        st.session_state.subscription = "premium"
        st.sidebar.success("✅ プレミアムプランが選択されました")

# セッション状態の初期化
if 'subscription' not in st.session_state:
    st.session_state.subscription = "free"  # デフォルトは無料プラン

# サイドバー - 基本パラメータ入力
with st.sidebar:
    st.header("企業情報と予測パラメータ")
    
    # サブスクリプションプランの表示
    show_subscription_plans()
    
    # データベースから企業一覧を取得
    companies = cached_get_companies()
    company_options = [""] + [f"{company['name']} ({company['symbol']})" for company in companies]
    selected_company = st.selectbox("企業を選択", options=company_options, index=0)
    
    company_name = ""
    company_id = None
    company_symbol = ""
    current_revenue = 10000
    current_net_income = 1000
    shares_outstanding = 100.0
    current_stock_price = 1000.0
    book_value_per_share = 500.0
    industry = "テクノロジー"
    
    # 企業を選択した場合はデータベースからデータを取得
    if selected_company and selected_company != "":
        selected_company_name, selected_company_symbol = selected_company.rsplit(" (", 1)
        company_symbol = selected_company_symbol[:-1]  # 閉じ括弧を削除
        company_name = selected_company_name
        
        # 企業IDを取得
        for company in companies:
            if company['symbol'] == company_symbol:
                company_id = company['id']
                industry = company['industry']
                break
        
        # 財務データを取得
        if company_id:
            financial_data = get_company_financial_data(company_id)
            if financial_data:
                current_revenue = financial_data.revenue
                current_net_income = financial_data.net_income
                shares_outstanding = financial_data.shares_outstanding
                current_stock_price = financial_data.current_stock_price
                book_value_per_share = financial_data.book_value_per_share
    
    # 手動入力のオプション
    if not selected_company or selected_company == "":
        # 企業の基本情報
        company_name = st.text_input("企業名", company_name)
        industry = st.selectbox(
            "業界",
            ["テクノロジー", "金融", "ヘルスケア", "消費財", "工業", "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"],
            index=["テクノロジー", "金融", "ヘルスケア", "消費財", "工業", "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"].index(industry)
        )
        
        # 証券コードまたはティッカーシンボル（ベーシックおよびプレミアムプラン用）
        if st.session_state.subscription in ["basic", "premium"]:
            company_symbol = st.text_input("証券コード/ティッカーシンボル（例: 7203.T, AAPL）", company_symbol)
    
    # 現在の財務情報（企業選択/手動入力に関わらず表示）
    st.subheader("現在の財務情報")
    current_revenue = st.number_input("現在の年間売上高（百万USD）", min_value=0, value=int(current_revenue))
    current_net_income = st.number_input("現在の純利益（百万USD）", min_value=-100000, value=int(current_net_income))
    current_net_margin = (current_net_income / current_revenue) * 100 if current_revenue > 0 else 0
    st.info(f"現在の純利益率: {current_net_margin:.2f}%")
    
    # 株式関連情報
    shares_outstanding = st.number_input("発行済株式数（百万株）", min_value=0.1, value=float(shares_outstanding), step=0.1)
    current_stock_price = st.number_input("現在の株価（USD）", min_value=0.0, value=float(current_stock_price), step=0.1)
    book_value_per_share = st.number_input("1株あたり純資産（USD）", min_value=0.0, value=float(book_value_per_share), step=0.1)
    
    # 予測パラメータ
    st.subheader("成長予測パラメータ")
    revenue_growth_rate = st.slider("年間売上高成長率 (%)", min_value=-20, max_value=100, value=10)
    target_net_margin = current_net_margin  # 簡素化のため、現在の利益率を目標にする
    forecast_years = 5  # 簡素化のため、予測期間を5年に固定
    discount_rate = st.slider("割引率 (%)", min_value=5, max_value=25, value=10)
    
    # 業界平均値
    st.subheader("業界平均指標")
    industry_pe = st.number_input("業界平均PER", min_value=1.0, value=15.0, step=0.1)
    industry_pb = st.number_input("業界平均PBR", min_value=0.1, value=1.5, step=0.1)
    industry_ps = st.number_input("業界平均PSR", min_value=0.1, value=2.0, step=0.1)

# メインコンテンツ
if company_name:
    # プロおよびエンタープライズプランでは、最新の決算情報も表示
    company_symbol = ""
    if 'company_symbol' in locals():
        company_symbol = company_symbol
        
    if st.session_state.subscription in ["basic", "premium"] and company_symbol:
        from earnings_scraper import get_earnings_highlights
        
        st.markdown("<div class='card'><h3 class='card-title'>🔍 最新の決算ハイライト</h3>", unsafe_allow_html=True)
        with st.expander("決算情報の詳細を表示", expanded=True):
            earnings_data = get_earnings_highlights(company_symbol)
            
            col_earnings1, col_earnings2 = st.columns(2)
            with col_earnings1:
                st.markdown("##### 📈 業績ハイライト")
                st.markdown(f"**売上成長率**: {earnings_data['revenue_growth']}")
                st.markdown(f"**営業利益率**: {earnings_data['operating_margin']}")
                st.markdown(f"**純利益**: {earnings_data['net_income']}")
            
            with col_earnings2:
                st.markdown("##### 🔮 今後の見通しと戦略")
                st.markdown(f"**今後の見通し**: {earnings_data['future_outlook']}")
                st.markdown(f"**戦略的施策**: {earnings_data['strategic_initiatives']}")
                st.markdown(f"**主要リスク要因**: {earnings_data['risk_factors']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # プレミアムプランのみ、業界の詳細分析も表示
    if st.session_state.subscription == "premium":
        st.subheader("🏢 業界詳細分析")
        with st.expander("業界のトレンドと競合状況", expanded=False):
            st.markdown("""
            ##### 業界トレンド
            1. **デジタルトランスフォーメーション**: 業界全体でデジタル化が加速しています
            2. **サステナビリティ**: ESG投資の増加に伴い、持続可能な事業モデルへの移行が進んでいます
            3. **規制環境**: 各国での規制強化が事業に影響を与えています
            
            ##### 競合状況
            - 主要競合他社とのシェア比較
            - 価格競争と差別化戦略の比較
            - 市場への新規参入状況と参入障壁の分析
            """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"{company_name}の企業価値分析")
        
        # 財務予測の計算
        forecasted_data = pd.DataFrame()
        years = list(range(0, forecast_years + 1))
        forecasted_data['年'] = years
        
        # 売上高の予測
        forecasted_data['売上高（百万USD）'] = [current_revenue * ((1 + revenue_growth_rate/100) ** year) for year in years]
        
        # 純利益率の予測（現在から目標まで線形に変化すると仮定）
        forecasted_data['純利益率 (%)'] = [current_net_margin + (target_net_margin - current_net_margin) * (year / forecast_years) for year in years]
        
        # 純利益の予測
        forecasted_data['純利益（百万USD）'] = forecasted_data['売上高（百万USD）'] * forecasted_data['純利益率 (%)'] / 100
        
        # 1株あたり利益（EPS）の予測
        forecasted_data['EPS（USD）'] = forecasted_data['純利益（百万USD）'] * 1000000 / shares_outstanding / 1000000
        
        # 予測データを表示
        st.subheader("財務予測")
        st.dataframe(forecasted_data.round(2))
        
        # 売上高と純利益のグラフ
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=forecasted_data['年'],
            y=forecasted_data['売上高（百万USD）'],
            name='売上高（百万USD）'
        ))
        fig1.add_trace(go.Line(
            x=forecasted_data['年'],
            y=forecasted_data['純利益（百万USD）'],
            name='純利益（百万USD）',
            yaxis='y2'
        ))
        fig1.update_layout(
            title='売上高と純利益の予測',
            xaxis_title='年',
            yaxis=dict(title='売上高（百万USD）'),
            yaxis2=dict(title='純利益（百万USD）', overlaying='y', side='right'),
            legend=dict(x=0.01, y=0.99),
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # 本質的価値の計算
        terminal_value_multiple = industry_pe
        intrinsic_values = calculate_intrinsic_value(
            forecasted_data, 
            discount_rate, 
            terminal_value_multiple, 
            shares_outstanding
        )
        
        # 現在の財務指標の計算
        current_market_cap = current_stock_price * shares_outstanding
        financial_ratios = calculate_financial_ratios(
            current_market_cap,
            current_revenue,
            current_net_income,
            book_value_per_share * shares_outstanding,
            shares_outstanding
        )
        
        # DCF法による株価計算
        dcf_price = intrinsic_values['dcf_per_share']
        upside_potential = ((dcf_price / current_stock_price) - 1) * 100
        
        # 本質的価値の表示
        st.subheader("本質的価値分析結果")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("DCF法による株価（USD）", f"{dcf_price:.2f}")
        with col_b:
            st.metric("現在の株価（USD）", f"{current_stock_price:.2f}")
        with col_c:
            st.metric("上昇余地", f"{upside_potential:.2f}%", delta=f"{upside_potential:.2f}%")
        
        # 財務指標の比較
        st.subheader("財務指標の比較")
        comparison_data = {
            '指標': ['PER（株価収益率）', 'PBR（株価純資産倍率）', 'PSR（株価売上高倍率）'],
            '現在値': [financial_ratios['pe_ratio'], financial_ratios['pb_ratio'], financial_ratios['ps_ratio']],
            '業界平均': [industry_pe, industry_pb, industry_ps],
            '差異 (%)': [
                ((financial_ratios['pe_ratio'] / industry_pe) - 1) * 100,
                ((financial_ratios['pb_ratio'] / industry_pb) - 1) * 100,
                ((financial_ratios['ps_ratio'] / industry_ps) - 1) * 100
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        
        # 財務指標の視覚化
        fig2 = go.Figure()
        for i, metric in enumerate(['PER（株価収益率）', 'PBR（株価純資産倍率）', 'PSR（株価売上高倍率）']):
            fig2.add_trace(go.Bar(
                x=[metric],
                y=[comparison_df['現在値'][i]],
                name='現在値'
            ))
            fig2.add_trace(go.Bar(
                x=[metric],
                y=[comparison_df['業界平均'][i]],
                name='業界平均'
            ))
        
        fig2.update_layout(
            title='財務指標の比較',
            yaxis_title='倍率',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # 評価結果の詳細
        st.subheader("投資判断の根拠")
        
        # 割安度の分析
        valuation_status = "割安" if upside_potential > 10 else "適正" if -10 <= upside_potential <= 10 else "割高"
        
        st.write(f"**株価評価**: 現在の{company_name}の株価は**{valuation_status}**と判断されます。DCF法による本質的価値は現在の株価に対して{upside_potential:.2f}%の{valuation_status}度を示しています。")
        
        # 成長性の分析
        growth_evaluation = "高い" if revenue_growth_rate > 15 else "平均的" if 5 <= revenue_growth_rate <= 15 else "低い"
        st.write(f"**成長性**: {forecast_years}年間の予想年間成長率は{revenue_growth_rate}%で、これは**{growth_evaluation}**成長率です。この成長率が達成されれば、{forecast_years}年後の売上高は{forecasted_data['売上高（百万円）'].iloc[-1]:.2f}百万円に達します。")
        
        # 収益性の分析
        profitability_trend = "改善" if target_net_margin > current_net_margin else "維持" if target_net_margin == current_net_margin else "悪化"
        st.write(f"**収益性**: 純利益率は現在の{current_net_margin:.2f}%から{target_net_margin:.2f}%へと**{profitability_trend}**する見込みです。これにより{forecast_years}年後の純利益は{forecasted_data['純利益（百万円）'].iloc[-1]:.2f}百万円に達すると予測されます。")
    
    with col2:
        # SWOT分析
        st.subheader("SWOT分析")
        swot = generate_swot_analysis(industry, revenue_growth_rate, current_net_margin, target_net_margin)
        
        st.markdown("##### 強み (Strengths)")
        st.write(swot['strengths'])
        
        st.markdown("##### 弱み (Weaknesses)")
        st.write(swot['weaknesses'])
        
        st.markdown("##### 機会 (Opportunities)")
        st.write(swot['opportunities'])
        
        st.markdown("##### 脅威 (Threats)")
        st.write(swot['threats'])
        
        # 競争優位性（モート）分析
        st.subheader("競争優位性（モート）分析")
        moat = generate_moat_analysis(industry, revenue_growth_rate, current_net_margin)
        
        st.markdown("##### 競争優位性の評価")
        st.write(moat['evaluation'])
        
        st.markdown("##### 持続可能な競争優位の源泉")
        st.write(moat['sources'])
        
        # 総合評価と投資推奨
        st.subheader("総合評価")
        
        # 投資推奨度を計算（例として、上昇余地、成長率、純利益率の改善度から計算）
        recommendation_score = (
            (upside_potential / 10) +  # 上昇余地の貢献
            (revenue_growth_rate / 10) +  # 成長率の貢献
            ((target_net_margin - current_net_margin) * 2)  # 純利益率改善の貢献
        )
        
        recommendation = ""
        if recommendation_score > 10:
            recommendation = "強く買い推奨"
        elif recommendation_score > 5:
            recommendation = "買い推奨"
        elif recommendation_score > 0:
            recommendation = "弱気な買い"
        elif recommendation_score > -5:
            recommendation = "様子見"
        else:
            recommendation = "売り推奨"
        
        # 投資推奨度を表示
        st.info(f"**投資推奨度**: {recommendation}")
        
        # 主要リスク要因
        st.markdown("##### 主要リスク要因")
        st.write("1. 予想成長率を達成できない可能性")
        st.write("2. 純利益率の目標達成に失敗する可能性")
        st.write(f"3. 業界平均を下回る財務パフォーマンス")
        st.write("4. 市場環境や競争状況の急激な変化")

# 使用方法のガイド（企業名が入力されていない場合に表示）
else:
    # サブスクリプションプランの説明を表示
    st.markdown("<div class='card'><h2 class='card-title' style='text-align: center;'>💰 企業価値分析ツールへようこそ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem;'>サイドバーから企業情報を入力して分析を開始しましょう</p>", unsafe_allow_html=True)
    
    # 3つのカードを横に並べる
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f0f5ff; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; color: #0066cc;">🧮 財務分析</h3>
            <p>収益成長率と割引率に基づいた企業の本質的価値を計算します。DCF法による株価評価と上昇余地の分析が可能です。</p>
            <ul>
                <li>売上高と純利益の予測</li>
                <li>本質的価値の計算</li>
                <li>財務指標の比較・分析</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f5fff0; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; color: #00aa44;">📊 SWOT分析</h3>
            <p>業界特性と成長性に基づいた包括的なSWOT分析を提供します。企業の強み、弱み、機会、脅威を明確に把握できます。</p>
            <ul>
                <li>強み・弱みの分析</li>
                <li>機会・脅威の特定</li>
                <li>競争優位性の評価</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #fff0f5; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; color: #cc0066;">🔮 投資判断サポート</h3>
            <p>様々な財務指標と分析結果を総合的に判断して、投資推奨度を算出します。投資判断の根拠を明確に理解できます。</p>
            <ul>
                <li>投資推奨度の算出</li>
                <li>主要リスク要因の特定</li>
                <li>投資判断の根拠の説明</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 使い方ガイド
    st.markdown("<div class='card' style='margin-top: 2rem;'><h3 class='card-title'>🚀 使い方ガイド</h3>", unsafe_allow_html=True)
    
    # ステップを示す
    steps = [
        {"icon": "🔍", "title": "企業を選択", "desc": "サイドバーから企業を選択するか、財務情報を手動で入力します。"},
        {"icon": "📈", "title": "成長率を設定", "desc": "予想される売上高成長率を設定します。"},
        {"icon": "💰", "title": "割引率を設定", "desc": "将来キャッシュフローの現在価値計算に使用する割引率を設定します。"},
        {"icon": "📊", "title": "結果を確認", "desc": "本質的価値分析、財務指標比較、SWOT分析などの結果を確認します。"}
    ]
    
    steps_html = ""
    for i, step in enumerate(steps):
        steps_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background-color: #0066cc; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 1.2rem;">
                {step["icon"]}
            </div>
            <div>
                <h4 style="margin: 0; color: #0066cc;">ステップ {i+1}: {step["title"]}</h4>
                <p style="margin: 0;">{step["desc"]}</p>
            </div>
        </div>
        """
    
    st.markdown(steps_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # プラン比較表
    st.markdown("<div class='card' style='margin-top: 2rem;'><h3 class='card-title'>💎 プラン比較</h3>", unsafe_allow_html=True)
    
    # 表形式でプラン比較
    plan_table = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <thead>
            <tr style="background-color: #f0f0f0;">
                <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">機能</th>
                <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">無料</th>
                <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">ベーシック</th>
                <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">プレミアム</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">月額料金</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">¥0</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">¥2,500</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">¥4,900</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">分析可能企業数</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">月3社</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">月20社</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">無制限</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">基本価値分析</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">SWOT分析</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">基本のみ</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">詳細</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">詳細</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">決算情報分析</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">×</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">業界詳細分析</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">×</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">×</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">✓</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">カスタマーサポート</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">×</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">Eメールのみ</td>
                <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">優先サポート</td>
            </tr>
        </tbody>
    </table>
    """
    
    st.markdown(plan_table, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# フッター
st.markdown("---")
st.markdown("このツールは投資判断のための参考情報を提供するものであり、投資の成果を保証するものではありません。実際の投資判断はご自身の責任で行ってください。")
