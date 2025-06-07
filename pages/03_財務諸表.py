import streamlit as st
import pandas as pd
import yfinance as yf
from auto_financial_data import get_auto_financial_data
from format_helpers import format_currency, format_large_number
import numpy as np

st.set_page_config(
    page_title="財務諸表分析 - 1000xStocks",
    page_icon="📊",
    layout="wide"
)

# CSS スタイリング
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    .financial-table {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>📊 財務諸表分析</h1>", unsafe_allow_html=True)
st.markdown("**企業の最新決算データから損益計算書、貸借対照表、株主資本の詳細を確認**")

# 企業選択
available_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", 
    "CRM", "ADBE", "PYPL", "INTC", "CSCO", "ORCL", "IBM", "UBER",
    "COIN", "SHOP", "SQ", "ZM", "DOCU", "OKTA", "SNOW", "PLTR"
]

col1, col2 = st.columns([3, 1])

with col1:
    selected_ticker = st.selectbox(
        "企業を選択してください",
        options=available_tickers,
        index=0,
        format_func=lambda x: f"{x}"
    )

with col2:
    if st.button("🔄 データ更新", use_container_width=True):
        st.cache_data.clear()
        st.success("データを更新しました")
        st.rerun()

if selected_ticker:
    with st.spinner("最新の財務データを取得中..."):
        # Get comprehensive financial data
        auto_data = get_auto_financial_data(selected_ticker)
        
        if auto_data:
            # Basic company info
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("企業名", auto_data['name'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("業界", auto_data['industry'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("現在株価", f"${auto_data['current_price']:.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                st.metric("時価総額", format_currency(market_cap, "$"))
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Get detailed financial statements using yfinance
            try:
                stock = yf.Ticker(selected_ticker)
                
                # 損益計算書 (Income Statement)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📈 損益計算書 (Income Statement)")
                
                income_stmt = stock.financials
                if not income_stmt.empty:
                    # Convert to Japanese labels and format
                    income_data = []
                    
                    # Key income statement items
                    income_items = {
                        'Total Revenue': '売上高',
                        'Cost Of Revenue': '売上原価',
                        'Gross Profit': '売上総利益',
                        'Operating Income': '営業利益',
                        'Net Income': '純利益',
                        'Basic EPS': '基本的1株当たり利益'
                    }
                    
                    for eng_item, jp_item in income_items.items():
                        if eng_item in income_stmt.index:
                            row_data = {"項目": jp_item}
                            for col in income_stmt.columns[:4]:  # Latest 4 years
                                year = col.strftime('%Y年')
                                value = income_stmt.loc[eng_item, col]
                                if not pd.isna(value):
                                    if eng_item == 'Basic EPS':
                                        row_data[year] = f"${value:.2f}"
                                    else:
                                        # Format with dollar sign in front
                                        if abs(value) >= 1_000_000_000:
                                            row_data[year] = f"${value/1_000_000_000:.2f}B"
                                        elif abs(value) >= 1_000_000:
                                            row_data[year] = f"${value/1_000_000:.1f}M"
                                        else:
                                            row_data[year] = f"${value:,.0f}"
                                else:
                                    row_data[year] = "N/A"
                            income_data.append(row_data)
                    
                    if income_data:
                        income_df = pd.DataFrame(income_data)
                        st.dataframe(income_df, use_container_width=True, hide_index=True)
                    else:
                        st.warning("損益計算書データが利用できません")
                else:
                    st.warning("損益計算書データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 貸借対照表 (Balance Sheet)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 🏦 貸借対照表 (Balance Sheet)")
                
                balance_sheet = stock.balance_sheet
                if not balance_sheet.empty:
                    balance_data = []
                    
                    # Key balance sheet items
                    balance_items = {
                        'Total Assets': '総資産',
                        'Current Assets': '流動資産',
                        'Cash And Cash Equivalents': '現金及び現金同等物',
                        'Total Liabilities Net Minority Interest': '総負債',
                        'Current Liabilities': '流動負債',
                        'Total Equity Gross Minority Interest': '株主資本',
                        'Retained Earnings': '利益剰余金'
                    }
                    
                    for eng_item, jp_item in balance_items.items():
                        if eng_item in balance_sheet.index:
                            row_data = {"項目": jp_item}
                            for col in balance_sheet.columns[:4]:  # Latest 4 years
                                year = col.strftime('%Y年')
                                value = balance_sheet.loc[eng_item, col]
                                if not pd.isna(value):
                                    # Format with dollar sign in front
                                    if abs(value) >= 1_000_000_000:
                                        row_data[year] = f"${value/1_000_000_000:.2f}B"
                                    elif abs(value) >= 1_000_000:
                                        row_data[year] = f"${value/1_000_000:.1f}M"
                                    else:
                                        row_data[year] = f"${value:,.0f}"
                                else:
                                    row_data[year] = "N/A"
                            balance_data.append(row_data)
                    
                    if balance_data:
                        balance_df = pd.DataFrame(balance_data)
                        st.dataframe(balance_df, use_container_width=True, hide_index=True)
                    else:
                        st.warning("貸借対照表データが利用できません")
                else:
                    st.warning("貸借対照表データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # キャッシュフロー計算書 (Cash Flow Statement)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 💰 キャッシュフロー計算書 (Cash Flow Statement)")
                
                cash_flow = stock.cashflow
                if not cash_flow.empty:
                    cf_data = []
                    
                    # Key cash flow items
                    cf_items = {
                        'Operating Cash Flow': '営業キャッシュフロー',
                        'Investing Cash Flow': '投資キャッシュフロー',
                        'Financing Cash Flow': '財務キャッシュフロー',
                        'Free Cash Flow': 'フリーキャッシュフロー',
                        'Capital Expenditure': '設備投資'
                    }
                    
                    for eng_item, jp_item in cf_items.items():
                        if eng_item in cash_flow.index:
                            row_data = {"項目": jp_item}
                            for col in cash_flow.columns[:4]:  # Latest 4 years
                                year = col.strftime('%Y年')
                                value = cash_flow.loc[eng_item, col]
                                if not pd.isna(value):
                                    row_data[year] = format_currency(value, "$")
                                else:
                                    row_data[year] = "N/A"
                            cf_data.append(row_data)
                    
                    if cf_data:
                        cf_df = pd.DataFrame(cf_data)
                        st.dataframe(cf_df, use_container_width=True, hide_index=True)
                    else:
                        st.warning("キャッシュフロー計算書データが利用できません")
                else:
                    st.warning("キャッシュフロー計算書データを取得できませんでした")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 主要財務指標
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📊 主要財務指標")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['eps'] > 0:
                        pe_ratio = auto_data['current_price'] / auto_data['eps']
                        st.metric("PER", f"{pe_ratio:.2f}倍")
                    else:
                        st.metric("PER", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['book_value_per_share'] > 0:
                        pb_ratio = auto_data['current_price'] / auto_data['book_value_per_share']
                        st.metric("PBR", f"{pb_ratio:.2f}倍")
                    else:
                        st.metric("PBR", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['revenue'] > 0:
                        market_cap = auto_data['current_price'] * auto_data['shares_outstanding']
                        ps_ratio = market_cap / auto_data['revenue']
                        st.metric("PSR", f"{ps_ratio:.2f}倍")
                    else:
                        st.metric("PSR", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col4:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    if auto_data['revenue'] > 0 and auto_data['net_income'] > 0:
                        profit_margin = (auto_data['net_income'] / auto_data['revenue']) * 100
                        st.metric("純利益率", f"{profit_margin:.1f}%")
                    else:
                        st.metric("純利益率", "N/A")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"財務データの取得中にエラーが発生しました: {str(e)}")
        
        else:
            st.error("選択された企業の財務データを取得できませんでした。")

# Footer
st.markdown("---")
st.markdown("**注意**: 表示されるデータは最新の決算発表に基づいていますが、投資判断の際は必ず最新の情報を確認してください。")