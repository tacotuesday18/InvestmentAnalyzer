import streamlit as st
import datetime
import os
import json

# Initialize database first
try:
    from database import setup_database, get_session
    # Setup database tables on first run
    setup_database()
except ImportError:
    st.error("データベースモジュールが見つかりません")
except Exception as e:
    st.warning(f"データベース初期化エラー: {str(e)}")

# Try to import auth functions, use dummy functions if not available
try:
    from auth import authenticate_user, create_user
except ImportError:
    st.warning("認証モジュールが見つかりません。デモモードで実行中...")
    def authenticate_user(username, password):
        return {"success": False, "message": "認証機能は現在利用できません"}
    def create_user(username, email, password):
        return {"success": False, "message": "登録機能は現在利用できません"}
except Exception as e:
    st.error(f"認証モジュールエラー: {str(e)}")
    def authenticate_user(username, password):
        return {"success": False, "message": "認証機能でエラーが発生しました"}
    def create_user(username, email, password):
        return {"success": False, "message": "登録機能でエラーが発生しました"}

# Try to import payment processor
try:
    from payment import PaymentProcessor
except ImportError:
    st.warning("決済モジュールが見つかりません")
    PaymentProcessor = None
except Exception as e:
    st.error(f"決済モジュールエラー: {str(e)}")
    PaymentProcessor = None

