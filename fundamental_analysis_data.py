import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def get_comprehensive_fundamental_data(ticker):
    """
    Get comprehensive fundamental analysis data for a company
    """
    try:
        # Define comprehensive fundamental data for major companies
        fundamental_data = {
            'AAPL': {
                'company_name': 'Apple Inc.',
                'sector': 'Technology',
                'industry': 'Consumer Electronics',
                'business_model': {
                    'description': 'ハードウェア、ソフトウェア、サービスの垂直統合エコシステム',
                    'revenue_streams': ['iPhone販売', 'Services収益', 'Mac・iPad・Wearables'],
                    'key_products': ['iPhone', 'Mac', 'iPad', 'Apple Watch', 'AirPods', 'Services']
                },
                'competitive_advantages': [
                    '強力なブランドロイヤリティ',
                    'エコシステムによる囲い込み効果',
                    '高い利益率を維持する価格決定力',
                    '継続的イノベーション能力',
                    '豊富なキャッシュフロー'
                ],
                'swot': {
                    'strengths': [
                        '世界最強レベルのブランド力',
                        '垂直統合されたエコシステム',
                        '継続的な技術革新',
                        '高い顧客満足度とロイヤリティ',
                        '強固な財務基盤'
                    ],
                    'weaknesses': [
                        'iPhoneへの収益依存度が高い',
                        '高価格による市場セグメント限定',
                        '部品サプライヤーへの依存',
                        '中国市場での競争激化'
                    ],
                    'opportunities': [
                        'インド等新興市場での成長',
                        'AI・AR/VR技術の活用',
                        '自動車市場への参入',
                        'ヘルスケア分野の拡大',
                        'サービス事業の更なる成長'
                    ],
                    'threats': [
                        '中国での地政学リスク',
                        'EU等での規制強化',
                        'スマートフォン市場の成熟化',
                        '為替変動リスク',
                        '競合他社の技術追い上げ'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 1.73,
                    'current_ratio': 1.01,
                    'gross_margin': 45.96,
                    'operating_margin': 29.78,
                    'net_margin': 25.31,
                    'roe': 160.58,
                    'roa': 22.09,
                    'asset_turnover': 0.87
                },
                'growth_metrics': {
                    'revenue_growth_5y': 7.8,
                    'earnings_growth_5y': 9.1,
                    'dividend_growth_5y': 7.3,
                    'book_value_growth_5y': -8.2
                },
                'investment_thesis': {
                    'bull_case': [
                        'サービス事業の継続的成長',
                        'AI統合による製品差別化',
                        '新興市場での普及拡大',
                        '自社株買いによる株主還元'
                    ],
                    'bear_case': [
                        'iPhone売上の減速',
                        '中国市場でのシェア低下',
                        '規制当局からの圧力増加',
                        '高いバリュエーション'
                    ]
                }
            },
            'MSFT': {
                'company_name': 'Microsoft Corporation',
                'sector': 'Technology',
                'industry': 'Software',
                'business_model': {
                    'description': 'クラウドファースト、AI統合のソフトウェア・サービス企業',
                    'revenue_streams': ['Azure・クラウドサービス', 'Microsoft 365', 'Windows・デバイス', 'LinkedIn'],
                    'key_products': ['Azure', 'Microsoft 365', 'Windows', 'LinkedIn', 'Xbox', 'Dynamics 365']
                },
                'competitive_advantages': [
                    'クラウド市場でのAWSに次ぐ地位',
                    '企業向けソフトウェアでの圧倒的シェア',
                    'AI技術（OpenAI連携）の先行優位',
                    '継続収益モデルの確立',
                    '多様な事業ポートフォリオ'
                ],
                'swot': {
                    'strengths': [
                        'クラウド事業の急成長',
                        '企業向けソフトウェアの独占的地位',
                        'AI・機械学習への先行投資',
                        '安定したキャッシュフロー',
                        '強力なパートナーエコシステム'
                    ],
                    'weaknesses': [
                        'コンシューマー市場でのプレゼンス不足',
                        'レガシーシステムへの依存',
                        'ハードウェア事業の伸び悩み'
                    ],
                    'opportunities': [
                        '生成AI市場でのリーダーシップ',
                        'ハイブリッドワーク需要の拡大',
                        'デジタル変革の加速',
                        '新興市場でのクラウド普及',
                        'LinkedIn活用の拡大'
                    ],
                    'threats': [
                        'AWSとの競争激化',
                        'Google・Amazonとの技術競争',
                        'サイバーセキュリティリスク',
                        '反トラスト規制の強化'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.47,
                    'current_ratio': 1.27,
                    'gross_margin': 69.05,
                    'operating_margin': 42.05,
                    'net_margin': 34.05,
                    'roe': 34.16,
                    'roa': 13.05,
                    'asset_turnover': 0.38
                },
                'growth_metrics': {
                    'revenue_growth_5y': 12.8,
                    'earnings_growth_5y': 15.2,
                    'dividend_growth_5y': 9.8,
                    'book_value_growth_5y': 12.1
                },
                'investment_thesis': {
                    'bull_case': [
                        'AI革命での先行者利益',
                        'クラウド移行の継続',
                        '企業デジタル化の恩恵',
                        '高収益性ビジネスモデル'
                    ],
                    'bear_case': [
                        'クラウド競争の激化',
                        'AI投資の収益化遅延',
                        '成長率の鈍化',
                        '高いバリュエーション'
                    ]
                }
            },
            'AMZN': {
                'company_name': 'Amazon.com Inc.',
                'sector': 'Consumer Discretionary',
                'industry': 'E-commerce',
                'business_model': {
                    'description': 'Eコマース、クラウド、デジタル広告の複合事業モデル',
                    'revenue_streams': ['オンラインストア', 'AWS', 'サードパーティ販売', '広告', 'サブスクリプション'],
                    'key_products': ['Amazon.com', 'AWS', 'Prime', 'Alexa', 'Advertising', 'Logistics']
                },
                'competitive_advantages': [
                    'Eコマースでの圧倒的規模',
                    'AWSでのクラウド市場リーダーシップ',
                    'Prime会員による顧客ロックイン',
                    '物流・配送ネットワークの優位性',
                    'データドリブンな経営'
                ],
                'swot': {
                    'strengths': [
                        'Eコマース市場での独占的地位',
                        'AWSの高収益性',
                        '顧客中心の文化',
                        '継続的なイノベーション',
                        '強力な物流ネットワーク'
                    ],
                    'weaknesses': [
                        '小売部門の低利益率',
                        '労働問題と組合化圧力',
                        '規制当局からの監視',
                        '巨大な設備投資負担'
                    ],
                    'opportunities': [
                        '国際市場での拡大',
                        'ヘルスケア・薬局事業',
                        'AI・機械学習の活用',
                        '広告事業の成長',
                        '自動配送技術'
                    ],
                    'threats': [
                        '反トラスト法による分割リスク',
                        'AlibabaやShopifyとの競争',
                        '人件費とインフレ圧力',
                        'サイバーセキュリティリスク'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.96,
                    'current_ratio': 1.09,
                    'gross_margin': 47.12,
                    'operating_margin': 5.71,
                    'net_margin': 4.32,
                    'roe': 21.82,
                    'roa': 5.89,
                    'asset_turnover': 1.36
                },
                'growth_metrics': {
                    'revenue_growth_5y': 22.1,
                    'earnings_growth_5y': 45.8,
                    'dividend_growth_5y': 0.0,
                    'book_value_growth_5y': 18.9
                },
                'investment_thesis': {
                    'bull_case': [
                        'Eコマースの継続成長',
                        'AWSの利益拡大',
                        '広告事業の急成長',
                        '物流効率化による利益改善'
                    ],
                    'bear_case': [
                        '小売部門の利益率低迷',
                        '競合の追い上げ',
                        '規制分割リスク',
                        '設備投資負担の重さ'
                    ]
                }
            },
            'GOOGL': {
                'company_name': 'Alphabet Inc.',
                'sector': 'Technology',
                'industry': 'Internet Services',
                'business_model': {
                    'description': '検索・広告を核とするデジタルプラットフォーム企業',
                    'revenue_streams': ['Google検索', 'YouTube', 'Google Cloud', 'Play Store', 'その他'],
                    'key_products': ['Google Search', 'YouTube', 'Android', 'Chrome', 'Google Cloud', 'Waymo']
                },
                'competitive_advantages': [
                    '検索エンジンでの圧倒的シェア',
                    'YouTubeでの動画配信独占',
                    'Androidエコシステム',
                    '膨大なデータ蓄積',
                    'AI・機械学習技術の先進性'
                ],
                'swot': {
                    'strengths': [
                        '検索市場での独占的地位',
                        'YouTube等の強力プラットフォーム',
                        '先進的AI技術',
                        '豊富なキャッシュフロー',
                        'グローバルな事業展開'
                    ],
                    'weaknesses': [
                        '広告収入への過度な依存',
                        'プライバシー規制への脆弱性',
                        'Other Betsの収益化遅延',
                        'エンタープライズ市場での後発'
                    ],
                    'opportunities': [
                        'クラウド事業の拡大',
                        'AI技術の商業化',
                        '自動運転技術（Waymo）',
                        '新興市場での成長',
                        'ヘルスケア分野への進出'
                    ],
                    'threats': [
                        '反トラスト規制の強化',
                        'TikTok等との競合',
                        'プライバシー規制の厳格化',
                        'AppleのATT等による影響'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.07,
                    'current_ratio': 2.87,
                    'gross_margin': 57.25,
                    'operating_margin': 25.31,
                    'net_margin': 21.05,
                    'roe': 28.28,
                    'roa': 18.67,
                    'asset_turnover': 0.59
                },
                'growth_metrics': {
                    'revenue_growth_5y': 17.8,
                    'earnings_growth_5y': 19.2,
                    'dividend_growth_5y': 0.0,
                    'book_value_growth_5y': 15.1
                },
                'investment_thesis': {
                    'bull_case': [
                        'AI技術での競争優位',
                        'クラウド事業の急成長',
                        'YouTube Shortsの成功',
                        '自動運転の商業化'
                    ],
                    'bear_case': [
                        '規制による事業分割リスク',
                        '広告市場の競争激化',
                        'AI競争での後れ',
                        'TikTokによるユーザー流出'
                    ]
                }
            },
            'META': {
                'company_name': 'Meta Platforms Inc.',
                'sector': 'Technology',
                'industry': 'Social Media',
                'business_model': {
                    'description': 'ソーシャルメディアプラットフォームとメタバース技術企業',
                    'revenue_streams': ['Facebook広告', 'Instagram広告', 'WhatsApp Business', 'Reality Labs'],
                    'key_products': ['Facebook', 'Instagram', 'WhatsApp', 'Meta Quest', 'Threads']
                },
                'competitive_advantages': [
                    '世界最大のソーシャルネットワーク',
                    '精密な広告ターゲティング',
                    '強力なネットワーク効果',
                    'VR/AR技術での先行投資',
                    '膨大なユーザーデータ'
                ],
                'swot': {
                    'strengths': [
                        '30億人を超えるユーザーベース',
                        '高精度な広告プラットフォーム',
                        '複数の成功プラットフォーム保有',
                        'VR/AR技術への先行投資',
                        '強力なネットワーク効果'
                    ],
                    'weaknesses': [
                        '広告収入への依存',
                        'プライバシー問題',
                        'Reality Labsの巨額損失',
                        '若年層ユーザーの減少'
                    ],
                    'opportunities': [
                        'メタバース市場の創造',
                        'Reels・TikTok競合での成長',
                        'WhatsApp収益化',
                        '新興市場でのユーザー拡大',
                        'AI技術の活用'
                    ],
                    'threats': [
                        'TikTokとの競合激化',
                        'Apple ATTによる広告効果低下',
                        '各国でのプライバシー規制',
                        '政治的・社会的批判',
                        'メタバース投資の不確実性'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.08,
                    'current_ratio': 2.78,
                    'gross_margin': 81.49,
                    'operating_margin': 29.05,
                    'net_margin': 23.21,
                    'roe': 22.11,
                    'roa': 16.24,
                    'asset_turnover': 0.53
                },
                'growth_metrics': {
                    'revenue_growth_5y': 18.8,
                    'earnings_growth_5y': 12.1,
                    'dividend_growth_5y': 0.0,
                    'book_value_growth_5y': 8.9
                },
                'investment_thesis': {
                    'bull_case': [
                        'Reelsの成功とユーザー回復',
                        'メタバース市場の先行者利益',
                        '効率化による利益率改善',
                        'AI活用による広告効果向上'
                    ],
                    'bear_case': [
                        'TikTokに対する競争劣位',
                        'Reality Labsの継続損失',
                        '規制強化によるビジネス制約',
                        '広告市場の成長鈍化'
                    ]
                }
            },
            'TSLA': {
                'company_name': 'Tesla Inc.',
                'sector': 'Consumer Discretionary',
                'industry': 'Electric Vehicles',
                'business_model': {
                    'description': '電気自動車とエネルギー貯蔵システムの統合企業',
                    'revenue_streams': ['電気自動車販売', 'エネルギー貯蔵', '充電インフラ', 'ソフトウェア'],
                    'key_products': ['Model Y', 'Model 3', 'Model S/X', 'Supercharger', 'Energy Storage']
                },
                'competitive_advantages': [
                    'EV市場での先行者利益',
                    '垂直統合による効率性',
                    '充電インフラネットワーク',
                    '自動運転技術',
                    '強力なブランド力'
                ],
                'swot': {
                    'strengths': [
                        'EV市場のパイオニア',
                        '技術革新力',
                        '強力なCEOブランド',
                        '垂直統合モデル',
                        '充電インフラの優位性'
                    ],
                    'weaknesses': [
                        '品質管理問題',
                        'CEOリスク',
                        '限定的な製品ラインナップ',
                        '高い株価ボラティリティ'
                    ],
                    'opportunities': [
                        'グローバルEV市場拡大',
                        '自動運転技術の商業化',
                        'エネルギー事業の成長',
                        '新興市場への展開',
                        'ロボタクシー事業'
                    ],
                    'threats': [
                        '伝統的自動車メーカーのEV参入',
                        '中国EV企業との競争',
                        'バッテリー原材料価格上昇',
                        '政府補助金の減少',
                        '品質・安全性問題'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.08,
                    'current_ratio': 1.84,
                    'gross_margin': 20.63,
                    'operating_margin': 9.62,
                    'net_margin': 8.19,
                    'roe': 28.05,
                    'roa': 12.05,
                    'asset_turnover': 0.89
                },
                'growth_metrics': {
                    'revenue_growth_5y': 47.2,
                    'earnings_growth_5y': 89.1,
                    'dividend_growth_5y': 0.0,
                    'book_value_growth_5y': 35.8
                },
                'investment_thesis': {
                    'bull_case': [
                        'EV市場の爆発的成長',
                        'FSD技術の実用化',
                        'エネルギー事業の収益化',
                        '新工場による生産拡大'
                    ],
                    'bear_case': [
                        '競合の技術追い上げ',
                        '成長率の鈍化',
                        '極めて高いバリュエーション',
                        'CEO関連リスク'
                    ]
                }
            },
            'NVDA': {
                'company_name': 'NVIDIA Corporation',
                'sector': 'Technology',
                'industry': 'Semiconductors',
                'business_model': {
                    'description': 'AI・機械学習向けGPUとデータセンター技術のリーダー',
                    'revenue_streams': ['データセンター', 'ゲーミング', 'プロフェッショナル可視化', '自動車'],
                    'key_products': ['A100/H100 GPU', 'RTX Gaming', 'Omniverse', 'DRIVE']
                },
                'competitive_advantages': [
                    'AI・機械学習向けGPUでの独占的地位',
                    'CUDA エコシステム',
                    '継続的な技術革新',
                    '強力なソフトウェアスタック',
                    'パートナーシップネットワーク'
                ],
                'swot': {
                    'strengths': [
                        'AI/ML市場での圧倒的リーダーシップ',
                        '技術的優位性',
                        '高い利益率',
                        '強力なエコシステム',
                        '多様な成長市場'
                    ],
                    'weaknesses': [
                        'AI・データセンター需要への依存',
                        '地政学的リスク（中国）',
                        'サプライチェーンリスク',
                        '極めて高いバリュエーション'
                    ],
                    'opportunities': [
                        'AI市場の爆発的成長',
                        'メタバース・デジタルツイン',
                        '自動運転車市場',
                        'エッジAI・IoT',
                        '量子コンピューティング'
                    ],
                    'threats': [
                        'AMD・Intelとの競争',
                        '中国規制による売上減少',
                        'AI バブル崩壊リスク',
                        'カスタムチップの脅威'
                    ]
                },
                'financial_health': {
                    'debt_to_equity': 0.28,
                    'current_ratio': 3.42,
                    'gross_margin': 73.98,
                    'operating_margin': 32.97,
                    'net_margin': 28.09,
                    'roe': 65.52,
                    'roa': 35.78,
                    'asset_turnover': 0.89
                },
                'growth_metrics': {
                    'revenue_growth_5y': 24.8,
                    'earnings_growth_5y': 35.2,
                    'dividend_growth_5y': 8.9,
                    'book_value_growth_5y': 22.1
                },
                'investment_thesis': {
                    'bull_case': [
                        'AI革命の最大受益者',
                        'データセンター需要の継続拡大',
                        '技術的優位性の維持',
                        'メタバース・自動運転の成長'
                    ],
                    'bear_case': [
                        '極めて高いバリュエーション',
                        'AI需要の一時的過熱',
                        '競合の技術追い上げ',
                        '地政学的リスク'
                    ]
                }
            }
        }
        
        # Get live financial data if available
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Update some financial metrics with live data if available
            if ticker in fundamental_data:
                live_data = fundamental_data[ticker]
                if info.get('trailingPE'):
                    live_data['financial_health']['pe_ratio'] = info['trailingPE']
                if info.get('priceToBook'):
                    live_data['financial_health']['pb_ratio'] = info['priceToBook']
                if info.get('returnOnEquity'):
                    live_data['financial_health']['roe'] = info['returnOnEquity'] * 100
                
                return live_data
        except:
            pass
        
        # Return data if available, otherwise return None
        return fundamental_data.get(ticker, None)
        
    except Exception as e:
        return None

def create_fundamental_scorecard(data):
    """
    Create a comprehensive fundamental analysis scorecard
    """
    if not data:
        return None
    
    # Calculate overall scores
    financial_score = calculate_financial_health_score(data['financial_health'])
    growth_score = calculate_growth_score(data['growth_metrics'])
    competitive_score = len(data['competitive_advantages']) * 20  # Max 100
    
    # Overall fundamental score (weighted average)
    overall_score = (financial_score * 0.4 + growth_score * 0.3 + competitive_score * 0.3)
    
    return {
        'overall_score': min(100, overall_score),
        'financial_score': financial_score,
        'growth_score': growth_score,
        'competitive_score': min(100, competitive_score)
    }

def calculate_financial_health_score(financial_data):
    """
    Calculate financial health score based on key metrics
    """
    score = 0
    
    # Debt to Equity (lower is better)
    if financial_data['debt_to_equity'] < 0.3:
        score += 25
    elif financial_data['debt_to_equity'] < 0.6:
        score += 20
    elif financial_data['debt_to_equity'] < 1.0:
        score += 15
    else:
        score += 10
    
    # Current Ratio (1.2-2.0 is ideal)
    if 1.2 <= financial_data['current_ratio'] <= 2.0:
        score += 25
    elif 1.0 <= financial_data['current_ratio'] < 1.2:
        score += 20
    else:
        score += 10
    
    # Operating Margin (higher is better)
    if financial_data['operating_margin'] > 25:
        score += 25
    elif financial_data['operating_margin'] > 15:
        score += 20
    elif financial_data['operating_margin'] > 10:
        score += 15
    else:
        score += 10
    
    # ROE (higher is better)
    if financial_data['roe'] > 20:
        score += 25
    elif financial_data['roe'] > 15:
        score += 20
    elif financial_data['roe'] > 10:
        score += 15
    else:
        score += 10
    
    return score

def calculate_growth_score(growth_data):
    """
    Calculate growth score based on historical growth metrics
    """
    score = 0
    
    # Revenue Growth
    if growth_data['revenue_growth_5y'] > 20:
        score += 30
    elif growth_data['revenue_growth_5y'] > 10:
        score += 25
    elif growth_data['revenue_growth_5y'] > 5:
        score += 20
    else:
        score += 10
    
    # Earnings Growth
    if growth_data['earnings_growth_5y'] > 25:
        score += 30
    elif growth_data['earnings_growth_5y'] > 15:
        score += 25
    elif growth_data['earnings_growth_5y'] > 10:
        score += 20
    else:
        score += 10
    
    # Consistency bonus
    if abs(growth_data['revenue_growth_5y'] - growth_data['earnings_growth_5y']) < 5:
        score += 40  # Consistent growth
    elif abs(growth_data['revenue_growth_5y'] - growth_data['earnings_growth_5y']) < 10:
        score += 30
    else:
        score += 20
    
    return score

def display_fundamental_analysis(ticker):
    """
    Display comprehensive fundamental analysis for a company
    """
    with st.spinner("ファンダメンタル分析を実行中..."):
        fundamental_data = get_comprehensive_fundamental_data(ticker)
        
        if not fundamental_data:
            st.warning(f"ティッカー {ticker} の詳細なファンダメンタル分析データは現在利用できません。")
            return False
        
        # Company Overview
        st.markdown(f"## 🏢 {fundamental_data['company_name']}")
        st.markdown(f"**セクター:** {fundamental_data['sector']} | **業界:** {fundamental_data['industry']}")
        
        # Fundamental Scorecard
        scorecard = create_fundamental_scorecard(fundamental_data)
        if scorecard:
            st.markdown("### 📊 ファンダメンタル・スコアカード")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score_color = "🟢" if scorecard['overall_score'] >= 80 else "🟡" if scorecard['overall_score'] >= 60 else "🔴"
                st.metric("総合スコア", f"{scorecard['overall_score']:.0f}/100 {score_color}")
            
            with col2:
                st.metric("財務健全性", f"{scorecard['financial_score']:.0f}/100")
            
            with col3:
                st.metric("成長性", f"{scorecard['growth_score']:.0f}/100")
            
            with col4:
                st.metric("競争優位性", f"{scorecard['competitive_score']:.0f}/100")
        
        # Tabs for detailed analysis
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 財務分析", "💪 競争優位性", "🔍 SWOT分析", "📊 成長性", "💡 投資判断"])
        
        with tab1:
            st.markdown("#### 財務健全性指標")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Financial ratios
                financial_metrics = [
                    ("負債比率", f"{fundamental_data['financial_health']['debt_to_equity']:.2f}"),
                    ("流動比率", f"{fundamental_data['financial_health']['current_ratio']:.2f}"),
                    ("売上総利益率", f"{fundamental_data['financial_health']['gross_margin']:.1f}%"),
                    ("営業利益率", f"{fundamental_data['financial_health']['operating_margin']:.1f}%")
                ]
                
                for metric, value in financial_metrics:
                    st.write(f"**{metric}:** {value}")
            
            with col2:
                financial_metrics_2 = [
                    ("純利益率", f"{fundamental_data['financial_health']['net_margin']:.1f}%"),
                    ("ROE", f"{fundamental_data['financial_health']['roe']:.1f}%"),
                    ("ROA", f"{fundamental_data['financial_health']['roa']:.1f}%"),
                    ("総資産回転率", f"{fundamental_data['financial_health']['asset_turnover']:.2f}")
                ]
                
                for metric, value in financial_metrics_2:
                    st.write(f"**{metric}:** {value}")
        
        with tab2:
            st.markdown("#### 🏆 競争優位性 (モート)")
            
            for i, advantage in enumerate(fundamental_data['competitive_advantages'], 1):
                st.write(f"{i}. {advantage}")
            
            st.markdown("#### 🚀 ビジネスモデル")
            st.write(f"**概要:** {fundamental_data['business_model']['description']}")
            
            st.markdown("**主要収益源:**")
            for revenue_stream in fundamental_data['business_model']['revenue_streams']:
                st.write(f"• {revenue_stream}")
            
            st.markdown("**主要製品・サービス:**")
            for product in fundamental_data['business_model']['key_products']:
                st.write(f"• {product}")
        
        with tab3:
            st.markdown("#### 🔍 SWOT分析")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💪 Strengths (強み)**")
                for strength in fundamental_data['swot']['strengths']:
                    st.write(f"✅ {strength}")
                
                st.markdown("**🚀 Opportunities (機会)**")
                for opportunity in fundamental_data['swot']['opportunities']:
                    st.write(f"🔥 {opportunity}")
            
            with col2:
                st.markdown("**⚠️ Weaknesses (弱み)**")
                for weakness in fundamental_data['swot']['weaknesses']:
                    st.write(f"❌ {weakness}")
                
                st.markdown("**⚡ Threats (脅威)**")
                for threat in fundamental_data['swot']['threats']:
                    st.write(f"⚠️ {threat}")
        
        with tab4:
            st.markdown("#### 📈 成長性指標")
            
            st.info("💡 CAGR（年平均成長率）は過去5年間の複利成長率を示します。例えば7.8%のCAGRは、毎年平均7.8%ずつ成長していることを意味します。")
            
            growth_data = [
                ("売上高CAGR（5年）", f"{fundamental_data['growth_metrics']['revenue_growth_5y']:.1f}%"),
                ("利益CAGR（5年）", f"{fundamental_data['growth_metrics']['earnings_growth_5y']:.1f}%"),
                ("配当CAGR（5年）", f"{fundamental_data['growth_metrics']['dividend_growth_5y']:.1f}%" if fundamental_data['growth_metrics']['dividend_growth_5y'] > 0 else "配当なし"),
                ("簿価CAGR（5年）", f"{fundamental_data['growth_metrics']['book_value_growth_5y']:.1f}%")
            ]
            
            for metric, value in growth_data:
                st.write(f"**{metric}:** {value}")
        
        with tab5:
            st.markdown("#### 💡 投資判断")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🟢 強気シナリオ**")
                for bull_point in fundamental_data['investment_thesis']['bull_case']:
                    st.write(f"📈 {bull_point}")
            
            with col2:
                st.markdown("**🔴 弱気シナリオ**")
                for bear_point in fundamental_data['investment_thesis']['bear_case']:
                    st.write(f"📉 {bear_point}")
        
        return True

def get_supported_tickers():
    """
    Return list of tickers that have comprehensive fundamental analysis data
    """
    return ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA']