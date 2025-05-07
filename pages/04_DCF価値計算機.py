import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import json
import datetime

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
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
    }
    
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        font-size: 1.4rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
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

# メインコンテンツ
st.markdown("<h1 class='main-header'>🧮 DCF価値計算機</h1>", unsafe_allow_html=True)
st.markdown("割引キャッシュフロー（DCF）法を使用して、企業の本質的価値を計算し、現在の株価と比較して投資判断をサポートします。")

# DCF計算の説明を追加
with st.expander("🔍 DCF計算方法について詳しく"):
    st.markdown("""
    <h3>DCF法とは？</h3>
    <p>DCF（Discounted Cash Flow：割引キャッシュフロー）法は、企業の<strong>将来の収益</strong>を予測し、
    それを<strong>現在の価値</strong>に割り引くことで企業の本質的価値を算出する方法です。</p>
    
    <h3>計算の流れ</h3>
    <ol>
        <li><strong>予測期間の設定</strong>：通常3～5年間の将来キャッシュフローを予測します</li>
        <li><strong>売上高の予測</strong>：売上高成長率を使って将来の売上高を予測します</li>
        <li><strong>純利益の計算</strong>：純利益率を使って将来の純利益を計算します</li>
        <li><strong>フリーキャッシュフローの計算</strong>：純利益の80%をフリーキャッシュフローと仮定します（このアプリでは簡易版として）</li>
        <li><strong>割引率の適用</strong>：将来のキャッシュフローを割引率で現在価値に割り引きます</li>
        <li><strong>終末価値の計算</strong>：予測期間以降の永続的な価値を計算します（永続成長率2%を使用）</li>
        <li><strong>企業価値の合計</strong>：割引後のキャッシュフローと終末価値を合計します</li>
        <li><strong>1株あたり価値の計算</strong>：企業価値合計を発行済株式数で割って算出します</li>
    </ol>
    
    <h3>単純化した計算式</h3>
    <p>企業価値 = 予測期間のDCF合計 + 終末価値</p>
    <p>1株あたり企業価値 = 企業価値 ÷ 発行済株式数</p>
    
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 20px;">
    <p style="margin-bottom: 5px;"><strong>注意点</strong>：</p>
    <ul style="margin-top: 0;">
        <li>DCF法は将来予測に依存するため、パラメータ変更で結果が大きく変わります</li>
        <li>感度分析を使って、成長率や割引率の変動が企業価値に与える影響を確認しましょう</li>
        <li>DCF法は完璧な方法ではないため、他の評価方法と組み合わせて総合的に判断しましょう</li>
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
        st.markdown(f"**時価総額**: ${(stock_data['current_price'] * stock_data['shares_outstanding']):.2f}百万")
    
    with col3:
        st.markdown(f"**発行済株式数**: {stock_data['shares_outstanding']:.2f}百万株")
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
        forecast_years = st.slider("予測期間（年）", min_value=1, max_value=5, value=3, step=1)
        revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=stock_data.get('historical_growth', 10.0), step=0.5)
    
    with col2:
        # 割引率とマージン
        discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5)
        net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=(net_income / revenue * 100) if revenue > 0 else 15.0, step=0.5)
        
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
            
            # フリーキャッシュフローの計算（簡易版：純利益の80%としてフリーキャッシュフローを推定）
            forecasted_data['free_cash_flow'] = forecasted_data['net_income'] * 0.8
            
            # 進捗バーの更新
            progress_bar.progress(50)
            
            # 企業価値の計算（簡易版DCF）
            discount_factors = [(1 + discount_rate/100) ** -year for year in forecasted_data['year']]
            discounted_cash_flows = [cf * df for cf, df in zip(forecasted_data['free_cash_flow'], discount_factors)]
            
            # 終末価値の計算（ゴードンモデル、永続成長率2%で固定）
            terminal_value = forecasted_data['free_cash_flow'].iloc[-1] * (1 + 2.0/100) / ((discount_rate/100) - (2.0/100))
            discounted_terminal_value = terminal_value * discount_factors[-1]
            
            # 企業価値の総和
            total_dcf = sum(discounted_cash_flows) + discounted_terminal_value
            equity_value = total_dcf # 簡略化のため、負債は無視
            
            # 1株あたり価値 (shares_outstandingは百万株単位から実際の株式数に変換)
            per_share_value = equity_value / (stock_data['shares_outstanding'] * 1000000)
            
            # 上昇余地の計算
            upside_potential = ((per_share_value / current_stock_price) - 1) * 100
            
            # 進捗バーの完了
            progress_bar.progress(100)
            
            # 結果表示
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>企業価値分析結果</h2>", unsafe_allow_html=True)
            
            # 平均株価と割引を計算（この時点ではまだないため）
            final_year_revenue = forecasted_data['revenue'].iloc[-1]
            final_year_net_income = forecasted_data['net_income'].iloc[-1]
            estimated_equity = final_year_net_income * 10
            
            per_valuation = final_year_net_income * industry_per
            psr_valuation = final_year_revenue * industry_psr
            pbr_valuation = estimated_equity * industry_pbr
            
            per_share_price = per_valuation / (stock_data['shares_outstanding'] * 1000000)
            psr_share_price = psr_valuation / (stock_data['shares_outstanding'] * 1000000)
            pbr_share_price = pbr_valuation / (stock_data['shares_outstanding'] * 1000000)
            
            avg_multiple_price = (per_share_price + psr_share_price + pbr_share_price) / 3
            discounted_multiple_price = avg_multiple_price / (1 + discount_rate/100)
            multiple_upside = ((discounted_multiple_price / current_stock_price) - 1) * 100
            
            # 評価方法の比較表示
            st.markdown("<h3>評価方法の比較</h3>", unsafe_allow_html=True)
            
            comparison_data = pd.DataFrame({
                '評価方法': ['DCF法', '業界平均倍率法'],
                '企業価値（$/株）': [per_share_value, discounted_multiple_price],
                '上昇余地': [upside_potential, multiple_upside]
            })
            
            # 平均値を追加
            avg_value = (per_share_value + discounted_multiple_price) / 2
            avg_upside = ((avg_value / current_stock_price) - 1) * 100
            avg_row = pd.DataFrame({
                '評価方法': ['平均値'],
                '企業価値（$/株）': [avg_value],
                '上昇余地': [avg_upside]
            })
            comparison_data = pd.concat([comparison_data, avg_row], ignore_index=True)
            
            # フォーマット
            comparison_data['企業価値（$/株）'] = comparison_data['企業価値（$/株）'].map('${:.2f}'.format)
            comparison_data['上昇余地'] = comparison_data['上昇余地'].map('{:+.1f}%'.format)
            
            st.dataframe(comparison_data, use_container_width=True)
            
            # DCF分析結果
            st.markdown("<h3>DCF分析結果</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${per_share_value:.2f}</p>
                    <p class='result-label'>DCF法による1株価値</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                upside_class = "up-value" if upside_potential >= 0 else "down-value"
                upside_sign = "+" if upside_potential >= 0 else ""
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {upside_class}'>{upside_sign}{upside_potential:.1f}%</p>
                    <p class='result-label'>DCF法による上昇余地</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # 総合的な投資推奨度（DCFと倍率法の平均）
                avg_upside = (upside_potential + multiple_upside) / 2
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
                </div>
                """, unsafe_allow_html=True)
            
            # 詳細なDCF計算結果の表示
            st.markdown("<h3>予測財務データ</h3>", unsafe_allow_html=True)
            
            # データフレームの表示用にカラム名を変更
            display_df = forecasted_data.copy()
            display_df.columns = ['予測年', '売上高（$）', '純利益（$）', 'フリーキャッシュフロー（$）']
            # 数値を見やすく表示するためにフォーマット
            for col in display_df.columns[1:]:
                display_df[col] = display_df[col].map('${:,.0f}'.format)
            st.dataframe(display_df, use_container_width=True)
            
            # 業界平均倍率による評価
            st.markdown("<h3>業界平均倍率による評価</h3>", unsafe_allow_html=True)
            
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
            
            # 現在価値への割引（割引率を1年分適用）
            discounted_multiple_price = avg_multiple_price / (1 + discount_rate/100)
            
            # 上昇余地
            multiple_upside = ((discounted_multiple_price / current_stock_price) - 1) * 100
            
            # 業界平均倍率による評価結果の表示
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${per_share_price:.2f}</p>
                    <p class='result-label'>PERベース価値</p>
                    <p class='result-note'>PER: {industry_per}倍</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${psr_share_price:.2f}</p>
                    <p class='result-label'>PSRベース価値</p>
                    <p class='result-note'>PSR: {industry_psr}倍</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${pbr_share_price:.2f}</p>
                    <p class='result-label'>PBRベース価値</p>
                    <p class='result-note'>PBR: {industry_pbr}倍</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                upside_class = "up-value" if multiple_upside >= 0 else "down-value"
                upside_sign = "+" if multiple_upside >= 0 else ""
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${discounted_multiple_price:.2f}</p>
                    <p class='result-label'>倍率法による割引後価値</p>
                    <p class='result-note'>割引率: {discount_rate}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {upside_class}'>{upside_sign}{multiple_upside:.1f}%</p>
                    <p class='result-label'>倍率法による上昇余地</p>
                    <p class='result-note'>現在株価: ${current_stock_price:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
            # 業界平均倍率による評価の説明
            with st.expander("📈 業界平均倍率評価について"):
                st.markdown(f"""
                <h4>業界平均倍率による評価とは？</h4>
                <p>企業の将来財務予測（{forecast_years}年後）に業界平均倍率を適用して株価を推定する方法です。</p>
                
                <h4>使用している主な倍率</h4>
                <ul>
                    <li><strong>PER（株価収益率）</strong>：純利益に対する倍率。{industry_per}倍を使用</li>
                    <li><strong>PSR（株価売上高倍率）</strong>：売上高に対する倍率。{industry_psr}倍を使用</li>
                    <li><strong>PBR（株価純資産倍率）</strong>：純資産に対する倍率。{industry_pbr}倍を使用</li>
                </ul>
                
                <h4>計算方法</h4>
                <p>1. {forecast_years}年後の財務予測を使用:</p>
                <ul>
                    <li>売上高: ${final_year_revenue:,.0f}</li>
                    <li>純利益: ${final_year_net_income:,.0f}</li>
                    <li>推定純資産: ${estimated_equity:,.0f}</li>
                </ul>
                
                <p>2. 各倍率ベースの企業価値:</p>
                <ul>
                    <li>PERベース: ${final_year_net_income:,.0f} × {industry_per} = ${per_valuation:,.0f}</li>
                    <li>PSRベース: ${final_year_revenue:,.0f} × {industry_psr} = ${psr_valuation:,.0f}</li>
                    <li>PBRベース: ${estimated_equity:,.0f} × {industry_pbr} = ${pbr_valuation:,.0f}</li>
                </ul>
                
                <p>3. 1株あたり価値計算:</p>
                <ul>
                    <li>PERベース: ${per_valuation:,.0f} ÷ {stock_data['shares_outstanding'] * 1000000:,.0f}株 = ${per_share_price:.2f}</li>
                    <li>PSRベース: ${psr_valuation:,.0f} ÷ {stock_data['shares_outstanding'] * 1000000:,.0f}株 = ${psr_share_price:.2f}</li>
                    <li>PBRベース: ${pbr_valuation:,.0f} ÷ {stock_data['shares_outstanding'] * 1000000:,.0f}株 = ${pbr_share_price:.2f}</li>
                </ul>
                
                <p>4. 平均株価の計算: (${per_share_price:.2f} + ${psr_share_price:.2f} + ${pbr_share_price:.2f}) ÷ 3 = ${avg_multiple_price:.2f}</p>
                
                <p>5. 割引率{discount_rate}%を使った現在価値への割引: ${avg_multiple_price:.2f} ÷ (1 + {discount_rate/100}) = ${discounted_multiple_price:.2f}</p>
                
                <p>6. 上昇余地の計算: (${discounted_multiple_price:.2f} ÷ ${current_stock_price:.2f} - 1) × 100 = {multiple_upside:.1f}%</p>
                """, unsafe_allow_html=True)
            
            # DCF構成要素の内訳
            st.markdown("<h3>DCF構成要素</h3>", unsafe_allow_html=True)
            
            # 計算過程の説明を追加
            with st.expander("📊 計算過程の詳細説明"):
                st.markdown(f"""
                <h4>1. 予測売上高と純利益の計算</h4>
                <p>入力された売上高成長率 <strong>{revenue_growth:.1f}%</strong> を使用して、{forecast_years}年間の売上高を予測しました。</p>
                <p>入力された純利益率 <strong>{net_margin:.1f}%</strong> を使用して、各年の純利益を計算しました。</p>
                
                <h4>2. フリーキャッシュフローへの変換</h4>
                <p>各年の純利益の <strong>80%</strong> をフリーキャッシュフロー(FCF)と仮定しました。</p>
                <p>これは投資や運転資本の変動を簡略化した推定方法です。</p>
                
                <h4>3. 割引率の適用</h4>
                <p>割引率 <strong>{discount_rate:.1f}%</strong> を使用して、将来のキャッシュフローを現在価値に割り引きました。</p>
                <p>割引係数 = 1 ÷ (1 + 割引率)<sup>年数</sup></p>
                <p>各年の割引係数: {[f"{df:.4f}" for df in discount_factors]}</p>
                
                <h4>4. 終末価値の計算</h4>
                <p>予測期間終了後の永続的な価値（終末価値）を計算しました。</p>
                <p>終末価値計算式: 最終年FCF × (1 + 永続成長率) ÷ (割引率 - 永続成長率)</p>
                <p>永続成長率は<strong>2.0%</strong>で固定しています。</p>
                <p>終末価値（割引前）: ${terminal_value / discount_factors[-1]:,.0f}</p>
                <p>終末価値（割引後）: ${discounted_terminal_value:,.0f}</p>
                
                <h4>5. 企業価値の計算</h4>
                <p>企業価値 = 予測期間の割引キャッシュフロー合計 + 割引後の終末価値</p>
                <p>企業価値: ${total_dcf:,.0f}</p>
                
                <h4>6. 1株あたり価値の計算</h4>
                <p>1株あたり価値 = 企業価値 ÷ 発行済株式数</p>
                <p>発行済株式数: {stock_data['shares_outstanding'] * 1000000:,.0f}株</p>
                <p>1株あたり価値: ${per_share_value:.2f}</p>
                """, unsafe_allow_html=True)
            
            dcf_components = pd.DataFrame({
                '項目': ['予測期間のDCF', '終末価値', '企業価値合計', '1株あたり企業価値'],
                '金額（$）': [
                    sum(discounted_cash_flows),
                    discounted_terminal_value,
                    total_dcf,
                    per_share_value
                ]
            })
            
            # 最後の行は1株あたりの値なので別表示
            enterprise_value_df = dcf_components.iloc[:-1].copy()
            enterprise_value_df['割合'] = enterprise_value_df['金額（$）'] / total_dcf * 100
            enterprise_value_df['割合'] = enterprise_value_df['割合'].map('{:.1f}%'.format)
            
            # 金額を見やすく表示するためにフォーマット
            enterprise_value_df['金額（$）'] = enterprise_value_df['金額（$）'].map('${:,.0f}'.format)
            
            st.dataframe(enterprise_value_df, use_container_width=True)
            
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
                    
                    # フリーキャッシュフローの計算（純利益の80%と仮定）
                    forecasted_data_sens['free_cash_flow'] = forecasted_data_sens['net_income'] * 0.8
                    
                    # 企業価値の計算
                    discount_factors_sens = [(1 + d/100) ** -year for year in forecasted_data_sens['year']]
                    discounted_cash_flows_sens = [cf * df for cf, df in zip(forecasted_data_sens['free_cash_flow'], discount_factors_sens)]
                    
                    # 終末価値の計算（永続成長率2%で固定）
                    terminal_value_sens = forecasted_data_sens['free_cash_flow'].iloc[-1] * (1 + 2.0/100) / ((d/100) - (2.0/100))
                    discounted_terminal_value_sens = terminal_value_sens * discount_factors_sens[-1]
                    
                    # 企業価値の総和
                    total_dcf_sens = sum(discounted_cash_flows_sens) + discounted_terminal_value_sens
                    
                    # 1株あたり価値（百万株単位から実際の株式数に変換）
                    per_share_value_sens = total_dcf_sens / (stock_data['shares_outstanding'] * 1000000)
                    
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