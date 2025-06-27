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
from historical_metrics_chart import display_historical_metrics_chart

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
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "AAPL"
if 'analysis_report' not in st.session_state:
    st.session_state.analysis_report = ""
if 'company_info' not in st.session_state:
    st.session_state.company_info = {}

with col1:
    search_input = st.text_input(
        "企業名またはティッカーシンボルを入力",
        placeholder="例: Apple, Microsoft, AAPL, MSFT",
        help="企業名（日本語・英語）またはティッカーシンボルで検索",
        value=st.session_state.get('search_input', '')
    )
    
    if search_input:
        st.session_state.search_input = search_input
        from comprehensive_stock_data import search_stocks_by_name
        results = search_stocks_by_name(search_input)
        if results:
            selected_ticker = results[0]['ticker']
        else:
            selected_ticker = search_input.upper()
    else:
        selected_ticker = st.session_state.current_ticker

with col2:
    analyze_button = st.button("📋 ファンダメンタル分析", type="primary", use_container_width=True)

# Check if we should run analysis
should_analyze = analyze_button and selected_ticker

# If ticker changed, reset analysis
if selected_ticker != st.session_state.current_ticker:
    st.session_state.analysis_completed = False
    st.session_state.current_ticker = selected_ticker

if should_analyze or (st.session_state.analysis_completed and st.session_state.current_ticker == selected_ticker):
    # Run analysis if needed
    if should_analyze and not st.session_state.analysis_completed:
        with st.spinner(f"{selected_ticker}のビジネスファンダメンタルを分析中..."):
            try:
                stock = yf.Ticker(selected_ticker)
                info = stock.info
                
                company_name = info.get('longName', selected_ticker)
                sector = info.get('sector', 'Technology')
                industry = info.get('industry', 'Software')
                
                # Store in session state
                st.session_state.company_info = {
                    'name': company_name,
                    'sector': sector,
                    'industry': industry,
                    'info': info
                }
                
                # Generate real-time fundamental analysis using Gemini AI
                st.session_state.analysis_report = analyze_company_fundamentals(selected_ticker)
                st.session_state.analysis_completed = True
                
            except Exception as e:
                st.error(f"企業情報の取得に失敗しました: {str(e)}")
                st.session_state.analysis_completed = False
    
    # Display analysis results if available
    if st.session_state.analysis_completed and st.session_state.company_info:
        company_info = st.session_state.company_info
        
        st.markdown(f"""
        <div class="research-paper">
            <h1 class="paper-title">{company_info['name']} ({selected_ticker})</h1>
            <h2 class="paper-subtitle">包括的ファンダメンタル分析レポート</h2>
            
            <div class="author-info">
                <strong>分析日:</strong> {datetime.now().strftime('%Y年%m月%d日')}<br>
                <strong>セクター:</strong> {company_info['sector']} | <strong>業界:</strong> {company_info['industry']}<br>
                <strong>データ源:</strong> Yahoo Finance
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the AI-generated analysis
        st.markdown(st.session_state.analysis_report)
        
        # Display current stock price in JPY
        try:
            info = company_info['info']
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price:
                st.markdown("### 💱 現在の株価（日本円換算）")
                display_stock_price_in_jpy(selected_ticker, current_price)
        except:
            pass
        
        # Market comparison section
        st.markdown("### 📈 市場指数との比較")
        st.markdown("主要市場指数（NASDAQ、S&P 500）とのパフォーマンス比較を表示します。")
        display_stock_market_comparison(selected_ticker)
        
        # Historical metrics section
        st.markdown("### 📊 過去の財務指標推移と業界比較")
        display_historical_metrics_chart(selected_ticker)

# Educational section
with st.expander("💡 ファンダメンタル分析の重要性"):
    st.markdown("""
    ### なぜビジネスファンダメンタルズが重要なのか
    
    **長期投資における本質的価値の理解**
    - 財務数値は過去の結果であり、ビジネスの本質的な強さを表すものです
    - 企業の「経済的堀」や競争優位性は数字だけでは見えません
    - 経営陣の質や戦略的ビジョンが長期的な成果を左右します
    
    **投資判断への活用方法**
    - 短期的な株価変動に惑わされない投資判断
    - 企業の持続可能な成長性の評価
    - リスク要因の事前把握と対策
    
    **このページの活用法**
    - 気になる企業のティッカーを入力して分析を開始
    - AIが生成する包括的なレポートで投資判断の参考に
    - 通貨換算機能で日本円での投資額を把握
    """)