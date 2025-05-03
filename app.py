import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import trafilatura
import requests
from utils import generate_swot_analysis, generate_moat_analysis
from financial_models import calculate_intrinsic_value, calculate_financial_ratios

# ページ設定
st.set_page_config(
    page_title="企業価値分析ツール",
    page_icon="📊",
    layout="wide"
)

# アプリケーションタイトル
st.title("企業の本質的価値分析ツール")
st.markdown("このアプリでは、予想収益成長率と純利益率に基づいて企業の本質的価値を計算し、投資判断をサポートします。")

# サブスクリプションプラン機能
def show_subscription_plans():
    st.sidebar.markdown("---")
    st.sidebar.header("サブスクリプションプラン")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        st.markdown("### 🔹 ベーシック")
        st.markdown("**¥1,980/月**")
        st.markdown("- 基本的な企業分析")
        st.markdown("- 月10社まで分析可能")
        st.markdown("- 基本的なSWOT分析")
        if st.button("選択", key="basic_plan"):
            st.session_state.subscription = "basic"
            st.success("ベーシックプランが選択されました")
    
    with col2:
        st.markdown("### 🔷 プロフェッショナル")
        st.markdown("**¥4,980/月**")
        st.markdown("- 無制限の企業分析")
        st.markdown("- 詳細な競合分析")
        st.markdown("- 決算情報分析")
        st.markdown("- プレミアムレポート")
        if st.button("選択", key="pro_plan"):
            st.session_state.subscription = "professional"
            st.success("プロフェッショナルプランが選択されました")
    
    with col3:
        st.markdown("### 💎 エンタープライズ")
        st.markdown("**¥9,980/月**")
        st.markdown("- すべてのプロ機能")
        st.markdown("- リアルタイム決算分析")
        st.markdown("- 業界詳細レポート")
        st.markdown("- API連携")
        st.markdown("- 専門家サポート")
        if st.button("選択", key="enterprise_plan"):
            st.session_state.subscription = "enterprise"
            st.success("エンタープライズプランが選択されました")

# セッション状態の初期化
if 'subscription' not in st.session_state:
    st.session_state.subscription = "basic"  # デフォルトはベーシックプラン

