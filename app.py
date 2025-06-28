#!/usr/bin/env python3
"""
Main entry point for the Stock Analysis Platform - Kabu2Easy
Comprehensive business analysis platform delivering financial insights through advanced data visualization.
This is the deployment-ready main application file.
"""

import streamlit as st
import datetime
import os
import json
import sys

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import required modules
try:
    from auth import authenticate_user, create_user
    from payment import PaymentProcessor
except ImportError:
    # Graceful fallback if auth modules are not available
    pass

# ページ設定
st.set_page_config(
    page_title="企業価値分析プロ - 株式分析とDCF法による本質的価値計算",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# カスタムCSS - Modern Airbnb-style design
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
    
    /* Style ALL possible sidebar control elements */
    button[kind="header"], 
    [data-testid="collapsedControl"],
    .st-emotion-cache-1rs6os, 
    .st-emotion-cache-17eq0hr,
    section[data-testid="stSidebar"] > div > button,
    .stSidebar > div > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 9999 !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    button[kind="header"]:hover,
    [data-testid="collapsedControl"]:hover,
    .st-emotion-cache-1rs6os:hover, 
    .st-emotion-cache-17eq0hr:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Sidebar with purple gradient */
    .stSidebar, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        border-right: none !important;
    }
    
    .stSidebar .stMarkdown, 
    .stSidebar .stSelectbox,
    .stSidebar .stButton,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stButton {
        color: white !important;
    }
    
    .stSidebar a, section[data-testid="stSidebar"] a {
        color: white !important;
        text-decoration: none !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        display: block !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSidebar a:hover, section[data-testid="stSidebar"] a:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
    }
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #fafbfc;
    }
    
    /* Header styles */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 0;
        margin: -1rem -6rem 0 -6rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .app-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Navigation styles */
    .nav-header {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Main content container */
    .main-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        height: 240px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-size: 0.9rem;
        color: #4a5568;
        line-height: 1.5;
    }
    
    /* Features section */
    .features-container {
        margin: 4rem 0 3rem 0;
        text-align: center;
    }
    
    .features-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-header {
            margin: -1rem -1rem 0 -1rem;
        }
        
        .main-content {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Top navigation bar
st.markdown("""
<div class="app-header">
    <h1 class="app-title">Kabu2Easy - 株式分析プラットフォーム</h1>
</div>
""", unsafe_allow_html=True)

# Add navigation help in sidebar
with st.sidebar:
    st.markdown('<div class="nav-header">📊 株式分析メニュー</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: white; padding: 1rem; font-size: 14px; line-height: 1.6;">
        上記のページリンクをクリックして<br/>
        各種分析ツールをご利用ください。
    </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Full-screen Hero section
st.markdown("""
<div style="background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 100%); padding: 6rem 0; margin: -1rem -6rem 3rem -6rem; min-height: 80vh; display: flex; align-items: center;">
    <div style="max-width: 1400px; margin: 0 auto; padding: 0 2rem; display: flex; align-items: center; gap: 4rem; width: 100%;">
        <div style="flex: 1; max-width: 600px;">
            <div style="font-size: 4rem; font-weight: 700; color: #1a202c; line-height: 1.1; margin-bottom: 2rem;">
                株式投資を<br>
                <span style="color: #667eea;">もっと簡単に</span><br>
                <span style="color: #764ba2;">もっとスマートに</span>
            </div>
            <div style="font-size: 1.4rem; color: #4a5568; margin-bottom: 3rem; line-height: 1.6;">
                Kabu2Easyは企業の本質的価値を瞬時に分析し、データに基づいた投資判断をサポートします。
            </div>
            <div style="display: flex; gap: 1.5rem; align-items: center; margin-bottom: 3rem;">
                <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 20px 40px; border-radius: 12px; font-size: 1.2rem; font-weight: 600; cursor: pointer; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); transition: all 0.3s ease;" 
                onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 10px 30px rgba(102, 126, 234, 0.6)'"
                onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.4)'">
                    今すぐ分析開始
                </button>
                <div style="color: #4a5568; font-size: 1rem;">
                    ✓ 無料で利用開始<br>
                    ✓ 登録不要ですぐ使える
                </div>
            </div>
        </div>
        <div style="flex: 1; max-width: 600px;">
            <div style="background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 20px 60px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;">
                <div style="font-size: 1.8rem; font-weight: 600; color: #1a202c; margin-bottom: 2rem; text-align: center;">
                    🎯 こんな悩みありませんか？
                </div>
                <div style="color: #4a5568; font-size: 1.1rem; line-height: 1.8;">
                    ✗ どの株が割安なのか判断できない<br>
                    ✗ 企業分析のやり方が分からない<br>
                    ✗ DCF法を使いたいけど計算が複雑<br>
                    ✗ 決算書を読むのに時間がかかりすぎる<br>
                    ✗ 投資の根拠を明確にしたい<br>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Value proposition section
st.markdown("""
<div style="background: white; padding: 4rem 2rem; margin: 0 -6rem;">
    <div style="max-width: 1400px; margin: 0 auto; text-align: center;">
        <div style="font-size: 2.5rem; font-weight: 700; color: #1a202c; margin-bottom: 2rem;">
            Kabu2Easyが選ばれる理由
        </div>
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 3rem; border-radius: 20px; color: #4a5568; font-size: 1.2rem; line-height: 1.8; text-align: left; max-width: 900px; margin: 0 auto;">
            🧮 <strong>瞬間DCF計算</strong>→ 企業の本質的価値を数値で明確化<br>
            📊 <strong>自動財務分析</strong>→ Yahoo Financeから最新データを自動取得<br>
            🔍 <strong>包括的企業評価</strong>→ PER・PBR・PSRを同時比較<br>
            📈 <strong>リアルタイム更新</strong>→ 常に最新の市場データで分析<br>
            🎯 <strong>明確な投資根拠</strong>→ 感情ではなくデータに基づく判断
        </div>
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
        <div class="feature-icon">⚖️</div>
        <div class="feature-title">銘柄比較</div>
        <div class="feature-description">複数企業の財務指標を同時比較分析</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">銘柄発見</div>
        <div class="feature-description">投資スタイル別の銘柄スクリーニング</div>
    </div>
    """, unsafe_allow_html=True)

# Quick access section
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4rem 2rem; margin: 4rem -6rem 0 -6rem;">
    <div style="max-width: 1400px; margin: 0 auto; text-align: center;">
        <div style="color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem;">
            今すぐ始めましょう
        </div>
        <div style="color: rgba(255,255,255,0.9); font-size: 1.3rem; margin-bottom: 3rem; line-height: 1.6;">
            左上のメニューボタン（☰）をクリックして、分析ツールにアクセス
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem 2rem; border-radius: 12px; backdrop-filter: blur(10px);">
                <div style="color: white; font-weight: 600; margin-bottom: 0.5rem;">ステップ 1</div>
                <div style="color: rgba(255,255,255,0.8);">企業名やティッカーを検索</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem 2rem; border-radius: 12px; backdrop-filter: blur(10px);">
                <div style="color: white; font-weight: 600; margin-bottom: 0.5rem;">ステップ 2</div>
                <div style="color: rgba(255,255,255,0.8);">自動で財務データを取得</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem 2rem; border-radius: 12px; backdrop-filter: blur(10px);">
                <div style="color: white; font-weight: 600; margin-bottom: 0.5rem;">ステップ 3</div>
                <div style="color: rgba(255,255,255,0.8);">詳細分析レポートを確認</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)