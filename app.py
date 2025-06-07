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

# Modern homepage content
st.markdown("""
<div class="hero-container">
    <div class="hero-title">企業価値分析プロ</div>
    <div class="hero-subtitle">DCF法と財務分析で企業の本質的価値を見極める</div>
    <div class="hero-cta">無料で分析を開始</div>
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