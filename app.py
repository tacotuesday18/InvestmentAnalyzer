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
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# 企業価値分析プロ\n企業の本質的価値を計算し、投資判断をサポートする分析ツールです。",
    }
)

# カスタムCSS
st.markdown("""
<style>
    /* 全体のフォントとカラー */
    body {
        font-family: 'Noto Sans JP', sans-serif;
        color: #333;
    }
    
    /* メインタイトル */
    .main-title {
        font-size: 3.5rem !important;
        color: #0066cc;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* モバイル対応 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem !important;
        }
        
        .subtitle {
            font-size: 1rem !important;
        }
        
        /* コンテナに最大幅を設定して小さな画面でも見やすく */
        .container {
            max-width: 100% !important;
            padding: 0 10px !important;
        }
        
        /* モバイルでは余白を減らす */
        .stButton>button {
            width: 100%;
            margin: 0.2rem 0;
        }
        
        /* グラフの高さをモバイルで調整 */
        .plotly-graph {
            height: 300px !important;
        }
    }
    
    /* サブタイトル */
    .subtitle {
        font-size: 1.2rem !important;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* レスポンシブグリッド */
    .responsive-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
    }
    
    /* カード要素 */
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* カードタイトル */
    .card-title {
        font-size: 1.4rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
    }
    
    /* プランカード（ハイライト用） */
    .plan-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .plan-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .plan-card-highlight {
        background-color: #e6f7ff;
        border: 2px solid #0066cc;
    }
    
    /* フォーム要素 */
    .form-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* ボタン要素 */
    .stButton>button {
        font-weight: bold !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* フィーチャーセクション */
    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .feature-icon {
        color: #0066cc;
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    /* ユーザーメニュー */
    .user-menu {
        text-align: right;
        margin-bottom: 1rem;
    }
    
    /* ダークモードサポート */
    @media (prefers-color-scheme: dark) {
        .card, .form-container, .plan-card {
            background-color: #262730;
        }
        
        .plan-card-highlight {
            background-color: #0e3450;
            border: 2px solid #4d94ff;
        }
    }
    
    /* テーブルスタイル */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .styled-table thead tr {
        background-color: #0066cc;
        color: white;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    
    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #0066cc;
    }
    
    /* 区切り線 */
    hr {
        margin: 2rem 0;
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0));
    }
    
    /* フッター */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #777;
        font-size: 0.9rem;
    }
    
    /* モバイル対応 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }
        
        .subtitle {
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

# ログイン状態管理
def login_user(username, password):
    """ユーザーをログインする"""
    result = authenticate_user(username, password)
    if result['success']:
        st.session_state.logged_in = True
        st.session_state.user = result['user']
        return True, result['message']
    else:
        return False, result['message']

def logout_user():
    """ユーザーをログアウトする"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.current_page = 'login'

def signup_user(username, email, password, confirm_password):
    """新しいユーザーを登録する"""
    if password != confirm_password:
        return False, "パスワードが一致しません。"
    
    result = create_user(username, email, password)
    if result['success']:
        return True, result['message']
    else:
        return False, result['message']

def switch_page(page_name):
    """表示するページを切り替える"""
    st.session_state.current_page = page_name

# ページヘッダー・ナビゲーション
def display_header():
    """ヘッダーとナビゲーションを表示"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='main-title'>💹 企業価値分析プロ</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>収益成長率と割引率から企業の本質的価値を計算し、投資判断をサポートする高度な分析ツール</p>", unsafe_allow_html=True)
    
    with col2:
        if st.session_state.logged_in:
            st.markdown(f"<div class='user-menu'><p>👤 {st.session_state.user['username']} さん</p></div>", unsafe_allow_html=True)
            if st.button("ログアウト", key="header_logout_btn"):
                logout_user()
        else:
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                if st.button("ログイン", key="header_login_btn", use_container_width=True):
                    switch_page('login')
            with col2_2:
                if st.button("登録", key="header_signup_btn", use_container_width=True):
                    switch_page('signup')

# ログインページ
def show_login_page():
    """ログインページを表示"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 左側に価値提案を表示
        st.markdown("<h2 style='color: #0066cc;'>投資の意思決定を強化する</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
                企業価値分析プロは、投資家が企業の本質的価値を正確に評価し、データに基づいた投資判断を行うためのツールです。
            </p>
            
            <h3 style="color: #0066cc; font-size: 1.3rem;">私たちの提供する価値</h3>
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background-color: #e6f7ff; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                    <span style="color: #0066cc; font-size: 1.2rem;">🔍</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #333;">正確な企業価値の算出</h4>
                    <p style="margin: 0; color: #666;">DCF法を用いた本質的価値の計算により、株価の割安度を評価します。</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background-color: #e6f7ff; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                    <span style="color: #0066cc; font-size: 1.2rem;">📊</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #333;">包括的な企業分析</h4>
                    <p style="margin: 0; color: #666;">財務指標、SWOT分析、競争優位性の評価を一つのダッシュボードで確認できます。</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background-color: #e6f7ff; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                    <span style="color: #0066cc; font-size: 1.2rem;">📈</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #333;">感度分析機能</h4>
                    <p style="margin: 0; color: #666;">成長率や割引率の変動が企業価値に与える影響を視覚的に確認できます。</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: center;">
                <div style="background-color: #e6f7ff; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                    <span style="color: #0066cc; font-size: 1.2rem;">⏱️</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #333;">時間の節約</h4>
                    <p style="margin: 0; color: #666;">複雑な財務モデリングを数分で完了し、投資判断に集中できます。</p>
                </div>
            </div>
        </div>
        
        <div style="background-color: #f0f9ff; padding: 15px; border-radius: 10px; border-left: 4px solid #0066cc;">
            <p style="margin: 0; color: #333; font-style: italic;">
                「企業価値分析プロを使い始めてから、投資判断の精度が格段に向上しました。特に感度分析機能は、様々なシナリオを検討するのに非常に役立っています。」
            </p>
            <p style="margin: 5px 0 0; text-align: right; color: #666;">
                - 山田太郎, 個人投資家
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    
    with col2:
        # 右側にログインフォームを表示
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>ログイン</h2>", unsafe_allow_html=True)
        
        username = st.text_input("ユーザー名またはメールアドレス")
        password = st.text_input("パスワード", type="password")
        
        if st.button("ログイン", key="login_form_btn", use_container_width=True):
            if username and password:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("ユーザー名とパスワードを入力してください。")
        
        st.markdown("<p style='text-align: center; margin-top: 1rem;'>アカウントをお持ちでない場合は<a href='javascript:void(0);' onclick='document.querySelector(\"[data-testid=root] button:last-child\").click();'>こちら</a>から登録できます。</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("新規登録ページへ", key="to_signup"):
            switch_page('signup')

# サインアップページ
def show_signup_page():
    """サインアップページを表示"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 左側に価値提案を表示
        st.markdown("<h2 style='color: #0066cc;'>データに基づく投資判断を始めましょう</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
                企業価値分析プロは、複雑な財務分析を簡単に行い、データに基づいた投資判断をサポートします。
            </p>
            
            <h3 style="color: #0066cc; font-size: 1.3rem;">無料プランでできること</h3>
            
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>月3社まで企業の本質的価値を分析</div>
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>DCF法による株価評価</div>
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>シンプルなSWOT分析で企業の強みと弱みを把握</div>
                </li>
            </ul>
            
            <h3 style="color: #0066cc; font-size: 1.3rem; margin-top: 1.5rem;">有料プランの特典</h3>
            
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>より多くの企業を分析可能（ベーシック：月20社、プレミアム：無制限）</div>
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>感度分析機能で様々なシナリオを検討</div>
                </li>
                <li style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div style="color: #0066cc; margin-right: 10px;">✓</div>
                    <div>最新の決算情報の詳細な分析（プレミアムプラン）</div>
                </li>
            </ul>
        </div>
        
        <div style="background-color: #f0f9ff; padding: 15px; border-radius: 10px; border-left: 4px solid #0066cc;">
            <p style="margin: 0; color: #333; font-style: italic;">
                「投資に関する重要な判断を下す際の根拠として、この分析ツールは非常に信頼性があります。DCF法の詳細な計算が自動化されているため、手作業での計算ミスを心配する必要がありません。」
            </p>
            <p style="margin: 5px 0 0; text-align: right; color: #666;">
                - 佐藤次郎, 証券アナリスト
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 右側に登録フォームを表示
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>新規アカウント登録</h2>", unsafe_allow_html=True)
        
        username = st.text_input("ユーザー名（半角英数）")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        confirm_password = st.text_input("パスワード（確認）", type="password")
        
        terms_agreed = st.checkbox("利用規約とプライバシーポリシーに同意します")
        
        if st.button("登録する", key="signup_form_btn", use_container_width=True):
            if username and email and password and confirm_password:
                if terms_agreed:
                    success, message = signup_user(username, email, password, confirm_password)
                    if success:
                        st.success(message)
                        st.info("登録が完了しました。ログインしてください。")
                        switch_page('login')
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("利用規約とプライバシーポリシーに同意する必要があります。")
            else:
                st.warning("すべての項目を入力してください。")
        
        st.markdown("<p style='text-align: center; margin-top: 1rem;'>すでにアカウントをお持ちの場合は<a href='javascript:void(0);' onclick='document.querySelector(\"[data-testid=root] button:last-child\").click();'>こちら</a>からログインできます。</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("ログインページへ", key="to_login"):
            switch_page('login')

# プランの紹介・選択ページ
def show_plans():
    """サブスクリプションプランの紹介と選択画面を表示"""
    st.markdown("<h2 style='text-align: center;'>サブスクリプションプラン</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>あなたのニーズに合ったプランをお選びください。</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # 無料プラン
    with col1:
        st.markdown("""
        <div class='plan-card'>
            <h3 style='text-align: center;'>🆓 無料プラン</h3>
            <h2 style='text-align: center; color: #0066cc;'>¥0</h2>
            <p style='text-align: center; color: #666;'>月額</p>
            <hr>
            <ul>
                <li>基本的な企業分析</li>
                <li>DCF法による株価評価</li>
                <li>シンプルなSWOT分析</li>
                <li>月3社まで分析可能</li>
            </ul>
            <div style='height: 50px;'></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("現在のプラン" if st.session_state.logged_in and st.session_state.user['subscription_plan'] == 'free' else "選択する", key="free_plan", use_container_width=True, disabled=not st.session_state.logged_in or st.session_state.user['subscription_plan'] == 'free'):
            st.success("無料プランが選択されました。")
    
    # ベーシックプラン
    with col2:
        st.markdown("""
        <div class='plan-card plan-card-highlight'>
            <h3 style='text-align: center;'>🔹 ベーシックプラン</h3>
            <h2 style='text-align: center; color: #0066cc;'>¥2,500</h2>
            <p style='text-align: center; color: #666;'>月額</p>
            <hr>
            <ul>
                <li>基本的な企業分析</li>
                <li>DCF法による株価評価</li>
                <li>詳細なSWOT分析</li>
                <li>決算情報の詳細分析</li>
                <li>財務指標の詳細比較</li>
                <li>月20社まで分析可能</li>
            </ul>
            <div style='height: 10px;'></div>
        </div>
        """, unsafe_allow_html=True)
        button_text = "現在のプラン" if st.session_state.logged_in and st.session_state.user['subscription_plan'] == 'basic' else "アップグレード"
        button_disabled = not st.session_state.logged_in or st.session_state.user['subscription_plan'] == 'basic'
        if st.button(button_text, key="basic_plan", use_container_width=True, disabled=button_disabled):
            switch_page('payment')
            st.session_state.selected_plan = 'basic'
            st.rerun()
    
    # プレミアムプラン
    with col3:
        st.markdown("""
        <div class='plan-card'>
            <h3 style='text-align: center;'>💎 プレミアムプラン</h3>
            <h2 style='text-align: center; color: #0066cc;'>¥4,900</h2>
            <p style='text-align: center; color: #666;'>月額</p>
            <hr>
            <ul>
                <li>基本的な企業分析</li>
                <li>DCF法による株価評価</li>
                <li>詳細なSWOT分析</li>
                <li>決算情報の詳細分析</li>
                <li>財務指標の詳細比較</li>
                <li>業界詳細レポート</li>
                <li>感度分析機能</li>
                <li>DCF価値の感度分析</li>
                <li>優先カスタマーサポート</li>
                <li>無制限の企業分析</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        button_text = "現在のプラン" if st.session_state.logged_in and st.session_state.user['subscription_plan'] == 'premium' else "アップグレード"
        button_disabled = not st.session_state.logged_in or st.session_state.user['subscription_plan'] == 'premium'
        if st.button(button_text, key="premium_plan", use_container_width=True, disabled=button_disabled):
            switch_page('payment')
            st.session_state.selected_plan = 'premium'
            st.rerun()

# 支払い画面
def show_payment_page():
    """支払い情報入力画面を表示"""
    if not st.session_state.logged_in:
        st.warning("支払い処理を行うにはログインが必要です。")
        if st.button("ログインページへ", key="payment_login_btn"):
            switch_page('login')
        return
    
    if 'selected_plan' not in st.session_state:
        st.session_state.selected_plan = 'basic'
    
    plan_details = PaymentProcessor.get_plan_details(st.session_state.selected_plan)
    
    st.markdown("<h2 style='text-align: center;'>お支払い情報の入力</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>選択されたプラン: <strong>{plan_details['name']}</strong> (¥{plan_details['price']:,}/月)</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    
    payment_method = st.radio(
        "お支払い方法を選択してください:",
        options=["クレジットカード", "銀行振込", "コンビニ決済"],
        index=0
    )
    
    if payment_method == "クレジットカード":
        st.markdown("### クレジットカード情報")
        card_number = st.text_input("カード番号", placeholder="1234 5678 9012 3456")
        col1, col2 = st.columns(2)
        with col1:
            expiry = st.text_input("有効期限 (MM/YY)", placeholder="12/25")
        with col2:
            cvc = st.text_input("セキュリティコード", type="password", placeholder="123")
        cardholder = st.text_input("カード名義人", placeholder="TARO YAMADA")
    elif payment_method == "銀行振込":
        st.markdown("### 銀行振込情報")
        st.info("以下の口座にお振込みください。お振込み後、確認ボタンを押してください。")
        st.markdown("""
        銀行名: サンプル銀行<br>
        支店名: 本店<br>
        口座種類: 普通<br>
        口座番号: 1234567<br>
        口座名義: カブシキガイシャサンプル<br>
        振込金額: ¥{:,}<br>
        """.format(plan_details['price']), unsafe_allow_html=True)
    else:  # コンビニ決済
        st.markdown("### コンビニ決済情報")
        st.info("以下の情報を入力すると、コンビニ決済用の払込票が発行されます。")
        st.selectbox("コンビニエンスストア", ["セブンイレブン", "ローソン", "ファミリーマート", "ミニストップ", "セイコーマート"])
        st.text_input("電話番号", placeholder="090-1234-5678")
    
    st.markdown("### お客様情報")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("氏名", value=st.session_state.user['username'])
    with col2:
        st.text_input("メールアドレス", value=st.session_state.user['email'])
    
    st.markdown("### 利用規約")
    terms_agreed = st.checkbox("利用規約・キャンセルポリシーに同意する")
    
    if st.button("支払いを完了する", key="complete_payment_btn", use_container_width=True, disabled=not terms_agreed):
        # 支払い処理（サンプル）
        payment_result = PaymentProcessor.process_payment(
            st.session_state.user['id'],
            st.session_state.selected_plan,
            payment_method.lower().replace(" ", "_"),
            {}  # 実際の実装では、カード情報などを安全に処理
        )
        
        if payment_result['success']:
            st.success(payment_result['message'])
            st.success("お支払いが完了しました。ありがとうございます！")
            st.session_state.user['subscription_plan'] = st.session_state.selected_plan
            if st.button("ホームに戻る", key="back_to_home_btn"):
                switch_page('home')
                st.rerun()
        else:
            st.error(payment_result['message'])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("プラン選択に戻る", key="back_to_plans_btn"):
        switch_page('plans')
        st.rerun()

# ホームページ（ダッシュボード）
def show_home():
    """ホームページ/ダッシュボードを表示"""
    if not st.session_state.logged_in:
        st.warning("この機能を利用するにはログインが必要です。")
        st.button("ログインページへ", on_click=lambda: switch_page('login'))
        return
    
    st.markdown("<h2>ダッシュボード</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-title'>📊 企業分析</h3>", unsafe_allow_html=True)
        st.markdown("DCF法による株価評価や詳細なSWOT分析など、企業の本質的価値を分析します。")
        if st.button("企業分析へ", use_container_width=True):
            st.switch_page("pages/01_企業分析.py")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-title'>🔍 銘柄比較</h3>", unsafe_allow_html=True)
        st.markdown("複数の銘柄を選択して様々な評価方法（PER、PBR、PSR、DCF法）で比較分析します。")
        if st.button("銘柄比較へ", use_container_width=True):
            st.switch_page("pages/02_銘柄比較.py")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-title'>📝 分析履歴</h3>", unsafe_allow_html=True)
        st.markdown("過去に行った企業分析の履歴を確認し、最新情報で更新することができます。")
        if st.button("分析履歴へ", use_container_width=True):
            st.switch_page("pages/03_分析履歴.py")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # アカウント情報
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='card-title'>👤 アカウント情報</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**ユーザー名**: {st.session_state.user['username']}")
        st.markdown(f"**メールアドレス**: {st.session_state.user['email']}")
        st.markdown(f"**プラン**: {PaymentProcessor.get_plan_details(st.session_state.user['subscription_plan'])['name']}")
    
    with col2:
        st.markdown(f"**分析回数**: {st.session_state.user['analysis_count']} / {PaymentProcessor.get_plan_details(st.session_state.user['subscription_plan'])['analysis_limit']} 回")
        if st.session_state.user['subscription_plan'] != 'free':
            # サブスクリプション情報の取得（サンプル）
            subscription = PaymentProcessor.check_subscription_status(st.session_state.user['id'])
            if subscription['success'] and 'end_date' in subscription:
                st.markdown(f"**サブスクリプション終了日**: {subscription['end_date']}")
        
        if st.session_state.user['subscription_plan'] == 'free':
            if st.button("プランをアップグレード"):
                switch_page('plans')
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 最近の分析
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='card-title'>🕒 最近の分析</h3>", unsafe_allow_html=True)
    
    # サンプルデータ（実際の実装ではデータベースから取得）
    recent_analyses = [
        {"id": 1, "company": "Apple Inc.", "date": "2023-05-01", "dcf_price": 178.42, "current_price": 175.04, "potential": 1.93},
        {"id": 2, "company": "Microsoft Corporation", "date": "2023-05-02", "dcf_price": 410.25, "current_price": 386.77, "potential": 6.07},
        {"id": 3, "company": "Tesla, Inc.", "date": "2023-05-03", "dcf_price": 224.50, "current_price": 235.87, "potential": -4.82}
    ]
    
    if recent_analyses:
        # テーブルのHTMLを作成
        table_html = """
        <table class="styled-table">
            <thead>
                <tr>
                    <th>企業名</th>
                    <th>分析日</th>
                    <th>DCF価値 (USD)</th>
                    <th>現在価格 (USD)</th>
                    <th>上昇余地 (%)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for analysis in recent_analyses:
            # 上昇余地の表示形式（正/負）
            potential_class = "positive" if analysis["potential"] > 0 else "negative"
            potential_sign = "+" if analysis["potential"] > 0 else ""
            
            table_html += f"""
            <tr>
                <td>{analysis["company"]}</td>
                <td>{analysis["date"]}</td>
                <td>${analysis["dcf_price"]:.2f}</td>
                <td>${analysis["current_price"]:.2f}</td>
                <td class="{potential_class}">{potential_sign}{analysis["potential"]:.2f}%</td>
            </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        if st.button("すべての分析履歴を見る"):
            st.switch_page("pages/03_分析履歴.py")
    else:
        st.info("まだ分析履歴がありません。企業分析を行って本質的価値を計算しましょう。")
        if st.button("分析を始める"):
            st.switch_page("pages/01_企業分析.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

# フッター
def show_footer():
    """フッターを表示"""
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("© 2023 企業価値分析プロ. All rights reserved.", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("[企業情報](#)")
    with col2:
        st.markdown("[利用規約](#)")
    with col3:
        st.markdown("[プライバシーポリシー](#)")
    with col4:
        st.markdown("[お問い合わせ](#)")
    
    st.markdown("</div>", unsafe_allow_html=True)

# メイン処理
display_header()

if st.session_state.current_page == 'login':
    show_login_page()
elif st.session_state.current_page == 'signup':
    show_signup_page()
elif st.session_state.current_page == 'plans':
    show_plans()
elif st.session_state.current_page == 'payment':
    show_payment_page()
else:  # ホーム/ダッシュボード
    if st.session_state.logged_in:
        show_home()
    else:
        # ログインしていない場合はランディングページを表示
        # ランディングページの内容
        st.markdown("<h2 style='text-align: center;'>企業の本質的価値を計算し、スマートな投資判断をサポート</h2>", unsafe_allow_html=True)
        
        # 3つの特徴
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>🧮 高度な財務分析</h3>", unsafe_allow_html=True)
            st.markdown("<p>DCF法による本質的価値計算、成長率と割引率の感度分析、財務指標の業界比較など、プロレベルの分析ツールを提供します。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>📊 包括的なデータ可視化</h3>", unsafe_allow_html=True)
            st.markdown("<p>財務予測、SWOT分析、モート（競争優位性）分析、リスク要因など、投資判断に必要な情報を直感的なチャートで表示します。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>🤝 使いやすさを追求</h3>", unsafe_allow_html=True)
            st.markdown("<p>複雑な財務モデリングの知識がなくても、必要なパラメータを入力するだけで、プロフェッショナルな分析結果を得られます。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 主要な機能紹介
        st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>主要機能</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-title'>DCF法による本質的価値計算</h3>", unsafe_allow_html=True)
            st.image("https://via.placeholder.com/600x300?text=DCF+Value+Calculation", use_column_width=True)
            st.markdown("<p>収益成長率と割引率に基づいて企業の本質的価値を計算し、現在の株価と比較することで投資判断をサポートします。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-title'>感度分析マトリックス</h3>", unsafe_allow_html=True)
            st.image("https://via.placeholder.com/600x300?text=Sensitivity+Analysis+Matrix", use_column_width=True)
            st.markdown("<p>成長率と割引率の変動が企業価値に与える影響を視覚化し、リスク要因の分析を支援します。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-title'>包括的なSWOT分析</h3>", unsafe_allow_html=True)
            st.image("https://via.placeholder.com/600x300?text=SWOT+Analysis", use_column_width=True)
            st.markdown("<p>企業の強み、弱み、機会、脅威を業界特性と成長性に基づいて自動的に分析し、投資リスクと機会を評価します。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-title'>財務指標の業界比較</h3>", unsafe_allow_html=True)
            st.image("https://via.placeholder.com/600x300?text=Financial+Ratios+Comparison", use_column_width=True)
            st.markdown("<p>PER, PBR, PSRなどの主要な財務指標を業界平均と比較し、企業の相対的な割安度と投資適正を評価します。</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # プラン紹介（簡易版）
        st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>料金プラン</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='plan-card'>
                <h3 style='text-align: center;'>🆓 無料プラン</h3>
                <h2 style='text-align: center; color: #0066cc;'>¥0</h2>
                <p style='text-align: center;'>月額</p>
                <ul>
                    <li>基本的な企業分析</li>
                    <li>DCF法による株価評価</li>
                    <li>月3社まで分析可能</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='plan-card plan-card-highlight'>
                <h3 style='text-align: center;'>🔹 ベーシックプラン</h3>
                <h2 style='text-align: center; color: #0066cc;'>¥2,500</h2>
                <p style='text-align: center;'>月額</p>
                <ul>
                    <li>基本的な企業分析</li>
                    <li>DCF法による株価評価</li>
                    <li>詳細なSWOT分析</li>
                    <li>決算情報の詳細分析</li>
                    <li>月20社まで分析可能</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='plan-card'>
                <h3 style='text-align: center;'>💎 プレミアムプラン</h3>
                <h2 style='text-align: center; color: #0066cc;'>¥4,900</h2>
                <p style='text-align: center;'>月額</p>
                <ul>
                    <li>基本的な企業分析</li>
                    <li>DCF法による株価評価</li>
                    <li>詳細なSWOT分析</li>
                    <li>決算情報の詳細分析</li>
                    <li>感度分析機能</li>
                    <li>無制限の企業分析</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # CTAボタン
        st.markdown("<div style='text-align: center; margin-top: 2rem; margin-bottom: 3rem;'>", unsafe_allow_html=True)
        if st.button("無料で始める", use_container_width=True):
            switch_page('signup')
        st.markdown("</div>", unsafe_allow_html=True)
        
        # お客様の声
        st.markdown("<h2 style='text-align: center;'>お客様の声</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='card'>
                <p style='font-style: italic;'>"この分析ツールを使い始めてから、投資判断の精度が格段に向上しました。特に感度分析機能は、様々なシナリオを検討するのに非常に役立っています。"</p>
                <p style='text-align: right;'>- 山田太郎, 個人投資家</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='card'>
                <p style='font-style: italic;'>"複雑な財務モデリングの知識がなくても、直感的な操作で高度な分析ができる点が素晴らしいです。投資初心者にもプロにもおすすめできるツールです。"</p>
                <p style='text-align: right;'>- 鈴木花子, ファイナンシャルアドバイザー</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='card'>
                <p style='font-style: italic;'>"SWOT分析と競争優位性の評価機能が非常に優れています。企業の定性的な側面も含めた総合的な分析ができるのが、他のツールにはない魅力です。"</p>
                <p style='text-align: right;'>- 佐藤次郎, 証券アナリスト</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 最終CTA
        st.markdown("""
        <div style='text-align: center; margin-top: 3rem; margin-bottom: 3rem;'>
            <h2>あなたの投資判断をサポートする分析ツールを今すぐ体験</h2>
            <p>登録は無料。クレジットカード情報も必要ありません。</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("無料アカウントを作成", use_container_width=True):
                switch_page('signup')
        with col2:
            if st.button("詳細を見る", use_container_width=True):
                switch_page('plans')

# フッターの表示
show_footer()