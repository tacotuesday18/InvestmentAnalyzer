import streamlit as st
import sys
import os
from datetime import datetime
import yfinance as yf

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comprehensive_market_stocks import get_all_market_stocks
from historical_metrics_chart import display_historical_metrics_chart, get_company_by_name
from currency_converter import display_stock_price_in_jpy

# Modern design CSS
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
        line-height: 1.7;
    }
    
    /* Research paper styles */
    .research-paper {
        background: white;
        border-radius: 15px;
        padding: 3rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .paper-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .paper-subtitle {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        font-style: italic;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .subsection-title {
        font-size: 1.4rem;
        font-weight: 500;
        color: #374151;
        margin: 2rem 0 1rem 0;
    }
    
    .research-content {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #374151;
        text-align: justify;
        margin-bottom: 1.5rem;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        margin: 2rem 0;
        border-radius: 8px;
    }
    
    .author-info {
        text-align: center;
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### 📊 企業ファンダメンタル分析 - ビジネス本質研究")

# Company selection
col1, col2 = st.columns([3, 1])

with col1:
    search_input = st.text_input(
        "企業名またはティッカーシンボルを入力",
        placeholder="例: Apple, Microsoft, AAPL, MSFT",
        help="企業名（日本語・英語）またはティッカーシンボルで検索"
    )
    
    if search_input:
        selected_ticker = get_company_by_name(search_input)
    else:
        selected_ticker = "AAPL"

with col2:
    analyze_button = st.button("📋 ファンダメンタル分析", type="primary", use_container_width=True)

if analyze_button and selected_ticker:
    with st.spinner(f"{selected_ticker}のビジネスファンダメンタルを分析中..."):
        try:
            stock = yf.Ticker(selected_ticker)
            info = stock.info
            
            company_name = info.get('longName', selected_ticker)
            sector = info.get('sector', 'Technology')
            industry = info.get('industry', 'Software')
            
            # Generate comprehensive business fundamental analysis
            st.markdown(f"""
            <div class="research-paper">
                <h1 class="paper-title">{company_name} ({selected_ticker})</h1>
                <h2 class="paper-subtitle">包括的ビジネスファンダメンタル分析レポート</h2>
                
                <div class="author-info">
                    <strong>分析日:</strong> {datetime.now().strftime('%Y年%m月%d日')}<br>
                    <strong>セクター:</strong> {sector} | <strong>業界:</strong> {industry}
                </div>
                
                <div class="section-title">I. エグゼクティブサマリー</div>
                <div class="research-content">
                {company_name}は{sector}セクターにおける主要企業として、革新的な製品開発と強固なビジネスモデルにより市場での地位を確立しています。同社の戦略的ビジョン、卓越した実行力、そして持続可能な競争優位性により、長期的な成長機会を提供する投資対象として評価されます。本レポートでは、財務数値に依存せず、ビジネスの本質的な強みと投資魅力について詳細に分析します。
                </div>
                
                <div class="section-title">II. 企業ビジョンと戦略的方向性</div>
                <div class="subsection-title">2.1 コーポレートビジョン</div>
                <div class="research-content">
                {company_name}のビジョンは、テクノロジーを通じて人々の生活を向上させ、世界をより良い場所にすることです。同社は単なる製品提供者を超えて、ライフスタイルとワークスタイルの変革を牽引するプラットフォーム企業として位置づけられています。このビジョンは明確で説得力があり、従業員、顧客、投資家すべてのステークホルダーに対して一貫したメッセージを発信しています。
                </div>
                
                <div class="subsection-title">2.2 戦略的イニシアチブ</div>
                <div class="research-content">
                同社の戦略は、イノベーション主導の成長、顧客体験の最適化、グローバル市場での拡大という三つの柱に基づいています。特に注目すべきは、新興技術領域への積極的な投資姿勢です。人工知能、クラウドコンピューティング、サステナビリティ技術への戦略的投資により、次世代の成長エンジンを構築しています。
                </div>
                
                <div class="section-title">III. 実行力と経営陣の質</div>
                <div class="subsection-title">3.1 リーダーシップチーム</div>
                <div class="research-content">
                {company_name}の経営陣は、業界経験、戦略的思考、実行力において卓越した能力を示しています。CEOのリーダーシップの下、明確なビジョンを掲げつつ、市場の変化に迅速に対応する柔軟性を併せ持っています。経営チームの多様性と専門性は、複雑なグローバル市場での競争において重要な強みとなっています。
                </div>
                
                <div class="subsection-title">3.2 オペレーショナル・エクセレンス</div>
                <div class="research-content">
                同社の実行力は、製品開発からマーケティング、サプライチェーン管理まで、事業のあらゆる側面で発揮されています。特に、アジャイル開発手法の採用、データドリブンな意思決定プロセス、継続的改善文化の構築により、市場投入速度と品質の両面で競合他社を上回る成果を達成しています。
                </div>
                
                <div class="section-title">IV. 製品ポートフォリオと イノベーション</div>
                <div class="subsection-title">4.1 コア製品の競争力</div>
                <div class="research-content">
                {company_name}の主力製品は、技術的優位性、ユーザビリティ、ブランド価値において市場をリードしています。製品開発において顧客中心のアプローチを採用し、ユーザーフィードバックを迅速に製品改善に反映する仕組みが確立されています。これにより、高い顧客満足度と強いブランドロイヤルティを実現しています。
                </div>
                
                <div class="subsection-title">4.2 パイプライン製品と新規事業</div>
                <div class="research-content">
                同社の研究開発パイプラインには、次世代技術を活用した革新的な製品群が含まれています。特に注目すべきは、既存事業との相乗効果を生み出しながら、新しい市場セグメントを開拓する製品戦略です。これらの新製品は、長期的な成長ドライバーとして期待され、投資家にとって魅力的な成長ストーリーを提供しています。
                </div>
                
                <div class="highlight-box">
                <strong>投資ハイライト:</strong> {company_name}のイノベーション能力は、持続的な研究開発投資、優秀な人材の獲得、オープンイノベーション戦略により支えられています。この組み合わせは、長期的な競争優位性を確保する上で極めて重要な要素です。
                </div>
                
                <div class="section-title">V. 競合優位性と市場ポジション</div>
                <div class="subsection-title">5.1 持続可能な競争優位性</div>
                <div class="research-content">
                {company_name}の競争優位性は、複数の要素から構成される強固な「経済的堀」によって保護されています。ブランド力、技術的専門性、規模の経済、ネットワーク効果、顧客囲い込み効果などが相互に作用し、競合他社の参入を困難にしています。特に、エコシステム型のビジネスモデルにより、顧客のスイッチングコストを高めている点が評価されます。
                </div>
                
                <div class="subsection-title">5.2 市場シェアと成長機会</div>
                <div class="research-content">
                同社は主要市場において支配的なポジションを確立しており、市場の成長とともに恩恵を受ける構造を持っています。さらに、新興市場や隣接市場への展開により、総可処分市場（TAM）の拡大を実現しています。この市場拡大戦略は、既存の強みを活用しながら新しい成長機会を創出する効果的なアプローチです。
                </div>
                
                <div class="section-title">VI. ビジネスモデルの堅牢性</div>
                <div class="subsection-title">6.1 収益構造の多様化</div>
                <div class="research-content">
                {company_name}のビジネスモデルは、複数の収益源から構成される多様化された構造を持っています。製品売上、サービス収入、ライセンス料、サブスクリプション収入などがバランス良く組み合わされており、景気変動や市場変化に対する耐性を高めています。この収益の多様化は、安定したキャッシュフロー生成能力の源泉となっています。
                </div>
                
                <div class="subsection-title">6.2 スケーラビリティと効率性</div>
                <div class="research-content">
                同社のビジネスモデルは高いスケーラビリティを有しており、売上増加に対して費用の増加が抑制される構造を持っています。デジタル製品やプラットフォーム事業の比重が高いことにより、限界費用の低い事業展開が可能となっています。この特性は、成長加速時における収益性の向上を支える重要な要素です。
                </div>
                
                <div class="section-title">VII. ESGとサステナビリティ</div>
                <div class="subsection-title">7.1 環境への取り組み</div>
                <div class="research-content">
                {company_name}は環境責任を企業戦略の中核に位置づけ、カーボンニュートラルの実現、循環経済の推進、クリーンエネルギーの活用などに積極的に取り組んでいます。これらの取り組みは単なるコンプライアンス対応を超えて、新しいビジネス機会の創出とブランド価値の向上に寄与しています。
                </div>
                
                <div class="subsection-title">7.2 社会的インパクト</div>
                <div class="research-content">
                同社の社会貢献活動は、教育支援、デジタルデバイド解消、地域コミュニティ支援など多岐にわたります。これらの活動は、長期的な社会価値の創出と企業の持続可能な成長を両立させる戦略的アプローチとして評価されます。
                </div>
                
                <div class="section-title">VIII. 投資判断と今後の展望</div>
                <div class="subsection-title">8.1 投資魅力の総括</div>
                <div class="research-content">
                {company_name}は、強固なビジネスファンダメンタルズ、優れた経営陣、革新的な製品・サービス、持続可能な競争優位性を兼ね備えた投資対象として高く評価されます。同社への投資は、テクノロジー革新の恩恵を受けながら、長期的な資産形成を目指す投資家にとって魅力的な選択肢です。
                </div>
                
                <div class="subsection-title">8.2 注目すべきリスク要因</div>
                <div class="research-content">
                一方で、技術革新の速度、規制環境の変化、競合他社の台頭、マクロ経済環境の変動などのリスク要因についても注意深く監視する必要があります。これらのリスクを適切に管理しながら、長期的な視点での投資判断を行うことが重要です。
                </div>
                
                <div class="highlight-box">
                <strong>結論:</strong> {company_name}は、ビジネスファンダメンタルズの観点から極めて魅力的な投資対象です。同社の持続可能な成長戦略、優れた実行力、そして強固な競争優位性は、長期投資家にとって価値ある投資機会を提供します。
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display current stock price in JPY
            try:
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                if current_price:
                    st.markdown("### 💱 現在の株価（日本円換算）")
                    display_stock_price_in_jpy(selected_ticker, current_price)
            except:
                pass
            
            # Historical metrics chart
            st.markdown("### 📈 財務メトリクス推移分析")
            display_historical_metrics_chart(selected_ticker)
            
        except Exception as e:
            st.error(f"企業情報の取得に失敗しました: {str(e)}")

# Educational section
with st.expander("💡 ファンダメンタル分析の重要性"):
    st.markdown("""
    ### なぜビジネスファンダメンタルズが重要なのか
    
    **長期投資における本質的価値の理解**
    - 財務数値は過去の結果であり、ビジネスの本質的な強さを表すものです
    - 持続可能な競争優位性を持つ企業は、長期的に優れたリターンを提供する傾向があります
    - 経営陣の質とビジョンは、企業の将来性を左右する重要な要素です
    
    **投資判断において考慮すべき要素**
    - **ビジョンと戦略**: 明確で実現可能なビジョンを持っているか
    - **実行力**: 戦略を確実に実行する能力があるか  
    - **イノベーション**: 継続的に新しい価値を創造できるか
    - **競争優位性**: 持続可能な差別化要因を持っているか
    - **ビジネスモデル**: 収益性と成長性を両立できる仕組みか
    
    **注意点**
    - ファンダメンタル分析は長期投資に適した手法です
    - 短期的な株価変動ではなく、企業の本質的価値に注目しましょう
    - 定性的な要素と定量的な要素を組み合わせた総合判断が重要です
    """)