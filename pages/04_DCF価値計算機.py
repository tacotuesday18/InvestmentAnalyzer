import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import json
import datetime

# フォーマット用ヘルパー関数
from format_helpers import format_currency, format_large_number, format_ja_number

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# stock_dataモジュールをインポート
from stock_data import get_stock_data, get_available_tickers
from financial_models import calculate_intrinsic_value

# ページ設定
st.set_page_config(
    page_title="DCF価値計算機 - 企業価値分析プロ",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern design CSS consistent with homepage
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #222222;
    }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        margin: -2rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cards */
    .analysis-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }
    
    .card-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #222222;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        color: #0066cc;
    }
    
    .result-card {
        background-color: #e6f7ff;
        border-left: 4px solid #0066cc;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .result-value {
        font-size: 2rem !important;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
    }
    
    .result-label {
        font-size: 1rem !important;
        color: #666;
        text-align: center;
    }
    
    .up-value {
        color: #36b37e;
    }
    
    .down-value {
        color: #ff5630;
    }
    
    /* モバイル対応 */
    @media (max-width: 768px) {
        .result-value {
            font-size: 1.6rem !important;
        }
        
        .result-label {
            font-size: 0.9rem !important;
        }
    }
    
    /* デュアルスライダー */
    .dual-slider {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .dual-slider .slider-container {
        flex: 1;
    }
    
    .dual-slider .slider-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #0066cc;
        margin-left: 1rem;
        width: 60px;
        text-align: center;
    }
    
    /* Buttons */
    .stButton > button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #5a67d8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Metrics */
    .metric-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("### DCF価値計算機")
    st.markdown("割引キャッシュフロー（DCF）法を使って、企業の本質的価値を計算します。")
    
    st.markdown("---")
    
    # ナビゲーション
    st.markdown("### ナビゲーション")
    if st.button("ホームに戻る", key="home_btn"):
        st.switch_page("app.py")
    
    if st.button("企業分析", key="analysis_btn"):
        st.switch_page("pages/01_企業分析.py")
    
    if st.button("銘柄比較", key="compare_btn"):
        st.switch_page("pages/02_銘柄比較.py")
    
    if st.button("銘柄スクリーナー", key="screener_btn"):
        st.switch_page("pages/03_銘柄スクリーナー.py")

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">🧮 DCF価値計算機</div>
    <div class="page-subtitle">割引キャッシュフロー法で企業の本質的価値を科学的に算出</div>
</div>
""", unsafe_allow_html=True)

# DCF計算の説明を追加
with st.expander("🔍 DCF計算方法について詳しく"):
    st.markdown("""
    <h3>DCF法とは？</h3>
    <p>DCF（Discounted Cash Flow：割引キャッシュフロー）法は、企業の<strong>将来の利益</strong>を予測し、
    それを<strong>現在の価値</strong>に割り引くことで企業の本質的価値を算出する方法です。</p>
    
    <h3>計算の流れ</h3>
    <ol>
        <li><strong>予測期間の設定</strong>：通常3～5年間の将来の財務状況を予測します</li>
        <li><strong>売上高の予測</strong>：売上高成長率を使って将来の売上高を予測します</li>
        <li><strong>純利益の計算</strong>：純利益率を使って将来の純利益を計算します</li>
        <li><strong>終末価値の計算</strong>：予測期間終了後の企業価値を業界平均PERを用いて推定します</li>
        <li><strong>割引率の適用</strong>：将来の価値を割引率で現在価値に割り引きます</li>
        <li><strong>1株あたり価値の計算</strong>：企業価値を発行済株式数で割って算出します</li>
    </ol>
    
    <h3>主な計算式</h3>
    <p>終末価値 = 予測期間最終年の純利益 × 業界平均PER</p>
    <p>割引係数 = 1 ÷ (1 + 割引率)<sup>予測年数</sup></p>
    <p>現在価値 = 終末価値 × 割引係数</p>
    <p>1株あたり本質的価値 = 現在価値 ÷ 発行済株式数</p>
    
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 20px;">
    <p style="margin-bottom: 5px;"><strong>注意点</strong>：</p>
    <ul style="margin-top: 0;">
        <li>DCF法は将来予測に依存するため、入力パラメータの変更で結果が大きく変動します</li>
        <li>売上成長率、純利益率、割引率が企業価値に大きな影響を与えます</li>
        <li>感度分析を活用して、パラメータ変動が企業価値に与える影響を確認しましょう</li>
        <li>DCF法は完璧な方法ではないため、業界平均倍率法などの他の評価方法と組み合わせて総合的に判断することをお勧めします</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# 入力カード
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>企業情報と予測パラメータ</h2>", unsafe_allow_html=True)

