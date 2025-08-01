import streamlit as st
import sys
import os
from datetime import datetime
import yfinance as yf

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comprehensive_market_stocks import get_all_market_stocks
from comprehensive_stock_data import search_stocks_by_name
from currency_converter import display_stock_price_in_jpy
from gemini_analyzer import analyze_company_fundamentals
from market_comparison import display_stock_market_comparison
from session_state_manager import init_session_state, reset_fundamental_analysis, should_reset_fundamental_analysis
from gemini_historical_metrics import create_historical_metrics_table_with_ai
from logo_utils import display_logo_header, display_company_logo

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
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Research paper styling */
    .research-paper {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .paper-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        text-align: center;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 1rem;
    }
    
    .paper-subtitle {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
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

# Initialize session state
init_session_state()

with col1:
    search_input = st.text_input(
        "企業名またはティッカーシンボルを入力",
        placeholder="例: Apple, Microsoft, AAPL, MSFT",
        help="企業名（日本語・英語）またはティッカーシンボルで検索",
        value=st.session_state.get('fundamental_search_input', '')
    )
    
    if search_input:
        st.session_state.fundamental_search_input = search_input
        from comprehensive_stock_data import search_stocks_by_name
        results = search_stocks_by_name(search_input)
        if results:
            selected_ticker = results[0]['ticker']
        else:
            selected_ticker = search_input.upper()
    else:
        selected_ticker = st.session_state.get('fundamental_current_ticker', 'AAPL')

with col2:
    analyze_button = st.button("ファンダメンタル分析", type="primary", use_container_width=True)

# Check if we should run analysis
should_analyze = analyze_button and selected_ticker

# If ticker changed, reset analysis
if should_reset_fundamental_analysis(selected_ticker):
    reset_fundamental_analysis()
    st.session_state.fundamental_current_ticker = selected_ticker

if should_analyze or (st.session_state.fundamental_analysis_completed and st.session_state.fundamental_current_ticker == selected_ticker):
    # Run analysis if needed
    if should_analyze and not st.session_state.fundamental_analysis_completed:
        with st.spinner(f"{selected_ticker}のビジネスファンダメンタルを分析中..."):
            try:
                stock = yf.Ticker(selected_ticker)
                info = stock.info
                
                company_name = info.get('longName', selected_ticker)
                sector = info.get('sector', 'Technology')
                industry = info.get('industry', 'Software')
                
                # Store in session state
                st.session_state.fundamental_company_info = {
                    'name': company_name,
                    'sector': sector,
                    'industry': industry,
                    'info': info
                }
                
                # Generate comprehensive due diligence analysis using Gemini AI, OpenAI, and Twitter
                from comprehensive_due_diligence_analyzer import get_comprehensive_due_diligence_report
                comprehensive_report = get_comprehensive_due_diligence_report(selected_ticker)
                st.session_state.fundamental_analysis_report = comprehensive_report.get('fundamental_analysis', {}).get('report_content', 'レポート生成に失敗しました')
                st.session_state.comprehensive_dd_report = comprehensive_report
                st.session_state.fundamental_analysis_completed = True
                
            except Exception as e:
                st.error(f"企業情報の取得に失敗しました: {str(e)}")
                st.session_state.fundamental_analysis_completed = False
    
    # Display analysis results if available
    if st.session_state.fundamental_analysis_completed and st.session_state.fundamental_company_info:
        company_info = st.session_state.fundamental_company_info
        
        # Display company logo header
        display_logo_header(
            selected_ticker, 
            company_info['name'], 
            f"長期投資家向け企業デューデリジェンス調査 - {company_info['sector']}"
        )
        
        # Company analysis info section
        st.markdown(f"""
        <div class="author-info">
            <strong>分析日:</strong> {datetime.now().strftime('%Y年%m月%d日')}<br>
            <strong>セクター:</strong> {company_info['sector']} | <strong>業界:</strong> {company_info['industry']}<br>
            <strong>分析方針:</strong> 財務比率を使わない質的競争力評価<br>
            <strong>データ源:</strong> Yahoo Finance
        </div>
        """, unsafe_allow_html=True)
        
        # Display the AI-generated analysis
        st.markdown(st.session_state.fundamental_analysis_report)
        
        # Display current stock price in JPY
        try:
            info = company_info['info']
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price:
                st.markdown("### 💱 現在の株価（日本円換算）")
                display_stock_price_in_jpy(selected_ticker, current_price)
        except:
            pass
        
        # Historical metrics table section (financecharts.com style)
        st.markdown("### 📈 過去の財務指標推移と業界比較")
        st.markdown("主要バリュエーション指標の現在値と過去平均値を比較して投資判断にご活用ください。")
        
        # Get current financial metrics
        stock = yf.Ticker(selected_ticker)
        info = stock.info
        current_pe = info.get('trailingPE', info.get('forwardPE', None))
        current_pb = info.get('priceToBook', None)
        current_ps = info.get('priceToSalesTrailing12Months', None)
        
        # Display historical metrics table
        create_historical_metrics_table_with_ai(selected_ticker, current_pe, current_pb, current_ps)

# Educational section
with st.expander("🔍 批判的ビジネス分析の価値"):
    st.markdown("""
    ### なぜ批判的な質的分析が重要なのか
    
    **財務比率を超えた企業理解**
    - 財務数値は過去の結果に過ぎず、将来の成功を保証しません
    - 企業の真の競争力は、数字に現れない定性的要因に隠されています
    - 投資家が見落としがちな「ストーリーの亀裂」を発見することが重要です
    
    **7つの重要な分析領域**
    - **経済的堀**: 持続可能な競争優位性の源泉と脆弱性
    - **ビジネスモデル**: 収益構造の回復力と成長・マーケティング戦略
    - **経営陣の質**: CEO/CFO/CTO/COO の実績と資本配分能力
    - **企業文化**: 人材の定着と組織の健全性
    - **業界ポジション**: 競合環境と脅威への対応力
    - **製品・サービス成功度**: 各製品の成功・失敗要因と収益貢献度
    - **ステークホルダー関係**: 顧客・パートナー・規制当局との信頼度
    
    **このページの活用法**
    - 懐疑的な視点で企業の弱点や課題を発見
    - 表面的な成功に隠された潜在的リスクを評価
    - 長期的な投資価値の本質を理解
    """)