# サイドバー - 基本パラメータ入力
with st.sidebar:
    st.header("企業情報と予測パラメータ")
    
    # サブスクリプションプランの表示
    show_subscription_plans()
    
    # 企業の基本情報
    company_name = st.text_input("企業名", "")
    industry = st.selectbox(
        "業界",
        ["テクノロジー", "金融", "ヘルスケア", "消費財", "工業", "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"]
    )
    
    # 証券コードまたはティッカーシンボル（プロおよびエンタープライズプラン用）
    if st.session_state.subscription in ["professional", "enterprise"]:
        company_symbol = st.text_input("証券コード/ティッカーシンボル（例: 7203.T, AAPL）", "")
    
    # 現在の財務情報
    st.subheader("現在の財務情報")
    current_revenue = st.number_input("現在の年間売上高（百万円）", min_value=0, value=10000)
    current_net_income = st.number_input("現在の純利益（百万円）", min_value=-10000, value=1000)
    current_net_margin = (current_net_income / current_revenue) * 100 if current_revenue > 0 else 0
    st.info(f"現在の純利益率: {current_net_margin:.2f}%")
    
    # 株式関連情報
    shares_outstanding = st.number_input("発行済株式数（百万株）", min_value=0.1, value=100.0, step=0.1)
    current_stock_price = st.number_input("現在の株価（円）", min_value=0.0, value=1000.0, step=0.1)
    book_value_per_share = st.number_input("1株あたり純資産（円）", min_value=0.0, value=500.0, step=0.1)
    
    # 予測パラメータ
    st.subheader("成長予測パラメータ")
    revenue_growth_rate = st.slider("年間売上高成長率 (%)", min_value=-20, max_value=100, value=10)
    target_net_margin = st.slider("目標純利益率 (%)", min_value=-20, max_value=50, value=int(current_net_margin))
    forecast_years = st.slider("予測期間（年）", min_value=1, max_value=10, value=5)
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
        
    if st.session_state.subscription in ["professional", "enterprise"] and company_symbol:
        from earnings_scraper import get_earnings_highlights
        
        st.subheader("🔍 最新の決算ハイライト")
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
    
    # エンタープライズプランのみ、業界の詳細分析も表示
    if st.session_state.subscription == "enterprise":
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
        forecasted_data['売上高（百万円）'] = [current_revenue * ((1 + revenue_growth_rate/100) ** year) for year in years]
        
        # 純利益率の予測（現在から目標まで線形に変化すると仮定）
        forecasted_data['純利益率 (%)'] = [current_net_margin + (target_net_margin - current_net_margin) * (year / forecast_years) for year in years]
        
        # 純利益の予測
        forecasted_data['純利益（百万円）'] = forecasted_data['売上高（百万円）'] * forecasted_data['純利益率 (%)'] / 100
        
        # 1株あたり利益（EPS）の予測
        forecasted_data['EPS（円）'] = forecasted_data['純利益（百万円）'] * 1000000 / shares_outstanding / 1000000
        
        # 予測データを表示
        st.subheader("財務予測")
        st.dataframe(forecasted_data.round(2))
        
        # 売上高と純利益のグラフ
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=forecasted_data['年'],
            y=forecasted_data['売上高（百万円）'],
            name='売上高（百万円）'
        ))
        fig1.add_trace(go.Line(
            x=forecasted_data['年'],
            y=forecasted_data['純利益（百万円）'],
            name='純利益（百万円）',
            yaxis='y2'
        ))
        fig1.update_layout(
            title='売上高と純利益の予測',
            xaxis_title='年',
            yaxis=dict(title='売上高（百万円）'),
            yaxis2=dict(title='純利益（百万円）', overlaying='y', side='right'),
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
            st.metric("DCF法による株価（円）", f"{dcf_price:.2f}")
        with col_b:
            st.metric("現在の株価（円）", f"{current_stock_price:.2f}")
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
    col_plan1, col_plan2 = st.columns([1, 2])
    
    with col_plan1:
        st.subheader("サブスクリプションプラン")
        st.info("👈 サイドバーから適切なプランを選択してください")
        
        st.markdown("### 🔹 ベーシック")
        st.markdown("- 基本的な企業分析機能")
        st.markdown("- 月額 ¥1,980")
        
        st.markdown("### 🔷 プロフェッショナル")
        st.markdown("- 決算情報の詳細分析")
        st.markdown("- 業績予測と比較機能")
        st.markdown("- 月額 ¥4,980")
        
        st.markdown("### 💎 エンタープライズ")
        st.markdown("- リアルタイムの業界分析")
        st.markdown("- 専門家によるレポート")
        st.markdown("- カスタマーサポート")
        st.markdown("- 月額 ¥9,980")
    
    with col_plan2:
        st.header("このツールの使い方")
        st.info("👈 サイドバーから企業情報と予測パラメータを入力してください。")
        
        st.markdown("""
        ### 基本的な使用方法
        1. サイドバーで企業名と業界を選択します。
        2. 現在の財務情報（売上高、純利益など）を入力します。
        3. 発行済株式数や現在の株価などの株式関連情報を入力します。
        4. 将来の成長予測パラメータを調整します：
           - 売上高成長率
           - 目標純利益率
           - 予測期間
           - 割引率
        5. 業界平均の財務指標を入力します（PER、PBR、PSRなど）。
        
        入力が完了すると、自動的に企業価値分析が表示されます。
        
        ### 主な機能
        - **財務予測**: 入力したパラメータに基づいて将来の売上高と純利益を予測
        - **本質的価値計算**: DCF法を用いた株価の本質的価値計算
        - **財務指標比較**: 現在の財務指標と業界平均の比較
        - **SWOT分析**: 企業の強み、弱み、機会、脅威の分析
        - **競争優位性分析**: 企業のモート（持続的競争優位性）の評価
        
        ### 指標の説明
        - **PER (株価収益率)**: 株価が1株当たり利益の何倍かを示す指標。低いほど割安と考えられる。
        - **PBR (株価純資産倍率)**: 株価が1株当たり純資産の何倍かを示す指標。1倍を下回ると純資産より安く買えることになる。
        - **PSR (株価売上高倍率)**: 株価が1株当たり売上高の何倍かを示す指標。特に利益が少ない成長企業の評価に使用される。
        - **DCF (割引キャッシュフロー)**: 将来の収益を現在価値に割り引いて企業価値を算出する方法。
        
        ### 最新決算情報（プロフェッショナル・エンタープライズプラン）
        プロフェッショナルおよびエンタープライズプランでは、最新の決算情報が自動的に取得・分析され、投資判断の精度が向上します。証券コードを入力するだけで、直近の決算発表内容を確認できます。
        
        ### 業界詳細分析（エンタープライズプラン）
        エンタープライズプランでは、業界全体のトレンドや競合状況の詳細な分析が提供され、より包括的な投資判断が可能になります。
        """)

# フッター
st.markdown("---")
st.markdown("このツールは投資判断のための参考情報を提供するものであり、投資の成果を保証するものではありません。実際の投資判断はご自身の責任で行ってください。")
