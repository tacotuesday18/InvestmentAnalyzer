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
    
    /* Hover effects for ALL buttons */
    button[kind="header"]:hover, 
    [data-testid="collapsedControl"]:hover,
    .st-emotion-cache-1rs6os:hover, 
    .st-emotion-cache-17eq0hr:hover,
    section[data-testid="stSidebar"] > div > button:hover,
    .stSidebar > div > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Hide ALL original icons */
    button[kind="header"] svg, 
    [data-testid="collapsedControl"] svg,
    .st-emotion-cache-1rs6os svg, 
    .st-emotion-cache-17eq0hr svg,
    section[data-testid="stSidebar"] > div > button svg,
    .stSidebar > div > button svg {
        display: none !important;
    }
    
    /* Add hamburger icon to ALL buttons */
    button[kind="header"]::after, 
    [data-testid="collapsedControl"]::after,
    .st-emotion-cache-1rs6os::after, 
    .st-emotion-cache-17eq0hr::after,
    section[data-testid="stSidebar"] > div > button::after,
    .stSidebar > div > button::after {
        content: "☰" !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
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
    
    /* Sidebar positioning */
    section[data-testid="stSidebar"] {
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        z-index: 1000 !important;
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
    
    .nav-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        margin: -1rem -1rem 1rem -1rem;
        border-radius: 0 0 15px 15px;
        text-align: center;
        font-weight: 700;
        font-size: 18px;
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #fafafa;
    }
    
    .main-content {
        margin-top: 0;
        padding: 0;
    }
    
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 0;
        text-align: center;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Button Styling */
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
        .app-title {
            font-size: 2rem;
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
        各分析ツールをご利用ください。
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
                <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 20px 40px; border-radius: 12px; font-size: 1.2rem; font-weight: 600; cursor: pointer; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);">
                    無料で始める →
                </button>
                <button style="background: transparent; color: #4a5568; border: 2px solid #e2e8f0; padding: 18px 36px; border-radius: 12px; font-size: 1.1rem; font-weight: 500; cursor: pointer;">
                    デモを見る
                </button>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="display: flex; align-items: center;">
                    <span style="color: #f59e0b; font-size: 1.4rem;">★★★★★</span>
                    <span style="margin-left: 0.75rem; color: #4a5568; font-weight: 700; font-size: 1.2rem;">4.8</span>
                    <span style="margin-left: 0.75rem; color: #6b7280; font-size: 1.1rem;">| 1,500+ レビュー</span>
                </div>
            </div>
        </div>
        <div style="flex: 1; text-align: center; max-width: 500px;">
            <div style="background: white; border-radius: 25px; padding: 2.5rem; box-shadow: 0 25px 80px rgba(0,0,0,0.15); transform: rotate(3deg);">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
                    <div style="font-size: 1.8rem; font-weight: bold;">AAPL分析結果</div>
                </div>
                <div style="text-align: left; color: #4a5568; font-size: 1.1rem;">
                    <div style="margin: 1rem 0;"><strong>現在株価:</strong> $175.25</div>
                    <div style="margin: 1rem 0;"><strong>目標株価:</strong> $195.80</div>
                    <div style="margin: 1rem 0; color: #10b981; font-weight: bold; font-size: 1.2rem;">上昇余地: +11.7%</div>
                    <div style="margin: 1rem 0; background: #10b981; color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.2rem;">買い推奨</div>
                </div>
            </div>
        </div>
    </div>
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

# Solution section
st.markdown("""
<div style="background-color: #d1ecf1; padding: 2rem; margin: 2rem 0; border-left: 4px solid #17a2b8;">
    <h2 style="color: #0c5460; margin-bottom: 1rem;">✨ Kabu2Easyが解決します</h2>
    <div style="color: #0c5460;">
        ✓ <strong>DCF法による科学的な企業価値算定</strong> - 感情に左右されない客観的な判断<br>
        ✓ <strong>財務データの自動分析</strong> - 複雑な計算は全て自動化<br>
        ✓ <strong>分かりやすい投資判断</strong> - 「買い」「売り」「保留」を明確に表示<br>
        ✓ <strong>リスク要因の可視化</strong> - 投資前にリスクを把握<br>
        ✓ <strong>定期的な再評価</strong> - 投資判断を常に最新の状態に保つ
    </div>
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("""
<div style="background: white; padding: 4rem 0;">
    <div style="max-width: 1400px; margin: 0 auto; padding: 0 2rem;">
        <div style="text-align: center; margin-bottom: 4rem;">
            <h2 style="font-size: 3rem; font-weight: 700; color: #1a202c; margin-bottom: 1rem;">
                プロレベルの分析を<br><span style="color: #667eea;">誰でも簡単に</span>
            </h2>
            <p style="font-size: 1.4rem; color: #4a5568; line-height: 1.6;">
                機関投資家が使う本格的な分析手法を、直感的なインターフェースで提供
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 4rem;">
            <div style="background: white; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #1a202c;">DCF価値算定</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    割引キャッシュフロー法による科学的な企業価値計算。複雑な財務モデルを自動化し、本質的価値を瞬時に算出。
                </p>
            </div>
            
            <div style="background: white; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #1a202c;">財務分析</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    売上成長率、利益率、ROEなど重要な財務指標を自動計算。過去のトレンドから将来の成長性を評価。
                </p>
            </div>
            
            <div style="background: white; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #1a202c;">投資判断</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    現在の株価と本質的価値を比較し、明確な投資推奨を提供。上昇余地や下落リスクも数値化。
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA section
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
        <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
            今すぐ始めて、賢い投資家になろう
        </h2>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
            感情的な投資判断から卒業し、データドリブンな投資を始めませんか？
        </p>
        <button style="background: white; color: #667eea; border: none; padding: 20px 40px; border-radius: 12px; font-size: 1.2rem; font-weight: 600; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.2);">
            無料で分析を始める →
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)