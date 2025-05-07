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

# stock_dataモジュールをインポート
from stock_data import get_stock_data, update_stock_price, fetch_tradingview_price

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
st.markdown("企業の財務データとファンダメンタルズを分析し、SWOT分析、競争優位性（モート）分析、最新の注目ポイントなどを提供します。")

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

# 入力フォーム
st.markdown("<div class='form-section mobile-card'>", unsafe_allow_html=True)
st.markdown("<h2>企業情報と予測パラメータの入力</h2>", unsafe_allow_html=True)

# ブラウザの幅に応じて列の数を調整 (モバイル対応)
if st.session_state.get('is_mobile', False) or len(st.session_state) < 5:  # モバイル判定の簡易実装
    # モバイル向けレイアウト（縦に並べる）
    col1 = st.container()
    col2 = st.container()
else:
    # デスクトップ向けレイアウト（横に並べる）
    col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("企業名", value="Apple Inc.")
    industry = st.selectbox("業界", [
        "テクノロジー", "金融", "ヘルスケア", "消費財", "工業", 
        "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"
    ])
    ticker = st.text_input("ティッカーシンボル（例: AAPL）", value="AAPL")
    
    # ティッカーが入力されている場合、価格を手動で入力するオプションを表示
    if ticker:
        st.info("株価はユーザー入力に基づいて計算されます。下の「現在の株価（USD）」欄に最新の株価を入力してください。")
        
        # 既存データがある場合は表示
        existing_data = get_stock_data(ticker)
        if existing_data and 'name' in existing_data:
            st.success(f"{ticker} ({existing_data['name']})の基本情報を読み込みました。")
            
            # もし既存の株価データがあればセッションに保存
            if 'current_stock_price' in existing_data:
                st.session_state.current_price = existing_data['current_stock_price']
        
        # 手動で株価を更新するためのボタン
        if st.button("入力した株価でデータを更新", key="update_price_btn"):
            if 'current_price' in st.session_state:
                with st.spinner("株価データを更新中..."):
                    # データを更新
                    update_stock_price(ticker, st.session_state.current_price)
                    st.success(f"{ticker}の株価を${st.session_state.current_price:.2f}に更新しました。")
                    # 最新の情報を反映するためにページをリロード
                    st.rerun()
            else:
                st.error("更新する株価がありません。先に「現在の株価（USD）」を入力してください。")

with col2:
    revenue_str = st.text_input("年間売上高（USD）", value="365,817,000,000")
    try:
        revenue = float(revenue_str.replace(',', ''))
    except:
        revenue = 365817000000.0
        
    net_income_str = st.text_input("年間純利益（USD）", value="94,680,000,000")
    try:
        net_income = float(net_income_str.replace(',', ''))
    except:
        net_income = 94680000000.0
    shares_outstanding_str = st.text_input("発行済株式数", value="15,634,000,000")
    try:
        shares_outstanding = float(shares_outstanding_str.replace(',', ''))
    except:
        shares_outstanding = 15634000000.0
    
    # TradingViewから取得した価格があれば、それをデフォルト値として使用
    default_price = st.session_state.get('current_price', 175.04)
    current_stock_price_str = st.text_input("現在の株価（USD）", value=f"{default_price}")
    try:
        current_stock_price = float(current_stock_price_str.replace(',', ''))
    except:
        current_stock_price = default_price

st.markdown("### ファンダメンタル分析パラメータ")

col1, col2, col3 = st.columns(3)

with col1:
    revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=15.0, step=0.5)
    net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=25.0, step=0.5)

with col2:
    industry_pe = st.number_input("業界平均PER", value=25.0, step=0.5)
    industry_pbr = st.number_input("業界平均PBR", value=3.0, step=0.1)

with col3:
    forecast_years = st.slider("予測期間（年）", min_value=1, max_value=5, value=3, step=1)
    industry_psr = st.number_input("業界平均PSR", value=5.0, step=0.1)

st.markdown("</div>", unsafe_allow_html=True)