# 利用可能なティッカーシンボル
available_tickers = get_available_tickers()
ticker_options = {ticker: f"{ticker} - {get_stock_data(ticker)['name']}" for ticker in available_tickers}

# 企業選択
selected_ticker = st.selectbox(
    "銘柄を選択",
    options=available_tickers,
    format_func=lambda x: ticker_options.get(x, x),
    index=0 if available_tickers else None
)

if selected_ticker:
    stock_data = get_stock_data(selected_ticker)
    
    # 基本情報の表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**企業名**: {stock_data['name']}")
        st.markdown(f"**業界**: {stock_data['industry']}")
    
    with col2:
        st.markdown(f"**現在の株価**: ${stock_data['current_price']:.2f}")
        market_cap = stock_data['current_price'] * stock_data['shares_outstanding']
        st.markdown(f"**時価総額**: {format_currency(market_cap, '$')} 百万")
    
    with col3:
        st.markdown(f"**発行済株式数**: {format_large_number(stock_data['shares_outstanding'])}百万株")
        st.markdown(f"**1株あたり純資産**: ${stock_data['book_value_per_share']:.2f}")
    
    # DCF分析パラメータ入力
    st.markdown("### DCF分析パラメータ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 売上と純利益の入力（数値入力の代わりにテキスト入力で桁区切りに対応）
        revenue_str = st.text_input(
            "年間売上高（USD）", 
            value=f"{stock_data['revenue'] * 1000000:,.0f}"
        )
        # カンマを除去して数値に変換
        try:
            revenue = float(revenue_str.replace(',', ''))
        except:
            revenue = stock_data['revenue'] * 1000000

        net_income_str = st.text_input(
            "年間純利益（USD）", 
            value=f"{stock_data['net_income'] * 1000000:,.0f}"
        )
        # カンマを除去して数値に変換
        try:
            net_income = float(net_income_str.replace(',', ''))
        except:
            net_income = stock_data['net_income'] * 1000000
        
        # 予測期間と成長率
        forecast_years = st.number_input("予測期間（年）", min_value=1, max_value=10, value=3, step=1)
        revenue_growth = st.number_input("売上高成長率（%）", min_value=-50.0, max_value=100.0, value=stock_data.get('historical_growth', 10.0), step=0.1, format="%.1f")
    
    with col2:
        # 割引率とマージン
        discount_rate = st.number_input("割引率（%）", min_value=1.0, max_value=50.0, value=10.0, step=0.1, format="%.1f")
        net_margin = st.number_input("純利益率（%）", min_value=-50.0, max_value=100.0, value=(net_income / revenue * 100) if revenue > 0 else 15.0, step=0.1, format="%.1f")
        
        # 業界平均倍率の入力
        st.markdown("#### 業界平均倍率")
        industry_per = st.number_input("業界平均PER（株価収益率）", min_value=1.0, max_value=100.0, value=25.0, step=1.0)
        industry_psr = st.number_input("業界平均PSR（株価売上高倍率）", min_value=0.1, max_value=50.0, value=5.0, step=0.1)
        industry_pbr = st.number_input("業界平均PBR（株価純資産倍率）", min_value=0.1, max_value=50.0, value=3.0, step=0.1)
        
        # カスタム株価の入力（オプション）
        custom_stock_price_str = st.text_input(
            "現在の株価（USD）を上書き（必要な場合のみ）",
            value=""
        )
        
        # 入力があれば変換
        try:
            if custom_stock_price_str and custom_stock_price_str.strip():
                custom_stock_price = float(custom_stock_price_str.replace(',', ''))
            else:
                custom_stock_price = 0.0
        except:
            custom_stock_price = 0.0
        
        if custom_stock_price > 0:
            current_stock_price = custom_stock_price
        else:
            current_stock_price = stock_data['current_price']
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 計算実行ボタン
    if st.button("企業価値を計算", key="calculate_btn", use_container_width=True):
        with st.spinner("DCF法による企業価値を計算中..."):
            # 進捗バーの表示
            progress_bar = st.progress(0)
            
            # DCF計算に必要なデータ構造の準備
            forecasted_data = pd.DataFrame()
            forecasted_data['year'] = list(range(1, forecast_years + 1))
            
            # 売上高の予測
            forecasted_data['revenue'] = [revenue * ((1 + revenue_growth/100) ** year) for year in forecasted_data['year']]
            
            # 純利益の予測
            forecasted_data['net_income'] = forecasted_data['revenue'] * (net_margin / 100)
            
            # 進捗バーの更新
            progress_bar.progress(50)
            
            # DCF法による企業価値計算
            # 修正版：キャッシュフローを使わず、純利益を直接割引く簡易的な方法
            
            # 最終年の純利益
            final_year_net_income = forecasted_data['net_income'].iloc[-1]
            
            # 最終年の利益に倍率を適用して終末価値を計算
            terminal_value = final_year_net_income * industry_per
            
            # 割引係数を計算
            discount_factor = 1 / ((1 + discount_rate/100) ** forecast_years)
            
            # 割引後の終末価値を計算
            dcf_value = terminal_value * discount_factor
            
            # 1株あたり価値
            per_share_value = dcf_value / (stock_data['shares_outstanding'] * 1000000)
            
            # 上昇余地の計算
            upside_potential = ((per_share_value / current_stock_price) - 1) * 100
            
            # 進捗バーの完了
            progress_bar.progress(100)
            
            # 結果表示
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>企業価値分析結果</h2>", unsafe_allow_html=True)
            
            # 業界平均倍率および本質的価値の計算準備
            
            # 予測最終年の値を使用
            final_year_revenue = forecasted_data['revenue'].iloc[-1]
            final_year_net_income = forecasted_data['net_income'].iloc[-1]
            
            # 簡易的な純資産（自己資本）の推定（通常は貸借対照表から）
            # ここでは純利益の10倍と仮定
            estimated_equity = final_year_net_income * 10
            
            # 業界平均倍率を使った企業価値評価
            per_valuation = final_year_net_income * industry_per
            psr_valuation = final_year_revenue * industry_psr
            pbr_valuation = estimated_equity * industry_pbr
            
            # 倍率ベースの株価
            per_share_price = per_valuation / (stock_data['shares_outstanding'] * 1000000)
            psr_share_price = psr_valuation / (stock_data['shares_outstanding'] * 1000000)
            pbr_share_price = pbr_valuation / (stock_data['shares_outstanding'] * 1000000)
            
            # 平均株価（3つの方法の平均）
            avg_multiple_price = (per_share_price + psr_share_price + pbr_share_price) / 3
            
            # 現在価値への割引（予測期間分の割引率を適用）
            discounted_multiple_price = avg_multiple_price / ((1 + discount_rate/100) ** forecast_years)
            
            # 上昇余地
            multiple_upside = ((discounted_multiple_price / current_stock_price) - 1) * 100
            
            # 将来の価値（比較表用）
            future_per_market_cap = per_valuation
            future_psr_market_cap = psr_valuation
            future_pbr_market_cap = pbr_valuation
            future_per_price = per_share_price
            future_psr_price = psr_share_price
            future_pbr_price = pbr_share_price
            future_avg_price = avg_multiple_price
            
            # DCF分析結果
            st.markdown("<h3>DCF分析結果</h3>", unsafe_allow_html=True)
            
            # DCFの評価結果の表示
            st.markdown(f"""
            <div style="background-color: #f2f7ff; padding: 10px; border-radius: 5px; margin-bottom: 15px; text-align: center;">
                <p style="margin-bottom: 0px;"><strong>{forecast_years}年後</strong>の予測価値と現在価値への割引結果</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${per_share_price:.2f}</p>
                    <p class='result-label'>{forecast_years}年後の株価（PER）</p>
                    <p class='result-note'>業界平均PER: {industry_per}倍</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${psr_share_price:.2f}</p>
                    <p class='result-label'>{forecast_years}年後の株価（PSR）</p>
                    <p class='result-note'>業界平均PSR: {industry_psr}倍</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${pbr_share_price:.2f}</p>
                    <p class='result-label'>{forecast_years}年後の株価（PBR）</p>
                    <p class='result-note'>業界平均PBR: {industry_pbr}倍</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                upside_class = "up-value" if multiple_upside >= 0 else "down-value"
                upside_sign = "+" if multiple_upside >= 0 else ""
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${discounted_multiple_price:.2f}</p>
                    <p class='result-label'>現在の本質的価値</p>
                    <p class='result-note'>{forecast_years}年分の割引率{discount_rate}%適用後</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {upside_class}'>{upside_sign}{multiple_upside:.1f}%</p>
                    <p class='result-label'>現在の上昇余地</p>
                    <p class='result-note'>本質的価値 ${discounted_multiple_price:.2f} vs 現在株価 ${current_stock_price:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                # 総合的な投資推奨度（DCFと倍率法の平均）
                avg_upside = (upside_potential + multiple_upside) / 2
                avg_upside_sign = "+" if avg_upside >= 0 else ""
                if avg_upside > 20:
                    recommendation = "強い買い"
                    recommendation_class = "up-value"
                elif avg_upside > 10:
                    recommendation = "買い"
                    recommendation_class = "up-value"
                elif avg_upside > -10:
                    recommendation = "中立"
                    recommendation_class = ""
                elif avg_upside > -20:
                    recommendation = "売り"
                    recommendation_class = "down-value"
                else:
                    recommendation = "強い売り"
                    recommendation_class = "down-value"
                
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {recommendation_class}'>{recommendation}</p>
                    <p class='result-label'>総合推奨度</p>
                    <p class='result-note'>平均上昇余地: {avg_upside_sign}{avg_upside:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 詳細なDCF計算結果の表示
            st.markdown("<h3>予測財務データ</h3>", unsafe_allow_html=True)
            
            # データフレームの表示用にカラム名を変更
            display_df = forecasted_data.copy()
            display_df.columns = ['予測年', '売上高（$）', '純利益（$）']
            # 数値を見やすく表示するためにフォーマット
            for col in display_df.columns[1:]:
                display_df[col] = display_df[col].map('${:,.0f}'.format)
            st.dataframe(display_df, use_container_width=True)
            
            # 業界平均倍率による評価の説明
            with st.expander("📈 業界平均倍率評価について"):
                st.markdown(f"""
                <h4>業界平均倍率による評価とは？</h4>
                <p>予測期間（{forecast_years}年後）の財務数値に業界平均倍率を適用して将来の企業価値を推定し、それを現在価値に割り引く方法です。</p>
                
                <h4>使用している主な倍率</h4>
                <ul>
                    <li><strong>PER（株価収益率）</strong>：純利益に対する倍率。{industry_per}倍を使用</li>
                    <li><strong>PSR（株価売上高倍率）</strong>：売上高に対する倍率。{industry_psr}倍を使用</li>
                    <li><strong>PBR（株価純資産倍率）</strong>：純資産に対する倍率。{industry_pbr}倍を使用</li>
                </ul>
                
                <h4>計算方法</h4>
                <p>1. {forecast_years}年後の財務予測を使用:</p>
                <ul>
                    <li>売上高: {format_currency(final_year_revenue, '$')}</li>
                    <li>純利益: {format_currency(final_year_net_income, '$')}</li>
                    <li>推定純資産: {format_currency(estimated_equity, '$')}</li>
                </ul>
                
                <p>2. {forecast_years}年後の予測企業価値（各倍率ベース）:</p>
                <ul>
                    <li>PERベース: {format_currency(final_year_net_income, '$')} × {industry_per} = {format_currency(future_per_market_cap, '$')}</li>
                    <li>PSRベース: {format_currency(final_year_revenue, '$')} × {industry_psr} = {format_currency(future_psr_market_cap, '$')}</li>
                    <li>PBRベース: {format_currency(estimated_equity, '$')} × {industry_pbr} = {format_currency(future_pbr_market_cap, '$')}</li>
                </ul>
                
                <p>3. {forecast_years}年後の予測1株価値:</p>
                <ul>
                    <li>PERベース: {format_currency(future_per_market_cap, '$')} ÷ {format_large_number(stock_data['shares_outstanding'] * 1000000)}株 = ${future_per_price:.2f}</li>
                    <li>PSRベース: {format_currency(future_psr_market_cap, '$')} ÷ {format_large_number(stock_data['shares_outstanding'] * 1000000)}株 = ${future_psr_price:.2f}</li>
                    <li>PBRベース: {format_currency(future_pbr_market_cap, '$')} ÷ {format_large_number(stock_data['shares_outstanding'] * 1000000)}株 = ${future_pbr_price:.2f}</li>
                </ul>
                
                <p>4. {forecast_years}年後の予測平均株価: (${future_per_price:.2f} + ${future_psr_price:.2f} + ${future_pbr_price:.2f}) ÷ 3 = ${future_avg_price:.2f}</p>
                
                <p>5. 現在価値への割引: ${future_avg_price:.2f} ÷ (1 + {discount_rate/100})<sup>{forecast_years}</sup> = ${discounted_multiple_price:.2f}</p>
                <p>※ 割引係数: 1 ÷ (1 + {discount_rate/100})<sup>{forecast_years}</sup> = {1/((1 + discount_rate/100) ** forecast_years):.4f}</p>
                
                <p>6. 上昇余地の計算: (${discounted_multiple_price:.2f} ÷ ${current_stock_price:.2f} - 1) × 100 = {multiple_upside:.1f}%</p>
                """, unsafe_allow_html=True)
            
            # DCF計算の説明
            st.markdown("<h3>本質的価値の計算方法</h3>", unsafe_allow_html=True)
            
            # 計算過程の説明を追加
            with st.expander("📊 本質的価値の計算方法の詳細説明"):
                st.markdown(f"""
                <h4>本質的価値計算とは？</h4>
                <p>本質的価値とは、企業の将来利益に基づいて算出される理論上の株価のことです。現在の株価と比較することで、投資判断の材料となります。</p>
                
                <h4>計算の流れ</h4>
                <p>本ツールでは、以下の手順で本質的価値を計算しています：</p>
                
                <h4>1. 将来の財務予測</h4>
                <p><strong>売上高成長率 {revenue_growth:.1f}%</strong> に基づいて将来の売上高を予測します。</p>
                <p><strong>純利益率 {net_margin:.1f}%</strong> に基づいて将来の純利益を計算します。</p>
                <p>この予測を <strong>{forecast_years}年間</strong> 行い、将来の財務状況をモデル化します。</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="font-weight: bold; margin-bottom: 10px;">【計算例】</p>
                <p>現在の売上高: {format_currency(revenue, '$')}</p>
                <ul>
                    <li>1年後の予測売上高: {format_currency(revenue, '$')} × (1 + {revenue_growth/100}) = {format_currency(revenue * (1 + revenue_growth/100), '$')}</li>
                    <li>2年後の予測売上高: {format_currency(revenue, '$')} × (1 + {revenue_growth/100})<sup>2</sup> = {format_currency(revenue * (1 + revenue_growth/100)**2, '$')}</li>
                    <li>{forecast_years}年後の予測売上高: {format_currency(revenue, '$')} × (1 + {revenue_growth/100})<sup>{forecast_years}</sup> = {format_currency(revenue * (1 + revenue_growth/100)**forecast_years, '$')}</li>
                </ul>
                <p>{forecast_years}年後の予測純利益: {format_currency(revenue * (1 + revenue_growth/100)**forecast_years, '$')} × {net_margin/100} = {format_currency(final_year_net_income, '$')}</p>
                </div>
                
                <h4>2. 終末価値（ターミナルバリュー）の計算</h4>
                <p>予測期間終了後も企業は存続し価値を生み出し続けるという前提のもと、<strong>業界平均PER（株価収益率）{industry_per}倍</strong> を使って終末価値を計算します。</p>
                <p>PERとは、株価が純利益の何倍であるかを示す指標で、業界や成長率によって適正値が異なります。</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="font-weight: bold; margin-bottom: 10px;">【終末価値の計算】</p>
                <p>終末価値 = {forecast_years}年後の予測純利益 × 業界平均PER</p>
                <p>終末価値 = {format_currency(final_year_net_income, '$')} × {industry_per} = {format_currency(terminal_value, '$')}</p>
                </div>
                
                <h4>3. 現在価値への割引</h4>
                <p>将来の価値を現在の価値に変換するために、<strong>割引率 {discount_rate:.1f}%</strong> を使用して割引計算を行います。</p>
                <p>割引率は投資のリスクや資本コストを反映し、高いほど将来価値は小さく評価されます。</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="font-weight: bold; margin-bottom: 10px;">【割引計算】</p>
                <p>割引係数 = 1 ÷ (1 + 割引率)<sup>予測年数</sup></p>
                <p>割引係数 = 1 ÷ (1 + {discount_rate/100})<sup>{forecast_years}</sup> = {1/((1 + discount_rate/100) ** forecast_years):.4f}</p>
                <p>現在価値 = 終末価値 × 割引係数</p>
                <p>現在価値 = {format_currency(terminal_value, '$')} × {1/((1 + discount_rate/100) ** forecast_years):.4f} = {format_currency(dcf_value, '$')}</p>
                </div>
                
                <h4>4. 1株あたり本質的価値の計算</h4>
                <p>企業全体の価値を発行済株式数で割ることで、1株あたりの本質的価値を計算します。</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="font-weight: bold; margin-bottom: 10px;">【1株あたり価値の計算】</p>
                <p>1株あたり本質的価値 = 企業価値 ÷ 発行済株式数</p>
                <p>1株あたり本質的価値 = {format_currency(dcf_value, '$')} ÷ {format_large_number(stock_data['shares_outstanding'] * 1000000)}株 = <span style="color: #36b37e; font-weight: bold;">${per_share_value:.2f}</span></p>
                </div>
                
                <h4>5. 投資判断の指標：上昇余地</h4>
                <p>計算された本質的価値と現在の株価を比較して、上昇余地（または下落リスク）を評価します。</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="font-weight: bold; margin-bottom: 10px;">【上昇余地の計算】</p>
                <p>上昇余地 = (本質的価値 ÷ 現在株価 - 1) × 100</p>
                <p>上昇余地 = (${per_share_value:.2f} ÷ ${current_stock_price:.2f} - 1) × 100 = <span style="color: {upside_potential >= 0 and '#36b37e' or '#ff5630'}; font-weight: bold;">{upside_potential >= 0 and '+' or ''}{upside_potential:.1f}%</span></p>
                </div>
                
                <h4>投資判断の目安</h4>
                <ul>
                    <li>上昇余地が <strong>+20%以上</strong>：割安（強い買い）</li>
                    <li>上昇余地が <strong>+10〜+20%</strong>：やや割安（買い）</li>
                    <li>上昇余地が <strong>-10〜+10%</strong>：適正水準（中立）</li>
                    <li>上昇余地が <strong>-20〜-10%</strong>：やや割高（売り）</li>
                    <li>上昇余地が <strong>-20%以下</strong>：割高（強い売り）</li>
                </ul>
                """, unsafe_allow_html=True)
                
            # DCFの結果概要を表示
            dcf_summary = pd.DataFrame({
                '項目': ['予測年数', '売上高成長率', '純利益率', '割引率', '業界平均PER', '1株あたり企業価値'],
                '値': [
                    f"{forecast_years}年",
                    f"{revenue_growth:.1f}%",
                    f"{net_margin:.1f}%",
                    f"{discount_rate:.1f}%",
                    f"{industry_per:.1f}倍",
                    f"${per_share_value:.2f}"
                ]
            })
            
            st.dataframe(dcf_summary, use_container_width=True)
            
            # 感度分析
            st.markdown("<h3>感度分析</h3>", unsafe_allow_html=True)
            st.markdown("成長率と割引率の変動が企業価値に与える影響を確認できます。")
            
            # 感度分析の説明を追加
            with st.expander("📈 感度分析について"):
                st.markdown("""
                <h4>感度分析とは？</h4>
                <p>感度分析とは、DCF計算の重要な入力値（売上高成長率と割引率）を変動させた場合に、
                企業価値がどのように変化するかを調べる分析方法です。</p>
                
                <h4>なぜ感度分析が重要なのか？</h4>
                <ul>
                    <li>将来の成長率や割引率は予測が難しく、不確実性があります</li>
                    <li>わずかなパラメータの変化で企業価値が大きく変動する可能性があります</li>
                    <li>投資判断の信頼性を高めるために、様々なシナリオを検討することが重要です</li>
                </ul>
                
                <h4>ヒートマップの見方</h4>
                <p>下のヒートマップは、売上高成長率（縦軸）と割引率（横軸）の組み合わせによる
                企業価値の変化を色で表しています。</p>
                <ul>
                    <li><strong>青色</strong>：現在の株価より高い企業価値（割安の可能性）</li>
                    <li><strong>赤色</strong>：現在の株価より低い企業価値（割高の可能性）</li>
                    <li><strong>白色</strong>：現在の株価に近い企業価値</li>
                </ul>
                <p>青色の領域が広いほど、様々な条件下でも割安である可能性が高く、
                投資判断の信頼性が高いと考えられます。</p>
                """, unsafe_allow_html=True)
            
            # 感度分析の範囲設定
            growth_range = np.linspace(revenue_growth - 5, revenue_growth + 5, 5)
            discount_range = np.linspace(discount_rate - 2, discount_rate + 2, 5)
            
            # 感度分析マトリックスの計算
            sensitivity_matrix = []
            
            for g in growth_range:
                row = []
                for d in discount_range:
                    # 簡易版の感度分析計算（実際はより複雑）
                    forecasted_data_sens = pd.DataFrame()
                    forecasted_data_sens['year'] = list(range(1, forecast_years + 1))
                    
                    # 売上高の予測
                    forecasted_data_sens['revenue'] = [revenue * ((1 + g/100) ** year) for year in forecasted_data_sens['year']]
                    
                    # 純利益の予測
                    forecasted_data_sens['net_income'] = forecasted_data_sens['revenue'] * (net_margin / 100)
                    
                    # 最終年の純利益
                    final_year_net_income_sens = forecasted_data_sens['net_income'].iloc[-1]
                    
                    # 最終年の利益に倍率を適用して終末価値を計算
                    terminal_value_sens = final_year_net_income_sens * industry_per
                    
                    # 割引係数を計算
                    discount_factor_sens = 1 / ((1 + d/100) ** forecast_years)
                    
                    # 割引後の終末価値を計算
                    dcf_value_sens = terminal_value_sens * discount_factor_sens
                    
                    # 1株あたり価値
                    per_share_value_sens = dcf_value_sens / (stock_data['shares_outstanding'] * 1000000)
                    
                    row.append(per_share_value_sens)
                    
                sensitivity_matrix.append(row)
            
            # 感度分析ヒートマップの作成
            fig = go.Figure(data=go.Heatmap(
                z=sensitivity_matrix,
                x=[f"{d:.1f}%" for d in discount_range],
                y=[f"{g:.1f}%" for g in growth_range],
                hoverongaps=False,
                colorscale='RdBu_r',
                zmid=current_stock_price,  # 現在の株価を中間値として設定
                colorbar=dict(title="価値 ($)"),
            ))
            
            fig.update_layout(
                title="成長率と割引率の感度分析",
                xaxis_title="割引率",
                yaxis_title="売上高成長率",
                height=500,
                margin=dict(l=50, r=50, t=50, b=50),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 現在の株価との比較ライン
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <p>現在の株価 (<span style="color: #ff5630;">${current_stock_price:.2f}</span>) と計算された本質的価値 (<span style="color: #36b37e;">${per_share_value:.2f}</span>) の比較</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 詳細分析へのリンク
            st.markdown("""
            <div style="margin-top: 2rem; text-align: center;">
                <p>より詳細な分析が必要ですか？企業分析ページでは、SWOT分析や競争優位性の評価なども含めた包括的な分析が可能です。</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("詳細な企業分析へ進む", key="to_analysis_btn", use_container_width=True):
                # 企業分析ページに遷移
                st.session_state.selected_ticker = selected_ticker
                st.switch_page("pages/01_企業分析.py")
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("銘柄を選択してください。")

# Add floating chatbot component
try:
    from floating_chatbot import render_floating_chatbot
    render_floating_chatbot()
except ImportError:
    pass