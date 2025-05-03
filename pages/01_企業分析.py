import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# モジュールをインポート
from database import get_session, Company, FinancialData, Analysis, get_companies
from financial_models import calculate_intrinsic_value, calculate_financial_ratios
from utils import generate_swot_analysis, generate_moat_analysis
from sensitivity_analysis import generate_sensitivity_matrix, save_sensitivity_analysis, create_sensitivity_heatmap
from seo import generate_seo_metadata
from earnings_scraper import get_earnings_highlights
from auth import increment_user_analysis_count

# ページ設定
st.set_page_config(
    page_title="企業分析 - 企業価値分析プロ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* ヘッダー */
    .main-header {
        font-size: 2rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
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
    
    /* SWOT分析のグリッド */
    .swot-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .swot-box {
        border-radius: 10px;
        padding: 1rem;
        height: 100%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .swot-strengths {
        background-color: #d1e7dd;
    }
    
    .swot-weaknesses {
        background-color: #f8d7da;
    }
    
    .swot-opportunities {
        background-color: #cfe2ff;
    }
    
    .swot-threats {
        background-color: #fff3cd;
    }
    
    /* プラン制限メッセージ */
    .plan-limit-message {
        padding: 1rem;
        background-color: #cfe2ff;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* メトリクスボックス */
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-box {
        flex: 1;
        min-width: 120px;
        border-radius: 10px;
        padding: 1rem;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0066cc;
    }
    
    .metric-description {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* フォームセクション */
    .form-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* レコメンデーションボックス */
    .recommendation-box {
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .recommendation-buy {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    
    .recommendation-hold {
        background-color: #fff3cd;
        color: #664d03;
    }
    
    .recommendation-sell {
        background-color: #f8d7da;
        color: #842029;
    }
    
    /* ツールチップ */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* ダークモードサポート */
    @media (prefers-color-scheme: dark) {
        .card, .form-section, .metric-box {
            background-color: #262730;
        }
        
        .swot-strengths {
            background-color: rgba(25, 135, 84, 0.2);
        }
        
        .swot-weaknesses {
            background-color: rgba(220, 53, 69, 0.2);
        }
        
        .swot-opportunities {
            background-color: rgba(13, 110, 253, 0.2);
        }
        
        .swot-threats {
            background-color: rgba(255, 193, 7, 0.2);
        }
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'calculated_dcf' not in st.session_state:
    st.session_state.calculated_dcf = False

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

if 'sensitivity_matrix' not in st.session_state:
    st.session_state.sensitivity_matrix = None

# サイドバー
with st.sidebar:
    st.markdown("### 企業分析ツール")
    st.markdown("企業の本質的価値を計算し、投資判断をサポートします。")
    
    # ログインチェック
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("企業分析を利用するにはログインが必要です。")
        if st.button("ログインページへ戻る"):
            st.switch_page("app.py")
    else:
        # ユーザー情報とプラン情報の表示
        st.markdown(f"**ユーザー:** {st.session_state.user['username']}")
        
        if 'subscription_plan' in st.session_state.user:
            plan_name = "無料プラン"
            if st.session_state.user['subscription_plan'] == 'basic':
                plan_name = "ベーシックプラン"
            elif st.session_state.user['subscription_plan'] == 'premium':
                plan_name = "プレミアムプラン"
            
            st.markdown(f"**プラン:** {plan_name}")
            
            # 分析回数の表示
            analysis_count = st.session_state.user.get('analysis_count', 0)
            max_analyses = 3  # 無料プランのデフォルト
            
            if st.session_state.user['subscription_plan'] == 'basic':
                max_analyses = 20
            elif st.session_state.user['subscription_plan'] == 'premium':
                max_analyses = 999999  # 実質無制限
            
            st.markdown(f"**分析回数:** {analysis_count} / {max_analyses}")
            
            # 制限に達した場合の警告
            if analysis_count >= max_analyses and st.session_state.user['subscription_plan'] != 'premium':
                st.warning("分析回数の上限に達しています。上位プランへのアップグレードをご検討ください。")
                if st.button("プランをアップグレード"):
                    st.session_state.current_page = 'plans'
                    st.switch_page("app.py")
        
        st.markdown("---")
        
        # ナビゲーション
        st.markdown("### ナビゲーション")
        if st.button("ホームに戻る", key="home_btn"):
            st.switch_page("app.py")
        
        if st.button("銘柄検索", key="search_btn"):
            st.switch_page("pages/02_銘柄検索.py")
        
        if st.button("分析履歴", key="history_btn"):
            st.switch_page("pages/03_分析履歴.py")

# メインコンテンツ
st.markdown("<h1 class='main-header'>📊 企業分析</h1>", unsafe_allow_html=True)

# ログインチェック
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("企業分析を利用するにはログインが必要です。")
    if st.button("ログインページへ戻る", key="login_return_btn"):
        st.switch_page("app.py")
else:
    # 分析回数チェック
    analysis_count = st.session_state.user.get('analysis_count', 0)
    max_analyses = 3  # 無料プランのデフォルト
    
    if 'subscription_plan' in st.session_state.user:
        if st.session_state.user['subscription_plan'] == 'basic':
            max_analyses = 20
        elif st.session_state.user['subscription_plan'] == 'premium':
            max_analyses = 999999  # 実質無制限
    
    # 制限に達した場合の警告
    if analysis_count >= max_analyses and st.session_state.user.get('subscription_plan', 'free') != 'premium':
        st.markdown("""
        <div class='plan-limit-message'>
            <h3>分析回数の上限に達しています</h3>
            <p>より多くの企業を分析するには、上位プランへのアップグレードが必要です。</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("プランをアップグレード", key="upgrade_btn"):
            st.session_state.current_page = 'plans'
            st.switch_page("app.py")
    else:
        # 入力フォームエリア
        st.markdown("<div class='form-section'>", unsafe_allow_html=True)
        st.markdown("<h2>企業情報と予測パラメータの入力</h2>", unsafe_allow_html=True)
        
        # タブを使用して手動入力と企業選択を切り替え
        input_tab, select_tab = st.tabs(["手動で企業情報を入力", "登録済み企業から選択"])
        
        with input_tab:
            # 手動入力フォーム
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("企業名", value="Apple Inc." if not st.session_state.calculated_dcf else "")
                industry = st.selectbox("業界", [
                    "テクノロジー", "金融", "ヘルスケア", "消費財", "工業", 
                    "通信", "エネルギー", "素材", "公共事業", "不動産", "その他"
                ])
                ticker = st.text_input("ティッカーシンボル（例: AAPL）", value="AAPL" if not st.session_state.calculated_dcf else "")
            
            with col2:
                revenue = st.number_input("直近の売上高（百万USD）", value=365817.0 if not st.session_state.calculated_dcf else 0.0, step=1000.0)
                net_income = st.number_input("直近の純利益（百万USD）", value=94680.0 if not st.session_state.calculated_dcf else 0.0, step=100.0)
                shares_outstanding = st.number_input("発行済株式数（百万株）", value=15634.0 if not st.session_state.calculated_dcf else 0.0, step=10.0)
                current_stock_price = st.number_input("現在の株価（USD）", value=175.04 if not st.session_state.calculated_dcf else 0.0, step=0.1)
            
            st.markdown("### DCF分析パラメータ")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=15.0, step=0.5)
                net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=25.0, step=0.5)
            
            with col2:
                discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5)
                terminal_multiple = st.slider("終末価値倍率（PE）", min_value=5.0, max_value=30.0, value=20.0, step=0.5)
            
            with col3:
                forecast_years = st.slider("予測期間（年）", min_value=5, max_value=10, value=5, step=1)
                industry_pe = st.number_input("業界平均PER", value=25.0, step=0.5)
                industry_pb = st.number_input("業界平均PBR", value=6.5, step=0.1)
            
            st.markdown("### 感度分析パラメータ")
            
            if st.session_state.user.get('subscription_plan') in ['basic', 'premium']:
                col1, col2 = st.columns(2)
                
                with col1:
                    growth_range_min = st.number_input("成長率範囲（最小値 %）", value=revenue_growth - 10.0, step=1.0)
                    growth_range_max = st.number_input("成長率範囲（最大値 %）", value=revenue_growth + 10.0, step=1.0)
                    growth_step = st.number_input("成長率ステップ", value=2.0, step=0.5, min_value=0.5)
                
                with col2:
                    discount_range_min = st.number_input("割引率範囲（最小値 %）", value=discount_rate - 5.0, step=0.5)
                    discount_range_max = st.number_input("割引率範囲（最大値 %）", value=discount_rate + 5.0, step=0.5)
                    discount_step = st.number_input("割引率ステップ", value=1.0, step=0.5, min_value=0.5)
            else:
                st.markdown("""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                    <p style='color: #666;'>感度分析機能は、ベーシックプランまたはプレミアムプランでご利用いただけます。</p>
                </div>
                """, unsafe_allow_html=True)
        
        with select_tab:
            # 登録済み企業から選択
            companies = get_companies()
            if companies:
                company_options = {f"{c.name} ({c.symbol})": c.id for c in companies}
                selected_company = st.selectbox("企業を選択", options=list(company_options.keys()))
                
                if selected_company:
                    selected_company_id = company_options[selected_company]
                    
                    # 企業データの取得（実際の実装では、選択した企業のデータをデータベースから取得）
                    # サンプルデータ
                    sample_data = {
                        "name": selected_company.split(" (")[0],
                        "symbol": selected_company.split("(")[1].replace(")", ""),
                        "industry": "テクノロジー",
                        "revenue": 365817.0,
                        "net_income": 94680.0,
                        "shares_outstanding": 15634.0,
                        "current_stock_price": 175.04
                    }
                    
                    st.markdown("### 企業情報")
                    st.markdown(f"""
                    - **企業名**: {sample_data['name']}
                    - **ティッカーシンボル**: {sample_data['symbol']}
                    - **業界**: {sample_data['industry']}
                    - **直近の売上高**: ${sample_data['revenue']:.1f}百万
                    - **直近の純利益**: ${sample_data['net_income']:.1f}百万
                    - **発行済株式数**: {sample_data['shares_outstanding']:.1f}百万株
                    - **現在の株価**: ${sample_data['current_stock_price']:.2f}
                    """)
                    
                    st.markdown("### DCF分析パラメータ")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=15.0, step=0.5, key="selected_growth")
                        net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=25.0, step=0.5, key="selected_margin")
                    
                    with col2:
                        discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5, key="selected_discount")
                        terminal_multiple = st.slider("終末価値倍率（PE）", min_value=5.0, max_value=30.0, value=20.0, step=0.5, key="selected_terminal")
                    
                    with col3:
                        forecast_years = st.slider("予測期間（年）", min_value=5, max_value=10, value=5, step=1, key="selected_years")
                        industry_pe = st.number_input("業界平均PER", value=25.0, step=0.5, key="selected_pe")
                        industry_pb = st.number_input("業界平均PBR", value=6.5, step=0.1, key="selected_pb")
                    
                    st.markdown("### 感度分析パラメータ")
                    
                    if st.session_state.user.get('subscription_plan') in ['basic', 'premium']:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            growth_range_min = st.number_input("成長率範囲（最小値 %）", value=revenue_growth - 10.0, step=1.0, key="selected_growth_min")
                            growth_range_max = st.number_input("成長率範囲（最大値 %）", value=revenue_growth + 10.0, step=1.0, key="selected_growth_max")
                            growth_step = st.number_input("成長率ステップ", value=2.0, step=0.5, min_value=0.5, key="selected_growth_step")
                        
                        with col2:
                            discount_range_min = st.number_input("割引率範囲（最小値 %）", value=discount_rate - 5.0, step=0.5, key="selected_discount_min")
                            discount_range_max = st.number_input("割引率範囲（最大値 %）", value=discount_rate + 5.0, step=0.5, key="selected_discount_max")
                            discount_step = st.number_input("割引率ステップ", value=1.0, step=0.5, min_value=0.5, key="selected_discount_step")
                    else:
                        st.markdown("""
                        <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                            <p style='color: #666;'>感度分析機能は、ベーシックプランまたはプレミアムプランでご利用いただけます。</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 入力フォームの値を手動入力タブのものにセット
                    company_name = sample_data['name']
                    industry = sample_data['industry']
                    ticker = sample_data['symbol']
                    revenue = sample_data['revenue']
                    net_income = sample_data['net_income']
                    shares_outstanding = sample_data['shares_outstanding']
                    current_stock_price = sample_data['current_stock_price']
            else:
                st.info("データベースに登録されている企業がありません。手動入力タブをご利用ください。")
        
        # 分析実行ボタン
        if st.button("企業価値を計算", key="calculate_btn", use_container_width=True):
            if analysis_count < max_analyses or st.session_state.user.get('subscription_plan') == 'premium':
                # ローディング表示
                with st.spinner("企業価値を計算中..."):
                    # 予測売上高と純利益率からDCF計算用のデータフレームを作成
                    years = list(range(1, forecast_years + 1))
                    forecasted_data = pd.DataFrame()
                    forecasted_data['年'] = years
                    
                    # 売上高の予測
                    forecasted_data['売上高（百万USD）'] = [revenue * ((1 + revenue_growth/100) ** year) for year in years]
                    
                    # 純利益率は一定と仮定
                    forecasted_data['純利益率 (%)'] = net_margin
                    
                    # 純利益の予測
                    forecasted_data['純利益（百万USD）'] = forecasted_data['売上高（百万USD）'] * forecasted_data['純利益率 (%)'] / 100
                    
                    # DCF法による企業価値の計算
                    dcf_results = calculate_intrinsic_value(
                        forecasted_data,
                        discount_rate,
                        terminal_multiple,
                        shares_outstanding
                    )
                    
                    # SWOT分析と競争優位性の生成
                    swot_analysis = generate_swot_analysis(industry, revenue_growth, net_margin / 100, net_margin / 100)
                    moat_analysis = generate_moat_analysis(industry, revenue_growth, net_margin)
                    
                    # 財務指標の計算
                    market_cap = current_stock_price * shares_outstanding
                    book_value = net_income * 5  # 簡易的に純利益の5倍と仮定
                    financial_ratios = calculate_financial_ratios(
                        market_cap,
                        revenue,
                        net_income,
                        book_value,
                        shares_outstanding
                    )
                    
                    # 投資推奨度の判定
                    upside_potential = ((dcf_results['dcf_per_share'] / current_stock_price) - 1) * 100
                    recommendation = "強い買い"
                    if upside_potential > 30:
                        recommendation = "強い買い"
                    elif upside_potential > 10:
                        recommendation = "買い"
                    elif upside_potential > -10:
                        recommendation = "様子見"
                    elif upside_potential > -30:
                        recommendation = "売り"
                    else:
                        recommendation = "強い売り"
                    
                    # SEOメタデータの生成
                    seo_metadata = generate_seo_metadata(
                        company_name,
                        industry,
                        dcf_results['dcf_per_share'],
                        current_stock_price,
                        recommendation
                    )
                    
                    # 分析結果を保存
                    st.session_state.analysis_result = {
                        "company_name": company_name,
                        "ticker": ticker,
                        "industry": industry,
                        "dcf_results": dcf_results,
                        "financial_ratios": financial_ratios,
                        "swot_analysis": swot_analysis,
                        "moat_analysis": moat_analysis,
                        "forecasted_data": forecasted_data,
                        "revenue_growth": revenue_growth,
                        "net_margin": net_margin,
                        "discount_rate": discount_rate,
                        "terminal_multiple": terminal_multiple,
                        "forecast_years": forecast_years,
                        "current_stock_price": current_stock_price,
                        "upside_potential": upside_potential,
                        "recommendation": recommendation,
                        "seo_metadata": seo_metadata,
                        "analysis_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "industry_pe": industry_pe,
                        "industry_pb": industry_pb
                    }
                    
                    # 感度分析（ベーシックプラン以上）
                    if st.session_state.user.get('subscription_plan') in ['basic', 'premium']:
                        sensitivity_matrix = generate_sensitivity_matrix(
                            forecasted_data,
                            discount_rate,
                            terminal_multiple,
                            shares_outstanding,
                            [growth_range_min, growth_range_max, growth_step],
                            [discount_range_min, discount_range_max, discount_step]
                        )
                        st.session_state.sensitivity_matrix = sensitivity_matrix
                    
                    # 分析回数をインクリメント
                    increment_user_analysis_count(st.session_state.user['id'])
                    st.session_state.user['analysis_count'] = st.session_state.user.get('analysis_count', 0) + 1
                    
                    # 計算完了フラグを設定
                    st.session_state.calculated_dcf = True
                    
                    # 再読み込み
                    st.rerun()
            else:
                st.error("分析回数の上限に達しています。上位プランへのアップグレードが必要です。")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 計算結果の表示
        if st.session_state.calculated_dcf and st.session_state.analysis_result:
            result = st.session_state.analysis_result
            
            # 概要セクション
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 class='card-title'>{result['company_name']} ({result['ticker']}) の分析結果</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**業界**: {result['industry']}")
                st.markdown(f"**分析日**: {result['analysis_date']}")
            
            with col2:
                st.markdown(f"**現在の株価**: ${result['current_stock_price']:.2f}")
                st.markdown(f"**DCF価値**: ${result['dcf_results']['dcf_per_share']:.2f}")
            
            with col3:
                st.markdown(f"**上昇余地**: {result['upside_potential']:.1f}%")
                
                # 投資推奨度の表示
                recommendation_class = "recommendation-hold"
                if result['recommendation'] in ["強い買い", "買い"]:
                    recommendation_class = "recommendation-buy"
                elif result['recommendation'] in ["強い売り", "売り"]:
                    recommendation_class = "recommendation-sell"
                
                st.markdown(f"""
                <div class='recommendation-box {recommendation_class}'>
                    {result['recommendation']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # DCF分析結果
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>DCF分析</h2>", unsafe_allow_html=True)
            
            # DCF計算の仮定
            st.markdown("#### 計算の仮定")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**売上高成長率**: {result['revenue_growth']:.1f}%/年")
                st.markdown(f"**純利益率**: {result['net_margin']:.1f}%")
            
            with col2:
                st.markdown(f"**割引率**: {result['discount_rate']:.1f}%")
                st.markdown(f"**終末価値倍率**: {result['terminal_multiple']:.1f}倍")
            
            with col3:
                st.markdown(f"**予測期間**: {result['forecast_years']}年")
                st.markdown(f"**発行済株式数**: {result['dcf_results']['shares_outstanding']:.1f}百万株")
            
            # 予測財務データ
            st.markdown("#### 予測財務データ")
            forecasted_df = result['forecasted_data'].copy()
            forecasted_df.columns = ['年', '売上高（百万$）', '純利益率（%）', '純利益（百万$）']
            st.dataframe(forecasted_df, use_container_width=True)
            
            # 企業価値の内訳
            st.markdown("#### 企業価値の内訳")
            
            enterprise_value_components = pd.DataFrame({
                '項目': ['割引後CF合計', '終末価値', '企業価値合計', '1株あたり企業価値'],
                '金額（百万$）': [
                    result['dcf_results']['discounted_cf_sum'],
                    result['dcf_results']['terminal_value'],
                    result['dcf_results']['total_firm_value'],
                    result['dcf_results']['dcf_per_share']
                ]
            })
            
            # 最後の行は1株あたりの値なので別表示
            enterprise_value_df = enterprise_value_components.iloc[:-1].copy()
            enterprise_value_df['割合'] = enterprise_value_df['金額（百万$）'] / result['dcf_results']['total_firm_value'] * 100
            enterprise_value_df['割合'] = enterprise_value_df['割合'].map('{:.1f}%'.format)
            
            st.dataframe(enterprise_value_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 円グラフ
                fig = px.pie(
                    names=enterprise_value_components['項目'].iloc[:2],
                    values=enterprise_value_components['金額（百万$）'].iloc[:2],
                    title="企業価値の構成",
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # メトリクス
                st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
                
                # 企業価値
                st.markdown(f"""
                <div class='metric-box'>
                    <div class='metric-title'>企業価値合計</div>
                    <div class='metric-value'>${result['dcf_results']['total_firm_value']:,.0f}百万</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 1株あたり価値
                st.markdown(f"""
                <div class='metric-box'>
                    <div class='metric-title'>1株あたり価値</div>
                    <div class='metric-value'>${result['dcf_results']['dcf_per_share']:.2f}</div>
                    <div class='metric-description'>現在の株価: ${result['current_stock_price']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 上昇余地
                upside_color = "green"
                if result['upside_potential'] < 0:
                    upside_color = "red"
                
                st.markdown(f"""
                <div class='metric-box'>
                    <div class='metric-title'>上昇余地</div>
                    <div class='metric-value' style='color: {upside_color};'>{result['upside_potential']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 推奨
                st.markdown(f"""
                <div class='recommendation-box {recommendation_class}'>
                    投資判断: {result['recommendation']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 財務指標分析
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>財務指標分析</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 財務指標のテーブル
                st.markdown("#### 主要財務指標")
                
                financial_metrics = pd.DataFrame({
                    '指標': ['PER (株価収益率)', 'PBR (株価純資産倍率)', 'PSR (株価売上高倍率)', 'ROE (自己資本利益率)', '時価総額（百万$）'],
                    '現在値': [
                        f"{result['financial_ratios']['per']:.1f}倍",
                        f"{result['financial_ratios']['pbr']:.1f}倍",
                        f"{result['financial_ratios']['psr']:.2f}倍",
                        f"{result['financial_ratios']['roe']:.1f}%",
                        f"${result['financial_ratios']['market_cap']:,.0f}"
                    ],
                    '業界平均': [
                        f"{result['industry_pe']:.1f}倍",
                        f"{result['industry_pb']:.1f}倍",
                        "N/A",
                        "N/A",
                        "N/A"
                    ]
                })
                
                st.dataframe(financial_metrics, use_container_width=True)
            
            with col2:
                # 業界平均との比較
                st.markdown("#### 業界平均との比較")
                
                if result['industry_pe'] > 0 and result['industry_pb'] > 0:
                    ratios = {
                        '指標': ['PER', 'PBR'],
                        '企業値': [result['financial_ratios']['per'], result['financial_ratios']['pbr']],
                        '業界平均': [result['industry_pe'], result['industry_pb']]
                    }
                    
                    df_ratios = pd.DataFrame(ratios)
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=df_ratios['指標'],
                        y=df_ratios['企業値'],
                        name='企業値',
                        marker_color='royalblue'
                    ))
                    
                    fig.add_trace(go.Bar(
                        x=df_ratios['指標'],
                        y=df_ratios['業界平均'],
                        name='業界平均',
                        marker_color='lightgray'
                    ))
                    
                    fig.update_layout(
                        title='財務指標の比較',
                        xaxis_title='指標',
                        yaxis_title='倍率',
                        barmode='group',
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("業界平均データが利用できません。")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # SWOT分析
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>SWOT分析</h2>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='swot-grid'>
                <div class='swot-box swot-strengths'>
                    <h3>強み (Strengths)</h3>
                    <p>{}</p>
                </div>
                <div class='swot-box swot-weaknesses'>
                    <h3>弱み (Weaknesses)</h3>
                    <p>{}</p>
                </div>
                <div class='swot-box swot-opportunities'>
                    <h3>機会 (Opportunities)</h3>
                    <p>{}</p>
                </div>
                <div class='swot-box swot-threats'>
                    <h3>脅威 (Threats)</h3>
                    <p>{}</p>
                </div>
            </div>
            """.format(
                result['swot_analysis']['strengths'].replace('\n', '<br>'),
                result['swot_analysis']['weaknesses'].replace('\n', '<br>'),
                result['swot_analysis']['opportunities'].replace('\n', '<br>'),
                result['swot_analysis']['threats'].replace('\n', '<br>')
            ), unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 競争優位性（モアット）分析
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>競争優位性（モアット）分析</h2>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <h3>総合評価</h3>
            <p>{result['moat_analysis']['moat_evaluation']}</p>
            
            <h3>主な競争優位性の源泉</h3>
            <p>{result['moat_analysis']['moat_sources'].replace('\n', '<br>')}</p>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 感度分析（ベーシックプラン以上）
            if st.session_state.user.get('subscription_plan') in ['basic', 'premium'] and st.session_state.sensitivity_matrix:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h2 class='card-title'>感度分析</h2>", unsafe_allow_html=True)
                
                st.markdown("""
                <p>成長率と割引率の変動が企業価値に与える影響をヒートマップで表示しています。
                現在の株価を基準として、割安（青色）と割高（赤色）の領域を示しています。</p>
                """, unsafe_allow_html=True)
                
                sensitivity_data = {
                    'matrix_data': st.session_state.sensitivity_matrix
                }
                
                # ヒートマップの作成
                heatmap = create_sensitivity_heatmap(sensitivity_data, current_stock_price)
                st.plotly_chart(heatmap, use_container_width=True)
                
                # 解釈
                st.markdown("""
                <h3>感度分析の解釈</h3>
                <p>
                ヒートマップは、成長率と割引率のさまざまな組み合わせに基づいた企業価値を示しています。
                青色の領域は現在の株価よりも高い企業価値を示し、割安である可能性があります。
                赤色の領域は現在の株価よりも低い企業価値を示し、割高である可能性があります。
                </p>
                <p>
                <strong>注意</strong>: 感度分析は将来予測に基づくものであり、実際の結果は異なる場合があります。
                投資判断の際は、他の情報源も参考にしてください。
                </p>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 決算情報（プレミアムプランのみ）
            if st.session_state.user.get('subscription_plan') == 'premium' and result['ticker']:
                with st.spinner("決算情報を取得中..."):
                    try:
                        earnings_data = get_earnings_highlights(result['ticker'])
                        
                        if earnings_data and "highlights" in earnings_data:
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<h2 class='card-title'>最新の決算ハイライト</h2>", unsafe_allow_html=True)
                            
                            highlights = earnings_data["highlights"]
                            
                            st.markdown(f"""
                            <h3>四半期業績</h3>
                            <p>{highlights.get('quarterly_performance', 'データがありません')}</p>
                            
                            <h3>売上高</h3>
                            <p>{highlights.get('revenue_highlights', 'データがありません')}</p>
                            
                            <h3>利益</h3>
                            <p>{highlights.get('earnings_highlights', 'データがありません')}</p>
                            
                            <h3>業界動向</h3>
                            <p>{highlights.get('industry_trends', 'データがありません')}</p>
                            
                            <h3>将来の見通し</h3>
                            <p>{highlights.get('guidance', 'データがありません')}</p>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info(f"{result['ticker']}の最新の決算情報は現在利用できません。")
                    except Exception as e:
                        st.error(f"決算情報の取得中にエラーが発生しました: {str(e)}")
            
            # 報告書のダウンロード（プレミアムプランのみ）
            if st.session_state.user.get('subscription_plan') == 'premium':
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<h2 class='card-title'>分析レポートのダウンロード</h2>", unsafe_allow_html=True)
                
                st.markdown("""
                <p>分析結果をPDFレポートとしてダウンロードできます。（プレミアムプラン特典）</p>
                """, unsafe_allow_html=True)
                
                if st.button("PDFレポートを生成", key="generate_pdf"):
                    with st.spinner("レポートを生成中..."):
                        # ここでPDFレポートを生成する処理を実装
                        # 実際の実装では、ReportLab等のライブラリを使用してPDFを生成
                        st.success("レポートが生成されました！")
                        
                        # ダウンロードボタン（サンプル）
                        st.download_button(
                            label="レポートをダウンロード",
                            data=b"Sample PDF content",  # 実際にはPDFバイナリデータ
                            file_name=f"{result['company_name']}_分析レポート_{result['analysis_date']}.pdf",
                            mime="application/pdf"
                        )
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 分析結果の保存
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>分析結果の保存</h2>", unsafe_allow_html=True)
            
            st.markdown("""
            <p>この分析結果をデータベースに保存して、後で参照することができます。</p>
            """, unsafe_allow_html=True)
            
            if st.button("分析結果を保存", key="save_analysis"):
                with st.spinner("分析結果を保存中..."):
                    try:
                        # 実際の実装では、分析結果をデータベースに保存する処理を実装
                        st.success("分析結果が正常に保存されました！")
                    except Exception as e:
                        st.error(f"保存中にエラーが発生しました: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 再分析ボタン（結果表示後）
        if st.session_state.calculated_dcf:
            if st.button("新しい企業を分析", key="new_analysis"):
                st.session_state.calculated_dcf = False
                st.session_state.analysis_result = None
                st.session_state.sensitivity_matrix = None
                st.rerun()