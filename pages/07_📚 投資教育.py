import streamlit as st
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from currency_converter import display_currency_converter, get_historical_usd_jpy_chart, display_investment_impact_calculator

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
    .education-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }
    
    .lesson-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1a202c;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .concept-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .example-box {
        background: #f0f9ff;
        border: 1px solid #0ea5e9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fef3cd;
        border: 1px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #dcfce7;
        border: 1px solid #22c55e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .nav-tabs {
        display: flex;
        margin-bottom: 2rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .nav-tab {
        padding: 1rem 2rem;
        background: none;
        border: none;
        font-size: 1rem;
        font-weight: 500;
        color: #6b7280;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .nav-tab.active {
        color: #667eea;
        border-bottom-color: #667eea;
    }
    
    .metric-explanation {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    .formula-box {
        background: #1f2937;
        color: #f9fafb;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">📚 投資教育センター</div>
    <div class="page-subtitle">プラットフォームの使い方と投資の基礎知識を学ぼう</div>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 プラットフォーム入門", 
    "📊 財務指標の理解", 
    "💰 DCF法とバリュエーション", 
    "💱 為替と投資", 
    "📈 投資戦略の構築"
])

with tab1:
    st.markdown('<div class="education-card">', unsafe_allow_html=True)
    st.markdown('<div class="lesson-header">プラットフォームの使い方</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 このプラットフォームでできること
    
    当プラットフォームは、日本の個人投資家向けに設計された包括的な株式分析ツールです。
    Yahoo Financeからの最新データを使用し、プロレベルの企業分析を提供します。
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h4>📊 ビジネスモデル分析</h4>
        <p>企業の本質的な強みと成長ポテンシャルを深く理解できます。数値だけでなく、ビジネスの質的な側面に焦点を当てた分析レポートを生成します。</p>
        <ul>
        <li>企業の競争優位性の評価</li>
        <li>経営陣の質と戦略の妥当性</li>
        <li>持続可能な成長の可能性</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>📈 財務諸表分析</h4>
        <p>企業の財務健全性と収益性を詳細に分析します。過去のトレンドから将来の業績を予測するための洞察を提供します。</p>
        <ul>
        <li>損益計算書、貸借対照表の分析</li>
        <li>キャッシュフロー計算書の評価</li>
        <li>財務健全性スコアの算出</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-box">
        <h4>💰 DCF価値計算機</h4>
        <p>企業の本質的価値を科学的に算出します。将来のキャッシュフローを現在価値に割り引くことで、適正株価を計算します。</p>
        <ul>
        <li>将来キャッシュフローの予測</li>
        <li>適切な割引率の設定</li>
        <li>感度分析による価値の検証</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>🔍 銘柄発見ツール</h4>
        <p>投資スタイルに合った優良銘柄を発見できます。成長株、バリュー株、配当株など、様々な投資戦略に対応したスクリーニング機能を提供します。</p>
        <ul>
        <li>投資スタイル別プリセット</li>
        <li>カスタム条件でのスクリーニング</li>
        <li>リアルタイムデータでの評価</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
    <h4>💡 効果的な使い方のヒント</h4>
    <ol>
    <li><strong>まず銘柄発見ツールで候補を絞り込み</strong>: 投資スタイルに合った銘柄を見つけましょう</li>
    <li><strong>ビジネスモデル分析で質的評価</strong>: 企業の本質的な強みを理解しましょう</li>
    <li><strong>財務諸表で健全性確認</strong>: 数値面での安全性を検証しましょう</li>
    <li><strong>DCF計算機で適正価格算出</strong>: 現在の株価が割安か割高かを判断しましょう</li>
    <li><strong>決算分析で最新動向把握</strong>: 企業の直近の業績とトレンドを確認しましょう</li>
    </ol>
    </div>
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="education-card">', unsafe_allow_html=True)
    st.markdown('<div class="lesson-header">重要な財務指標の理解</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-explanation">
        <h4>PER（株価収益率）</h4>
        <div class="formula-box">PER = 株価 ÷ 1株あたり利益(EPS)</div>
        <p><strong>意味</strong>: 企業の利益に対して株価がどの程度の水準にあるかを示す指標</p>
        <p><strong>目安</strong>:</p>
        <ul>
        <li>10-15倍: 割安水準</li>
        <li>15-25倍: 適正水準</li>
        <li>25倍以上: 割高水準（成長企業は例外）</li>
        </ul>
        </div>
        
        <div class="metric-explanation">
        <h4>PBR（株価純資産倍率）</h4>
        <div class="formula-box">PBR = 株価 ÷ 1株あたり純資産(BPS)</div>
        <p><strong>意味</strong>: 企業の純資産に対する株価の水準を示す</p>
        <p><strong>目安</strong>:</p>
        <ul>
        <li>1倍未満: 割安（ただし業績悪化の可能性も）</li>
        <li>1-3倍: 適正水準</li>
        <li>3倍以上: 割高（成長企業は例外）</li>
        </ul>
        </div>
        
        <div class="metric-explanation">
        <h4>ROE（自己資本利益率）</h4>
        <div class="formula-box">ROE = 純利益 ÷ 自己資本 × 100</div>
        <p><strong>意味</strong>: 企業が株主資本をどれだけ効率的に活用して利益を生み出しているか</p>
        <p><strong>目安</strong>:</p>
        <ul>
        <li>15%以上: 優秀</li>
        <li>10-15%: 良好</li>
        <li>10%未満: 要改善</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-explanation">
        <h4>PSR（株価売上高倍率）</h4>
        <div class="formula-box">PSR = 時価総額 ÷ 売上高</div>
        <p><strong>意味</strong>: 企業の売上高に対する株価の水準を示す</p>
        <p><strong>特徴</strong>:</p>
        <ul>
        <li>赤字企業でも評価可能</li>
        <li>売上操作が利益操作より困難</li>
        <li>成長企業の評価に適している</li>
        </ul>
        </div>
        
        <div class="metric-explanation">
        <h4>PEG レシオ</h4>
        <div class="formula-box">PEG = PER ÷ 利益成長率</div>
        <p><strong>意味</strong>: 企業の成長率を考慮した株価の割安・割高を判断</p>
        <p><strong>目安</strong>:</p>
        <ul>
        <li>1.0未満: 割安</li>
        <li>1.0-1.5: 適正</li>
        <li>1.5以上: 割高</li>
        </ul>
        </div>
        
        <div class="metric-explanation">
        <h4>配当利回り</h4>
        <div class="formula-box">配当利回り = 年間配当金 ÷ 株価 × 100</div>
        <p><strong>意味</strong>: 投資額に対する年間配当収入の割合</p>
        <p><strong>日本市場の目安</strong>:</p>
        <ul>
        <li>3%以上: 高配当</li>
        <li>2-3%: 標準的</li>
        <li>2%未満: 低配当（成長重視企業に多い）</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
    <h4>⚠️ 財務指標を見る際の注意点</h4>
    <ul>
    <li><strong>業界比較が重要</strong>: 指標は同業他社と比較して評価しましょう</li>
    <li><strong>トレンドを重視</strong>: 単年の数値ではなく、過去数年の推移を確認しましょう</li>
    <li><strong>複数指標で総合判断</strong>: 一つの指標だけでなく、複数の指標を組み合わせて評価しましょう</li>
    <li><strong>定性要因も考慮</strong>: 数値だけでなく、企業の戦略や市場環境も考慮しましょう</li>
    </ul>
    </div>
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="education-card">', unsafe_allow_html=True)
    st.markdown('<div class="lesson-header">DCF法による企業価値評価</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 💰 DCF法とは？
    
    DCF（Discounted Cash Flow）法は、企業が将来生み出すキャッシュフローを現在価値に割り引いて、
    企業の本質的価値を算出する手法です。Warren Buffettなど著名投資家も使用する、
    最も理論的に正しいとされる企業価値評価手法です。
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h4>DCF法の基本概念</h4>
        <div class="formula-box">
        企業価値 = Σ(将来キャッシュフロー ÷ (1+割引率)^年数)
        </div>
        <p>これは「今日の100万円と1年後の100万円では価値が異なる」という<strong>貨幣の時間価値</strong>の概念に基づいています。</p>
        
        <h5>主要なステップ:</h5>
        <ol>
        <li><strong>売上高成長率の予測</strong></li>
        <li><strong>利益率の予測</strong></li>
        <li><strong>適切な割引率の設定</strong></li>
        <li><strong>終末価値の算出</strong></li>
        <li><strong>現在価値への割引</strong></li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
        <h4>💡 例: A社のDCF分析</h4>
        <p><strong>前提条件:</strong></p>
        <ul>
        <li>現在の売上: 1000億円</li>
        <li>予想成長率: 年10%</li>
        <li>純利益率: 15%</li>
        <li>割引率: 8%</li>
        <li>予測期間: 5年</li>
        </ul>
        
        <p><strong>計算結果:</strong></p>
        <ul>
        <li>5年後の売上: 1610億円</li>
        <li>5年後の純利益: 242億円</li>
        <li>現在価値: 165億円</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-box">
        <h4>重要なパラメータの設定</h4>
        
        <h5>🎯 売上高成長率</h5>
        <ul>
        <li>過去の実績を参考に設定</li>
        <li>業界の成長率を考慮</li>
        <li>企業の戦略と市場環境を評価</li>
        </ul>
        
        <h5>💹 割引率（WACC）</h5>
        <ul>
        <li>企業のリスクを反映</li>
        <li>一般的に8-12%程度</li>
        <li>業界やビジネスモデルにより調整</li>
        </ul>
        
        <h5>🏁 終末価値</h5>
        <ul>
        <li>予測期間終了後の企業価値</li>
        <li>業界平均PERやPBRを使用</li>
        <li>永続成長率モデルも使用可能</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ DCF法の限界と注意点</h4>
        <ul>
        <li><strong>予測の不確実性</strong>: 将来の業績予測は困難</li>
        <li><strong>パラメータの敏感性</strong>: 少しの変更で結果が大きく変わる</li>
        <li><strong>定性要因の無視</strong>: ブランド価値や技術力などは反映されにくい</li>
        <li><strong>市場の非効率性</strong>: 理論価格と市場価格は常に一致するわけではない</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
    <h4>🚀 DCF分析を効果的に活用するコツ</h4>
    <ol>
    <li><strong>感度分析を実施</strong>: 成長率や割引率を変更して価値のレンジを把握</li>
    <li><strong>複数シナリオで検証</strong>: 楽観、中立、悲観の3シナリオで分析</li>
    <li><strong>他の評価手法と組み合わせ</strong>: PERやPBRなどの相対評価と併用</li>
    <li><strong>定期的な見直し</strong>: 新しい情報に基づいて定期的に更新</li>
    </ol>
    </div>
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="education-card">', unsafe_allow_html=True)
    st.markdown('<div class="lesson-header">為替と海外投資の関係</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 💱 なぜ為替レートが重要なのか？
    
    日本の投資家がアメリカ株に投資する場合、**株価の変動**と**為替レートの変動**の両方が
    投資リターンに影響します。これを理解することは、海外投資で成功するために不可欠です。
    """)
    
    # Currency converter component
    display_currency_converter()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h4>為替リスクの基本</h4>
        
        <h5>📈 円安の場合（例: 120円→140円）</h5>
        <ul>
        <li><strong>プラス効果</strong>: 保有するドル建て資産の円換算価値が上昇</li>
        <li><strong>マイナス効果</strong>: 新規投資時により多くの円が必要</li>
        </ul>
        
        <h5>📉 円高の場合（例: 140円→120円）</h5>
        <ul>
        <li><strong>プラス効果</strong>: 新規投資時に必要な円が少なくて済む</li>
        <li><strong>マイナス効果</strong>: 保有するドル建て資産の円換算価値が減少</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
        <h4>💡 実例: Apple株への投資</h4>
        <p><strong>シナリオ1: 円安が進行した場合</strong></p>
        <ul>
        <li>投資時: Apple $150、1ドル=130円 → 19,500円</li>
        <li>1年後: Apple $150、1ドル=150円 → 22,500円</li>
        <li>株価変動: 0%、為替利益: +15.4%、<strong>総リターン: +15.4%</strong></li>
        </ul>
        
        <p><strong>シナリオ2: 円高が進行した場合</strong></p>
        <ul>
        <li>投資時: Apple $150、1ドル=130円 → 19,500円</li>
        <li>1年後: Apple $150、1ドル=110円 → 16,500円</li>
        <li>株価変動: 0%、為替損失: -15.4%、<strong>総リターン: -15.4%</strong></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-box">
        <h4>為替リスクへの対処法</h4>
        
        <h5>🎯 分散投資戦略</h5>
        <ul>
        <li><strong>時間分散</strong>: ドルコスト平均法で定期積立</li>
        <li><strong>通貨分散</strong>: 円建て資産と外貨建て資産のバランス</li>
        <li><strong>地域分散</strong>: 米国以外の市場への投資も検討</li>
        </ul>
        
        <h5>🛡️ ヘッジ戦略</h5>
        <ul>
        <li><strong>為替ヘッジ型ETF</strong>: 為替変動をヘッジした商品</li>
        <li><strong>通貨ペアの活用</strong>: USD/JPYの先物やオプション</li>
        <li><strong>自然ヘッジ</strong>: 輸出関連の日本株との組み合わせ</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ 為替投資の注意点</h4>
        <ul>
        <li><strong>予測の困難性</strong>: 為替レートの予測は非常に困難</li>
        <li><strong>ボラティリティ</strong>: 為替変動は株価以上に大きい場合がある</li>
        <li><strong>金利差の影響</strong>: 日米金利差が為替に大きく影響</li>
        <li><strong>地政学リスク</strong>: 国際情勢が為替に与える影響</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment impact calculator
    display_investment_impact_calculator()
    
    # Historical USD/JPY chart
    usd_jpy_chart = get_historical_usd_jpy_chart()
    if usd_jpy_chart:
        st.markdown("### 📊 USD/JPY 為替レート推移")
        st.plotly_chart(usd_jpy_chart, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="education-card">', unsafe_allow_html=True)
    st.markdown('<div class="lesson-header">投資戦略の構築</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 自分に適した投資戦略を見つけよう
    
    投資で成功するためには、自分のリスク許容度、投資期間、資金状況に合った戦略を選択することが重要です。
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h4>📈 成長株投資（グロース投資）</h4>
        <p><strong>特徴:</strong> 高い成長率を持つ企業への投資</p>
        
        <h5>向いている人:</h5>
        <ul>
        <li>長期投資を前提とできる</li>
        <li>価格変動に耐えられる</li>
        <li>高いリターンを求める</li>
        </ul>
        
        <h5>選定基準:</h5>
        <ul>
        <li>売上高成長率: 15%以上</li>
        <li>利益成長率: 20%以上</li>
        <li>PEG レシオ: 1.5以下</li>
        <li>革新的な事業モデル</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>💰 バリュー投資</h4>
        <p><strong>特徴:</strong> 本質的価値より安く取引される企業への投資</p>
        
        <h5>向いている人:</h5>
        <ul>
        <li>市場の非効率性を活用したい</li>
        <li>じっくり待つことができる</li>
        <li>安全性を重視する</li>
        </ul>
        
        <h5>選定基準:</h5>
        <ul>
        <li>PER: 15倍以下</li>
        <li>PBR: 1.5倍以下</li>
        <li>配当利回り: 3%以上</li>
        <li>安定した収益基盤</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-box">
        <h4>🎁 配当投資</h4>
        <p><strong>特徴:</strong> 安定した配当収入を目的とした投資</p>
        
        <h5>向いている人:</h5>
        <ul>
        <li>インカムゲインを重視</li>
        <li>リタイア世代や年金補完</li>
        <li>安定性を最重視</li>
        </ul>
        
        <h5>選定基準:</h5>
        <ul>
        <li>配当利回り: 4%以上</li>
        <li>配当性向: 30-60%</li>
        <li>連続増配年数: 10年以上</li>
        <li>安定したキャッシュフロー</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>⚖️ バランス投資</h4>
        <p><strong>特徴:</strong> 複数の投資スタイルを組み合わせた投資</p>
        
        <h5>向いている人:</h5>
        <ul>
        <li>投資初心者</li>
        <li>リスクを分散したい</li>
        <li>市場全体の成長を享受したい</li>
        </ul>
        
        <h5>ポートフォリオ例:</h5>
        <ul>
        <li>成長株: 40%</li>
        <li>バリュー株: 30%</li>
        <li>配当株: 20%</li>
        <li>キャッシュ: 10%</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
    <h4>🚀 成功する投資家の共通点</h4>
    <ol>
    <li><strong>明確な投資方針</strong>: 自分の投資目的とリスク許容度を理解している</li>
    <li><strong>長期的視点</strong>: 短期的な市場変動に惑わされない</li>
    <li><strong>継続的学習</strong>: 常に新しい知識と情報を吸収している</li>
    <li><strong>感情のコントロール</strong>: 恐怖と欲望に支配されない</li>
    <li><strong>分散投資</strong>: リスクを適切に分散している</li>
    <li><strong>定期的見直し</strong>: ポートフォリオを定期的に見直している</li>
    </ol>
    </div>
    """)
    
    st.markdown("""
    <div class="warning-box">
    <h4>⚠️ 避けるべき投資行動</h4>
    <ul>
    <li><strong>追っかけ買い</strong>: 高値で買い、安値で売る行動</li>
    <li><strong>集中投資</strong>: 特定の銘柄や業界への過度な集中</li>
    <li><strong>短期売買</strong>: 頻繁な売買による手数料負担とタイミングの失敗</li>
    <li><strong>感情的判断</strong>: ニュースや噂に基づく感情的な売買</li>
    <li><strong>勉強不足</strong>: 十分な分析なしに投資判断を下すこと</li>
    </ul>
    </div>
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add links to other pages
st.markdown("""
<div style="background: #f8fafc; padding: 2rem; border-radius: 16px; margin-top: 2rem; text-align: center;">
    <h3>🔗 実践に移そう</h3>
    <p>理論を学んだら、実際にプラットフォームの各機能を使って投資分析を始めてみましょう。</p>
    <div style="margin-top: 1rem;">
        <a href="/" style="text-decoration: none; color: #667eea; font-weight: 600;">ホームページに戻る</a> |
        <a href="#" style="text-decoration: none; color: #667eea; font-weight: 600;">銘柄発見ツール</a> |
        <a href="#" style="text-decoration: none; color: #667eea; font-weight: 600;">DCF計算機</a>
    </div>
</div>
""", unsafe_allow_html=True)