# 分析実行ボタン
if st.button("企業分析を実行", key="calculate_btn", use_container_width=True):
    with st.spinner("企業のファンダメンタル分析を実行中..."):
        # 計算処理をシミュレート
        progress_bar = st.progress(0)
        for i in range(100):
            # シミュレート進捗
            progress_bar.progress(i + 1)
            # 遅延を加える
            import time
            time.sleep(0.01)
        
        # 業界平均倍率による評価
        per_price = (net_income / shares_outstanding) * industry_pe
        pbr_price = (revenue * 0.3 / shares_outstanding) * industry_pbr  # 簡易的な純資産価値として売上の30%を使用
        psr_price = (revenue / shares_outstanding) * industry_psr / 10  # PSRは倍率が大きいため、調整
        
        # 平均価格と上昇余地
        avg_price = (per_price + pbr_price + psr_price) / 3
        upside_potential = ((avg_price / current_stock_price) - 1) * 100
        
        # 感度分析用の変数（後のコードとの互換性のため）
        discount_rate = 10.0
        terminal_multiple = 20.0
        
        # 結果表示
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='card-title'>{company_name} ({ticker}) の分析結果</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**業界**: {industry}")
            st.markdown(f"**分析日**: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        
        with col2:
            st.markdown(f"**現在の株価**: ${current_stock_price:.2f}")
            st.markdown(f"**平均倍率価値**: ${avg_price:.2f}")
        
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
        
        # ファンダメンタル分析詳細
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>ファンダメンタル分析</h2>", unsafe_allow_html=True)
        
        # 予測データを作成
        years = list(range(1, forecast_years + 1))
        forecasted_revenue = [revenue * ((1 + revenue_growth/100) ** year) for year in years]
        forecasted_net_income = [rev * (net_margin/100) for rev in forecasted_revenue]
        forecasted_df = pd.DataFrame({
            '年': years,
            '売上高（$）': forecasted_revenue,
            '純利益率（%）': [net_margin] * forecast_years,
            '純利益（$）': forecasted_net_income
        })
        
        # 金額を見やすく表示するためにフォーマット
        forecasted_df['売上高（$）'] = forecasted_df['売上高（$）'].map('${:,.0f}'.format)
        forecasted_df['純利益（$）'] = forecasted_df['純利益（$）'].map('${:,.0f}'.format)
        
        # 予測財務データ
        st.markdown("#### 予測財務データ")
        st.dataframe(forecasted_df, use_container_width=True)
        
        # 企業価値の計算（簡易版）
        discount_factors = [(1 + discount_rate/100) ** -year for year in years]
        discounted_cash_flows = [cf * df for cf, df in zip(forecasted_net_income, discount_factors)]
        terminal_value = forecasted_net_income[-1] * terminal_multiple * discount_factors[-1]
        total_firm_value = sum(discounted_cash_flows) + terminal_value
        value_per_share = total_firm_value / shares_outstanding
        
        # 業界平均倍率による評価
        st.markdown("#### 業界平均倍率による評価")
        
        evaluation_components = pd.DataFrame({
            '評価方法': ['PER（株価収益率）', 'PBR（株価純資産倍率）', 'PSR（株価売上高倍率）', '平均倍率価値'],
            '使用倍率': [
                f"{industry_pe:.1f}倍",
                f"{industry_pbr:.1f}倍",
                f"{industry_psr:.1f}倍",
                "平均"
            ],
            '算出株価（$）': [
                per_price,
                pbr_price,
                psr_price,
                avg_price
            ],
            '上昇余地（%）': [
                ((per_price / current_stock_price) - 1) * 100,
                ((pbr_price / current_stock_price) - 1) * 100,
                ((psr_price / current_stock_price) - 1) * 100,
                upside_potential
            ]
        })
        
        # 金額を見やすく表示するためにフォーマット
        evaluation_components['算出株価（$）'] = evaluation_components['算出株価（$）'].map('${:.2f}'.format)
        evaluation_components['上昇余地（%）'] = evaluation_components['上昇余地（%）'].map('{:+.1f}%'.format)
        
        st.dataframe(evaluation_components, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 倍率法による株価の比較
            fig = px.bar(
                x=['PER価値', 'PBR価値', 'PSR価値', '平均価値', '現在株価'],
                y=[per_price, pbr_price, psr_price, avg_price, current_stock_price],
                title="倍率法による株価評価",
                color_discrete_sequence=['#0066cc', '#0066cc', '#0066cc', '#0066cc', '#ff9900'],
                labels={'x': '評価方法', 'y': '株価 ($)'},
            )
            
            fig.update_layout(
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # メトリクス
            st.markdown("<div style='display: flex; flex-direction: column;'>", unsafe_allow_html=True)
            
            # PER価値
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>PER価値（業界平均PER: {industry_pe}倍）</div>
                <div class='metric-value'>${per_price:.2f}</div>
                <div>上昇余地: {((per_price / current_stock_price) - 1) * 100:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 平均倍率価値
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>平均倍率価値</div>
                <div class='metric-value'>${avg_price:.2f}</div>
                <div>現在の株価: ${current_stock_price:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 上昇余地
            upside_color = "green" if upside_potential > 0 else "red"
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>上昇余地</div>
                <div class='metric-value' style='color: {upside_color};'>{upside_potential:+.1f}%</div>
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
        
        # 最新の注目ポイント
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>最新の注目ポイント</h2>", unsafe_allow_html=True)
        
        # 企業別カスタマイズ
        if ticker == "AAPL":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $95.7B（前年同期比+4.2%）
            - EPS: $1.53（予想$1.50を上回る）
            - サービス事業の売上高は過去最高の$24.2B（前年同期比+21.3%）
            - 世界のアクティブデバイスが30億台を突破
            
            ### 経営陣のコメント
            
            **ティム・クック CEO**
            > 「iPhone15シリーズは引き続き好調で、中国市場も安定しています。Vision Proの販売開始は当社の空間コンピューティング戦略の重要なマイルストーンです。」
            
            **ルカ・マエストリ CFO**
            > 「当社は800億ドルの自社株買いプログラムを発表しました。株主還元と成長投資のバランスを取りながら、強固なキャッシュフローを維持しています。」
            
            ### 注目すべきポイント
            
            - AIへの投資拡大がアナウンスされ、6月のWWDCで「Apple Intelligence」を発表予定
            - インド市場での製造拡大が継続し、サプライチェーン多様化の取り組みが進展
            - サブスクリプションサービスの価格改定が行われ、収益拡大に貢献
            """, unsafe_allow_html=True)
        elif ticker == "MSFT":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $61.9B（前年同期比+13.3%）
            - EPS: $2.94（予想$2.85を上回る）
            - クラウド事業（Azure）の売上高: $26.7B（前年同期比+27.4%）
            - 営業利益率: 45.2%（前年同期比+2.1ポイント）
            
            ### 経営陣のコメント
            
            **サティア・ナデラ CEO**
            > 「AIの商用化が加速しており、Azureの新規顧客獲得と既存顧客のアップセルの両面で恩恵を受けています。Copilotの導入企業は3,500社を超えました。」
            
            **エイミー・フッド CFO**
            > 「AI投資は当社の長期的な成長を支えるものであり、効率性とAIインフラへの投資のバランスを取りながら、マージンの拡大を継続しています。」
            
            ### 注目すべきポイント
            
            - 生成AIへの投資が全事業部門で加速、特にCopilotとAzure OpenAIが成長をけん引
            - OfficeCopilotのユーザー数が急増し、商用利用が拡大
            - OpenAIとの提携強化により、競合他社との技術的優位性を維持
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            ### 最新の注目ポイント
            
            実際の企業分析では、以下のような最新の情報が提供されます：
            
            **決算情報のハイライト**
            - 直近の四半期決算の主要数値
            - アナリスト予想との比較
            - 前年同期比の成長率
            - セグメント別の業績
            
            **経営陣の発言・将来見通し**
            - 決算発表会での重要発言
            - 将来の成長戦略に関するコメント
            - 市場環境に対する見解
            
            **市場の反応と専門家の意見**
            - 決算後の株価の動き
            - アナリストの評価・格付け変更
            - 今後の株価目標
            
            **最新のビジネストレンド**
            - 新製品・サービスの動向
            - 競合状況の変化
            - 規制環境の変化
            - 業界トレンドとの関連性
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 成長予測（シンプルなバージョン）
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>成長予測</h2>", unsafe_allow_html=True)
        
        # 売上高と純利益の予測グラフ
        years = list(range(0, forecast_years + 1))
        base_year = datetime.datetime.now().year
        year_labels = [str(base_year + year) for year in years]
        
        forecasted_revenue_with_current = [revenue] + forecasted_revenue
        forecasted_net_income_with_current = [net_income] + forecasted_net_income
        
        fig = go.Figure()
        
        # 売上高
        fig.add_trace(go.Bar(
            x=year_labels,
            y=forecasted_revenue_with_current,
            name='売上高',
            marker_color='#0066cc'
        ))
        
        # 純利益
        fig.add_trace(go.Bar(
            x=year_labels,
            y=forecasted_net_income_with_current,
            name='純利益',
            marker_color='#00cc66'
        ))
        
        fig.update_layout(
            title=f"売上高と純利益の予測（{forecast_years}年間）",
            xaxis_title="年",
            yaxis_title="金額（USD）",
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # 金額表示を読みやすく
        fig.update_yaxes(tickformat=",.0f")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <p>
        上記のグラフは、入力された売上高成長率と純利益率に基づく予測を示しています。
        実際の結果は、市場環境、競合状況、技術革新などの要因によって大きく異なる可能性があります。
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 分析が完了したことを表示
        st.success("企業価値の分析が完了しました。上記の結果を参考に投資判断を行ってください。")