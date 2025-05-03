import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ページ設定
st.set_page_config(
    page_title="企業分析 - 企業価値分析プロ",
    page_icon="📊",
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
    
    .form-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
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
    
    .recommendation-box {
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .recommendation-buy {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    
    .recommendation-hold {
        background-color: #fff3cd;
        color: #664d03;
    }
    
    .recommendation-sell {
        background-color: #f8d7da;
        color: #842029;
    }
</style>
""", unsafe_allow_html=True)

# メインコンテンツ
st.markdown("<h1 class='main-header'>📊 企業分析</h1>", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("### 企業分析ツール")
    st.markdown("企業の本質的価値を計算し、投資判断をサポートします。")
    
    st.markdown("---")
    
    # ナビゲーション
    st.markdown("### ナビゲーション")
    if st.button("ホームに戻る", key="home_btn"):
        st.switch_page("app.py")

# 入力フォーム
st.markdown("<div class='form-section'>", unsafe_allow_html=True)
st.markdown("<h2>企業情報と予測パラメータの入力</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("企業名", value="Apple Inc.")
    industry = st.selectbox("業界", [
        "テクノロジー", "金融", "ヘルスケア", "消費財", "工業", 
        "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"
    ])
    ticker = st.text_input("ティッカーシンボル（例: AAPL）", value="AAPL")

with col2:
    revenue = st.number_input("直近の売上高（百万USD）", value=365817.0, step=1000.0)
    net_income = st.number_input("直近の純利益（百万USD）", value=94680.0, step=100.0)
    shares_outstanding = st.number_input("発行済株式数（百万株）", value=15634.0, step=10.0)
    current_stock_price = st.number_input("現在の株価（USD）", value=175.04, step=0.1)

st.markdown("### DCF分析パラメータ")

col1, col2, col3 = st.columns(3)

with col1:
    revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=15.0, step=0.5)
    net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=25.0, step=0.5)

with col2:
    discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5)
    terminal_multiple = st.slider("終末価値倍率（PE）", min_value=5.0, max_value=30.0, value=20.0, step=0.5)

with col3:
    forecast_years = st.slider("予測期間（年）", min_value=5, max_value=10, value=5, step=1)
    industry_pe = st.number_input("業界平均PER", value=25.0, step=0.5)

st.markdown("</div>", unsafe_allow_html=True)

# 分析実行ボタン
if st.button("企業価値を計算", key="calculate_btn", use_container_width=True):
    with st.spinner("企業価値を計算中..."):
        # 計算処理をシミュレート
        progress_bar = st.progress(0)
        for i in range(100):
            # シミュレート進捗
            progress_bar.progress(i + 1)
            # 遅延を加える
            import time
            time.sleep(0.01)
        
        # サンプルデータの作成
        dcf_price = current_stock_price * (1 + (revenue_growth - discount_rate) / 100)
        upside_potential = ((dcf_price / current_stock_price) - 1) * 100
        
        # 結果表示
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='card-title'>{company_name} ({ticker}) の分析結果</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**業界**: {industry}")
            st.markdown(f"**分析日**: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        
        with col2:
            st.markdown(f"**現在の株価**: ${current_stock_price:.2f}")
            st.markdown(f"**DCF価値**: ${dcf_price:.2f}")
        
        with col3:
            st.markdown(f"**上昇余地**: {upside_potential:.1f}%")
            
            # 投資推奨度
            recommendation = "様子見"
            recommendation_class = "recommendation-hold"
            
            if upside_potential > 20:
                recommendation = "強い買い"
                recommendation_class = "recommendation-buy"
            elif upside_potential > 10:
                recommendation = "買い"
                recommendation_class = "recommendation-buy"
            elif upside_potential > -10:
                recommendation = "様子見"
                recommendation_class = "recommendation-hold"
            elif upside_potential > -20:
                recommendation = "売り"
                recommendation_class = "recommendation-sell"
            else:
                recommendation = "強い売り"
                recommendation_class = "recommendation-sell"
            
            st.markdown(f"""
            <div class='recommendation-box {recommendation_class}'>
                {recommendation}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # DCF分析詳細
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>DCF分析</h2>", unsafe_allow_html=True)
        
        # 予測データを作成
        years = list(range(1, forecast_years + 1))
        forecasted_revenue = [revenue * ((1 + revenue_growth/100) ** year) for year in years]
        forecasted_net_income = [rev * (net_margin/100) for rev in forecasted_revenue]
        forecasted_df = pd.DataFrame({
            '年': years,
            '売上高（百万$）': forecasted_revenue,
            '純利益率（%）': [net_margin] * forecast_years,
            '純利益（百万$）': forecasted_net_income
        })
        
        # 予測財務データ
        st.markdown("#### 予測財務データ")
        st.dataframe(forecasted_df, use_container_width=True)
        
        # 企業価値の計算（簡易版）
        discount_factors = [(1 + discount_rate/100) ** -year for year in years]
        discounted_cash_flows = [cf * df for cf, df in zip(forecasted_net_income, discount_factors)]
        terminal_value = forecasted_net_income[-1] * terminal_multiple * discount_factors[-1]
        total_firm_value = sum(discounted_cash_flows) + terminal_value
        value_per_share = total_firm_value / shares_outstanding
        
        # 企業価値の内訳
        st.markdown("#### 企業価値の内訳")
        
        enterprise_value_components = pd.DataFrame({
            '項目': ['割引後CF合計', '終末価値', '企業価値合計', '1株あたり企業価値'],
            '金額（百万$）': [
                sum(discounted_cash_flows),
                terminal_value,
                total_firm_value,
                value_per_share
            ]
        })
        
        # 最後の行は1株あたりの値なので別表示
        enterprise_value_df = enterprise_value_components.iloc[:-1].copy()
        enterprise_value_df['割合'] = enterprise_value_df['金額（百万$）'] / total_firm_value * 100
        enterprise_value_df['割合'] = enterprise_value_df['割合'].map('{:.1f}%'.format)
        
        st.dataframe(enterprise_value_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 円グラフ
            fig = px.pie(
                names=enterprise_value_components['項目'].iloc[:2],
                values=enterprise_value_components['金額（百万$）'].iloc[:2],
                title="企業価値の構成",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # メトリクス
            st.markdown("<div style='display: flex; flex-direction: column;'>", unsafe_allow_html=True)
            
            # 企業価値
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>企業価値合計</div>
                <div class='metric-value'>${total_firm_value:,.0f}百万</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 1株あたり価値
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>1株あたり価値</div>
                <div class='metric-value'>${value_per_share:.2f}</div>
                <div>現在の株価: ${current_stock_price:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 上昇余地
            upside_color = "green" if upside_potential > 0 else "red"
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>上昇余地</div>
                <div class='metric-value' style='color: {upside_color};'>{upside_potential:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # SWOT分析（シンプルなバージョン）
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>SWOT分析</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 強み (Strengths)")
            
            if industry == "テクノロジー":
                st.markdown("- 強力なブランド認知度と顧客ロイヤリティ")
                st.markdown("- 持続的なイノベーション能力")
                st.markdown("- 多様な収益源と製品ラインナップ")
            else:
                st.markdown("- 業界内での確立された地位")
                st.markdown("- 優れた資本効率と利益率")
                st.markdown("- コスト管理と運営効率")
            
            st.markdown("#### 機会 (Opportunities)")
            
            if industry == "テクノロジー":
                st.markdown("- 新興市場への拡大機会")
                st.markdown("- AI・クラウドサービスの成長")
                st.markdown("- サブスクリプションモデルによる安定収益")
            else:
                st.markdown("- デジタル変革の機会")
                st.markdown("- 新しい製品・サービスラインの開発")
                st.markdown("- 戦略的買収による成長")
            
        with col2:
            st.markdown("#### 弱み (Weaknesses)")
            
            if industry == "テクノロジー":
                st.markdown("- 一部製品への依存度")
                st.markdown("- 高い研究開発コスト")
                st.markdown("- 規制圧力の増加")
            else:
                st.markdown("- 新技術への適応の遅れ")
                st.markdown("- 市場変化への対応速度")
                st.markdown("- 人材獲得競争")
            
            st.markdown("#### 脅威 (Threats)")
            
            if industry == "テクノロジー":
                st.markdown("- 激しい競合環境")
                st.markdown("- 技術の急速な変化")
                st.markdown("- 経済的不確実性")
            else:
                st.markdown("- 新規参入者の脅威")
                st.markdown("- 代替製品・サービスの台頭")
                st.markdown("- 規制環境の変化")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 感度分析（シンプルなバージョン）
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>感度分析</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <p>成長率と割引率の変動が企業価値に与える影響をヒートマップで表示しています。</p>
        """, unsafe_allow_html=True)
        
        # シンプルな感度分析のためのデータ作成
        growth_rates = np.linspace(revenue_growth - 10, revenue_growth + 10, 5)
        discount_rates = np.linspace(discount_rate - 5, discount_rate + 5, 5)
        
        sensitivity_matrix = []
        for g in growth_rates:
            row = []
            for d in discount_rates:
                # 簡易計算
                adjusted_value = current_stock_price * (1 + (g - d) / 100)
                row.append(adjusted_value)
            sensitivity_matrix.append(row)
        
        # ヒートマップの作成
        fig = go.Figure(data=go.Heatmap(
            z=sensitivity_matrix,
            x=[f"{d:.1f}%" for d in discount_rates],
            y=[f"{g:.1f}%" for g in growth_rates],
            colorscale='RdBu_r',
            colorbar=dict(title="株価 ($)"),
            hovertemplate="成長率: %{y}<br>割引率: %{x}<br>株価: $%{z:.2f}<extra></extra>"
        ))
        
        fig.update_layout(
            title="成長率と割引率の感度分析",
            xaxis_title="割引率 (%)",
            yaxis_title="成長率 (%)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <h3>感度分析の解釈</h3>
        <p>
        ヒートマップは、成長率と割引率のさまざまな組み合わせに基づいた企業価値を示しています。
        青色の領域は高い企業価値を示し、赤色の領域は低い企業価値を示します。
        </p>
        <p>
        <strong>注意</strong>: 感度分析は将来予測に基づくものであり、実際の結果は異なる場合があります。
        投資判断の際は、他の情報源も参考にしてください。
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 分析が完了したことを表示
        st.success("企業価値の分析が完了しました。上記の結果を参考に投資判断を行ってください。")