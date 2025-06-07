import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import json

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# stock_dataモジュールをインポート
from stock_data import get_stock_data, get_available_tickers, load_sample_data

# ページ設定
st.set_page_config(
    page_title="銘柄スクリーナー - 企業価値分析プロ",
    page_icon="🔎",
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
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 1.8rem !important;
        font-weight: bold;
        color: #0066cc;
    }
    
    .metric-label {
        font-size: 1rem !important;
        color: #666;
    }
    
    .filter-section {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .data-table {
        margin-top: 1.5rem;
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
    
    /* モバイル対応 */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.4rem !important;
        }
        
        .metric-label {
            font-size: 0.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("### 銘柄スクリーナーツール")
    st.markdown("様々な条件で銘柄をフィルタリングして、投資候補を探しましょう。")
    
    st.markdown("---")
    
    # ナビゲーション
    st.markdown("### ナビゲーション")
    if st.button("ホームに戻る", key="home_btn"):
        st.switch_page("app.py")
    
    if st.button("企業分析", key="analysis_btn"):
        st.switch_page("pages/01_企業分析.py")
    
    if st.button("銘柄比較", key="compare_btn"):
        st.switch_page("pages/02_銘柄比較.py")

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">🔎 銘柄スクリーナー</div>
    <div class="page-subtitle">財務指標とバリュエーションで投資候補を効率的に発見</div>
</div>
""", unsafe_allow_html=True)

# 全銘柄データの取得
stocks_data, industry_data = load_sample_data()
stocks_df = pd.DataFrame()

# データフレームの作成
for ticker, data in stocks_data.items():
    row = {
        'ティッカー': ticker,
        '企業名': data['name'],
        '業界': data['industry'],
        '株価': data['current_price'],
        'EPS': data['eps'],
        'PER': data['pe_ratio'],
        'PBR': data['pb_ratio'],
        'PSR': data['ps_ratio'],
        'ROE': data['roe'],
        '成長率': data['historical_growth'],
        '時価総額': data['current_price'] * data['shares_outstanding'],
        '純利益': data['net_income'],
        '売上高': data['revenue']
    }
    stocks_df = pd.concat([stocks_df, pd.DataFrame([row])], ignore_index=True)

# フィルタリングセクション
st.markdown("""
<div class="analysis-card">
    <div class="card-header">条件でフィルタリング</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    industry_filter = st.multiselect(
        "業界",
        options=list(stocks_df['業界'].unique()),
        default=[]
    )
    
    min_price = st.slider(
        "最小株価 ($)",
        min_value=float(stocks_df['株価'].min()),
        max_value=float(stocks_df['株価'].max()),
        value=float(stocks_df['株価'].min())
    )
    
    max_price = st.slider(
        "最大株価 ($)",
        min_value=float(stocks_df['株価'].min()),
        max_value=float(stocks_df['株価'].max()),
        value=float(stocks_df['株価'].max())
    )

with col2:
    min_per = st.slider(
        "最小PER",
        min_value=0.0,
        max_value=200.0,
        value=0.0
    )
    
    max_per = st.slider(
        "最大PER",
        min_value=0.0,
        max_value=200.0,
        value=100.0
    )
    
    min_pbr = st.slider(
        "最小PBR",
        min_value=0.0,
        max_value=30.0,
        value=0.0
    )

with col3:
    min_roe = st.slider(
        "最小ROE (%)",
        min_value=0.0,
        max_value=50.0,
        value=0.0
    )
    
    min_growth = st.slider(
        "最小成長率 (%)",
        min_value=-20.0,
        max_value=150.0,
        value=0.0
    )
    
    sort_by = st.selectbox(
        "並び替え",
        options=["株価", "PER", "PBR", "PSR", "ROE", "成長率", "時価総額"],
        index=1
    )

# フィルタリングの適用
filtered_df = stocks_df.copy()

# 業界フィルタ
if industry_filter:
    filtered_df = filtered_df[filtered_df['業界'].isin(industry_filter)]

# 価格フィルタ
filtered_df = filtered_df[(filtered_df['株価'] >= min_price) & (filtered_df['株価'] <= max_price)]

# PERフィルタ
filtered_df = filtered_df[(filtered_df['PER'] >= min_per) & (filtered_df['PER'] <= max_per)]

# PBRフィルタ
filtered_df = filtered_df[filtered_df['PBR'] >= min_pbr]

# ROEフィルタ
filtered_df = filtered_df[filtered_df['ROE'] >= min_roe]

# 成長率フィルタ
filtered_df = filtered_df[filtered_df['成長率'] >= min_growth]

# 並び替え
filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)

# 統計情報の表示
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <p class='metric-value'>{len(filtered_df)}</p>
        <p class='metric-label'>銘柄数</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_per = filtered_df['PER'].mean()
    st.markdown(f"""
    <div class='metric-card'>
        <p class='metric-value'>{avg_per:.2f}</p>
        <p class='metric-label'>平均PER</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_pbr = filtered_df['PBR'].mean()
    st.markdown(f"""
    <div class='metric-card'>
        <p class='metric-value'>{avg_pbr:.2f}</p>
        <p class='metric-label'>平均PBR</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_roe = filtered_df['ROE'].mean()
    st.markdown(f"""
    <div class='metric-card'>
        <p class='metric-value'>{avg_roe:.2f}%</p>
        <p class='metric-label'>平均ROE</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 結果表示
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>スクリーニング結果</h2>", unsafe_allow_html=True)

# 表示する列を選択
display_columns = ['ティッカー', '企業名', '業界', '株価', 'PER', 'PBR', 'ROE', '成長率']
st.dataframe(filtered_df[display_columns], use_container_width=True)

# 詳細情報表示エリア
st.markdown("<h3>銘柄詳細</h3>", unsafe_allow_html=True)
selected_ticker = st.selectbox(
    "銘柄を選択して詳細を表示",
    options=filtered_df['ティッカー'].tolist(),
    format_func=lambda x: f"{x} - {stocks_data[x]['name']}"
)

if selected_ticker:
    stock_info = get_stock_data(selected_ticker)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**企業名**: {stock_info['name']}")
        st.markdown(f"**業界**: {stock_info['industry']}")
        st.markdown(f"**株価**: ${stock_info['current_price']:.2f}")
        st.markdown(f"**時価総額**: ${(stock_info['current_price'] * stock_info['shares_outstanding']):.2f}百万")
    
    with col2:
        st.markdown(f"**EPS**: ${stock_info['eps']:.2f}")
        st.markdown(f"**1株あたり純資産**: ${stock_info['book_value_per_share']:.2f}")
        st.markdown(f"**PER**: {stock_info['pe_ratio']:.2f}")
        st.markdown(f"**PBR**: {stock_info['pb_ratio']:.2f}")
        st.markdown(f"**PSR**: {stock_info['ps_ratio']:.2f}")
        st.markdown(f"**ROE**: {stock_info['roe']:.2f}%")
    
    # 財務指標の推移グラフ
    if 'historical_data' in stock_info:
        hist_data = stock_info['historical_data']
        
        # 売上高の推移
        revenue_fig = px.bar(
            x=hist_data['years'],
            y=hist_data['revenue'],
            labels={'x': '年度', 'y': '売上高（百万USD）'},
            title=f"{stock_info['name']}の売上高推移"
        )
        revenue_fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(revenue_fig, use_container_width=True)
        
        # 純利益の推移
        income_fig = px.bar(
            x=hist_data['years'],
            y=hist_data['net_income'],
            labels={'x': '年度', 'y': '純利益（百万USD）'},
            title=f"{stock_info['name']}の純利益推移"
        )
        income_fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(income_fig, use_container_width=True)
    
    # 企業分析ページへのリンク
    if st.button("この銘柄を詳細分析", key="analyze_btn", use_container_width=True):
        # セッション変数に銘柄情報を保存
        st.session_state.selected_ticker = selected_ticker
        # 企業分析ページに遷移
        st.switch_page("pages/01_企業分析.py")

st.markdown("</div>", unsafe_allow_html=True)

# バリュエーション分布の可視化
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>バリュエーション分布</h2>", unsafe_allow_html=True)

tabs = st.tabs(["PER分布", "PBR分布", "PSR分布", "ROE分布"])

with tabs[0]:  # PER分布
    per_fig = px.histogram(
        filtered_df,
        x='PER',
        color='業界',
        nbins=20,
        title="業界別PER分布",
        labels={'PER': 'PER (株価収益率)'}
    )
    per_fig.update_layout(
        xaxis_range=[0, 100],  # PERの表示範囲を制限
        bargap=0.1,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(per_fig, use_container_width=True)

with tabs[1]:  # PBR分布
    pbr_fig = px.histogram(
        filtered_df,
        x='PBR',
        color='業界',
        nbins=20,
        title="業界別PBR分布",
        labels={'PBR': 'PBR (株価純資産倍率)'}
    )
    pbr_fig.update_layout(
        xaxis_range=[0, 20],  # PBRの表示範囲を制限
        bargap=0.1,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(pbr_fig, use_container_width=True)

with tabs[2]:  # PSR分布
    psr_fig = px.histogram(
        filtered_df,
        x='PSR',
        color='業界',
        nbins=20,
        title="業界別PSR分布",
        labels={'PSR': 'PSR (株価売上高倍率)'}
    )
    psr_fig.update_layout(
        xaxis_range=[0, 20],  # PSRの表示範囲を制限
        bargap=0.1,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(psr_fig, use_container_width=True)

with tabs[3]:  # ROE分布
    roe_fig = px.histogram(
        filtered_df,
        x='ROE',
        color='業界',
        nbins=20,
        title="業界別ROE分布",
        labels={'ROE': 'ROE (%)'}
    )
    roe_fig.update_layout(
        xaxis_range=[0, 50],  # ROEの表示範囲を制限
        bargap=0.1,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(roe_fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# 業界比較
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>業界比較</h2>", unsafe_allow_html=True)

# 業界ごとの平均値を計算
industry_averages = filtered_df.groupby('業界').agg({
    'PER': 'mean',
    'PBR': 'mean',
    'PSR': 'mean',
    'ROE': 'mean',
    '成長率': 'mean'
}).reset_index()

# 業界比較チャート
industry_chart_type = st.selectbox(
    "表示する指標",
    options=["PER", "PBR", "PSR", "ROE", "成長率"],
    index=0
)

industry_fig = px.bar(
    industry_averages.sort_values(industry_chart_type, ascending=False),
    x='業界',
    y=industry_chart_type,
    color='業界',
    title=f"業界別平均{industry_chart_type}",
    labels={'業界': '業界', industry_chart_type: industry_chart_type}
)
industry_fig.update_layout(
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(industry_fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# バブルチャート（成長率とPERの関係）
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='card-title'>成長率とバリュエーションの関係</h2>", unsafe_allow_html=True)

# X軸とY軸の選択
col1, col2 = st.columns(2)
with col1:
    x_axis = st.selectbox(
        "X軸",
        options=["PER", "PBR", "PSR", "ROE", "成長率"],
        index=0
    )
with col2:
    y_axis = st.selectbox(
        "Y軸",
        options=["PER", "PBR", "PSR", "ROE", "成長率"],
        index=4
    )

# バブルチャート
bubble_fig = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    size="時価総額",
    color="業界",
    hover_name="企業名",
    size_max=60,
    title=f"{x_axis}と{y_axis}の関係",
    labels={x_axis: x_axis, y_axis: y_axis, "時価総額": "時価総額（百万USD）"}
)
bubble_fig.update_layout(
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(bubble_fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)