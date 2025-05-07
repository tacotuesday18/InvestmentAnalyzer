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
        # 売上と純利益の入力
        revenue = st.number_input("年間売上高（USD）", value=stock_data['revenue'] * 1000000, step=1000000.0, format="%.0f")
        net_income = st.number_input("年間純利益（USD）", value=stock_data['net_income'] * 1000000, step=1000000.0, format="%.0f")
        
        # 予測期間と成長率
        forecast_years = st.slider("予測期間（年）", min_value=1, max_value=5, value=3, step=1)
        revenue_growth = st.slider("売上高成長率（%）", min_value=-10.0, max_value=50.0, value=stock_data.get('historical_growth', 10.0), step=0.5)
    
    with col2:
        # 割引率とマージン
        discount_rate = st.slider("割引率（%）", min_value=5.0, max_value=25.0, value=10.0, step=0.5)
        net_margin = st.slider("純利益率（%）", min_value=-5.0, max_value=40.0, value=(net_income / revenue * 100) if revenue > 0 else 15.0, step=0.5)
        
        # カスタム株価の入力（オプション）
        custom_stock_price = st.number_input(
            "現在の株価（USD）を上書き（必要な場合のみ）",
            value=0.0,
            step=0.1
        )
        
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
            
            # 1株あたり価値
            per_share_value = equity_value / stock_data['shares_outstanding']
            
            # 上昇余地の計算
            upside_potential = ((per_share_value / current_stock_price) - 1) * 100
            
            # 進捗バーの完了
            progress_bar.progress(100)
            
            # 結果表示
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h2 class='card-title'>DCF分析結果</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value'>${per_share_value:.2f}</p>
                    <p class='result-label'>1株あたり本質的価値</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                upside_class = "up-value" if upside_potential >= 0 else "down-value"
                upside_sign = "+" if upside_potential >= 0 else ""
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {upside_class}'>{upside_sign}{upside_potential:.1f}%</p>
                    <p class='result-label'>上昇余地</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # 投資推奨度の決定
                if upside_potential > 20:
                    recommendation = "強い買い"
                    recommendation_class = "up-value"
                elif upside_potential > 10:
                    recommendation = "買い"
                    recommendation_class = "up-value"
                elif upside_potential > -10:
                    recommendation = "中立"
                    recommendation_class = ""
                elif upside_potential > -20:
                    recommendation = "売り"
                    recommendation_class = "down-value"
                else:
                    recommendation = "強い売り"
                    recommendation_class = "down-value"
                
                st.markdown(f"""
                <div class='result-card'>
                    <p class='result-value {recommendation_class}'>{recommendation}</p>
                    <p class='result-label'>投資推奨度</p>
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
            
            # DCF構成要素の内訳
            st.markdown("<h3>DCF構成要素</h3>", unsafe_allow_html=True)
            
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
                    
                    # 1株あたり価値
                    per_share_value_sens = total_dcf_sens / stock_data['shares_outstanding']
                    
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