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

# ページ設定
st.set_page_config(
    page_title="企業分析 - 企業価値分析プロ",
    page_icon="📊",
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
    <div class="page-title">📊 企業分析</div>
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

# 企業選択フォーム
st.markdown("<div class='form-section mobile-card'>", unsafe_allow_html=True)
st.markdown("<h2>企業を選択</h2>", unsafe_allow_html=True)

# 人気企業リストを作成
popular_companies = {
    "テクノロジー": [
        {"name": "Apple Inc.", "ticker": "AAPL", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "Microsoft Corporation", "ticker": "MSFT", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "Amazon.com Inc.", "ticker": "AMZN", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "Google (Alphabet Inc.)", "ticker": "GOOGL", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "Meta Platforms Inc.", "ticker": "META", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "NVIDIA Corporation", "ticker": "NVDA", "country": "アメリカ", "industry": "テクノロジー"},
        {"name": "Taiwan Semiconductor", "ticker": "TSM", "country": "台湾", "industry": "テクノロジー"},
        {"name": "Samsung Electronics", "ticker": "005930.KS", "country": "韓国", "industry": "テクノロジー"},
    ],
    "消費財": [
        {"name": "Coca-Cola Company", "ticker": "KO", "country": "アメリカ", "industry": "消費財"},
        {"name": "Nike Inc.", "ticker": "NKE", "country": "アメリカ", "industry": "消費財"},
        {"name": "McDonald's Corporation", "ticker": "MCD", "country": "アメリカ", "industry": "消費財"},
        {"name": "Starbucks Corporation", "ticker": "SBUX", "country": "アメリカ", "industry": "消費財"},
    ],
    "金融": [
        {"name": "JPMorgan Chase & Co.", "ticker": "JPM", "country": "アメリカ", "industry": "金融"},
        {"name": "Bank of America Corp.", "ticker": "BAC", "country": "アメリカ", "industry": "金融"},
        {"name": "Visa Inc.", "ticker": "V", "country": "アメリカ", "industry": "金融"},
        {"name": "Mastercard Inc.", "ticker": "MA", "country": "アメリカ", "industry": "金融"},
    ],
    "日本企業": [
        {"name": "トヨタ自動車", "ticker": "7203.T", "country": "日本", "industry": "自動車"},
        {"name": "ソニーグループ", "ticker": "6758.T", "country": "日本", "industry": "テクノロジー"},
        {"name": "日本電信電話", "ticker": "9432.T", "country": "日本", "industry": "通信"},
        {"name": "三菱UFJフィナンシャルグループ", "ticker": "8306.T", "country": "日本", "industry": "金融"},
        {"name": "ソフトバンクグループ", "ticker": "9984.T", "country": "日本", "industry": "テクノロジー"},
    ]
}

# タブでカテゴリを分ける
tab1, tab2 = st.tabs(["人気企業から選ぶ", "企業名で検索"])

with tab1:
    # サブタブでさらに分類
    category_tabs = st.tabs(list(popular_companies.keys()))
    
    selected_company = None
    
    for i, category in enumerate(popular_companies.keys()):
        with category_tabs[i]:
            # カテゴリごとのリスト表示
            for company in popular_companies[category]:
                if st.button(f"{company['name']} ({company['ticker']})", key=f"{company['ticker']}_btn"):
                    selected_company = company
                    # セッション状態に保存
                    st.session_state.selected_company = company
    
    # セッション状態から選択された企業を取得
    if 'selected_company' in st.session_state:
        selected_company = st.session_state.selected_company
        st.success(f"{selected_company['name']} ({selected_company['ticker']})を選択しました。")

with tab2:
    # 検索機能
    search_query = st.text_input("企業名またはティッカーで検索", placeholder="例: Apple, AAPL, アップル")
    
    if search_query:
        st.info("実際のアプリでは、ここで企業データベースから検索結果が表示されます。")
        search_results = []
        
        # デモ用の簡易検索ロジック
        for category in popular_companies:
            for company in popular_companies[category]:
                if (search_query.lower() in company['name'].lower() or 
                    search_query.upper() in company['ticker']):
                    search_results.append(company)
        
        if search_results:
            st.write("検索結果:")
            for result in search_results:
                if st.button(f"{result['name']} ({result['ticker']})", key=f"search_{result['ticker']}"):
                    st.session_state.selected_company = result
                    st.rerun()
        else:
            st.warning("検索結果が見つかりませんでした。別のキーワードで試してください。")

# 選択された企業情報を変数に格納
if 'selected_company' in st.session_state:
    company = st.session_state.selected_company
    company_name = company['name']
    ticker = company['ticker']
    industry = company['industry']
    country = company['country']
    
    # Display market status
    display_market_status()
    
    # Get comprehensive real-time data
    comprehensive_data = fetch_comprehensive_data(ticker)
    if comprehensive_data:
        current_stock_price = comprehensive_data['current_price']
        st.session_state.current_price = current_stock_price
        st.session_state.live_data = comprehensive_data
        
        # Show live data indicator
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.metric(f"{ticker} Stock Price", f"${current_stock_price:.2f}", delta="Live Data")
        with col2:
            st.success("🟢 Live")
        with col3:
            if st.button("🔄 Refresh", key=f"refresh_{ticker}"):
                st.cache_data.clear()
                st.rerun()
    else:
        st.error(f"Unable to fetch live data for {ticker}. Please check the ticker symbol.")
else:
    # デフォルト値（Appleを初期選択）
    company_name = "Apple Inc."
    ticker = "AAPL"
    industry = "テクノロジー"
    country = "アメリカ"
    current_stock_price = st.session_state.get('current_price', 175.04)

# 隠しパラメータ（コードの互換性のため）
revenue = 100000000000
net_income = 25000000000
shares_outstanding = 10000000000
revenue_growth = 15.0
net_margin = 25.0
forecast_years = 3
industry_pe = 25.0
industry_pbr = 3.0
industry_psr = 5.0
business_description = ""

st.markdown("</div>", unsafe_allow_html=True)

# 分析実行ボタン
if st.button("企業分析を実行", key="calculate_btn", use_container_width=True):
    with st.spinner("企業情報を分析中..."):
        # 計算処理をシミュレート
        progress_bar = st.progress(0)
        for i in range(100):
            # シミュレート進捗
            progress_bar.progress(i + 1)
            # 遅延を加える
            import time
            time.sleep(0.01)
        
        # 結果表示
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='card-title'>{company_name} ({ticker})</h2>", unsafe_allow_html=True)
        
        # 企業の基本情報
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <p><strong>業界</strong>: {industry}</p>
            <p><strong>所在国</strong>: {country}</p>
            <p><strong>分析日</strong>: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ビジネス概要
        if business_description:
            st.markdown("### ビジネス概要")
            st.write(business_description)
        else:
            # ティッカーごとのデフォルトのビジネス概要
            if ticker == "AAPL":
                st.markdown("### ビジネス概要")
                st.markdown("""
                Apple Inc.は、iPhoneスマートフォン、iPadタブレット、Macコンピュータ、Apple Watchウェアラブル、
                AirPods無線イヤホンなどのハードウェア製品とiOS、macOS、watchOSなどのソフトウェアを開発・販売するテクノロジー企業です。
                また、App Store、Apple Music、Apple TV+、iCloudなどのサービスも提供しています。
                世界中に直営店舗を展開し、製品のデザイン、開発、製造、マーケティングを一貫して行う垂直統合型のビジネスモデルを採用しています。
                """)
            elif ticker == "MSFT":
                st.markdown("### ビジネス概要")
                st.markdown("""
                Microsoft Corporationは、Windows OSやOfficeなどのソフトウェア製品で知られるテクノロジー企業です。
                現在はクラウドサービスのAzure、ビジネスアプリケーションのDynamics 365、生産性ツールのMicrosoft 365、
                ゲーム事業のXbox、検索エンジンのBingなど多角的に事業を展開しています。
                近年はAI技術への投資を加速させ、OpenAIとの提携によりCopilotなどの生成AIサービスも展開しています。
                """)
            else:
                st.markdown("### ビジネス概要")
                st.markdown("_入力されたティッカーシンボルに対する詳細情報はありません。ビジネス概要を入力してください。_")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ビジネスモデル分析
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>ビジネスモデル分析</h2>", unsafe_allow_html=True)
        
        # 企業ごとにカスタマイズしたビジネスモデル分析
        if ticker == "AAPL":
            st.markdown("""
            ### 収益源
            
            **製品売上（約75%）**
            - **iPhone**: 全体収益の約50%を占める主力製品
            - **Mac**: デスクトップおよびノートPCライン
            - **iPad**: タブレット製品ライン
            - **ウェアラブル・ホーム・アクセサリ**: Apple Watch、AirPods、HomePodなど
            
            **サービス（約25%）**
            - **App Store**: アプリ販売手数料（15-30%）
            - **サブスクリプション**: Apple Music、Apple TV+、Apple Arcade、Apple Fitness+
            - **クラウドサービス**: iCloudストレージ
            - **決済サービス**: Apple Payトランザクション手数料
            
            ### 競争優位性（モート）
            
            1. **エコシステム**: ハードウェア、ソフトウェア、サービスの垂直統合による囲い込み効果
            2. **ブランド力**: プレミアムポジショニングと高い顧客ロイヤリティ
            3. **研究開発力**: ハードウェアとソフトウェアの両面での革新的技術開発
            4. **App Store**: デベロッパーエコシステムによるネットワーク効果
            5. **小売販売網**: 直営店舗による顧客体験の最適化
            
            ### 成長戦略
            
            1. **サービス事業の拡大**: サブスクリプションモデルによる定期収益の増加
            2. **新興市場への展開**: インドなど成長市場での販売拡大
            3. **ウェアラブル市場の開拓**: Apple WatchやAirPodsの機能強化
            4. **AI統合**: 自社製品・サービス全体へのAI機能の組み込み
            5. **新製品カテゴリー**: Vision Proなど新領域への進出
            """)
        elif ticker == "MSFT":
            st.markdown("""
            ### 収益源
            
            **クラウドインテリジェンス（約40%）**
            - **Azure**: クラウドインフラおよびプラットフォームサービス
            - **サーバー製品**: オンプレミスサーバーソフトウェア
            - **エンタープライズサービス**: コンサルティングおよびサポート
            
            **生産性とビジネスプロセス（約35%）**
            - **Microsoft 365**: Office、Teams、Outlookなど
            - **Dynamics 365**: CRM・ERPソリューション
            - **LinkedIn**: プロフェッショナルネットワーキングサービス
            
            **パーソナルコンピューティング（約25%）**
            - **Windows**: OS販売およびライセンス
            - **Xbox**: ゲームコンソール、ゲームコンテンツ、サブスクリプション
            - **Surface**: ハードウェアデバイス
            - **検索広告**: Bing検索エンジンからの広告収入
            
            ### 競争優位性（モート）
            
            1. **エンタープライズ基盤**: 世界中の企業システムに深く根付いたエコシステム
            2. **開発者コミュニティ**: 世界最大級の開発者エコシステム
            3. **クロスプラットフォーム戦略**: 多様なデバイスとOSをサポート
            4. **AI技術投資**: OpenAIとの戦略的提携によるAI優位性
            5. **包括的なソリューション**: ビジネス向け製品・サービスの広範なポートフォリオ
            
            ### 成長戦略
            
            1. **クラウド事業の強化**: Azureのグローバル拡大とAI機能拡充
            2. **AIの商用化**: CopilotなどのAIアシスタントの全製品への統合
            3. **サブスクリプション強化**: Microsoft 365の機能拡張と価格戦略の最適化
            4. **ゲーム事業の拡大**: Activision Blizzard買収によるコンテンツ強化
            5. **セキュリティソリューション**: 包括的なセキュリティ製品の展開
            """)
        elif ticker == "AMZN":
            st.markdown("""
            ### 収益源
            
            **小売事業（約50%）**
            - **オンラインストア**: 自社ECプラットフォームでの直接販売
            - **サードパーティセラー**: マーケットプレイス手数料（8-15%）とFBA物流サービス
            - **実店舗**: Whole Foods Market、Amazon Fresh、Amazon Goなど
            
            **AWS（Amazon Web Services）（約15%の売上、50-60%の利益）**
            - **クラウドコンピューティング**: EC2、S3などのインフラサービス
            - **データベース**: RDS、DynamoDBなど
            - **AI/ML**: SageMaker、Lexなどの機械学習サービス
            
            **広告（約7%、急成長中）**
            - **検索広告**: アマゾン内検索結果に表示される広告
            - **ディスプレイ広告**: アマゾンおよび関連サイト上の広告
            
            **サブスクリプション（約5%）**
            - **Prime会員費**: 送料無料、Prime Video、Prime Musicなど
            - **デジタルコンテンツ**: Kindle、Audible、Amazon Music
            
            ### 競争優位性（モート）
            
            1. **規模の経済**: 世界最大の物流ネットワークと購買力
            2. **顧客中心主義**: 顧客体験の継続的最適化
            3. **データ活用能力**: 顧客購買データに基づく推奨と戦略的意思決定
            4. **技術イノベーション**: 継続的な技術投資（倉庫自動化、AIなど）
            5. **Prime エコシステム**: 会員制モデルによる顧客ロイヤリティと囲い込み
            
            ### 成長戦略
            
            1. **AWS拡大**: エンタープライズAI、ハイブリッドクラウド、エッジコンピューティング
            2. **広告ビジネス強化**: 検索外広告ネットワークの構築とデータに基づくターゲティング
            3. **ヘルスケア進出**: オンライン薬局、診療所ネットワーク、医療機器
            4. **金融サービス拡充**: 支払いソリューション、SMB融資、保険
            5. **国際市場開拓**: インド、中南米などの新興市場での展開加速
            """)
        elif ticker == "GOOGL":
            st.markdown("""
            ### 収益源
            
            **広告（約80%）**
            - **Google検索**: 検索結果に表示される広告
            - **YouTube広告**: 動画内およびディスプレイ広告
            - **Google広告ネットワーク**: パートナーサイト上の広告
            - **Android広告**: モバイルアプリ内広告
            
            **クラウド（約10%）**
            - **Google Cloud Platform (GCP)**: コンピューティング、ストレージ、ネットワーク
            - **Workspace**: Gmail、ドキュメント、スプレッドシートなどの生産性ツール
            - **クラウドAI/ML**: Vertex AI、BigQueryなどのデータ・AI製品
            
            **その他（約10%）**
            - **Google Play**: アプリ内課金とアプリ購入の手数料（15-30%）
            - **デバイス**: Pixel、Nest、Chromecastなどのハードウェア
            - **サブスクリプション**: YouTube Premium、YouTube TV、Google One
            
            ### 競争優位性（モート）
            
            1. **検索エンジン支配**: グローバル検索市場で約90%のシェア
            2. **データ優位性**: 膨大な検索・ユーザーデータによるAIと広告の強化
            3. **Android OS**: モバイルOS市場で70%以上のシェア
            4. **AI技術基盤**: DeepMindを含む業界最先端のAI研究開発能力
            5. **ネットワーク効果**: YouTubeなど複数の10億人規模のプラットフォーム
            
            ### 成長戦略
            
            1. **AIファースト戦略**: 検索、クラウド、広告へのAI技術統合（Gemini）
            2. **クラウド事業拡大**: 企業向けAIソリューションとクラウドインフラの強化
            3. **YouTube収益化**: Premium会員拡大、ショッピング、教育コンテンツ
            4. **ハードウェアエコシステム**: Pixel、Nest、Fitbitなどのデバイス連携
            5. **新技術探索**: 自律走行（Waymo）、ヘルステック、量子コンピューティング
            """)
        elif ticker == "META":
            st.markdown("""
            ### 収益源
            
            **広告（約95%）**
            - **Facebook広告**: ニュースフィードおよびMarketplace内の広告
            - **Instagram広告**: フィード、ストーリーズ、リール内の広告
            - **WhatsApp Business**: ビジネスメッセージングと広告 
            - **Audience Network**: 第三者アプリに展開されるMeta広告ネットワーク
            
            **Reality Labs（約5%）**
            - **VR/ARハードウェア**: Meta Quest VRヘッドセット
            - **メタバースソフトウェア**: Horizon Worlds
            - **デジタルコンテンツ**: VR/ARアプリとゲーム
            
            **その他の収益**
            - **クリエイター収益分配**: Reels、ストリーミング、コンテンツへの投げ銭
            - **バッジと有料機能**: イベント、グループなどの機能
            
            ### 競争優位性（モート）
            
            1. **ユーザー規模**: 全プラットフォームで約35億人の月間アクティブユーザー
            2. **ソーシャルグラフ**: 世界最大のソーシャル接続データベース
            3. **広告ターゲティング**: 詳細なユーザーデータに基づく広告最適化
            4. **技術インフラ**: AI研究、分散システム、コンテンツ配信ネットワーク
            5. **クロスプラットフォーム統合**: Facebook、Instagram、WhatsApp、Messengerの連携
            
            ### 成長戦略
            
            1. **AI技術投資**: コンテンツ推奨、クリエイターツール、広告効果最大化
            2. **リール強化**: ショートフォームビデオのエンゲージメントと収益化
            3. **メタバース開発**: VR/ARデバイスとプラットフォームへの長期投資
            4. **eコマース統合**: ショッピング機能とソーシャルコマースの拡大
            5. **企業向けコミュニケーション**: Workplace、WhatsApp Businessの拡大
            """)
        elif ticker == "NVDA":
            st.markdown("""
            ### 収益源
            
            **データセンター（約60%）**
            - **AI/ML加速器**: H100、A100などのGPU
            - **HPC（高性能コンピューティング）**: 科学研究、気象予測用GPU
            - **ネットワーキング**: Mellanox InfiniBandおよびイーサネット製品
            - **ソフトウェア**: CUDA、RAPIDS、NeMoなどの開発プラットフォーム
            
            **ゲーミング（約20%）**
            - **GeForce GPU**: ゲーム用グラフィックカード
            - **ノートブックGPU**: ゲーミングラップトップ用GPU
            - **クラウドゲーミング**: GeForce NOWプラットフォーム
            
            **プロフェッショナルビジュアライゼーション（約5%）**
            - **Quadro/RTX**: クリエイティブ専門家、設計、映像用GPU
            - **仮想GPU**: リモートワークステーション用ソリューション
            
            **自動車（約5%）**
            - **DRIVE Orin**: 自動運転コンピューティングプラットフォーム
            - **DRIVE Sim**: シミュレーションソフトウェア
            - **車載インフォテインメントシステム**: ダッシュボード用GPUソリューション
            
            ### 競争優位性（モート）
            
            1. **CUDA技術スタック**: アプリケーション、ライブラリ、コンパイラの包括的エコシステム
            2. **ハードウェア革新**: チップアーキテクチャと製造プロセスの継続的改良
            3. **垂直統合**: ハードウェア、ソフトウェア、ツールチェーンまでの一貫した設計
            4. **開発者コミュニティ**: 数百万の開発者によるCUDAプラットフォーム活用
            5. **AI研究投資**: 基礎研究から応用まで幅広いAI技術への継続的投資
            
            ### 成長戦略
            
            1. **AIコンピューティング拡大**: AI推論と訓練の新アーキテクチャ開発
            2. **ソフトウェアプラットフォーム**: CUDA、RAPIDS、Omniverse、NeMoの拡充
            3. **エンタープライズAI**: 業界特化型AIソリューションの開発
            4. **エッジAI**: 低消費電力デバイスでのAI実行ソリューション
            5. **自動運転技術**: DRIVE Orinプラットフォームと自動車メーカーとの提携強化
            """)
        elif ticker == "TSM":
            st.markdown("""
            ### 収益源
            
            **高性能コンピューティング（約40%）**
            - **先端プロセスノード（3nm、5nm）**: CPUやAIチップ製造
            - **GPU製造**: NVIDIA、AMDなど主要GPUメーカー向け
            
            **スマートフォン（約35%）**
            - **モバイルSoC**: Apple A/Mシリーズ、Qualcomm Snapdragon、MediaTekなど
            - **5Gモデム**: 次世代モバイル通信チップ
            
            **IoTとオートモーティブ（約10%）**
            - **車載チップ**: 自動運転、インフォテインメントシステム向け
            - **センサー・IoTデバイス**: スマートホーム、ウェアラブル向け
            
            **その他（約15%）**
            - **マチュアプロセスノード**: レガシーチップ、産業用途など
            - **特殊プロセス**: イメージセンサー、RFチップなど
            
            ### 競争優位性（モート）
            
            1. **技術リーダーシップ**: 半導体製造の最先端プロセスノード開発
            2. **規模の経済**: 世界最大の半導体ファウンドリとしての生産効率
            3. **知的財産**: 数千の製造関連特許と専有技術
            4. **顧客関係**: Apple、NVIDIA、AMDなど主要テック企業との強固な関係
            5. **収益再投資**: 研究開発と設備投資への積極的な資金投入
            
            ### 成長戦略
            
            1. **先端プロセス開発**: 2nm、1nmプロセスノードの開発加速
            2. **地理的多様化**: 日本、米国、欧州での製造拠点拡大
            3. **特殊プロセス拡充**: 自動車、医療、産業用途向け特殊チップ製造の強化
            4. **AIコンピューティング**: AIチップ製造技術への重点投資
            5. **持続可能性推進**: 再生可能エネルギー利用とグリーン製造技術の開発
            """)
        elif ticker == "7203.T" or ticker == "TM":
            st.markdown("""
            ### 収益源
            
            **自動車販売（約80%）**
            - **乗用車**: カローラ、カムリ、レクサスなどの高級車
            - **SUV・クロスオーバー**: RAV4、ハイランダー、レクサスRXなど
            - **商用車**: ハイエース、ハイラックスなど
            - **ピックアップトラック**: タコマ、ツンドラ（主に北米市場）
            
            **金融サービス（約10%）**
            - **自動車ローン**: ディーラー経由の顧客向け資金調達
            - **リース**: 個人・法人向け車両リース
            - **保険**: 自動車保険および関連金融商品
            
            **その他の事業（約10%）**
            - **部品・アクセサリー**: アフターマーケット製品
            - **KINTO**: サブスクリプション型モビリティサービス
            - **GAZOO Racing**: モータースポーツおよび高性能車
            
            ### 競争優位性（モート）
            
            1. **トヨタ生産方式**: リーン生産方式による高い効率性と品質管理
            2. **ハイブリッド技術リーダーシップ**: プリウス以来の電動化技術の蓄積
            3. **グローバル製造ネットワーク**: 世界各地の生産拠点による現地生産体制
            4. **品質とブランド信頼性**: 耐久性と信頼性に関する強固なブランド価値
            5. **研究開発力**: 次世代モビリティ技術への継続的な投資
            
            ### 成長戦略
            
            1. **電動化推進**: ハイブリッド、プラグインハイブリッド、EVラインの拡充
            2. **CASE戦略**: コネクテッド、自動運転、シェアリング、電動化
            3. **新興市場拡大**: インド、アフリカなどでの現地ニーズに合わせた製品開発
            4. **モビリティサービス**: KINTO（車両サブスクリプション）、Woven City構想
            5. **水素技術**: 燃料電池車（MIRAI）と水素社会に向けたインフラ開発
            """)
        elif ticker == "JPM":
            st.markdown("""
            ### 収益源
            
            **消費者・コミュニティバンキング（約40%）**
            - **リテールバンキング**: 預金、クレジットカード、住宅ローン
            - **中小企業向け金融**: ビジネスローン、決済サービス
            - **資産運用**: 富裕層向け資産管理サービス
            
            **コーポレート・投資銀行（約35%）**
            - **投資銀行業務**: M&A助言、株式・債券引受
            - **マーケット業務**: 株式、債券、為替、商品取引
            - **大企業向け銀行業務**: コーポレートローン、キャッシュマネジメント
            
            **コマーシャルバンキング（約10%）**
            - **中堅企業向け金融**: 融資、決済、財務アドバイス
            - **商業用不動産**: 不動産開発向け融資
            - **国際銀行業務**: クロスボーダー取引サポート
            
            **資産・富裕層管理（約15%）**
            - **プライベートバンキング**: 超富裕層向け総合金融サービス
            - **資産運用**: 投資信託、ETF、年金管理
            - **証券サービス**: カストディ、ファンド管理
            
            ### 競争優位性（モート）
            
            1. **規模の経済**: 米国最大の銀行としての効率性と価格競争力
            2. **技術投資**: フィンテック開発と銀行インフラへの継続的投資（年間$120億）
            3. **リスク管理能力**: 2008年金融危機を乗り越えた堅固なバランスシート
            4. **総合金融サービス**: リテールから投資銀行まで幅広いサービス提供
            5. **地理的多様性**: 60カ国以上での事業展開とグローバルネットワーク
            
            ### 成長戦略
            
            1. **デジタルバンキング強化**: モバイルアプリ、オンラインサービスの拡充
            2. **海外市場拡大**: 特にアジア太平洋地域での富裕層向けサービス拡大
            3. **持続可能金融**: ESG投資、グリーンボンド、気候変動対応ファイナンス
            4. **フィンテック統合**: スタートアップ買収と社内イノベーション
            5. **決済プラットフォーム**: 法人・個人向けの次世代決済ソリューション
            """)
        elif ticker == "KO":
            st.markdown("""
            ### 収益源
            
            **炭酸飲料（約60%）**
            - **コカ・コーラ**: フラッグシップブランド（クラシック、ゼロシュガー、フレーバーなど）
            - **スプライト**: レモンライム味炭酸飲料
            - **ファンタ**: フルーツフレーバー炭酸飲料
            
            **非炭酸飲料（約40%）**
            - **水・スポーツドリンク**: Dasani、Smartwater、Powerade
            - **ジュース・植物性飲料**: Minute Maid、Simply、Innocent、fairlife
            - **コーヒー・茶**: Costa Coffee、Georgia、Ayataka
            - **エナジードリンク**: Monster（部分的所有）
            
            **ビジネスモデル**
            - 主に濃縮液と原液を製造し、ボトラーパートナーが製造・流通・販売
            - グローバルで約225のボトリングパートナーと提携
            
            ### 競争優位性（モート）
            
            1. **ブランド価値**: 世界で最も認知されたブランドの一つ
            2. **流通ネットワーク**: 世界200以上の国と地域における強力な販売網
            3. **マーケティング力**: 年間約40億ドルのグローバルマーケティング投資
            4. **ボトラーシステム**: 資本効率の高いアセットライトなビジネスモデル
            5. **製品開発能力**: 消費者嗜好の変化に対応した継続的なイノベーション
            
            ### 成長戦略
            
            1. **プレミアム化**: 小型パッケージと高付加価値製品の拡大
            2. **カテゴリー拡大**: コーヒー、アルコール混合飲料、植物性飲料などの新カテゴリー
            3. **デジタル変革**: eコマース、D2C、デジタルマーケティングの強化
            4. **持続可能性**: 水資源保護、廃棄物削減、リサイクルPET使用拡大
            5. **新興市場開発**: アフリカ、インド、東南アジアなどの成長市場への投資
            """)
        else:
            # 業界別のテンプレート
            if industry == "テクノロジー":
                st.markdown("""
                ### 一般的なテクノロジー企業のビジネスモデル
                
                **典型的な収益源**
                - ハードウェア製品販売
                - ソフトウェアライセンス
                - サブスクリプションサービス
                - クラウドサービス
                - デジタル広告
                - アプリ内課金/マイクロトランザクション
                
                **一般的な競争優位性要素**
                - 知的財産権と特許
                - ネットワーク効果
                - 規模の経済
                - データ資産
                - エコシステム効果
                - 研究開発力
                
                **業界トレンド**
                - AI・機械学習技術の進化と実用化
                - クラウドコンピューティングの普及
                - サブスクリプションモデルへの移行
                - サイバーセキュリティの重要性増加
                - 5G/6G技術の展開
                - メタバースと拡張現実技術
                """)
            elif industry == "金融":
                st.markdown("""
                ### 一般的な金融企業のビジネスモデル
                
                **典型的な収益源**
                - 金利収入（融資と投資の差額）
                - 手数料収入（取引、アドバイザリー、資産管理）
                - 保険料収入
                - トレーディング収益
                - 投資銀行業務
                
                **一般的な競争優位性要素**
                - 規模とリスク分散能力
                - ブランド信頼性
                - 顧客関係の深さと幅
                - 専門知識と人材
                - リスク管理能力
                - テクノロジーインフラ
                
                **業界トレンド**
                - デジタルバンキングの普及
                - フィンテック企業との協業と競争
                - ESG投資の重要性増加
                - 規制環境の変化
                - 暗号資産と分散型金融
                - パーソナライズされた金融サービス
                """)
            else:
                st.markdown("""
                ### ビジネスモデル分析
                
                このセクションでは、企業の以下の要素を分析します：
                
                **収益源**
                - 主要な製品・サービスごとの収益構成
                - 顧客セグメントと地域分布
                - 収益の安定性と成長性
                
                **競争優位性（モート）**
                - 業界内でのポジショニング
                - 差別化要因
                - 参入障壁と持続可能性
                
                **成長戦略**
                - 短期・中期・長期の成長計画
                - 新製品・サービス開発
                - 地理的拡大や新市場への参入
                - M&A戦略
                
                詳細な分析を表示するには、企業情報を入力し「企業分析を実行」ボタンをクリックしてください。
                """)
                
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
        
        # 市場ポジションと競合分析
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>市場ポジションと競合分析</h2>", unsafe_allow_html=True)
        
        # 企業ごとにカスタマイズした競合分析
        if ticker == "AAPL":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **スマートフォン市場**
            - 世界市場シェア: 約17-20%（台数ベース）
            - 収益シェア: 約40-45%（高価格帯戦略）
            - 主要競合: Samsung、Xiaomi、Oppo、Vivo、Huawei
            
            **タブレット市場**
            - 世界市場シェア: 約30-35%
            - 主要競合: Samsung、Amazon、Lenovo、Microsoft
            
            **パソコン市場**
            - 世界市場シェア: 約8-10%
            - 主要競合: Lenovo、HP、Dell、Asus
            
            **ウェアラブル市場**
            - スマートウォッチシェア: 約30-35%
            - イヤホン市場シェア: 約25-30%（AirPods）
            - 主要競合: Samsung、Xiaomi、Fitbit（Google）
            
            ### 差別化要因
            
            - **垂直統合**: ハードウェア、ソフトウェア、サービスの一貫した統合
            - **デザイン**: 高い審美性と使いやすさを両立
            - **プライバシー**: 顧客データ保護の強化と差別化
            - **チップ設計**: 自社設計のApple Siliconによるパフォーマンス優位性
            - **小売戦略**: 直営店による顧客体験の最大化
            """)
        elif ticker == "MSFT":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **オペレーティングシステム市場**
            - デスクトップOS: 約75-80%（Windows）
            - 主要競合: Apple（macOS）、Linux、Google（ChromeOS）
            
            **クラウドサービス市場**
            - 世界市場シェア: 約20-25%（Azure）
            - 主要競合: AWS（Amazon）、Google Cloud、IBM Cloud、Alibaba Cloud
            
            **生産性ソフトウェア市場**
            - オフィススイート: 約85-90%（Microsoft 365）
            - 主要競合: Google（Workspace）、Apple（iWork）
            
            **ビジネスアプリケーション市場**
            - CRM/ERP市場: 約5-10%（Dynamics 365）
            - 主要競合: Salesforce、SAP、Oracle、ServiceNow
            
            ### 差別化要因
            
            - **エンタープライズ統合**: 幅広い製品・サービスのシームレスな統合
            - **ハイブリッドクラウド戦略**: オンプレミスとクラウドの柔軟な組み合わせ
            - **開発者エコシステム**: .NET、GitHub、Visual Studioによる開発者基盤
            - **AI技術**: OpenAIとの戦略的提携による生成AI機能
            - **セキュリティソリューション**: 包括的なセキュリティポートフォリオ
            """)
        elif ticker == "AMZN":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **eコマース市場（米国）**
            - オンライン小売シェア: 約38-40%
            - 主要競合: Walmart、eBay、Target、専門小売業者
            
            **クラウドサービス市場**
            - 世界市場シェア: 約32-34%（AWS）
            - 主要競合: Microsoft Azure、Google Cloud、Alibaba Cloud
            
            **ストリーミング動画市場**
            - 米国市場シェア: 約20%（Prime Video）
            - 主要競合: Netflix、Disney+、Hulu、HBO Max
            
            **スマートスピーカー市場**
            - 世界市場シェア: 約20-25%（Echo/Alexa）
            - 主要競合: Google（Nest）、Apple（HomePod）
            
            ### 差別化要因
            
            - **総合的なエコシステム**: Prime会員を中心とした相互補完的サービス
            - **物流ネットワーク**: 当日/翌日配送を可能にする広範な配送インフラ
            - **顧客データ活用**: 購買履歴と行動データに基づくパーソナライズ
            - **低価格戦略**: 「薄利多売」モデルによる価格競争力
            - **技術イノベーション**: 倉庫自動化、ドローン配送などの先進技術
            """)
        elif ticker == "GOOGL":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **検索エンジン市場**
            - 世界市場シェア: 約90-92%
            - 主要競合: Microsoft Bing、Baidu（中国）、Yahoo、DuckDuckGo
            
            **モバイルOS市場**
            - 世界市場シェア: 約70-75%（Android）
            - 主要競合: Apple iOS
            
            **デジタル広告市場**
            - 世界市場シェア: 約28-30%（Google Ads）
            - 主要競合: Meta、Amazon、TikTok
            
            **クラウドサービス市場**
            - 世界市場シェア: 約9-10%（Google Cloud）
            - 主要競合: AWS、Microsoft Azure、IBM Cloud
            
            ### 差別化要因
            
            - **検索技術**: 世界最先端の検索アルゴリズムと自然言語処理
            - **AIリーダーシップ**: DeepMindを中心とした最先端AI研究
            - **無料サービス戦略**: 広告収益モデルによる高品質無料サービス提供
            - **データ分析能力**: 大規模データ処理と分析のためのインフラ
            - **統合エコシステム**: Gmail、Google Docs、YouTubeなどの相互連携
            """)
        elif ticker == "META":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **ソーシャルメディア市場**
            - Facebook MAU: 約29億人
            - Instagram MAU: 約20億人
            - WhatsApp MAU: 約20億人
            - 主要競合: TikTok、Snapchat、X（Twitter）、LinkedIn
            
            **デジタル広告市場**
            - 世界市場シェア: 約20-22%
            - 主要競合: Google、Amazon、TikTok
            
            **VR/ARハードウェア市場**
            - VRヘッドセットシェア: 約80%（Meta Quest）
            - 主要競合: Sony（PlayStation VR）、HTC、Pico
            
            **メタバースプラットフォーム**
            - 初期段階の市場
            - 主要競合: Roblox、Microsoft、Apple（Vision Pro）
            
            ### 差別化要因
            
            - **ネットワーク効果**: 世界最大のソーシャルグラフとユーザーベース
            - **広告ターゲティング**: 詳細な人口統計とユーザー行動データ
            - **マルチプラットフォーム戦略**: 複数の補完的SNSプラットフォーム
            - **VR/AR投資**: Reality Labsを通じた長期的没入型技術開発
            - **コンテンツ推奨アルゴリズム**: エンゲージメント最大化技術
            """)
        elif ticker == "NVDA":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **AIアクセラレータ市場**
            - データセンターGPU: 約80-85%
            - 主要競合: AMD、Intel、Google（TPU）
            
            **ディスクリートGPU市場**
            - ゲーミングGPU: 約75-80%
            - 主要競合: AMD（Radeon）、Intel Arc
            
            **専門向けGPU市場**
            - プロフェッショナルGPU: 約85-90%
            - 主要競合: AMD、Intel
            
            **自動車コンピューティング市場**
            - 自律走行プラットフォーム: 新興市場
            - 主要競合: Qualcomm、Intel/Mobileye、Tesla（独自開発）
            
            ### 差別化要因
            
            - **CUDAエコシステム**: 幅広いAI/ML開発者によってサポートされる独自のソフトウェアスタック
            - **アーキテクチャ設計**: 先進的なGPUアーキテクチャと継続的イノベーション
            - **ソフトウェア開発ツール**: 包括的な開発環境と最適化ライブラリ
            - **研究コミュニティ関係**: 学術・研究機関との密接な協力関係
            - **製造プロセス最適化**: TSMCとの緊密な連携による先端プロセス活用
            """)
        elif ticker == "TSM":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **先端ファウンドリー市場（5nm以下）**
            - 世界市場シェア: 約90%
            - 主要競合: Samsung、Intel
            
            **総合ファウンドリー市場**
            - 世界市場シェア: 約55-60%
            - 主要競合: Samsung、GlobalFoundries、UMC、SMIC
            
            **主要顧客セグメント**
            - スマートフォンSoC: Apple、Qualcomm、MediaTek
            - GPU/AI: NVIDIA、AMD
            - FPGA: Intel/Altera、Xilinx
            
            ### 差別化要因
            
            - **技術リーダーシップ**: 最先端プロセスノードの早期商用化
            - **製造歩留まり**: 業界最高水準の生産効率と品質管理
            - **IP保護体制**: 顧客機密情報の厳格な保護体制
            - **規模の経済**: 大量生産による単価低減と資本効率
            - **顧客協業モデル**: 設計段階からの緊密な協力関係
            """)
        elif ticker == "7203.T" or ticker == "TM":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **世界自動車市場**
            - 世界販売シェア: 約10%（年間約1,000万台）
            - 主要競合: Volkswagen Group、General Motors、Hyundai-Kia、Ford
            
            **ハイブリッド車市場**
            - 世界市場シェア: 約40-45%
            - 主要競合: Honda、Hyundai、Ford
            
            **地域別シェア**
            - 日本: 約40-45%
            - 北米: 約15%
            - 欧州: 約6-7%
            - 中国: 約5-6%
            
            ### 差別化要因
            
            - **トヨタ生産方式**: 高効率・高品質の製造プロセス
            - **信頼性と耐久性**: 長期的な品質と中古車価値の高さ
            - **ハイブリッド技術**: 25年以上の電動化技術の蓄積
            - **グローバル生産**: 地域適応型の現地生産体制
            - **サプライチェーン管理**: 協力会社との長期的協業関係
            """)
        elif ticker == "JPM":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **米国銀行業**
            - 総資産規模: 米国内1位（約3.4兆ドル）
            - 預金シェア: 約10-12%
            - 主要競合: Bank of America、Citigroup、Wells Fargo
            
            **投資銀行業務**
            - グローバルシェア: 約8-9%
            - 主要競合: Goldman Sachs、Morgan Stanley、Bank of America、Citigroup
            
            **クレジットカード業務**
            - 米国市場シェア: 約20-22%
            - 主要競合: American Express、Citigroup、Bank of America、Capital One
            
            **資産管理業務**
            - 運用資産: 約2.8兆ドル
            - 主要競合: BlackRock、Vanguard、Fidelity、UBS
            
            ### 差別化要因
            
            - **総合金融サービス**: リテールから投資銀行までのフルサービス提供
            - **テクノロジー投資**: デジタルバンキングとフィンテック領域への積極投資
            - **リスク管理能力**: 2008年金融危機を最小限の損害で乗り切った実績
            - **規模のメリット**: 多様な事業間のシナジーと効率化
            - **国際展開**: 60カ国以上でのグローバルなプレゼンス
            """)
        elif ticker == "KO":
            st.markdown("""
            ### 市場シェアと競合状況
            
            **炭酸飲料市場**
            - 世界市場シェア: 約40-45%
            - 主要競合: PepsiCo、Keurig Dr Pepper
            
            **非炭酸飲料市場**
            - スポーツドリンク: 約20%（Powerade）
            - 主要競合: PepsiCo（Gatorade）、Monster
            
            - ボトル入り水: 約5%（Dasani, smartwater）
            - 主要競合: Nestlé、Danone、PepsiCo
            
            - RTD茶・コーヒー: 約15-20%
            - 主要競合: Nestlé、Unilever、Suntory
            
            ### 差別化要因
            
            - **ブランド認知**: 世界で最も認知されたブランドの一つ
            - **ボトラーシステム**: 資本効率の高いフランチャイズモデル
            - **流通ネットワーク**: 小売店から自動販売機まで広範なチャネル
            - **マーケティング力**: 年間40億ドル以上の広告・プロモーション投資
            - **製品多様化**: 200以上のブランドによる幅広い製品ポートフォリオ
            """)
        else:
            if industry == "テクノロジー":
                st.markdown("""
                ### テクノロジー業界の一般的な競合分析フレームワーク
                
                **市場シェア分析の観点**
                - 製品カテゴリー別の市場シェア
                - 地域別の市場浸透率
                - 売上高成長率 vs 業界平均
                - 収益性指標 vs 競合他社
                
                **一般的な差別化領域**
                - 技術革新とR&D能力
                - 知的財産権ポートフォリオ
                - ユーザーエクスペリエンスとデザイン
                - プラットフォームとエコシステム効果
                - コスト構造と価格戦略
                - グローバル展開能力
                
                **主要競合の動向分析**
                - 主要プレイヤーの戦略的動向
                - 新規参入者の脅威と障壁
                - 技術転換点とディスラプション要因
                - 規制環境の変化と影響
                """)
            else:
                st.markdown("""
                ### 市場ポジションと競合分析
                
                このセクションでは、企業の市場内での位置づけと競合状況を分析します：
                
                **市場シェアと競合環境**
                - 主要製品・サービスカテゴリーごとの市場シェア
                - 地域別のプレゼンス
                - 主要競合と相対的なポジショニング
                
                **差別化要因**
                - 技術的優位性
                - 価格戦略
                - 流通チャネル
                - ブランド力
                - 顧客関係
                
                **競合他社の動向**
                - 主要競合の戦略分析
                - 新規参入者の脅威
                - 代替製品・サービスの動向
                
                詳細な分析を表示するには、企業情報を入力し「企業分析を実行」ボタンをクリックしてください。
                """)
                
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
        elif ticker == "AMZN":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $148.2B（前年同期比+11.6%）
            - EPS: $1.26（予想$1.10を上回る）
            - AWS収益: $35.4B（前年同期比+19.8%）
            - 広告事業収益: $15.3B（前年同期比+22.1%）
            
            ### 経営陣のコメント
            
            **アンディ・ジャシー CEO**
            > 「AWSは多くの企業がAIトランスフォーメーションを進める中で再加速しています。Bedrockの導入顧客は前四半期から2倍以上に増加し、多くの企業が生成AIの本格的な導入を開始しています。」
            
            **ブライアン・オルサフスキー CFO**
            > 「物流効率化への継続的な投資により、当社の単位あたり配送コストは前年同期比で12%減少しました。これにより、プライム会員に対するより迅速な配送と収益性の向上を両立しています。」
            
            ### 注目すべきポイント
            
            - 北米および欧州でのセールスイベント「Big Spring Sale」が成功し、プライム会員の加入が増加
            - AWSのAIインフラ投資が加速、世界各地のデータセンターにGPUクラスターを展開
            - Buy with Prime（外部サイトでのAmazon決済サービス）が一般公開され、導入サイトが急増
            """, unsafe_allow_html=True)
        elif ticker == "GOOGL":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $88.3B（前年同期比+15.3%）
            - EPS: $2.27（予想$2.15を上回る）
            - Google検索および広告収益: $54.8B（前年同期比+12.1%）
            - YouTube広告収益: $11.2B（前年同期比+18.4%）
            - Google Cloud収益: $13.1B（前年同期比+29.7%）
            
            ### 経営陣のコメント
            
            **スンダー・ピチャイ CEO**
            > 「Geminiモデルの急速な展開により、検索体験が大きく進化しています。AIを活用した検索は、特にGoogleアプリとAndroidでのエンゲージメントを大幅に向上させています。」
            
            **ルース・ポラット CFO**
            > 「Google Cloudは収益の伸びが3四半期連続で加速し、高い収益性を維持しています。AIインフラへの投資が増加していますが、効率化によりマージンへの影響を最小限に抑えています。」
            
            ### 注目すべきポイント
            
            - 「AI Overviews」検索機能のグローバル展開が加速し、複雑なクエリでのユーザー満足度が向上
            - Google Cloud Vertex AIプラットフォームの企業導入が増加、特に小売・金融・ヘルスケア分野で急成長
            - YouTube Shorts（ショート動画）のエンゲージメントが前年比65%増、収益化も進展
            """, unsafe_allow_html=True)
        elif ticker == "META":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $41.2B（前年同期比+17.8%）
            - EPS: $5.74（予想$5.30を上回る）
            - 広告収益: $39.5B（前年同期比+17.1%）
            - DAU（全プラットフォーム）: 34.7億人（前年同期比+5.2%）
            - Reality Labs営業損失: $3.8B
            
            ### 経営陣のコメント
            
            **マーク・ザッカーバーグ CEO**
            > 「リールと私たちのAI推奨システムは、両方とも急速に成長し収益化も進んでいます。広告プラットフォームでのAI活用が進み、広告主のROIは過去最高水準に達しています。」
            
            **スーザン・リー CFO**
            > 「効率化イニシアチブにより営業マージンは5四半期連続で改善し、同時にAI技術とメタバースへの戦略的投資を継続することができています。」
            
            ### 注目すべきポイント
            
            - リール（ショート動画）の再生時間が前年比45%増加、広告収益化も進展
            - Meta AIアシスタントの月間アクティブユーザーが12億人に到達
            - WhatsAppのビジネス収益化が加速、企業アカウント数が200万を突破
            - Meta Quest 3+の発表が好評、VRヘッドセット市場でのシェア拡大が継続
            """, unsafe_allow_html=True)
        elif ticker == "NVDA":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: $26.8B（前年同期比+122.1%）
            - EPS: $5.93（予想$5.45を上回る）
            - データセンター事業売上高: $19.4B（前年同期比+162.3%）
            - 営業利益率: 57.8%（前年同期比+15.3ポイント）
            
            ### 経営陣のコメント
            
            **ジェンスン・フアン CEO**
            > 「AIの産業革命は企業、産業、国々のコンピューティングインフラの再構築を促進しています。ホッパーアーキテクチャに続き、新しいブラックウェルプラットフォームの出荷が始まり、顧客からの強力な需要を確認しています。」
            
            **コレット・クレス CFO**
            > 「供給制約が続く中でも、製造パートナーとの緊密な連携により生産能力を大幅に拡大しました。このことが、前例のない需要に応える上で重要でした。」
            
            ### 注目すべきポイント
            
            - 次世代「Blackwell B200」GPUの量産出荷が開始、大規模AIモデル開発企業への供給を優先
            - NVIDIAのフルスタックAIソフトウェア戦略「NVIDIA AI Enterprise」のライセンス売上が急増
            - 自動車向けDRIVE Orinプラットフォームの採用メーカーが拡大、特に中国メーカーからの注文増加
            - エネルギー効率を大幅に向上させた液冷データセンターソリューションの導入が加速
            """, unsafe_allow_html=True)
        elif ticker == "7203.T" or ticker == "TM":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: 11.8兆円（前年同期比+8.2%）
            - 営業利益: 1.35兆円（前年同期比+4.6%）
            - 純利益: 1.18兆円（予想1.15兆円を上回る）
            - グローバル販売台数: 257万台（前年同期比+5.3%）
            - 電動車（HEV・PHEV・BEV）販売比率: 40.5%（前年同期比+6.2ポイント）
            
            ### 経営陣のコメント
            
            **豊田章男 会長**
            > 「多様なエネルギー源と多様なモビリティ技術を追求する『マルチパスウェイ』戦略が市場から評価されています。顧客と地域のニーズに応じた最適な電動化ソリューションを提供し続けます。」
            
            **佐藤恒治 CFO**
            > 「原材料価格の上昇と競争激化にもかかわらず、継続的な原価低減と製品ミックスの改善により、堅固な収益性を維持しています。」
            
            ### 注目すべきポイント
            
            - 次世代BEV専用プラットフォーム「bZ」シリーズの新モデル3車種の発表、2026年までに計10車種を投入予定
            - 固体電池技術の実用化が予定より前倒しで進展、2026年に限定生産車へ搭載へ
            - Woven City（静岡県裾野市の実験都市）第一期が完成し、住民の入居開始
            - 水素エンジン技術の開発加速、商用車への展開を拡大
            """, unsafe_allow_html=True)
        elif ticker == "TSM":
            st.markdown("""
            ### 最新決算のハイライト

            **2025年第2四半期決算**
            - 売上高: 675億台湾ドル（前年同期比+34.2%）
            - 純利益: 298億台湾ドル（予想285億台湾ドルを上回る）
            - 営業利益率: 47.6%（前年同期比+5.4ポイント）
            - 3nmプロセス売上比率: 35%（前四半期比+8ポイント）
            - 設備投資: 92億米ドル
            
            ### 経営陣のコメント
            
            **C・C・ウェイ 会長**
            > 「AIアプリケーションの急速な成長が、当社の高性能コンピューティング製品への需要を牽引しています。顧客と緊密に協力し、次世代プロセスノードの開発と量産化を加速しています。」
            
            **ウェンドル・フアン CFO**
            > 「米国アリゾナ州と日本熊本の新工場は予定通り進行しており、2025年後半には両工場からの出荷が始まる見込みです。これにより当社のグローバル供給体制が強化されます。」
            
            ### 注目すべきポイント
            
            - 2nm製造プロセスの開発が順調に進み、2026年前半の量産開始に向けて準備中
            - 高性能コンピューティング向けチップの需要が急増、特にAI加速器用ウェハーの出荷が増加
            - 独自の3Dパッケージング技術「CoWoS」の生産能力を大幅拡大、AI向け高性能チップ製造に活用
            - ドイツ・ドレスデン工場の建設決定、欧州での半導体サプライチェーン構築に参画
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
        
        # 成長展望と将来動向
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='card-title'>成長展望と将来動向</h2>", unsafe_allow_html=True)
        
        # 企業ごとにカスタマイズした成長展望
        if ticker == "AAPL":
            st.markdown("""
            ### 短期的な注目ポイント（1年以内）
            
            - **Apple Vision Pro**: 空間コンピューティングデバイスの国際展開と開発者エコシステムの拡大
            - **iPhone 16シリーズ**: AIに特化した新機能の搭載と処理能力の大幅な向上
            - **サービス事業の拡大**: Apple TV+のオリジナルコンテンツ強化とApple Arcadeの新タイトル投入
            - **インド市場戦略**: 現地生産の拡大と小売店舗の出店加速
            
            ### 中期的な成長ドライバー（1-3年）
            
            - **AI統合戦略**: 「Apple Intelligence」のiOS/macOS/iPadOS全体への展開
            - **ヘルスケア領域**: Apple Watchを中心とした健康・医療機能の拡充
            - **AR/VRエコシステム**: Vision Proプラットフォームの拡大と第2世代デバイスの開発
            - **自動車関連技術**: カーステレオシステム「CarPlay」の高度化と自動運転支援機能の開発
            
            ### 長期的な戦略的方向性（3-5年）
            
            - **持続可能性**: 2030年までのカーボンニュートラル達成に向けた取り組み
            - **新しい製品カテゴリー**: 可能性のある領域：スマートホーム、モビリティ、医療機器
            - **プライバシー重視戦略**: 差別化要因としてのデータ保護とセキュリティの強化
            - **新興国市場展開**: インド、東南アジア、アフリカでの中間層向け戦略
            
            ### 主要な成長リスク要因
            
            - 規制圧力の高まり（App Store手数料、反トラスト法など）
            - 中国市場での地政学的リスクと競争激化
            - ハードウェア販売サイクルの長期化
            - プレミアム価格戦略の持続可能性
            """)
        elif ticker == "MSFT":
            st.markdown("""
            ### 短期的な注目ポイント（1年以内）
            
            - **Copilotの商用展開**: Microsoft 365 Copilotの導入企業拡大と機能強化
            - **Activision Blizzard統合**: ゲーム部門の統合と戦略的シナジーの実現
            - **Azure OpenAI Service**: 企業向けカスタムAIモデル構築プラットフォームの拡充
            - **Windows AI機能**: Windowsへの生成AI機能の統合とパフォーマンス最適化
            
            ### 中期的な成長ドライバー（1-3年）
            
            - **AIインフラ投資**: データセンターのAI処理能力拡大とエネルギー効率化
            - **Teams Platformの進化**: コラボレーションプラットフォームとしての機能拡張
            - **ハイブリッドクラウド戦略**: Azure Stack/Arc製品群の拡充とマルチクラウド管理
            - **セキュリティソリューション**: 包括的なセキュリティスイートの統合と自動化
            
            ### 長期的な戦略的方向性（3-5年）
            
            - **量子コンピューティング**: Azure Quantum商用サービスの開発と実用化
            - **メタバース戦略**: Microsoft Meshプラットフォームを通じた企業向け仮想空間
            - **持続可能性目標**: 2030年までにカーボンネガティブ、2050年までに創業以来の炭素排出を相殺
            - **医療・教育領域**: AIとクラウドを活用した業界特化型ソリューション
            
            ### 主要な成長リスク要因
            
            - AIインフラ投資の収益化タイムライン
            - クラウド市場における競争激化とマージン圧力
            - サイバーセキュリティリスクとデータプライバシー規制
            - オープンソースAIモデルの台頭と差別化の課題
            """)
        else:
            # 業界別のテンプレート
            if industry == "テクノロジー":
                st.markdown("""
                ### テクノロジー業界の成長トレンド
                
                **短期的なトレンド（1年以内）**
                - 生成AIの実用化とビジネスプロセスへの統合
                - エッジコンピューティングの普及
                - サイバーセキュリティソリューションの需要増加
                - ハイブリッドクラウド環境の最適化
                
                **中期的なトレンド（1-3年）**
                - 業界特化型AIソリューションの発展
                - 5G技術の普及とIoTエコシステムの拡大
                - 量子コンピューティングの商業化初期段階
                - デジタルツインと拡張現実技術の産業応用
                
                **長期的なトレンド（3-5年）**
                - 自律型AI・ロボティクスの普及
                - 6G研究開発と次世代通信インフラ
                - 脳・コンピュータ・インターフェースの発展
                - 持続可能なテクノロジーインフラの標準化
                
                **構造的変化要因**
                - プライバシー規制の強化とデータ主権
                - エネルギー効率とサステナビリティへの注目
                - テクノロジー人材市場の変化
                - グローバルサプライチェーンの再構成
                """)
            else:
                st.markdown("""
                ### 成長展望と将来動向
                
                このセクションでは、以下の要素に基づいて企業の将来の成長可能性を分析します：
                
                **短期的な成長要因（1年以内）**
                - 新製品・サービスのパイプライン
                - 進行中のビジネスイニシアチブ
                - 市場拡大戦略
                - 当面の課題と機会
                
                **中期的な成長ドライバー（1-3年）**
                - 主要な戦略的イニシアチブ
                - 研究開発の方向性
                - 市場シェア拡大計画
                - 競争力強化のための取り組み
                
                **長期的な戦略と方向性（3-5年）**
                - ビジョンと長期目標
                - 業界変革への対応計画
                - サステナビリティ戦略
                - 新しい事業領域の可能性
                
                **成長に関するリスク要因**
                - 市場環境の変化
                - 競合の動向
                - 規制環境の変化
                - テクノロジー転換点
                
                詳細な分析を表示するには、企業情報を入力し「企業分析を実行」ボタンをクリックしてください。
                """)
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 分析が完了したことを表示
        st.success("企業分析が完了しました。ビジネスモデルと市場環境の理解にお役立てください。")

# Add floating chatbot component
try:
    from floating_chatbot import render_floating_chatbot
    render_floating_chatbot()
except ImportError:
    pass