# ページ設定
st.set_page_config(
    page_title="Kabu2Easy - 株式分析プラットフォーム",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# カスタムCSS - Clean, modern design with excellent UX
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
    
    /* FIXED: Style ALL possible sidebar control elements */
    button[kind="header"], 
    [data-testid="collapsedControl"],
    .st-emotion-cache-1rs6os, 
    .st-emotion-cache-17eq0hr,
    .st-emotion-cache-1gulkj5,
    section[data-testid="stSidebar"] > div:first-child > button,
    .stSidebar > div:first-child > button,
    button[aria-label="Open sidebar"] {
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
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Hover effects for ALL buttons */
    button[kind="header"]:hover, 
    [data-testid="collapsedControl"]:hover,
    .st-emotion-cache-1rs6os:hover, 
    .st-emotion-cache-17eq0hr:hover,
    .st-emotion-cache-1gulkj5:hover,
    section[data-testid="stSidebar"] > div:first-child > button:hover,
    .stSidebar > div:first-child > button:hover,
    button[aria-label="Open sidebar"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Hide ALL original icons */
    button[kind="header"] svg, 
    [data-testid="collapsedControl"] svg,
    .st-emotion-cache-1rs6os svg, 
    .st-emotion-cache-17eq0hr svg,
    .st-emotion-cache-1gulkj5 svg,
    section[data-testid="stSidebar"] > div:first-child > button svg,
    .stSidebar > div:first-child > button svg,
    button[aria-label="Open sidebar"] svg {
        display: none !important;
    }
    
    /* Add hamburger icon to ALL buttons */
    button[kind="header"]::after, 
    [data-testid="collapsedControl"]::after,
    .st-emotion-cache-1rs6os::after, 
    .st-emotion-cache-17eq0hr::after,
    .st-emotion-cache-1gulkj5::after,
    section[data-testid="stSidebar"] > div:first-child > button::after,
    .stSidebar > div:first-child > button::after,
    button[aria-label="Open sidebar"]::after {
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
    
    /* Style Streamlit page navigation */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
        padding: 1.5rem 0 !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stSidebarNav"] li {
        margin: 10px 0 !important;
    }
    
    [data-testid="stSidebarNav"] a {
        display: flex !important;
        align-items: center !important;
        padding: 14px 18px !important;
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        text-decoration: none !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 600 !important;
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f8f9fa;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        button[kind="header"], 
        [data-testid="collapsedControl"],
        button[aria-label="Open sidebar"] {
            width: 50px !important;
            height: 50px !important;
            top: 15px !important;
            left: 15px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for auto-closing sidebar on navigation
st.markdown("""
<script>
    // Wait for the page to load
    window.addEventListener('load', function() {
        // Function to close sidebar
        function closeSidebar() {
            const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            const collapseButton = window.parent.document.querySelector('[data-testid="collapsedControl"]');
            
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'true') {
                if (collapseButton) {
                    collapseButton.click();
                }
            }
        }
        
        // Add click event listeners to all navigation links
        const navLinks = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                setTimeout(closeSidebar, 300);
            });
        });
        
        // Also handle any custom buttons in sidebar
        const sidebarButtons = window.parent.document.querySelectorAll('.stSidebar button');
        sidebarButtons.forEach(button => {
            if (!button.hasAttribute('data-testid') || button.getAttribute('data-testid') !== 'collapsedControl') {
                button.addEventListener('click', function() {
                    setTimeout(closeSidebar, 300);
                });
            }
        });
    });
    
    // Ensure hamburger button is always visible
    setInterval(function() {
        const collapseButton = window.parent.document.querySelector('[data-testid="collapsedControl"]');
        if (collapseButton) {
            collapseButton.style.display = 'flex';
            collapseButton.style.visibility = 'visible';
            collapseButton.style.opacity = '1';
        }
    }, 500);
</script>
""", unsafe_allow_html=True)

# Initialize session state for auth
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'show_auth_modal' not in st.session_state:
    st.session_state.show_auth_modal = False

# Top right auth button
st.markdown("""
<style>
    .auth-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: white;
        color: #667eea;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #667eea;
    }
    .auth-button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.3);
    }
    .user-badge {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Add navigation in sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1rem 0; border-bottom: 2px solid rgba(255,255,255,0.2); margin-bottom: 1rem;">
        <h2 style="color: white; font-size: 24px; font-weight: 700; margin: 0; text-align: center;">
            📊 Kabu2Easy
        </h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 13px; text-align: center; margin: 0.5rem 0 0 0;">
            株式分析プラットフォーム
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show user info if authenticated
    if st.session_state.authenticated and st.session_state.user:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <div style="color: white; font-size: 14px; font-weight: 600; margin-bottom: 0.5rem;">
                ログイン中: {st.session_state.user.get('username', 'ユーザー')}
            </div>
            <div style="color: rgba(255,255,255,0.8); font-size: 12px;">
                プラン: {st.session_state.user.get('subscription_plan', 'free').upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("ログアウト", key="sidebar_logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    st.markdown("""
    <div style="color: white; padding: 0 0.5rem; font-size: 13px; line-height: 1.5; margin-bottom: 1rem;">
        左のメニューから各ツールにアクセスできます
    </div>
    """, unsafe_allow_html=True)

# Top auth button section
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    if st.session_state.authenticated:
        st.markdown(f"""
        <div class="user-badge">
            👤 {st.session_state.user.get('username', 'ユーザー')}
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("ログイン / 登録", key="top_auth_button", use_container_width=True):
            st.session_state.show_auth_modal = True

# Auth modal
if st.session_state.show_auth_modal and not st.session_state.authenticated:
    with st.container():
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;">
        </div>
        """, unsafe_allow_html=True)
        
        modal_col1, modal_col2, modal_col3 = st.columns([1, 2, 1])
        with modal_col2:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); position: relative; z-index: 10001;">
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔐 ログイン / 新規登録")
            
            tab1, tab2 = st.tabs(["ログイン", "新規登録"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("ユーザー名またはメール", key="login_username")
                    password = st.text_input("パスワード", type="password", key="login_password")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.form_submit_button("ログイン", use_container_width=True):
                            if username and password:
                                result = authenticate_user(username, password)
                                if result['success']:
                                    st.session_state.authenticated = True
                                    st.session_state.user = result['user']
                                    st.session_state.show_auth_modal = False
                                    st.success("ログインに成功しました！")
                                    st.rerun()
                                else:
                                    st.error(result['message'])
                            else:
                                st.error("全ての項目を入力してください")
                    
                    with col_b:
                        if st.form_submit_button("キャンセル", use_container_width=True):
                            st.session_state.show_auth_modal = False
                            st.rerun()
            
            with tab2:
                with st.form("signup_form"):
                    new_username = st.text_input("ユーザー名", key="signup_username")
                    new_email = st.text_input("メールアドレス", key="signup_email")
                    new_password = st.text_input("パスワード", type="password", key="signup_password")
                    new_password_confirm = st.text_input("パスワード（確認）", type="password", key="signup_password_confirm")
                    
                    col_c, col_d = st.columns(2)
                    with col_c:
                        if st.form_submit_button("登録", use_container_width=True):
                            if new_username and new_email and new_password and new_password_confirm:
                                if new_password != new_password_confirm:
                                    st.error("パスワードが一致しません")
                                elif len(new_password) < 6:
                                    st.error("パスワードは6文字以上にしてください")
                                else:
                                    result = create_user(new_username, new_email, new_password)
                                    if result['success']:
                                        st.success("アカウントが作成されました！ログインしてください。")
                                        st.balloons()
                                    else:
                                        st.error(result['message'])
                            else:
                                st.error("全ての項目を入力してください")
                    
                    with col_d:
                        if st.form_submit_button("キャンセル", use_container_width=True):
                            st.session_state.show_auth_modal = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# Clean, centered hero section
st.markdown("""
<div style="max-width: 1200px; margin: 0 auto; padding: 4rem 2rem 2rem 2rem;">
    <div style="text-align: center; margin-bottom: 4rem;">
        <h1 style="font-size: 3rem; font-weight: 700; color: #1a202c; margin-bottom: 1rem; line-height: 1.2;">
            株式投資を<span style="color: #667eea;">データで</span>もっとスマートに
        </h1>
        <p style="font-size: 1.3rem; color: #4a5568; margin-bottom: 2rem; line-height: 1.6;">
            DCF法による科学的な企業価値分析で、感情に左右されない投資判断をサポート
        </p>
        <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2.5rem; border-radius: 50px; font-size: 1.1rem; font-weight: 600; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3); cursor: pointer; transition: all 0.3s ease;">
            今すぐ分析を始める →
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Simple feature cards
st.markdown("""
<div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 3rem 2rem;">
    <h2 style="text-align: center; font-size: 2rem; font-weight: 700; color: #1a202c; margin-bottom: 3rem;">
        主な機能
    </h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">
        
        <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; border: 1px solid #e2e8f0;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.75rem; color: #1a202c;">
                DCF価値算定
            </h3>
            <p style="color: #4a5568; line-height: 1.6; font-size: 0.95rem;">
                割引キャッシュフロー法で企業の本質的価値を計算。複雑な財務モデルを自動化。
            </p>
        </div>
        
        <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; border: 1px solid #e2e8f0;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.75rem; color: #1a202c;">
                財務分析
            </h3>
            <p style="color: #4a5568; line-height: 1.6; font-size: 0.95rem;">
                売上成長率、利益率、ROEなど重要指標を自動計算。過去トレンドから将来性を評価。
            </p>
        </div>
        
        <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; border: 1px solid #e2e8f0;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.75rem; color: #1a202c;">
                投資判断
            </h3>
            <p style="color: #4a5568; line-height: 1.6; font-size: 0.95rem;">
                現在株価と本質的価値を比較。明確な投資推奨と上昇余地を数値化して表示。
            </p>
        </div>
        
    </div>
</div>
""", unsafe_allow_html=True)

# How to use section - Clear navigation guide
st.markdown("""
<div style="max-width: 1200px; margin: 3rem auto; padding: 3rem 2rem; background: linear-gradient(135deg, #f0f4ff 0%, #e6f2ff 100%); border-radius: 20px;">
    <h2 style="text-align: center; font-size: 2rem; font-weight: 700; color: #1a202c; margin-bottom: 2.5rem;">
        使い方は簡単3ステップ
    </h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; max-width: 900px; margin: 0 auto;">
        
        <div style="text-align: center;">
            <div style="background: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);">
                <span style="font-size: 1.8rem; font-weight: 700; color: #667eea;">1</span>
            </div>
            <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; color: #1a202c;">
                左上のメニューを開く
            </h3>
            <p style="color: #4a5568; line-height: 1.5; font-size: 0.95rem;">
                ☰ボタンをクリックして<br>サイドバーを表示
            </p>
        </div>
        
        <div style="text-align: center;">
            <div style="background: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);">
                <span style="font-size: 1.8rem; font-weight: 700; color: #667eea;">2</span>
            </div>
            <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; color: #1a202c;">
                分析ツールを選択
            </h3>
            <p style="color: #4a5568; line-height: 1.5; font-size: 0.95rem;">
                DCF分析、財務分析など<br>使いたいツールを選択
            </p>
        </div>
        
        <div style="text-align: center;">
            <div style="background: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);">
                <span style="font-size: 1.8rem; font-weight: 700; color: #667eea;">3</span>
            </div>
            <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; color: #1a202c;">
                銘柄を分析
            </h3>
            <p style="color: #4a5568; line-height: 1.5; font-size: 0.95rem;">
                銘柄コードを入力して<br>即座に分析結果を確認
            </p>
        </div>
        
    </div>
</div>
""", unsafe_allow_html=True)

# Benefits section
st.markdown("""
<div style="max-width: 1200px; margin: 3rem auto; padding: 0 2rem;">
    <div style="background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
        <h2 style="text-align: center; font-size: 2rem; font-weight: 700; color: #1a202c; margin-bottom: 2rem;">
            Kabu2Easyで解決できること
        </h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <h3 style="font-size: 1.1rem; font-weight: 600; color: #dc2626; margin-bottom: 1rem;">
                    ❌ よくある投資の悩み
                </h3>
                <ul style="color: #4a5568; line-height: 2; padding-left: 1.5rem;">
                    <li>感情的な売買で損失</li>
                    <li>割高な株を掴んでしまう</li>
                    <li>決算書が読めない</li>
                    <li>正確な価値が分からない</li>
                </ul>
            </div>
            <div>
                <h3 style="font-size: 1.1rem; font-weight: 600; color: #059669; margin-bottom: 1rem;">
                    ✓ Kabu2Easyなら
                </h3>
                <ul style="color: #4a5568; line-height: 2; padding-left: 1.5rem;">
                    <li>データに基づく客観的判断</li>
                    <li>本質的価値で適正価格を把握</li>
                    <li>財務データを自動分析</li>
                    <li>科学的なDCF法で算定</li>
                </ul>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA section
st.markdown("""
<div style="max-width: 800px; margin: 4rem auto 2rem auto; padding: 0 2rem;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 3rem; text-align: center; color: white;">
        <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">
            賢い投資家への第一歩を
        </h2>
        <p style="font-size: 1.1rem; opacity: 0.95; margin-bottom: 2rem;">
            左上のメニューから今すぐ分析を始めましょう
        </p>
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: white; color: #667eea; padding: 1rem 2rem; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer;">
            <span>☰</span>
            <span>メニューを開く</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="max-width: 1200px; margin: 3rem auto 1rem auto; padding: 2rem; text-align: center; color: #6b7280; font-size: 0.9rem; border-top: 1px solid #e2e8f0;">
    <p>© 2024 Kabu2Easy. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
