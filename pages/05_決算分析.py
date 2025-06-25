import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime, timedelta

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from auto_financial_data import get_auto_financial_data
from comprehensive_market_stocks import get_all_market_stocks
from format_helpers import format_currency, format_large_number

# Modern design CSS
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
    
    /* Earnings card */
    .earnings-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .trend-positive {
        color: #10b981;
    }
    
    .trend-negative {
        color: #ef4444;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### 📈 決算分析 - 最新の業績データと市場動向")

# Company selection
st.markdown("#### 企業を選択")
col1, col2 = st.columns([3, 1])

with col1:
    # Get comprehensive list of market stocks
    all_tickers = get_all_market_stocks()
    selected_ticker = st.selectbox(
        "分析したい企業のティッカーシンボルを選択",
        options=all_tickers,
        index=0 if all_tickers else None,
        help="企業のティッカーシンボル（例：AAPL、MSFT、GOOGL）"
    )

with col2:
    analyze_button = st.button("📊 決算分析", type="primary", use_container_width=True)

if analyze_button and selected_ticker:
    with st.spinner(f"{selected_ticker}の決算データを分析中..."):
        # Get comprehensive financial data
        data = get_auto_financial_data(selected_ticker)
        
        if data:
            # Company header
            st.markdown(f"""
            <div class="earnings-card">
                <h2 style="margin: 0; color: #1e293b;">{data.get('name', selected_ticker)} ({selected_ticker})</h2>
                <p style="margin: 0.5rem 0 0 0; color: #64748b;">
                    セクター: {data.get('sector', 'N/A')} | 
                    現在株価: ${data.get('current_price', 0):.2f} | 
                    時価総額: {format_currency(data.get('market_cap', 0), use_ja_format=True)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Key financial metrics
            st.markdown('<div class="section-header">📊 主要財務指標</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                revenue_growth = data.get('historical_growth', 0) or 0
                trend_class = "trend-positive" if revenue_growth > 0 else "trend-negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{revenue_growth:.1f}%</div>
                    <div class="metric-label">売上成長率</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                roe = data.get('roe', 0) or 0
                trend_class = "trend-positive" if roe > 15 else "trend-negative" if roe < 10 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{roe:.1f}%</div>
                    <div class="metric-label">ROE</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                profit_margin = data.get('profit_margin', 0) or 0
                trend_class = "trend-positive" if profit_margin > 20 else "trend-negative" if profit_margin < 5 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{profit_margin:.1f}%</div>
                    <div class="metric-label">純利益率</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                pe_ratio = data.get('pe_ratio', 0) or 0
                trend_class = "trend-positive" if 10 <= pe_ratio <= 25 else "trend-negative" if pe_ratio > 30 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{pe_ratio:.1f}</div>
                    <div class="metric-label">PER</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Financial health indicators
            st.markdown('<div class="section-header">💪 財務健全性</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                debt_ratio = data.get('debt_to_equity', 0) or 0
                trend_class = "trend-positive" if debt_ratio < 0.5 else "trend-negative" if debt_ratio > 1.0 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{debt_ratio:.2f}</div>
                    <div class="metric-label">負債比率</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                current_ratio = data.get('current_ratio', 0) or 0
                trend_class = "trend-positive" if current_ratio > 1.2 else "trend-negative" if current_ratio < 1.0 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{current_ratio:.2f}</div>
                    <div class="metric-label">流動比率</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                roa = data.get('roa', 0) or 0
                trend_class = "trend-positive" if roa > 10 else "trend-negative" if roa < 5 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{roa:.1f}%</div>
                    <div class="metric-label">ROA</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Valuation metrics
            st.markdown('<div class="section-header">💰 バリュエーション</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pb_ratio = data.get('pb_ratio', 0) or 0
                trend_class = "trend-positive" if 1 <= pb_ratio <= 3 else "trend-negative" if pb_ratio > 5 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{pb_ratio:.1f}</div>
                    <div class="metric-label">PBR</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Calculate price-to-sales ratio
                market_cap = data.get('market_cap', 0) or 0
                revenue = data.get('revenue', 0) or 0
                ps_ratio = (market_cap / revenue) if revenue > 0 else 0
                trend_class = "trend-positive" if 1 <= ps_ratio <= 5 else "trend-negative" if ps_ratio > 10 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{ps_ratio:.1f}</div>
                    <div class="metric-label">PSR</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Calculate enterprise value
                enterprise_value = market_cap + (data.get('total_debt', 0) or 0) - (data.get('cash', 0) or 0)
                ev_revenue = (enterprise_value / revenue) if revenue > 0 else 0
                trend_class = "trend-positive" if 1 <= ev_revenue <= 8 else "trend-negative" if ev_revenue > 15 else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {trend_class}">{ev_revenue:.1f}</div>
                    <div class="metric-label">EV/売上</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Investment recommendation
            st.markdown('<div class="section-header">🎯 投資推奨</div>', unsafe_allow_html=True)
            
            # Calculate overall score
            score = 0
            max_score = 7
            
            if revenue_growth > 10: score += 1
            if roe > 15: score += 1
            if profit_margin > 15: score += 1
            if debt_ratio < 0.5: score += 1
            if current_ratio > 1.2: score += 1
            if 10 <= pe_ratio <= 25: score += 1
            if 1 <= pb_ratio <= 3: score += 1
            
            score_percentage = (score / max_score) * 100
            
            if score_percentage >= 70:
                recommendation = "強い買い推奨"
                rec_color = "#10b981"
            elif score_percentage >= 50:
                recommendation = "買い推奨"
                rec_color = "#3b82f6"
            elif score_percentage >= 30:
                recommendation = "ホールド"
                rec_color = "#f59e0b"
            else:
                recommendation = "売り推奨"
                rec_color = "#ef4444"
            
            st.markdown(f"""
            <div class="earnings-card" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700; color: {rec_color}; margin-bottom: 1rem;">
                    {recommendation}
                </div>
                <div style="font-size: 1.2rem; color: #64748b; margin-bottom: 1rem;">
                    財務スコア: {score}/{max_score} ({score_percentage:.0f}%)
                </div>
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; color: #475569;">
                    この評価は財務指標に基づく定量分析です。投資判断には市場環境、業界動向、企業の戦略などの定性要因も考慮してください。
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error(f"❌ {selected_ticker}の財務データを取得できませんでした。別のティッカーシンボルを試してください。")

# Market overview section
st.markdown('<div class="section-header">📈 市場概況</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="earnings-card">
        <h3 style="color: #1e293b; margin-top: 0;">今四半期の注目ポイント</h3>
        <ul style="color: #475569; line-height: 1.8;">
            <li>インフレ圧力とFRBの金融政策動向</li>
            <li>AI関連企業の収益成長と投資動向</li>
            <li>消費者支出パターンの変化</li>
            <li>サプライチェーン正常化の進展</li>
            <li>エネルギー価格の安定化</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="earnings-card">
        <h3 style="color: #1e293b; margin-top: 0;">投資家が注目すべき指標</h3>
        <ul style="color: #475569; line-height: 1.8;">
            <li>売上成長率と収益性の持続可能性</li>
            <li>フリーキャッシュフローの安定性</li>
            <li>負債水準と資本効率</li>
            <li>経営陣のガイダンスと戦略</li>
            <li>市場シェアと競争優位性</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Educational section
with st.expander("💡 決算分析のポイント"):
    st.markdown("""
    ### 決算分析で重要な指標の見方
    
    **収益性指標**
    - **売上成長率**: 企業の事業拡大力を示す。10%以上が理想的
    - **純利益率**: 売上に対する最終的な利益の割合。業界平均との比較が重要
    - **ROE**: 株主資本の効率性。15%以上が優秀とされる
    
    **健全性指標**
    - **負債比率**: 自己資本に対する負債の割合。0.5以下が健全
    - **流動比率**: 短期債務に対する支払い能力。1.2以上が安全
    - **ROA**: 総資産の効率性。10%以上が優秀
    
    **バリュエーション指標**
    - **PER**: 株価の割安・割高を判断。業界平均との比較が重要
    - **PBR**: 資産価値に対する株価の水準。1-3倍が適正範囲
    - **PSR**: 売上に対する時価総額の倍率。成長企業では高めになる傾向
    
    **注意点**
    - 単一の指標だけでなく総合的に判断する
    - 業界特性と市場環境を考慮する
    - 過去のトレンドと将来の見通しを確認する
    """)