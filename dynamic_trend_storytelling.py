import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_stock_story_data(ticker, period="1y"):
    """Get comprehensive stock data for storytelling visualization"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical data
        hist = stock.history(period=period)
        if hist.empty:
            return None
            
        # Get company info
        info = stock.info
        
        # Get financial data
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        
        # Get earnings data
        earnings = stock.earnings_history
        
        # Calculate key metrics
        current_price = hist['Close'].iloc[-1]
        start_price = hist['Close'].iloc[0]
        price_change = ((current_price - start_price) / start_price) * 100
        
        # Volatility analysis
        returns = hist['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
        
        # Volume analysis
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].tail(5).mean()
        volume_trend = "increasing" if recent_volume > avg_volume else "decreasing"
        
        # Price momentum
        ma_20 = hist['Close'].rolling(20).mean()
        ma_50 = hist['Close'].rolling(50).mean()
        
        return {
            'ticker': ticker,
            'company_name': info.get('longName', ticker),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'hist': hist,
            'info': info,
            'current_price': current_price,
            'start_price': start_price,
            'price_change': price_change,
            'volatility': volatility,
            'volume_trend': volume_trend,
            'avg_volume': avg_volume,
            'recent_volume': recent_volume,
            'ma_20': ma_20,
            'ma_50': ma_50,
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'revenue': info.get('totalRevenue', 0),
            'financials': financials,
            'earnings': earnings
        }
        
    except Exception as e:
        st.error(f"データ取得エラー: {str(e)}")
        return None

def create_story_narrative(data):
    """Generate dynamic narrative based on stock performance"""
    if not data:
        return "データが利用できません"
    
    ticker = data['ticker']
    company = data['company_name']
    sector = data['sector']
    price_change = data['price_change']
    volatility = data['volatility']
    volume_trend = data['volume_trend']
    
    # Price performance story
    if price_change > 20:
        performance_story = f"🚀 **驚異的な成長**: {company}は素晴らしいパフォーマンスを見せており、{price_change:.1f}%の上昇を記録しています。"
    elif price_change > 10:
        performance_story = f"📈 **堅調な成長**: {company}は安定した上昇トレンドを維持し、{price_change:.1f}%のプラスリターンを達成しています。"
    elif price_change > 0:
        performance_story = f"🔄 **緩やかな上昇**: {company}は{price_change:.1f}%の小幅な上昇を見せており、底堅い動きを続けています。"
    elif price_change > -10:
        performance_story = f"📉 **軽微な調整**: {company}は{abs(price_change):.1f}%の調整局面にありますが、これは正常な市場の動きと考えられます。"
    else:
        performance_story = f"⚠️ **大幅な下落**: {company}は{abs(price_change):.1f}%の大きな下落を経験しており、注意深い分析が必要です。"
    
    # Volatility story
    if volatility > 40:
        volatility_story = f"この期間中、株価は{volatility:.1f}%の高いボラティリティを示しており、リスクの高い投資対象となっています。"
    elif volatility > 20:
        volatility_story = f"株価ボラティリティは{volatility:.1f}%で、適度なリスクレベルを維持しています。"
    else:
        volatility_story = f"株価は{volatility:.1f}%の低いボラティリティで安定した動きを見せており、堅実な投資選択肢と言えるでしょう。"
    
    # Volume story
    if volume_trend == "increasing":
        volume_story = "最近の取引量増加は投資家の関心の高まりを示唆しています。"
    else:
        volume_story = "取引量の減少は市場の関心の低下または安定期を反映している可能性があります。"
    
    # Sector context
    sector_story = f"{sector}セクターに属する{company}は、業界特有の動向と市場環境の影響を受けています。"
    
    return f"""
    {performance_story}
    
    {sector_story}
    
    {volatility_story} {volume_story}
    
    この分析は過去のデータに基づいており、将来の投資成果を保証するものではありません。
    """

def identify_key_events(data):
    """Identify significant price movements and events"""
    hist = data['hist']
    events = []
    
    # Daily returns
    returns = hist['Close'].pct_change()
    
    # Find significant movements (>5% daily change)
    significant_moves = returns[abs(returns) > 0.05]
    
    for date, return_val in significant_moves.items():
        if return_val > 0.05:
            events.append({
                'date': date,
                'type': 'surge',
                'magnitude': return_val * 100,
                'description': f"+{return_val*100:.1f}%の急騰"
            })
        elif return_val < -0.05:
            events.append({
                'date': date,
                'type': 'drop',
                'magnitude': abs(return_val * 100),
                'description': f"-{abs(return_val)*100:.1f}%の急落"
            })
    
    # Find price peaks and troughs
    closes = hist['Close']
    
    # Recent high/low
    recent_high = closes.tail(30).max()
    recent_low = closes.tail(30).min()
    current = closes.iloc[-1]
    
    if current == recent_high:
        events.append({
            'date': closes.tail(30).idxmax(),
            'type': 'peak',
            'description': "30日間の最高値更新"
        })
    
    if current == recent_low:
        events.append({
            'date': closes.tail(30).idxmin(),
            'type': 'trough',
            'description': "30日間の最安値"
        })
    
    return events[:10]  # Return top 10 events

def create_storytelling_chart(data):
    """Create an interactive storytelling chart"""
    if not data:
        return None
    
    hist = data['hist']
    
    # Create subplot with secondary y-axis for volume
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=('株価推移とストーリーポイント', '取引量'),
        vertical_spacing=0.1
    )
    
    # Price line with gradient
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            name='株価',
            line=dict(
                color='rgba(102, 126, 234, 1)',
                width=3
            ),
            hovertemplate='<b>%{x}</b><br>株価: ¥%{y:,.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=data['ma_20'],
            mode='lines',
            name='20日移動平均',
            line=dict(color='orange', width=2, dash='dash'),
            opacity=0.7
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=data['ma_50'],
            mode='lines',
            name='50日移動平均',
            line=dict(color='red', width=2, dash='dash'),
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Identify and mark key events
    events = identify_key_events(data)
    
    for event in events:
        if event['type'] == 'surge':
            color = 'green'
            symbol = 'triangle-up'
        elif event['type'] == 'drop':
            color = 'red'
            symbol = 'triangle-down'
        elif event['type'] == 'peak':
            color = 'gold'
            symbol = 'star'
        else:
            color = 'blue'
            symbol = 'circle'
        
        # Get price for that date
        try:
            price = hist.loc[event['date'], 'Close']
            fig.add_trace(
                go.Scatter(
                    x=[event['date']],
                    y=[price],
                    mode='markers',
                    name=event['description'],
                    marker=dict(
                        color=color,
                        size=12,
                        symbol=symbol,
                        line=dict(color='white', width=2)
                    ),
                    hovertemplate=f"<b>{event['description']}</b><br>%{{x}}<br>株価: ¥%{{y:,.2f}}<extra></extra>"
                ),
                row=1, col=1
            )
        except:
            continue
    
    # Volume bars
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='取引量',
            marker_color='rgba(102, 126, 234, 0.3)',
            hovertemplate='<b>%{x}</b><br>取引量: %{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"{data['company_name']} ({data['ticker']}) - 株価ストーリー",
            font=dict(size=20, color='#1f2937')
        ),
        template='plotly_white',
        height=700,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(title_text="日付", row=2, col=1)
    fig.update_yaxes(title_text="株価 (¥)", row=1, col=1)
    fig.update_yaxes(title_text="取引量", row=2, col=1)
    
    return fig

def create_sentiment_analysis(data):
    """Analyze market sentiment based on price action"""
    if not data:
        return {}
    
    hist = data['hist']
    
    # Recent price momentum (last 20 days)
    recent_returns = hist['Close'].pct_change().tail(20)
    positive_days = (recent_returns > 0).sum()
    negative_days = (recent_returns < 0).sum()
    
    # Price vs moving averages
    current_price = data['current_price']
    ma_20_current = data['ma_20'].iloc[-1] if not pd.isna(data['ma_20'].iloc[-1]) else current_price
    ma_50_current = data['ma_50'].iloc[-1] if not pd.isna(data['ma_50'].iloc[-1]) else current_price
    
    # Sentiment scoring
    sentiment_score = 0
    
    # Price momentum
    if positive_days > negative_days:
        sentiment_score += 1
    elif negative_days > positive_days:
        sentiment_score -= 1
    
    # Moving average position
    if current_price > ma_20_current:
        sentiment_score += 1
    else:
        sentiment_score -= 1
        
    if current_price > ma_50_current:
        sentiment_score += 1
    else:
        sentiment_score -= 1
    
    # Volume trend
    if data['volume_trend'] == 'increasing':
        sentiment_score += 1
    else:
        sentiment_score -= 1
    
    # Determine overall sentiment
    if sentiment_score >= 2:
        sentiment = "強気 (Bullish)"
        sentiment_color = "green"
        sentiment_emoji = "🟢"
    elif sentiment_score <= -2:
        sentiment = "弱気 (Bearish)"
        sentiment_color = "red"
        sentiment_emoji = "🔴"
    else:
        sentiment = "中立 (Neutral)"
        sentiment_color = "orange"
        sentiment_emoji = "🟡"
    
    return {
        'sentiment': sentiment,
        'score': sentiment_score,
        'color': sentiment_color,
        'emoji': sentiment_emoji,
        'positive_days': positive_days,
        'negative_days': negative_days,
        'above_ma20': current_price > ma_20_current,
        'above_ma50': current_price > ma_50_current
    }

def display_storytelling_visualization(ticker):
    """Main function to display the storytelling visualization"""
    
    # Period selection
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 📈 {ticker} - 動的株価ストーリー分析")
    with col2:
        period = st.selectbox(
            "期間選択",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=3,
            format_func=lambda x: {
                "1mo": "1ヶ月",
                "3mo": "3ヶ月", 
                "6mo": "6ヶ月",
                "1y": "1年",
                "2y": "2年"
            }[x]
        )
    
    # Get data
    with st.spinner("株価データを分析中..."):
        data = get_stock_story_data(ticker, period)
    
    if not data:
        st.error("データを取得できませんでした。銘柄コードを確認してください。")
        return
    
    # Display main storytelling chart
    chart = create_storytelling_chart(data)
    if chart:
        st.plotly_chart(chart, use_container_width=True)
    
    # Story narrative and sentiment analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📖 株価ストーリー")
        narrative = create_story_narrative(data)
        st.markdown(narrative)
        
        # Key events
        events = identify_key_events(data)
        if events:
            st.markdown("### 🎯 注目すべき出来事")
            for event in events[:5]:  # Show top 5 events
                st.markdown(f"- **{event['date'].strftime('%Y-%m-%d')}**: {event['description']}")
    
    with col2:
        # Sentiment analysis
        sentiment = create_sentiment_analysis(data)
        
        st.markdown("### 🎭 市場センチメント")
        st.markdown(f"**総合判定**: {sentiment['emoji']} {sentiment['sentiment']}")
        
        # Sentiment details
        st.markdown("**詳細分析:**")
        st.markdown(f"- 上昇日数: {sentiment['positive_days']}/20日")
        st.markdown(f"- 下落日数: {sentiment['negative_days']}/20日")
        st.markdown(f"- 20日平均上: {'✅' if sentiment['above_ma20'] else '❌'}")
        st.markdown(f"- 50日平均上: {'✅' if sentiment['above_ma50'] else '❌'}")
        
        # Key metrics
        st.markdown("### 📊 主要指標")
        st.metric("現在株価", f"${data['current_price']:.2f}")
        st.metric("期間リターン", f"{data['price_change']:.2f}%")
        st.metric("ボラティリティ", f"{data['volatility']:.1f}%")
        
        if data['pe_ratio']:
            st.metric("PER", f"{data['pe_ratio']:.1f}")

def render_dynamic_storytelling_page():
    """Render the main storytelling page"""
    
    # Custom CSS for storytelling theme
    st.markdown("""
    <style>
        .storytelling-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .story-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        .sentiment-badge {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="storytelling-header">
        <h1>📚 動的株価ストーリー可視化</h1>
        <p>株価の動きを物語として理解し、市場の心理と トレンドを視覚的に分析</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock selection
    st.markdown("### 🎯 分析する銘柄を選択")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker_input = st.text_input(
            "銘柄コードを入力",
            value="AAPL",
            placeholder="例: AAPL, MSFT, TSLA"
        )
    with col2:
        analyze_button = st.button("分析開始", type="primary", use_container_width=True)
    
    # Popular stocks quick selection
    st.markdown("**人気銘柄から選択:**")
    popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX"]
    
    cols = st.columns(len(popular_stocks))
    for i, stock in enumerate(popular_stocks):
        with cols[i]:
            if st.button(stock, key=f"popular_{stock}"):
                ticker_input = stock
                analyze_button = True
    
    # Show analysis if button clicked or ticker entered
    if analyze_button or ticker_input:
        if ticker_input:
            display_storytelling_visualization(ticker_input.upper())
        else:
            st.warning("銘柄コードを入力してください。")
    
    # Feature explanation
    with st.expander("💡 この機能について"):
        st.markdown("""
        **動的株価ストーリー可視化**は、単なる株価チャートを超えて、以下の要素を統合した包括的な分析を提供します：
        
        - **📈 視覚的ストーリーテリング**: 株価の動きを物語として表現
        - **🎯 重要イベント特定**: 急騰・急落などの注目すべき動きを自動検出
        - **🎭 センチメント分析**: 市場心理を数値化して表示
        - **📊 テクニカル分析**: 移動平均、ボラティリティなどの指標を統合
        - **🔍 コンテキスト情報**: セクター動向や企業特性を考慮した解説
        
        この分析により、投資判断に必要な「なぜそうなったのか」という背景を理解できます。
        """)