import streamlit as st
import datetime
import os
import json
from auth import authenticate_user, create_user
from payment import PaymentProcessor

# ページ設定
st.set_page_config(
    page_title="企業価値分析プロ - 株式分析とDCF法による本質的価値計算",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# 企業価値分析プロ\n企業の本質的価値を計算し、投資判断をサポートする分析ツールです。",
    }
)

# カスタムCSS - Modern Airbnb-style design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styles */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #222222;
    }
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        text-align: center;
        margin: -1rem -1rem 0 -1rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-cta {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .hero-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Feature cards */
    .features-container {
        padding: 4rem 2rem;
        background: #f8f9fa;
    }
    
    .features-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 3rem;
        color: #222222;
    }
    
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #222222;
    }
    
    .feature-description {
        font-size: 1rem;
        color: #717171;
        line-height: 1.6;
    }
    
    /* Stats section */
    .stats-container {
        background: white;
        padding: 4rem 2rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stat-item {
        padding: 1.5rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #717171;
        margin-top: 0.5rem;
    }
    
    /* CTA section */
    .cta-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        text-align: center;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .cta-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Navigation buttons */
    .stButton > button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    
    .stButton > button:hover {
        background: #5a67d8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .features-title, .cta-title {
            font-size: 2rem;
        }
        
        .hero-container, .features-container, .stats-container, .cta-container {
            padding: 3rem 1rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Modern homepage content with customer acquisition focus
st.markdown("""
<div class="hero-container">
    <div class="hero-title">株式投資で失敗していませんか？</div>
    <div class="hero-subtitle">感情に左右されず、データに基づいた投資判断を</div>
    <div class="hero-cta">プロレベルの企業価値分析を今すぐ開始</div>
</div>
""", unsafe_allow_html=True)

# Pain points section
st.markdown("""
<div style="background-color: #fff3cd; padding: 2rem; margin: 2rem 0; border-left: 4px solid #ffc107;">
    <h2 style="color: #856404; margin-bottom: 1rem;">🔥 こんな投資の悩みはありませんか？</h2>
    <div style="color: #856404;">
        ✗ 株価チャートだけを見て感情的に売買してしまう<br>
        ✗ 企業の本当の価値が分からず、割高な株を掴んでしまう<br>
        ✗ 決算書の読み方が分からず、表面的な情報だけで判断<br>
        ✗ いつも「買い」推奨ばかりのアナリストレポートに騙される<br>
        ✗ 複雑なExcelでDCF計算を試みるも、結果に確信が持てない
    </div>
</div>
""", unsafe_allow_html=True)

# Agitation section  
st.markdown("""
<div style="background-color: #f8d7da; padding: 2rem; margin: 2rem 0; border-left: 4px solid #dc3545;">
    <h2 style="color: #721c24; margin-bottom: 1rem;">⚠️ そのまま投資を続けると...</h2>
    <div style="color: #721c24;">
        📉 <strong>市場の暴落時にパニック売り</strong>→ 大きな損失を確定<br>
        💸 <strong>割高な成長株を高値掴み</strong>→ 数年間含み損を抱える<br>
        🎯 <strong>投資根拠が曖昧</strong>→ いつ売買すべきか分からず機会損失<br>
        📊 <strong>感情的な投資判断</strong>→ 長期的な資産形成に失敗<br>
        🔄 <strong>同じ失敗を繰り返す</strong>→ 投資資金が減り続ける
    </div>
</div>
""", unsafe_allow_html=True)

# Solution section
st.markdown("""
<div style="background-color: #d1ecf1; padding: 2rem; margin: 2rem 0; border-left: 4px solid #17a2b8;">
    <h2 style="color: #0c5460; margin-bottom: 1rem;">✅ 1000xStocksが解決します</h2>
    <div style="color: #0c5460;">
        🧮 <strong>プロ級DCF計算</strong>→ 企業の本質的価値を数値で明確化<br>
        📊 <strong>自動財務分析</strong>→ Yahoo Financeから最新データを自動取得<br>
        🔍 <strong>包括的企業評価</strong>→ PER・PBR・PSRを同時比較<br>
        📈 <strong>リアルタイム更新</strong>→ 常に最新の市場データで分析<br>
        🎯 <strong>明確な投資根拠</strong>→ 感情ではなくデータに基づく判断
    </div>
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("""
<div class="features-container">
    <div class="features-title">プロレベルの企業分析ツール</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧮</div>
        <div class="feature-title">DCF価値計算</div>
        <div class="feature-description">割引キャッシュフロー法で企業の本質的価値を算出</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">企業分析</div>
        <div class="feature-description">SWOT分析と競争優位性の詳細評価</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">銘柄比較</div>
        <div class="feature-description">複数企業の多角的な価値評価比較</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">感度分析</div>
        <div class="feature-description">パラメータ変動による価値変化の可視化</div>
    </div>
    """, unsafe_allow_html=True)

# Live market data section
st.markdown("""
<div class="stats-container">
    <h3 style="text-align: center; margin-bottom: 2rem; color: #222;">📈 Live Market Data</h3>
</div>
""", unsafe_allow_html=True)

# Display live prices for popular stocks
try:
    from real_time_fetcher import fetch_current_stock_price, display_market_status
    
    display_market_status()
    
    col1, col2, col3, col4 = st.columns(4)
    popular_tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
    
    for i, ticker in enumerate(popular_tickers):
        with [col1, col2, col3, col4][i]:
            price_data = fetch_current_stock_price(ticker)
            if price_data.get('success'):
                st.metric(
                    label=ticker,
                    value=f"${price_data['price']:.2f}",
                    delta="Live"
                )
            else:
                st.metric(
                    label=ticker,
                    value="N/A",
                    delta="Offline"
                )
except ImportError:
    pass

# Stats section
st.markdown("""
<div class="stats-container">
    <div class="stats-grid">
        <div class="stat-item">
            <span class="stat-number">20+</span>
            <div class="stat-label">分析可能企業</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">5</span>
            <div class="stat-label">評価手法</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">∞</span>
            <div class="stat-label">シナリオ分析</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
st.markdown("<div style='text-align: center; padding: 2rem;'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 企業分析", key="nav_analysis", use_container_width=True):
        st.switch_page("pages/01_企業分析.py")

with col2:
    if st.button("🔍 銘柄比較", key="nav_compare", use_container_width=True):
        st.switch_page("pages/02_銘柄比較.py")

with col3:
    if st.button("🧮 DCF計算機", key="nav_dcf", use_container_width=True):
        st.switch_page("pages/04_DCF価値計算機.py")

with col4:
    if st.button("🎯 銘柄スクリーナー", key="nav_screener", use_container_width=True):
        st.switch_page("pages/03_銘柄スクリーナー.py")

st.markdown("</div>", unsafe_allow_html=True)

# CTA section
st.markdown("""
<div class="cta-container">
    <div class="cta-title">投資判断を科学的に</div>
    <div class="cta-subtitle">感情ではなくデータに基づいた投資戦略を構築しましょう</div>
</div>
""", unsafe_allow_html=True)

# Add floating chatbot component
try:
    from floating_chatbot import render_floating_chatbot
    render_floating_chatbot()
except ImportError:
    pass