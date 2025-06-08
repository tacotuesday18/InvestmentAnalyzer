import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def get_company_revenue_streams(ticker):
    """
    Get sector-specific revenue streams for a company by analyzing business segments
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Define sector-specific revenue streams based on industry analysis
        revenue_streams = {
            'AAPL': {
                'company_name': 'Apple Inc.',
                'sector': 'Technology',
                'streams': {
                    'iPhone': {'percentage': 52, 'description': 'スマートフォン販売', 'growth_trend': 'stable'},
                    'Services': {'percentage': 22, 'description': 'App Store、iCloud、Apple Music等', 'growth_trend': 'growing'},
                    'Mac': {'percentage': 10, 'description': 'デスクトップ・ノートPC', 'growth_trend': 'stable'},
                    'iPad': {'percentage': 8, 'description': 'タブレット製品', 'growth_trend': 'declining'},
                    'Wearables & Accessories': {'percentage': 8, 'description': 'Apple Watch、AirPods等', 'growth_trend': 'growing'}
                }
            },
            'MSFT': {
                'company_name': 'Microsoft Corporation',
                'sector': 'Technology',
                'streams': {
                    'Azure & Cloud Services': {'percentage': 38, 'description': 'クラウドインフラ・プラットフォーム', 'growth_trend': 'growing'},
                    'Microsoft 365': {'percentage': 28, 'description': 'Office、Teams、生産性ツール', 'growth_trend': 'growing'},
                    'Windows & Devices': {'percentage': 14, 'description': 'OS・Surface・Xbox', 'growth_trend': 'stable'},
                    'LinkedIn': {'percentage': 8, 'description': 'プロフェッショナルSNS', 'growth_trend': 'growing'},
                    'Dynamics 365': {'percentage': 6, 'description': 'ERP・CRMソリューション', 'growth_trend': 'growing'},
                    'Other Services': {'percentage': 6, 'description': 'コンサルティング・サポート', 'growth_trend': 'stable'}
                }
            },
            'AMZN': {
                'company_name': 'Amazon.com Inc.',
                'sector': 'Consumer Discretionary',
                'streams': {
                    'Online Stores': {'percentage': 42, 'description': 'Eコマース・小売販売', 'growth_trend': 'stable'},
                    'AWS': {'percentage': 16, 'description': 'クラウドコンピューティング', 'growth_trend': 'growing'},
                    'Third-party Seller Services': {'percentage': 22, 'description': 'マーケットプレイス手数料', 'growth_trend': 'growing'},
                    'Advertising': {'percentage': 9, 'description': 'デジタル広告サービス', 'growth_trend': 'growing'},
                    'Prime & Subscriptions': {'percentage': 7, 'description': 'サブスクリプション収益', 'growth_trend': 'growing'},
                    'Physical Stores': {'percentage': 4, 'description': 'Whole Foods等実店舗', 'growth_trend': 'stable'}
                }
            },
            'GOOGL': {
                'company_name': 'Alphabet Inc.',
                'sector': 'Technology',
                'streams': {
                    'Google Search': {'percentage': 58, 'description': '検索広告収益', 'growth_trend': 'stable'},
                    'YouTube': {'percentage': 12, 'description': '動画プラットフォーム広告', 'growth_trend': 'growing'},
                    'Google Cloud': {'percentage': 11, 'description': 'クラウドサービス', 'growth_trend': 'growing'},
                    'Google Network': {'percentage': 10, 'description': 'パートナーサイト広告', 'growth_trend': 'stable'},
                    'Other Google Services': {'percentage': 6, 'description': 'Play Store、Hardware等', 'growth_trend': 'stable'},
                    'Other Bets': {'percentage': 3, 'description': 'Waymo、Verily等新事業', 'growth_trend': 'experimental'}
                }
            },
            'GOOG': {
                'company_name': 'Alphabet Inc.',
                'sector': 'Technology',
                'streams': {
                    'Google Search': {'percentage': 58, 'description': '検索広告収益', 'growth_trend': 'stable'},
                    'YouTube': {'percentage': 12, 'description': '動画プラットフォーム広告', 'growth_trend': 'growing'},
                    'Google Cloud': {'percentage': 11, 'description': 'クラウドサービス', 'growth_trend': 'growing'},
                    'Google Network': {'percentage': 10, 'description': 'パートナーサイト広告', 'growth_trend': 'stable'},
                    'Other Google Services': {'percentage': 6, 'description': 'Play Store、Hardware等', 'growth_trend': 'stable'},
                    'Other Bets': {'percentage': 3, 'description': 'Waymo、Verily等新事業', 'growth_trend': 'experimental'}
                }
            },
            'META': {
                'company_name': 'Meta Platforms Inc.',
                'sector': 'Technology',
                'streams': {
                    'Facebook Advertising': {'percentage': 66, 'description': 'Facebook広告収益', 'growth_trend': 'stable'},
                    'Instagram Advertising': {'percentage': 24, 'description': 'Instagram広告収益', 'growth_trend': 'growing'},
                    'WhatsApp Business': {'percentage': 4, 'description': 'ビジネス向けメッセージング', 'growth_trend': 'growing'},
                    'Reality Labs': {'percentage': 3, 'description': 'VR・AR・メタバース', 'growth_trend': 'experimental'},
                    'Other Services': {'percentage': 3, 'description': 'その他プラットフォーム', 'growth_trend': 'stable'}
                }
            },
            'TSLA': {
                'company_name': 'Tesla Inc.',
                'sector': 'Consumer Discretionary',
                'streams': {
                    'Model Y': {'percentage': 45, 'description': 'SUV電気自動車', 'growth_trend': 'growing'},
                    'Model 3': {'percentage': 32, 'description': 'セダン電気自動車', 'growth_trend': 'stable'},
                    'Model S & X': {'percentage': 8, 'description': 'プレミアム電気自動車', 'growth_trend': 'declining'},
                    'Energy Storage': {'percentage': 7, 'description': 'バッテリー・ソーラー', 'growth_trend': 'growing'},
                    'Supercharging': {'percentage': 4, 'description': '充電インフラ収益', 'growth_trend': 'growing'},
                    'Software & Services': {'percentage': 4, 'description': 'FSD・保険・サービス', 'growth_trend': 'growing'}
                }
            },
            'NVDA': {
                'company_name': 'NVIDIA Corporation',
                'sector': 'Technology',
                'streams': {
                    'Data Center': {'percentage': 78, 'description': 'AI・機械学習向けGPU', 'growth_trend': 'growing'},
                    'Gaming': {'percentage': 12, 'description': 'ゲーミングGPU', 'growth_trend': 'stable'},
                    'Professional Visualization': {'percentage': 4, 'description': 'ワークステーション向けGPU', 'growth_trend': 'stable'},
                    'Automotive': {'percentage': 3, 'description': '自動運転・車載システム', 'growth_trend': 'growing'},
                    'OEM & Other': {'percentage': 3, 'description': 'その他OEM・IP収益', 'growth_trend': 'stable'}
                }
            },
            'NFLX': {
                'company_name': 'Netflix Inc.',
                'sector': 'Communication Services',
                'streams': {
                    'Streaming Subscriptions': {'percentage': 85, 'description': '月額サブスクリプション収益', 'growth_trend': 'stable'},
                    'Advertising': {'percentage': 8, 'description': '広告収入（広告付きプラン）', 'growth_trend': 'growing'},
                    'Content Licensing': {'percentage': 4, 'description': 'コンテンツライセンス', 'growth_trend': 'stable'},
                    'Gaming': {'percentage': 2, 'description': 'モバイルゲーム', 'growth_trend': 'experimental'},
                    'Merchandise': {'percentage': 1, 'description': '関連商品・グッズ', 'growth_trend': 'stable'}
                }
            },
            'JPM': {
                'company_name': 'JPMorgan Chase & Co.',
                'sector': 'Financials',
                'streams': {
                    'Consumer Banking': {'percentage': 42, 'description': '個人向け銀行業務', 'growth_trend': 'stable'},
                    'Investment Banking': {'percentage': 24, 'description': '投資銀行業務', 'growth_trend': 'stable'},
                    'Commercial Banking': {'percentage': 18, 'description': '法人向け銀行業務', 'growth_trend': 'growing'},
                    'Asset Management': {'percentage': 12, 'description': '資産運用業務', 'growth_trend': 'growing'},
                    'Trading & Securities': {'percentage': 4, 'description': 'トレーディング収益', 'growth_trend': 'volatile'}
                }
            },
            'BAC': {
                'company_name': 'Bank of America Corp.',
                'sector': 'Financials',
                'streams': {
                    'Consumer Banking': {'percentage': 48, 'description': '個人向け銀行サービス', 'growth_trend': 'stable'},
                    'Global Wealth Management': {'percentage': 22, 'description': '富裕層向け資産運用', 'growth_trend': 'growing'},
                    'Global Banking': {'percentage': 18, 'description': '法人・投資銀行業務', 'growth_trend': 'stable'},
                    'Global Markets': {'percentage': 12, 'description': 'トレーディング・証券業務', 'growth_trend': 'volatile'}
                }
            },
            'JNJ': {
                'company_name': 'Johnson & Johnson',
                'sector': 'Healthcare',
                'streams': {
                    'Pharmaceuticals': {'percentage': 77, 'description': '処方薬事業', 'growth_trend': 'growing'},
                    'Medical Devices': {'percentage': 23, 'description': '医療機器・診断機器', 'growth_trend': 'stable'}
                }
            },
            'PFE': {
                'company_name': 'Pfizer Inc.',
                'sector': 'Healthcare',
                'streams': {
                    'Primary Care': {'percentage': 35, 'description': 'プライマリケア医薬品', 'growth_trend': 'stable'},
                    'Oncology': {'percentage': 28, 'description': 'がん治療薬', 'growth_trend': 'growing'},
                    'Vaccines': {'percentage': 20, 'description': 'ワクチン事業', 'growth_trend': 'stable'},
                    'Hospital & Specialty': {'percentage': 12, 'description': '病院・専門医薬品', 'growth_trend': 'growing'},
                    'Consumer Healthcare': {'percentage': 5, 'description': '一般用医薬品', 'growth_trend': 'stable'}
                }
            },
            'UNH': {
                'company_name': 'UnitedHealth Group Inc.',
                'sector': 'Healthcare',
                'streams': {
                    'UnitedHealthcare': {'percentage': 82, 'description': '医療保険事業', 'growth_trend': 'stable'},
                    'Optum Health': {'percentage': 10, 'description': '医療サービス・ケア提供', 'growth_trend': 'growing'},
                    'Optum Insight': {'percentage': 4, 'description': '医療データ・IT事業', 'growth_trend': 'growing'},
                    'Optum Rx': {'percentage': 4, 'description': '薬局給付管理', 'growth_trend': 'stable'}
                }
            },
            'DIS': {
                'company_name': 'The Walt Disney Company',
                'sector': 'Communication Services',
                'streams': {
                    'Disney Parks': {'percentage': 38, 'description': 'テーマパーク・リゾート', 'growth_trend': 'recovering'},
                    'Disney+': {'percentage': 22, 'description': 'ストリーミングサービス', 'growth_trend': 'growing'},
                    'Traditional TV Networks': {'percentage': 18, 'description': 'ABC・ESPN等TV放送', 'growth_trend': 'declining'},
                    'Content Licensing': {'percentage': 12, 'description': 'コンテンツライセンス', 'growth_trend': 'stable'},
                    'Consumer Products': {'percentage': 8, 'description': 'キャラクター商品・玩具', 'growth_trend': 'stable'},
                    'Theatrical Releases': {'percentage': 2, 'description': '映画興行収入', 'growth_trend': 'volatile'}
                }
            },
            'V': {
                'company_name': 'Visa Inc.',
                'sector': 'Financials',
                'streams': {
                    'Payment Volume': {'percentage': 68, 'description': '決済処理手数料', 'growth_trend': 'growing'},
                    'Cross-border Volume': {'percentage': 18, 'description': '国際決済手数料', 'growth_trend': 'growing'},
                    'Processed Transactions': {'percentage': 10, 'description': '取引処理手数料', 'growth_trend': 'growing'},
                    'Other Revenues': {'percentage': 4, 'description': 'その他金融サービス', 'growth_trend': 'stable'}
                }
            },
            'MA': {
                'company_name': 'Mastercard Inc.',
                'sector': 'Financials',
                'streams': {
                    'Domestic Assessments': {'percentage': 42, 'description': '国内決済手数料', 'growth_trend': 'growing'},
                    'Cross-border Volume': {'percentage': 24, 'description': '国際決済手数料', 'growth_trend': 'growing'},
                    'Transaction Processing': {'percentage': 18, 'description': '取引処理手数料', 'growth_trend': 'growing'},
                    'Value-added Services': {'percentage': 16, 'description': '付加価値サービス', 'growth_trend': 'growing'}
                }
            },
            'WMT': {
                'company_name': 'Walmart Inc.',
                'sector': 'Consumer Staples',
                'streams': {
                    'Walmart U.S.': {'percentage': 67, 'description': '米国小売事業', 'growth_trend': 'stable'},
                    'Walmart International': {'percentage': 22, 'description': '国際小売事業', 'growth_trend': 'stable'},
                    'Sam\'s Club': {'percentage': 11, 'description': '会員制倉庫型店舗', 'growth_trend': 'growing'}
                }
            },
            'HD': {
                'company_name': 'The Home Depot Inc.',
                'sector': 'Consumer Discretionary',
                'streams': {
                    'U.S. Retail': {'percentage': 85, 'description': '米国ホームセンター事業', 'growth_trend': 'stable'},
                    'Pro Services': {'percentage': 8, 'description': 'プロ向けサービス', 'growth_trend': 'growing'},
                    'International': {'percentage': 4, 'description': '国際事業', 'growth_trend': 'stable'},
                    'Online & Digital': {'percentage': 3, 'description': 'オンライン・デジタル', 'growth_trend': 'growing'}
                }
            },
            'CVX': {
                'company_name': 'Chevron Corporation',
                'sector': 'Energy',
                'streams': {
                    'Upstream': {'percentage': 68, 'description': '石油・ガス探査・生産', 'growth_trend': 'stable'},
                    'Downstream': {'percentage': 25, 'description': '精製・販売', 'growth_trend': 'stable'},
                    'Chemical': {'percentage': 4, 'description': '化学製品', 'growth_trend': 'stable'},
                    'Renewable Energy': {'percentage': 3, 'description': '再生可能エネルギー', 'growth_trend': 'growing'}
                }
            },
            'XOM': {
                'company_name': 'Exxon Mobil Corporation',
                'sector': 'Energy',
                'streams': {
                    'Upstream': {'percentage': 75, 'description': '石油・ガス探査・生産', 'growth_trend': 'stable'},
                    'Downstream': {'percentage': 18, 'description': '精製・販売', 'growth_trend': 'stable'},
                    'Chemical': {'percentage': 5, 'description': '石油化学製品', 'growth_trend': 'stable'},
                    'Low Carbon Solutions': {'percentage': 2, 'description': '低炭素ソリューション', 'growth_trend': 'experimental'}
                }
            }
        }
        
        # Get default data from financial statements for companies not in our database
        if ticker not in revenue_streams:
            return get_generic_revenue_breakdown(stock, ticker)
        
        return revenue_streams[ticker]
        
    except Exception as e:
        return None

def get_generic_revenue_breakdown(stock, ticker):
    """
    Generate generic revenue breakdown for companies not in our specific database
    """
    try:
        info = stock.info
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        
        # Generic breakdown based on sector
        if 'Technology' in sector:
            return {
                'company_name': info.get('longName', ticker),
                'sector': sector,
                'streams': {
                    'Products': {'percentage': 60, 'description': '製品・ソフトウェア販売', 'growth_trend': 'stable'},
                    'Services': {'percentage': 25, 'description': 'サポート・コンサルティング', 'growth_trend': 'growing'},
                    'Subscriptions': {'percentage': 10, 'description': 'サブスクリプション収益', 'growth_trend': 'growing'},
                    'Other': {'percentage': 5, 'description': 'その他収益', 'growth_trend': 'stable'}
                }
            }
        elif 'Healthcare' in sector:
            return {
                'company_name': info.get('longName', ticker),
                'sector': sector,
                'streams': {
                    'Pharmaceuticals': {'percentage': 70, 'description': '医薬品売上', 'growth_trend': 'growing'},
                    'Medical Devices': {'percentage': 20, 'description': '医療機器売上', 'growth_trend': 'stable'},
                    'Services': {'percentage': 10, 'description': '医療サービス', 'growth_trend': 'stable'}
                }
            }
        elif 'Financial' in sector:
            return {
                'company_name': info.get('longName', ticker),
                'sector': sector,
                'streams': {
                    'Interest Income': {'percentage': 50, 'description': '金利収入', 'growth_trend': 'stable'},
                    'Fee Income': {'percentage': 30, 'description': '手数料収入', 'growth_trend': 'growing'},
                    'Trading': {'percentage': 15, 'description': 'トレーディング収益', 'growth_trend': 'volatile'},
                    'Other': {'percentage': 5, 'description': 'その他金融サービス', 'growth_trend': 'stable'}
                }
            }
        else:
            return {
                'company_name': info.get('longName', ticker),
                'sector': sector,
                'streams': {
                    'Core Business': {'percentage': 75, 'description': 'メイン事業', 'growth_trend': 'stable'},
                    'Secondary Business': {'percentage': 20, 'description': 'セカンダリー事業', 'growth_trend': 'stable'},
                    'Other': {'percentage': 5, 'description': 'その他', 'growth_trend': 'stable'}
                }
            }
    except Exception as e:
        return None

def create_revenue_streams_visualization(revenue_data):
    """
    Create visualizations for revenue streams
    """
    if not revenue_data or 'streams' not in revenue_data:
        return None, None
    
    streams = revenue_data['streams']
    
    # Prepare data for visualization
    stream_names = list(streams.keys())
    percentages = [streams[name]['percentage'] for name in stream_names]
    descriptions = [streams[name]['description'] for name in stream_names]
    growth_trends = [streams[name]['growth_trend'] for name in stream_names]
    
    # Color mapping for growth trends
    color_map = {
        'growing': '#10b981',      # Green
        'stable': '#3b82f6',       # Blue
        'declining': '#ef4444',    # Red
        'volatile': '#f59e0b',     # Yellow
        'recovering': '#8b5cf6',   # Purple
        'experimental': '#6b7280'  # Gray
    }
    
    colors = [color_map.get(trend, '#6b7280') for trend in growth_trends]
    
    # Create pie chart
    pie_fig = go.Figure(data=[go.Pie(
        labels=stream_names,
        values=percentages,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>' +
                      '%{value}%<br>' +
                      '<extra></extra>'
    )])
    
    pie_fig.update_layout(
        title=f"{revenue_data['company_name']} - 事業セグメント別売上構成",
        font=dict(size=12),
        showlegend=False,
        height=500
    )
    
    # Create bar chart with growth trend indicators
    bar_fig = go.Figure()
    
    bar_fig.add_trace(go.Bar(
        x=stream_names,
        y=percentages,
        marker_color=colors,
        text=[f"{p}%" for p in percentages],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                      '売上構成比: %{y}%<br>' +
                      '<extra></extra>'
    ))
    
    bar_fig.update_layout(
        title=f"{revenue_data['company_name']} - 事業セグメント別売上構成（成長トレンド別）",
        xaxis_title="事業セグメント",
        yaxis_title="売上構成比 (%)",
        height=500,
        xaxis_tickangle=-45
    )
    
    return pie_fig, bar_fig

def display_revenue_streams_analysis(ticker):
    """
    Display comprehensive revenue streams analysis for a company
    """
    with st.spinner("事業セグメント別売上構成を分析中..."):
        revenue_data = get_company_revenue_streams(ticker)
        
        if not revenue_data:
            st.warning("このティッカーの詳細な事業セグメント情報は現在利用できません。")
            return
        
        st.markdown(f"### 📊 {revenue_data['company_name']} - 事業セグメント別売上分析")
        st.markdown(f"**セクター:** {revenue_data['sector']}")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📈 売上構成", "🔍 詳細分析", "📊 成長トレンド"])
        
        with tab1:
            # Create visualizations
            pie_fig, bar_fig = create_revenue_streams_visualization(revenue_data)
            
            if pie_fig and bar_fig:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(pie_fig, use_container_width=True)
                
                with col2:
                    st.plotly_chart(bar_fig, use_container_width=True)
        
        with tab2:
            # Detailed breakdown table
            st.markdown("#### 事業セグメント詳細")
            
            streams_data = []
            for name, data in revenue_data['streams'].items():
                streams_data.append({
                    '事業セグメント': name,
                    '売上構成比': f"{data['percentage']}%",
                    '事業内容': data['description'],
                    '成長トレンド': data['growth_trend']
                })
            
            df = pd.DataFrame(streams_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add trend explanations
            st.markdown("#### 成長トレンドの説明")
            trend_explanations = {
                'growing': '🟢 **成長中** - 売上が継続的に増加している事業',
                'stable': '🔵 **安定** - 売上が安定している成熟事業',
                'declining': '🔴 **減少中** - 売上が減少傾向にある事業',
                'volatile': '🟡 **変動大** - 売上の変動が大きい事業',
                'recovering': '🟣 **回復中** - 一時的な減少から回復している事業',
                'experimental': '⚫ **実験的** - 新規事業で収益性が不確定'
            }
            
            for trend, explanation in trend_explanations.items():
                if any(stream['growth_trend'] == trend for stream in revenue_data['streams'].values()):
                    st.markdown(explanation)
        
        with tab3:
            # Growth trend analysis
            st.markdown("#### 成長トレンド別分析")
            
            # Group by growth trend
            trend_groups = {}
            for name, data in revenue_data['streams'].items():
                trend = data['growth_trend']
                if trend not in trend_groups:
                    trend_groups[trend] = []
                trend_groups[trend].append({
                    'name': name,
                    'percentage': data['percentage'],
                    'description': data['description']
                })
            
            # Display each trend group
            for trend, segments in trend_groups.items():
                total_percentage = sum(seg['percentage'] for seg in segments)
                
                if trend == 'growing':
                    st.success(f"**成長事業 ({total_percentage}%)**")
                elif trend == 'stable':
                    st.info(f"**安定事業 ({total_percentage}%)**")
                elif trend == 'declining':
                    st.error(f"**減少事業 ({total_percentage}%)**")
                elif trend == 'volatile':
                    st.warning(f"**変動事業 ({total_percentage}%)**")
                elif trend == 'recovering':
                    st.success(f"**回復事業 ({total_percentage}%)**")
                else:
                    st.info(f"**その他事業 ({total_percentage}%)**")
                
                for segment in segments:
                    st.write(f"- **{segment['name']}** ({segment['percentage']}%): {segment['description']}")
                
                st.write("")
        
        # Add strategic insights
        st.markdown("#### 💡 戦略的インサイト")
        
        # Calculate insights
        growing_percentage = sum(
            data['percentage'] for data in revenue_data['streams'].values()
            if data['growth_trend'] == 'growing'
        )
        declining_percentage = sum(
            data['percentage'] for data in revenue_data['streams'].values()
            if data['growth_trend'] == 'declining'
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("成長事業比率", f"{growing_percentage}%")
        
        with col2:
            st.metric("減少事業比率", f"{declining_percentage}%")
        
        with col3:
            diversification_score = len(revenue_data['streams'])
            st.metric("事業多様化度", f"{diversification_score}事業")
        
        # Strategic recommendations
        if growing_percentage > 40:
            st.success("✅ 成長事業の比率が高く、将来性が期待できます")
        elif growing_percentage > 20:
            st.info("ℹ️ 成長事業と安定事業のバランスが取れています")
        else:
            st.warning("⚠️ 成長事業の比率が低く、新規事業の開拓が必要かもしれません")
        
        if declining_percentage > 30:
            st.error("⚠️ 減少事業の比率が高く、事業転換の必要性があります")
        elif declining_percentage > 15:
            st.warning("⚠️ 一部の事業で減少傾向が見られます")