import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from auto_financial_data import get_auto_financial_data
from comprehensive_stock_data import get_all_tickers, get_stock_info, get_stocks_by_category, get_all_categories
from comprehensive_market_stocks import get_all_market_stocks, get_stock_info_enhanced, search_stocks_comprehensive, get_stock_sector_mapping, get_market_categories
from format_helpers import format_currency, format_large_number

# Modern design CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    
    /* Enhanced Navigation Styles */
    .stSidebar, section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 20px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stSidebar > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar content styling */
    .stSidebar .stMarkdown, .stSidebar .stButton, .stSidebar .stForm {
        color: white !important;
    }
    
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, .stSidebar .stMarkdown p {
        color: white !important;
    }
    
    .stSidebar .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 5px 0 !important;
    }
    
    .stSidebar .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Style Streamlit page navigation */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
        padding: 1rem 0 !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stSidebarNav"] li {
        margin: 8px 0 !important;
    }
    
    [data-testid="stSidebarNav"] a {
        display: block !important;
        padding: 12px 16px !important;
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        text-decoration: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 600 !important;
    }
    
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
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Cards */
    .filter-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .investment-style {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">🔍 銘柄発見</div>
    <div class="page-subtitle">米国株式800銘柄以上から投資スタイルに合った企業を発見</div>
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; border-radius: 8px; margin: 15px 0; font-size: 14px;">
        <strong>🇺🇸 検索対象:</strong> S&P500 • NASDAQ • ダウ30 • Russell2000 • 成長株 • バイオテック • フィンテック • クリーンエネルギー • 暗号通貨関連株など<br>
        <strong>📊 米国株式データベース:</strong> 主要取引所の800銘柄以上をリアルタイム分析 • 投資スタイル別検索 • 業界別検索 • 高速モード対応
    </div>
</div>
""", unsafe_allow_html=True)

# Investment style guide
with st.expander("💡 投資スタイルガイド - どの投資戦略があなたに合っているか？"):
    st.markdown("""
    <div class="investment-style">
    <h4>🚀 成長株投資</h4>
    <p><strong>特徴:</strong> 高い成長率を持つ企業に投資</p>
    <p><strong>適した方:</strong> リスクを取ってでも高いリターンを目指したい方</p>
    <p><strong>スクリーニング条件:</strong> 売上成長率 > 20%, ROE > 15%, PEG < 2</p>
    </div>
    
    <div class="investment-style">
    <h4>💰 バリュー株投資</h4>
    <p><strong>特徴:</strong> 割安で取引されている優良企業に投資</p>
    <p><strong>適した方:</strong> 安定性を重視し、長期的な値上がりを期待する方</p>
    <p><strong>スクリーニング条件:</strong> PER < 15, PBR < 2, 配当利回り > 2%</p>
    </div>
    
    <div class="investment-style">
    <h4>💵 配当株投資</h4>
    <p><strong>特徴:</strong> 安定した配当収入を重視</p>
    <p><strong>適した方:</strong> 定期的な収入を求める方、リタイア世代</p>
    <p><strong>スクリーニング条件:</strong> 配当利回り > 3%, 配当性向 < 60%</p>
    </div>
    
    <div class="investment-style">
    <h4>🛡️ 安定株投資</h4>
    <p><strong>特徴:</strong> 財務が安定した大型株中心</p>
    <p><strong>適した方:</strong> リスクを抑えて着実に資産を増やしたい方</p>
    <p><strong>スクリーニング条件:</strong> 時価総額 > 100億ドル, 負債比率 < 0.5, 流動比率 > 1.5</p>
    </div>
    """, unsafe_allow_html=True)

# Stock screening filters
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
st.markdown("### 🎯 スクリーニング条件を設定")

# Investment style presets
col1, col2 = st.columns([2, 1])

with col1:
    # Simplified search method selection for beginners
    search_method = st.radio(
        "検索方法を選択",
        ["簡単検索（おすすめ）", "詳細検索（上級者向け）"],
        horizontal=True,
        help="簡単検索：投資スタイルを選ぶだけで最適な条件を自動設定 | 詳細検索：すべての条件を手動で調整"
    )
    
    # Stock universe size selection with time estimates
    st.markdown("#### 📊 検索対象の銘柄数")
    stock_universe_options = [
        "250銘柄（約1-2分）",
        "500銘柄（約2-4分）", 
        "1000銘柄（約4-8分）",
        "2000銘柄（約8-15分）"
    ]
    selected_option = st.selectbox(
        "検索する銘柄数を選択",
        stock_universe_options,
        index=1,  # Default to 500
        help="多い銘柄数ほど詳細な検索結果が得られますが、処理時間が長くなります"
    )
    
    # Extract the actual number from the selected option
    if "250" in selected_option:
        stock_universe_size = 250
    elif "500" in selected_option:
        stock_universe_size = 500
    elif "1000" in selected_option:
        stock_universe_size = 1000
    else:
        stock_universe_size = 2000
    
    if search_method == "簡単検索（おすすめ）":
        st.markdown("**🎯 投資スタイルを選択するだけ！**")
        investment_style = st.selectbox(
            "あなたにピッタリの投資スタイルは？",
            [
                "🚀 成長株投資 - 将来性重視（リスク高・リターン高）",
                "💰 バリュー株投資 - 割安株狙い（安定重視）", 
                "💎 配当株投資 - 定期収入重視（配当金狙い）",
                "🏦 安定株投資 - 大企業中心（低リスク）"
            ],
            index=0,
            label_visibility="collapsed",
            help="投資スタイルに応じて最適な条件を自動設定します"
        )
        # Extract the actual style for logic
        if "成長株投資" in investment_style:
            actual_style = "成長株投資"
        elif "バリュー株投資" in investment_style:
            actual_style = "バリュー株投資"
        elif "配当株投資" in investment_style:
            actual_style = "配当株投資"
        else:
            actual_style = "安定株投資"
        
        # Show explanation for beginners
        with st.expander("💡 この投資スタイルについて"):
            if actual_style == "成長株投資":
                st.markdown("""
                **🚀 成長株投資とは？**
                - 売上や利益が急成長している企業への投資
                - テクノロジー、バイオテック、新興企業が中心
                - 高いリターンを期待できるが、リスクも高い
                - **売上成長率20%以上**を重視 - 急成長企業を発見
                """)
            elif actual_style == "バリュー株投資":
                st.markdown("""
                **💰 バリュー株投資とは？**
                - 市場価値より安く取引されている企業への投資
                - 伝統的な大企業や製造業が中心
                - 安定したリターンを期待、リスクは中程度
                - **歴史的な指標と比較**して現在割安な株を発見
                """)
            elif actual_style == "配当株投資":
                st.markdown("""
                **💎 配当株投資とは？**
                - 定期的に配当金を支払う企業への投資
                - 公益事業、金融、消費財企業が中心
                - **配当利回り3-8%** を目安に安定した配当収入を重視
                - 年4回の配当支払いで定期的な現金収入を獲得
                - 企業の配当継続性と増配実績を重視
                
                **💰 配当利回りの目安：**
                - 3-4%：安定した大企業（AT&T、コカ・コーラなど）
                - 4-6%：中堅企業や金融株
                - 6%以上：高配当だが要注意（業績悪化の可能性）
                """)
            else:
                st.markdown("""
                **🏦 安定株投資とは？**
                - 大型で安定した企業への投資
                - S&P500の大企業が中心
                - 低リスクで安定したリターンを重視
                - 時価総額と財務の安定性を重視
                """)
    else:
        st.markdown("**🔧 詳細検索 - すべての条件を手動調整**")
        # Keep original detailed options but simplified
        detail_method = st.radio(
            "詳細検索方法",
            ["投資スタイル別", "業界別"],
            horizontal=True
        )
        
        if detail_method == "投資スタイル別":
            investment_style = st.selectbox(
                "投資スタイル選択",
                ["カスタム設定", "成長株投資", "バリュー株投資", "配当株投資", "安定株投資"],
                label_visibility="collapsed"
            )
            actual_style = investment_style
        else:
            # Industry search for detailed mode
            st.markdown("**業界を選択**")
            industry_options = [
                "すべての業界",
                "テクノロジー", 
                "ヘルスケア・バイオテック",
                "金融サービス",
                "消費者向けサービス", 
                "消費者向け日用品",
                "エネルギー・石油ガス",
                "クリーンエネルギー・再生可能エネルギー",
                "電気自動車・自動車",
                "不動産・REIT",
                "産業・製造業", 
                "素材・鉱業",
                "通信・メディア",
                "公益事業",
                "エンターテイメント・メディア",
                "ゲーミング・カジノ",
                "大麻・代替投資",
                "暗号通貨関連",
                "小売・Eコマース"
            ]
            selected_industry = st.selectbox(
                "業界選択",
                industry_options,
                label_visibility="collapsed"
            )
            actual_style = "業界別"

with col2:
    if st.button("🔄 条件をリセット", use_container_width=True):
        st.rerun()

# Set default values based on search method
# Handle both simple and detailed search modes
if search_method == "簡単検索（おすすめ）" or (search_method == "詳細検索（上級者向け）" and detail_method == "投資スタイル別"):
    if actual_style == "成長株投資":
        # Growth stocks: focus on revenue growth over 20%, very relaxed valuation
        default_revenue_growth = (20.0, 100.0)
        default_roe = (-50.0, 100.0)  # Allow negative ROE for young growth companies
        default_per = (0.0, 500.0)  # Allow very high PER for growth stocks
        default_psr = (0.0, 100.0)   # Allow high PSR for growth stocks
        default_market_cap = (0.1, 5000.0)  # Include small and large cap growth
    elif actual_style == "バリュー株投資":
        # Value stocks: PER less than 20, revenue growth 5%+
        default_revenue_growth = (5.0, 50.0)
        default_roe = (5.0, 100.0)
        default_per = (0.0, 20.0)   # PER less than 20
        default_psr = (0.0, 10.0)    # Relaxed PSR for value stocks
        default_market_cap = (1.0, 5000.0)
    elif actual_style == "配当株投資":
        default_revenue_growth = (-10.0, 50.0)  # Allow slight negative growth
        default_roe = (0.0, 100.0)  # Relaxed ROE requirement
        default_per = (0.0, 50.0)   # Relaxed PER requirement
        default_psr = (0.0, 20.0)   # Relaxed PSR requirement
        default_market_cap = (1.0, 5000.0)  # Relaxed market cap requirement
    elif actual_style == "安定株投資":
        default_revenue_growth = (-5.0, 50.0)  # Allow slight negative growth
        default_roe = (0.0, 100.0)  # Relaxed ROE requirement
        default_per = (0.0, 50.0)   # Relaxed PER requirement
        default_psr = (0.0, 20.0)   # Relaxed PSR requirement
        default_market_cap = (5.0, 5000.0)  # Relaxed market cap requirement
    else:  # カスタム設定
        default_revenue_growth = (0.0, 50.0)
        default_roe = (0.0, 100.0)
        default_per = (0.0, 100.0)
        default_psr = (0.0, 30.0)
        default_market_cap = (0.1, 5000.0)
else:  # 業界別検索
    # Industry-based search uses more relaxed default criteria
    default_revenue_growth = (0.0, 50.0)
    default_roe = (0.0, 100.0)
    default_per = (0.0, 100.0)
    default_psr = (0.0, 30.0)
    default_market_cap = (0.1, 5000.0)

# Screening criteria - different UI based on search mode
if search_method == "簡単検索（おすすめ）":
    st.markdown("### ✨ 自動設定された検索条件")
    st.info(f"🎯 **{actual_style}** 向けの最適な条件を自動設定しました。「検索開始」ボタンを押すだけでOKです！")
    
    # Show the conditions being used but don't allow editing
    with st.expander("📊 使用されている検索条件を確認"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"売上成長率: {default_revenue_growth[0]}% - {default_revenue_growth[1]}%")
            st.write(f"ROE: {default_roe[0]}% - {default_roe[1]}%")
            st.write(f"PER: {default_per[0]} - {default_per[1]}")
        with col2:
            st.write(f"PSR: {default_psr[0]} - {default_psr[1]}")
            st.write(f"時価総額: {default_market_cap[0]}億USD - {default_market_cap[1]}億USD")
            if actual_style == "配当株投資":
                st.write("**配当利回り: 2.0% - 15.0%**（有意義な配当株のみ）")
                st.write("利益率: -50% - 50%")
            else:
                st.write("利益率: -50% - 50%（赤字企業も含む）")
                st.write("配当利回り: 0% - 15%（全範囲）")
    
    # Set default values for filtering - no user interaction needed
    revenue_growth_range = default_revenue_growth
    roe_range = default_roe
    per_range = default_per
    psr_range = default_psr
    market_cap_range = default_market_cap
    profit_margin_range = (-50.0, 50.0)
    
    # Set dividend yield range based on investment style
    if actual_style == "配当株投資":
        dividend_yield_range = (1.0, 15.0)  # Focus on meaningful dividend yields (reduced from 2.0 to 1.0)
    else:
        dividend_yield_range = (0.0, 15.0)  # Allow all ranges for other styles
        
    roa_range = (0.0, 30.0)
    pbr_range = (0.0, 10.0)
    debt_ratio_range = (0.0, 2.0)
    
    # Add beginner-friendly tips
    with st.expander("💡 初心者向けヒント"):
        st.markdown(f"""
        **{actual_style}** について：
        
        📈 **検索時間**: 約1-2分で結果が表示されます
        
        📊 **結果の見方**:
        - 上位に表示される企業ほど条件に合致
        - 企業名をクリックで詳細分析ページへ移動
        - PSR/PERで割安度を確認
        
        🎯 **次のステップ**:
        - 気になる企業が見つかったら「ビジネスモデル分析」で詳しく調査
        - 複数企業の比較は「銘柄比較」ページで実施
        """)
    
else:
    # Show full filter interface for advanced users
    st.markdown("### 🎯 検索条件設定")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**財務指標**")
        
        revenue_growth_range = st.slider(
            "売上成長率 (%)",
            min_value=0.0,
            max_value=50.0,
            value=default_revenue_growth,
            step=0.5,
            help="過去の年間売上成長率"
        )
        
        roe_range = st.slider(
            "ROE (%)",
            min_value=0.0,
            max_value=100.0,
            value=default_roe,
            step=1.0,
            help="自己資本利益率"
        )
        
        roa_range = st.slider(
            "ROA (%)",
            min_value=0.0,
            max_value=30.0,
            value=(0.0, 30.0),
            step=0.5,
            help="総資産利益率"
        )

    with col2:
        st.markdown("**バリュエーション**")
        
        per_range = st.slider(
            "PER (収益性のある株式のみ)",
            min_value=0.0,
            max_value=200.0,  # Increased for high-growth stocks
            value=default_per,  # Use default value
            step=1.0,
            help="株価収益率（高成長株は高PERでも対象に含む）"
        )
        
        psr_range = st.slider(
            "PSR (全ての株式)",
            min_value=0.0,
            max_value=50.0,
            value=default_psr,
            step=0.5,
            help="株価売上高倍率（成長株や赤字企業の評価に重要）"
        )
        
        pbr_range = st.slider(
            "PBR",
            min_value=0.0,
            max_value=10.0,
            value=(0.0, 10.0),
            step=0.1,
            help="株価純資産倍率"
        )
        
        profit_margin_range = st.slider(
            "純利益率 (%)",
            min_value=-50.0,  # Allow negative margins for unprofitable growth stocks
            max_value=50.0,
            value=(-50.0, 50.0),  # More inclusive default
            step=1.0,
            help="売上に対する純利益の割合（マイナスも含む）"
        )

        st.markdown("**企業規模・安定性**")
        
        market_cap_range = st.slider(
            "時価総額 (億ドル)",
            min_value=0.1,
            max_value=5000.0,
            value=default_market_cap,
            step=0.1,
            help="企業の規模"
        )
        
        debt_ratio_range = st.slider(
            "負債比率",
            min_value=0.0,
            max_value=2.0,
            value=(0.0, 2.0),
            step=0.1,
            help="負債÷自己資本"
        )
        
        dividend_yield_range = st.slider(
            "配当利回り (%)",
            min_value=0.0,
            max_value=15.0,
            value=(0.0, 15.0),
            step=0.1,
            help="年間配当利回り"
        )
        
        # Ensure all variables are defined for advanced search
        debt_ratio_range = (0.0, 2.0)  # Default for now

# Sector filter - show only for detailed search or when relevant
if search_method == "詳細検索（上級者向け）" and detail_method == "業界別":
    sectors = ["All"] + list(get_stock_sector_mapping().keys())
    selected_sectors = st.multiselect(
        "業界・セクター",
        sectors,
        default=["All"],
        help="特定の業界に絞り込み"
    )
else:
    # For simple search, use all sectors by default
    selected_sectors = ["All"]

st.markdown('</div>', unsafe_allow_html=True)

# Make search button more prominent for beginners
if search_method == "簡単検索（おすすめ）":
    st.markdown("### 🚀 検索開始")
    if actual_style == "配当株投資":
        st.markdown("**準備完了！** 配当利回り0.5%以上の配当株を検索します。検索後にフィルターで利回りを調整できます。")
        search_button_text = "💎 配当株を検索開始！"
    else:
        st.markdown("**準備完了！** 下のボタンを押すだけで、あなたにピッタリの銘柄を見つけます。")
        search_button_text = f"🎯 {actual_style}で検索開始！"
else:
    search_button_text = "🔍 銘柄を検索"

# Search button
if st.button(search_button_text, use_container_width=True, type="primary"):
    
    with st.spinner("条件に合う銘柄を検索中..."):
        # Get comprehensive stock universe based on user selection
        from comprehensive_market_stocks import get_sp500_tickers, get_nasdaq100_tickers, get_russell2000_stocks, get_all_market_stocks
        
        # Build stock universe based on selected size
        if stock_universe_size == 250:
            sp500_stocks = get_sp500_tickers()
            available_tickers = sp500_stocks[:250]
        elif stock_universe_size == 500:
            sp500_stocks = get_sp500_tickers()
            nasdaq100_stocks = get_nasdaq100_tickers()
            available_tickers = list(set(sp500_stocks + nasdaq100_stocks))[:500]
        elif stock_universe_size == 1000:
            sp500_stocks = get_sp500_tickers()
            nasdaq100_stocks = get_nasdaq100_tickers()
            russell2000_stocks = get_russell2000_stocks()
            available_tickers = list(set(sp500_stocks + nasdaq100_stocks + russell2000_stocks[:500]))[:1000]
        else:  # 2000 stocks
            available_tickers = get_all_market_stocks()[:2000]
        
        # Remove any problematic tickers from our list
        available_tickers = [t for t in available_tickers if t not in ['GOOGL', 'BRK.B', 'BF.B']]
        
        # Use comprehensive market coverage - remove artificial limit
        # Now screening from thousands of stocks instead of just 200
        st.info(f"📊 {len(available_tickers):,}銘柄から条件に合致する企業を検索中...")
        
        # Process stocks based on selected universe size
        max_process = min(stock_universe_size, len(available_tickers))
        available_tickers = available_tickers[:max_process]
        
        # Pre-filter out known delisted/problematic stocks to improve performance
        delisted_stocks = {
            'ALXN', 'APHA', 'ATVI', 'BBBY', 'NAKD', 'SNDL', 'EXPR', 'KOSS', 'BF.B',
            'BLUE', 'BOOKING', 'BRK.B', 'CERN', 'COUP', 'CTXS', 'CELG', 'MYL',
            'WORK', 'XLNX', 'MXIM', 'TCOM', 'PARA', 'WBD', 'ACCD', 'ACER', 'ACHN',
            'ACIA', 'ACRX', 'ACST', 'ADES', 'ADHD', 'ADMP', 'ADMS', 'ADOM', 'ADRE',
            'ADRO', 'ADVS', 'AEL', 'AENZ', 'AERI', 'AEY', 'AEZS', 'AFAM', 'AFS',
            'ARVL', 'ATSG', 'CDR', 'DFS', 'DISH', 'EQC', 'FISV', 'FSR', 'GNUS',
            'GRUB', 'HA', 'HEXO', 'IDEX', 'JTKPY', 'KSU', 'KTOV', 'LIFE', 'AAWW',
            'ABMD', 'ADSK', 'BMCH', 'CBOE', 'CDAY', 'CERN', 'CTSH', 'CVNA', 'DDOG',
            'DLR', 'EQIX', 'ETSY', 'FAST', 'FISV', 'FTNT', 'GILD', 'ILMN', 'INCY',
            'ISRG', 'KLAC', 'LRCX', 'MCHP', 'MRNA', 'MXIM', 'NXPI', 'PAYX', 'PCAR',
            'REGN', 'ROST', 'SBUX', 'SWKS', 'TMUS', 'VRSK', 'VRTX', 'WBA', 'WDAY',
            'XEL', 'XLNX', 'ZM'
        }
        available_tickers = [t for t in available_tickers if t not in delisted_stocks]
        
        # Fix common ticker naming issues
        ticker_fixes = {
            'BRK.B': 'BRK-B',
            'BF.B': 'BF-B'
        }
        available_tickers = [ticker_fixes.get(t, t) for t in available_tickers]
        
        # Screen stocks
        matching_stocks = []
        processed_count = 0
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, ticker in enumerate(available_tickers):
            try:
                status_text.text(f"分析中: {ticker} ({i+1}/{len(available_tickers)})")
                progress_bar.progress((i + 1) / len(available_tickers))
                
                # Get financial data
                data = get_auto_financial_data(ticker)
                if not data:
                    continue
                
                processed_count += 1
                
                # Simplified screening - Extract key metrics
                revenue_growth = data.get('historical_growth', 0) or 0
                per = data.get('pe_ratio', 0) or 0
                psr = data.get('ps_ratio', 0) or 0
                profit_margin = data.get('profit_margin', 0) or 0
                market_cap_billions = (data.get('market_cap', 0) or 0) / 1000
                dividend_yield = data.get('dividend_yield', 0) or 0
                roe = data.get('roe', 0) or 0
                pbr = data.get('pb_ratio', 0) or 0
                debt_ratio = data.get('debt_to_equity', 0) or 0
                roa = data.get('roa', 0) or 0
                
                # Only apply basic filters that are essential for each investment style
                should_include = False
                
                if actual_style == "成長株投資":
                    # Growth: Focus on stocks with 20%+ revenue growth
                    if (revenue_growth >= 20 or 
                        (revenue_growth >= 15 and roe >= 20) or
                        (market_cap_billions >= 1 and revenue_growth >= 15)):
                        should_include = True
                        
                elif actual_style == "バリュー株投資":
                    # Value: Include stocks trading cheap based on historical metrics
                    # Focus on profitable companies with reasonable valuations
                    historical_pe = data.get('historical_pe_avg', per * 1.2) or per * 1.2  # Use 20% above current as fallback
                    historical_pb = data.get('historical_pb_avg', pbr * 1.2) or pbr * 1.2
                    
                    # Value criteria: profitable + trading below historical averages OR low absolute valuations
                    if (profit_margin > 0 and per > 0 and 
                        ((per < historical_pe * 0.8 and pbr < historical_pb * 0.8) or  # Trading 20% below historical
                         (per <= 15 and pbr <= 2.5 and revenue_growth >= 0))):  # Or absolute value criteria
                        should_include = True
                        
                elif actual_style == "配当株投資":
                    # Dividend: Include any stock with dividend yield above 0.5% (lower threshold for better coverage)
                    if dividend_yield >= 0.5:
                        should_include = True
                        
                elif actual_style == "安定株投資":
                    # Stability: Include large profitable companies
                    if (market_cap_billions >= 1.0 and profit_margin > 0):
                        should_include = True
                
                if not should_include:
                    continue
                
                # Get company description from existing data or fetch if needed
                try:
                    # Try to get description from existing data first
                    description = data.get('business_summary', '')
                    if not description:
                        # If not available, fetch from yfinance
                        stock_info = yf.Ticker(ticker)
                        business_summary = stock_info.info.get('longBusinessSummary', '')
                        description = business_summary[:200] + "..." if len(business_summary) > 200 else business_summary
                    
                    # If still no description, provide a fallback
                    if not description:
                        description = f"{data.get('sector', 'Unknown')}セクターの企業"
                except Exception as e:
                    description = f"{data.get('sector', 'Unknown')}セクターの企業"
                
                # If all criteria pass, add to results
                matching_stocks.append({
                    'ticker': ticker,
                    'name': data.get('name', ticker),
                    'sector': data.get('sector', 'Unknown'),
                    'description': description,
                    'current_price': data.get('current_price', 0),
                    'market_cap': data.get('market_cap', 0),
                    'revenue_growth': revenue_growth,
                    'roe': roe,
                    'roa': roa,
                    'pe_ratio': per,
                    'ps_ratio': psr,
                    'pb_ratio': pbr,
                    'profit_margin': profit_margin,
                    'debt_ratio': debt_ratio,
                    'dividend_yield': dividend_yield,
                    'is_profitable': profit_margin > 0 and per > 0,
                    'data': data
                })
                
            except Exception as e:
                continue
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Store results in session state to prevent re-searching when filtering
        st.session_state['search_results'] = matching_stocks
        st.session_state['processed_count'] = processed_count
        st.session_state['search_info'] = f"業界: {selected_industry}" if search_method == "業界別" else f"投資スタイル: {investment_style if 'investment_style' in locals() else 'カスタム設定'}"

# Display results (whether from fresh search or session state)
if 'search_results' in st.session_state and st.session_state['search_results']:
    matching_stocks = st.session_state['search_results']
    processed_count = st.session_state.get('processed_count', len(matching_stocks))
    search_info = st.session_state.get('search_info', 'Unknown')
    
    # Header with clear button
    result_col1, result_col2 = st.columns([3, 1])
    with result_col1:
        st.markdown(f"### 検索結果: {len(matching_stocks)}銘柄が条件に合致")
        st.markdown(f"<small>分析対象: {processed_count}銘柄 | {search_info}</small>", unsafe_allow_html=True)
    with result_col2:
        if st.button("🗑️ 検索結果をクリア", key="clear_results"):
            # Clear all session state related to search
            for key in ["search_results", "processed_count", "search_info", "per_filter", "psr_filter", "growth_filter", "cap_filter", "dividend_filter"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Add seamless post-search filtering controls
    with st.expander("🔧 結果を絞り込み（リアルタイム）", expanded=False):
        st.markdown("**検索結果をリアルタイムで絞り込み：**")
        
        filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)
        
        with filter_col1:
            # PER filter
            per_values = [s['pe_ratio'] for s in matching_stocks if s['is_profitable'] and s['pe_ratio'] > 0]
            if per_values:
                min_per, max_per = min(per_values), max(per_values)
                per_filter = st.slider(
                    "PER 範囲",
                    min_value=float(min_per),
                    max_value=float(max_per),
                    value=(float(min_per), float(max_per)),
                    step=0.5,
                    help="収益性のある銘柄のみ対象",
                    key="per_filter"
                )
            else:
                per_filter = None
        
        with filter_col2:
            # PSR filter  
            psr_values = [s['ps_ratio'] for s in matching_stocks if s['ps_ratio'] > 0]
            if psr_values:
                min_psr, max_psr = min(psr_values), max(psr_values)
                psr_filter = st.slider(
                    "PSR 範囲",
                    min_value=float(min_psr),
                    max_value=float(max_psr),
                    value=(float(min_psr), float(max_psr)),
                    step=0.1,
                    help="全銘柄が対象",
                    key="psr_filter"
                )
            else:
                psr_filter = None
        
        with filter_col3:
            # Revenue growth filter
            growth_values = [s['revenue_growth'] for s in matching_stocks if s['revenue_growth'] is not None]
            if growth_values:
                min_growth, max_growth = min(growth_values), max(growth_values)
                growth_filter = st.slider(
                    "売上成長率 (%)",
                    min_value=float(min_growth),
                    max_value=float(max_growth),
                    value=(float(min_growth), float(max_growth)),
                    step=1.0,
                    help="売上成長率で絞り込み",
                    key="growth_filter"
                )
            else:
                growth_filter = None
        
        with filter_col4:
            # Market cap filter
            market_caps = [s['market_cap'] / 1000 for s in matching_stocks if s['market_cap'] > 0]
            if market_caps:
                min_cap, max_cap = min(market_caps), max(market_caps)
                cap_filter = st.slider(
                    "時価総額 (億ドル)",
                    min_value=float(min_cap),
                    max_value=float(max_cap),
                    value=(float(min_cap), float(max_cap)),
                    step=0.1,
                    key="cap_filter"
                )
            else:
                cap_filter = None
        
        with filter_col5:
            # Dividend yield filter - especially important for dividend stocks
            dividend_values = [s['dividend_yield'] for s in matching_stocks if s['dividend_yield'] > 0]
            if dividend_values:
                min_dividend, max_dividend = min(dividend_values), max(dividend_values)
                dividend_filter = st.slider(
                    "配当利回り (%)",
                    min_value=float(min_dividend),
                    max_value=float(max_dividend),
                    value=(float(min_dividend), float(max_dividend)),
                    step=0.1,
                    help="配当を支払う銘柄のみ",
                    key="dividend_filter"
                )
            else:
                dividend_filter = None
        
        # Apply filters in real-time without triggering rerun
        filtered_stocks = matching_stocks.copy()
        
        if per_filter:
            filtered_stocks = [s for s in filtered_stocks 
                             if not s['is_profitable'] or not s['pe_ratio'] > 0 or 
                             (per_filter[0] <= s['pe_ratio'] <= per_filter[1])]
        
        if psr_filter:
            filtered_stocks = [s for s in filtered_stocks 
                             if s['ps_ratio'] <= 0 or (psr_filter[0] <= s['ps_ratio'] <= psr_filter[1])]
        
        if growth_filter:
            filtered_stocks = [s for s in filtered_stocks 
                             if s['revenue_growth'] is None or (growth_filter[0] <= s['revenue_growth'] <= growth_filter[1])]
        
        if cap_filter:
            filtered_stocks = [s for s in filtered_stocks 
                             if cap_filter[0] <= (s['market_cap'] / 1000) <= cap_filter[1]]
        
        if dividend_filter:
            filtered_stocks = [s for s in filtered_stocks 
                             if s['dividend_yield'] > 0 and (dividend_filter[0] <= s['dividend_yield'] <= dividend_filter[1])]
        
        # Show filter results immediately
        filter_col_result1, filter_col_result2 = st.columns(2)
        with filter_col_result1:
            st.markdown(f"**絞り込み前: {len(matching_stocks)}銘柄**")
        with filter_col_result2:
            st.markdown(f"**絞り込み後: {len(filtered_stocks)}銘柄**")
        
        # Special message for dividend stock users
        if dividend_filter:
            dividend_stocks_count = len([s for s in filtered_stocks if s['dividend_yield'] > 0])
            if dividend_stocks_count > 0:
                st.info(f"💰 {dividend_stocks_count}銘柄が配当利回り{dividend_filter[0]:.1f}%-{dividend_filter[1]:.1f}%の範囲にあります")
        
        # Clear filters button
        if st.button("🔄 フィルターをクリア", key="clear_filters"):
            # Reset all filter keys
            for key in ["per_filter", "psr_filter", "growth_filter", "cap_filter", "dividend_filter"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Use filtered results for display
    display_stocks = filtered_stocks if 'filtered_stocks' in locals() else matching_stocks
        
    if display_stocks:
        # Sort by market cap descending
        display_stocks.sort(key=lambda x: x['market_cap'], reverse=True)
        
        # Display results in cards
        for i, stock in enumerate(display_stocks[:20]):  # Show top 20 results
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{stock['ticker']} - {stock['name']}**")
                st.markdown(f"セクター: {stock['sector']}")
                st.markdown(f"現在株価: ${stock['current_price']:.2f}")
                # Add company description
                st.markdown(f"<small style='color: #666;'>{stock['description']}</small>", unsafe_allow_html=True)
            
            with col2:
                # Key metrics
                if stock['revenue_growth'] > 0:
                    st.markdown(f"<span class='metric-badge'>成長率 {stock['revenue_growth']:.1f}%</span>", unsafe_allow_html=True)
                if stock['roe'] > 0:
                    st.markdown(f"<span class='metric-badge'>ROE {stock['roe']:.1f}%</span>", unsafe_allow_html=True)
                
                # Show both PER and PSR for all stocks
                if stock['is_profitable'] and stock['pe_ratio'] > 0:
                    st.markdown(f"<span class='metric-badge'>PER {stock['pe_ratio']:.1f}</span>", unsafe_allow_html=True)
                
                if stock['ps_ratio'] > 0:
                    st.markdown(f"<span class='metric-badge'>PSR {stock['ps_ratio']:.1f}</span>", unsafe_allow_html=True)
                
                # Show dividend yield if available
                if stock['dividend_yield'] > 0:
                    st.markdown(f"<span class='metric-badge'>配当利回り {stock['dividend_yield']:.1f}%</span>", unsafe_allow_html=True)
            
            with col3:
                market_cap_billions = stock['market_cap'] / 1000
                st.metric("時価総額", f"${market_cap_billions:.1f}B")
            
            # Detailed metrics in expandable section
            with st.expander(f"{stock['ticker']} 詳細データ"):
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.write(f"**売上成長率:** {stock['revenue_growth']:.1f}%")
                    st.write(f"**ROE:** {stock['roe']:.1f}%")
                    st.write(f"**ROA:** {stock['roa']:.1f}%")
                
                with metric_col2:
                    # Show both PER and PSR for all stocks
                    if stock['is_profitable'] and stock['pe_ratio'] > 0:
                        st.write(f"**PER:** {stock['pe_ratio']:.1f}")
                    else:
                        st.write("**PER:** N/A (赤字)")
                    
                    if stock['ps_ratio'] > 0:
                        st.write(f"**PSR:** {stock['ps_ratio']:.1f}")
                    else:
                        st.write("**PSR:** N/A")
                    
                    st.write(f"**PBR:** {stock['pb_ratio']:.1f}")
                    st.write(f"**純利益率:** {stock['profit_margin']:.1f}%")
                
                with metric_col3:
                    st.write(f"**負債比率:** {stock['debt_ratio']:.2f}")
                    st.write(f"**時価総額:** ${market_cap_billions:.1f}B")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.warning("条件に合致する銘柄が見つかりませんでした。条件を緩和して再検索してください。")
        
        # Suggestions for better results
        st.markdown("""
        ### 💡 検索のコツ
        - 条件範囲を広げてみてください
        - 投資スタイルのプリセットを試してみてください  
        - 特定のセクターに絞り込んでみてください
        - 時価総額の範囲を調整してみてください
        """)

# Investment tips
with st.expander("💡 投資のアドバイス"):
    st.markdown("""
    ### 銘柄選択のポイント
    
    **1. 分散投資を心がける**
    - 異なるセクターから複数の銘柄を選択
    - 時価総額の違う企業を組み合わせる
    
    **2. ファンダメンタルズを重視**
    - 財務の健全性（負債比率、流動比率）
    - 収益性（ROE、ROA、純利益率）
    - 成長性（売上成長率）
    
    **3. バリュエーションを確認**
    - PER、PBRが適正水準か
    - 同業他社との比較
    
    **4. 継続的なモニタリング**
    - 定期的な財務データの確認
    - 業界トレンドの把握
    - 経営陣の方針変更に注意
    
    **注意:** このツールは投資判断の参考情報です。実際の投資は自己責任で行ってください。
    """)