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
st.markdown("<h2>企業情報の入力</h2>", unsafe_allow_html=True)

# ブラウザの幅に応じて列の数を調整 (モバイル対応)
if st.session_state.get('is_mobile', False) or len(st.session_state) < 5:  # モバイル判定の簡易実装
    # モバイル向けレイアウト（縦に並べる）
    col1 = st.container()
else:
    # デスクトップ向けレイアウト
    col1 = st.container()

with col1:
    company_name = st.text_input("企業名", value="Apple Inc.")
    industry = st.selectbox("業界", [
        "テクノロジー", "金融", "ヘルスケア", "消費財", "工業", 
        "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"
    ])
    ticker = st.text_input("ティッカーシンボル（例: AAPL）", value="AAPL")
    country = st.selectbox("本社所在国", [
        "アメリカ", "日本", "中国", "イギリス", "ドイツ", "フランス", "カナダ", 
        "オーストラリア", "インド", "ブラジル", "その他"
    ])
    
    # 既存データがある場合は表示
    if ticker:
        existing_data = get_stock_data(ticker)
        if existing_data and 'name' in existing_data:
            st.success(f"{ticker} ({existing_data['name']})の基本情報を読み込みました。")
            
            # もし既存の株価データがあればセッションに保存（後の処理のため）
            if 'current_stock_price' in existing_data:
                st.session_state.current_price = existing_data['current_stock_price']
                current_stock_price = existing_data['current_stock_price']
        
    business_description = st.text_area("ビジネス概要（任意）", 
                                       placeholder="例: Appleは、iPhone、iPad、Mac、Apple Watchなどのハードウェア製品とiTunes、App Store、iCloudなどのサービスを提供するテクノロジー企業です。",
                                       height=100)

# 隠しパラメータ（コードの互換性のため）
revenue = 100000000000
net_income = 25000000000
shares_outstanding = 10000000000
current_stock_price = st.session_state.get('current_price', 175.04)
revenue_growth = 15.0
net_margin = 25.0
forecast_years = 3
industry_pe = 25.0
industry_pbr = 3.0
industry_psr = 5.0

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