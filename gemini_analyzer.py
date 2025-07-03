import os
import json
import logging
from google import genai
from google.genai import types
import yfinance as yf
from twitter_sentiment_analyzer import TwitterDueDiligenceAnalyzer

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def analyze_company_fundamentals(ticker):
    """
    Generate comprehensive fundamental analysis report using Gemini AI
    """
    try:
        # Get company data
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get Twitter sentiment analysis for comprehensive due diligence
        twitter_analyzer = TwitterDueDiligenceAnalyzer()
        social_analysis = twitter_analyzer.generate_social_due_diligence_summary(ticker, info.get('longName', ticker))
        
        # Prepare company data for analysis
        company_data = {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'revenue': info.get('totalRevenue', 0),
            'profit_margins': info.get('profitMargins', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'roe': info.get('returnOnEquity', 0),
            'business_summary': info.get('longBusinessSummary', '')[:1000]  # Limit length
        }
        
        prompt = f"""
{company_data['name']} ({company_data['ticker']})の長期投資家向けの包括的なデューデリジェンス調査を作成してください。
財務データ、市場データ、そしてソーシャルメディア分析を統合した多角的な視点から詳細分析を提供してください。

企業名: {company_data['name']} ({company_data['ticker']})
セクター: {company_data['sector']}
業界: {company_data['industry']}
事業概要: {company_data['business_summary']}

## ソーシャルメディア投資家情勢
**Twitter分析結果**: 
- 全体センチメント: {social_analysis.get('sentiment_analysis', {}).get('overall_sentiment', 'データなし')}
- 投資家議論数: {social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0)}件
- 主要テーマ: {', '.join(social_analysis.get('sentiment_analysis', {}).get('key_themes', [])[:3])}
- 強気シグナル: {', '.join(social_analysis.get('sentiment_analysis', {}).get('bullish_signals', [])[:3])}
- 弱気シグナル: {', '.join(social_analysis.get('sentiment_analysis', {}).get('bearish_signals', [])[:3])}
- 機関投資家関連議論: {len(social_analysis.get('institutional_insights', {}).get('insights', []))}件

このソーシャルメディア分析結果も踏まえ、投資家コミュニティの視点や懸念点も考慮して以下の分析を行ってください。

まず、魅力的な企業ビジョンのヘッドラインで分析レポートを開始してください：

## 📈 企業ビジョン・ヘッドライン
（この企業の核となるビジョンや野心的な目標を、投資家が興味を持つような魅力的なキャッチフレーズで表現してください）

以下の7つの重要領域について、長期投資家向けの包括的なデューデリジェンス分析を提供してください。
各セクションで投資判断に必要な質的要因を客観的に評価し、強みと課題の両面を明確にしてください：

## 💼 A. ビジネスモデル・価値提案の本質
**事業の核心理解：**
- **事業内容**: この企業は具体的に何をして、どんな問題を誰のために解決しているのか
- **収益モデル**: どのようにして収益を上げているのか、そのモデルの持続性は？
- **顧客価値**: 顧客が本当に必要としている価値を提供しているか
- **ビジネスモデルの進化**: 市場変化に対する適応力と柔軟性

## 🎯 B. 製品・サービスと顧客基盤
**提供価値の評価：**
- **主力製品/サービス**: 核となる製品・サービスとその競争力
- **製品ライフサイクル**: イノベーション力と製品の防御可能性
- **顧客基盤**: 主要顧客層の特徴と顧客ロイヤルティの強さ
- **顧客満足度**: 顧客維持率と新規顧客獲得力

## 🏆 C. 業界地位と競争優位性（経済的堀）
**市場での立ち位置：**
- **業界構造**: 業界の成長性、競争激化度、規制環境
- **市場シェア**: 業界内でのポジションと影響力
- **競争の堀**: ブランド力、ネットワーク効果、特許、規模の経済、コスト優位性
- **脅威への対応**: 新規参入者、代替技術、破壊的イノベーションへの備え

**独自の構造的競争優位性：**
- **コスト構造の優位性**: 従来型競合と比較した根本的なコスト優位性（例：物理店舗なし、直販モデル、自動化、垂直統合）
- **オペレーションモデルの違い**: 業界慣行と異なる効率的なビジネスプロセス、技術活用による生産性向上
- **バリューチェーン最適化**: 垂直統合、中間業者排除、直接顧客関係などによる価値創造
- **資産効率性**: 資産軽量型モデル、デジタル化による固定費削減、スケーラブルな事業構造
- **顧客体験の差別化**: 従来型サービスとの根本的な体験の違い、利便性・満足度の向上
- **技術的優位性**: 独自技術、データ活用能力、イノベーション速度における競合優位
- **規制・制度の活用**: 新しい規制環境や制度変化を競合より効果的に活用する能力

**具体的なマーケティング戦略分析：**
- **顧客獲得戦略**: CAC（顧客獲得コスト）効率性、チャネル別ROI、具体的キャンペーン事例
- **ブランド構築手法**: ブランド投資の効果測定、競合との差別化戦略、認知度向上施策
- **デジタルマーケティング**: SEO/SEM、ソーシャルメディア、コンテンツマーケティングの成果
- **顧客セグメンテーション**: ターゲット市場の明確化、ペルソナ戦略、セグメント別アプローチ
- **リテンション戦略**: 顧客維持率、LTV（生涯価値）最大化、解約率削減の取り組み
- **価格戦略**: 価格決定権、競合価格への対応、価値ベース価格設定の実績

## 👥 D. 経営陣と企業文化
**リーダーシップの質：**
- **主要幹部の実績**: CEO、CFO、CTO等の過去の経歴と成果
- **経営の資質**: リーダーシップスタイル、戦略実行力、株主との利害一致
- **企業文化**: 革新性、倫理観、従業員への配慮
- **後継者計画**: 次世代リーダーの育成状況

## ⚠️ E. 事業リスクと課題
**主要リスク要因：**
- **運営リスク**: サプライチェーン、品質管理、オペレーション上の課題
- **規制リスク**: 法規制変更、コンプライアンス、政府政策の影響
- **評判リスク**: ブランド毀損、不祥事、社会的責任への配慮
- **市場集中リスク**: 特定顧客・市場・製品への過度な依存
- **適応力**: 業界変化への対応能力と柔軟性

## 📈 F. 成長ドライバーと長期展望
**成長機会の評価：**
- **有機成長**: 内部技術開発、新製品開発、市場拡大の機会
- **無機成長**: M&A戦略、戦略的パートナーシップの効果
- **持続可能性**: 競争優位性の長期維持可能性
- **業界トレンド**: 企業にプラス/マイナスとなる長期トレンド

## 🌱 G. ESG・企業評判
**持続可能性と社会的責任：**
- **環境配慮**: 環境への取り組み、サステナビリティ戦略
- **社会的責任**: 従業員、顧客、地域社会への配慮
- **ガバナンス**: 企業統治、透明性、倫理的経営
- **評判・ブランド**: 公的評価、論争や訴訟の有無、ブランド価値

## 💭 総合投資判断
**長期保有の適性評価：**
- この企業は根本的に優良なビジネスか？
- 短期的な市場変動を無視して長期保有する価値があるか？
- 主要な強み・弱み・不明な要素の総括
- 信頼できる根拠に基づく投資判断の提示



各セクションでは以下の分析アプローチを採用してください：
- 具体的な事例、数値、最近の動向を含める
- 投資判断に必要な客観的事実を重視する
- 強みと課題の両面を公平に評価する
- 長期投資家の視点から重要な要因を特定する
- 業界比較や競合との差別化を明確にする
- 信頼できる情報源に基づく分析を提供する

**構造的競争優位性の特定について：**
この企業が従来型競合に対して持つ根本的な優位性を深く分析してください：
- コスト構造：なぜこの企業は競合より低コストで同等以上のサービスを提供できるのか？（例：SoFiの物理店舗なしモデル、テスラの垂直統合）
- オペレーション効率：業界の既存慣行と異なる革新的なアプローチは何か？
- 顧客価値：コスト削減をどのように顧客価値向上に転換しているか？
- 模倣困難性：なぜ既存プレイヤーはこのモデルを簡単に真似できないのか？

分析は明確で誠実、実用的なトーンで作成し、質的洞察に重点を置いて、表面的な記述を避けてください。
各セクションで2000文字以上の詳細な分析を提供し、日本語で回答してください。

**重要**: この分析は長期投資家が投資判断を行う際の包括的なデューデリジェンス調査として使用されます。
表面的な一般論ではなく、この企業特有の詳細な洞察を提供し、優れた投資家が重視する質的要因を明確にしてください。
特に、この企業の独自のビジネスモデルがなぜ持続可能な競争優位性を生み出すのかを詳細に説明してください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.text if response.text else "分析レポートの生成に失敗しました。"
        
    except Exception as e:
        logging.error(f"Fundamental analysis error: {e}")
        return f"分析エラー: {str(e)}"

def translate_earnings_transcript(transcript_text):
    """
    Translate and analyze earnings call transcript using Gemini
    """
    try:
        if not transcript_text or len(transcript_text.strip()) < 100:
            return "翻訳対象のテキストが不十分です。"
        
        # Limit text length for API efficiency
        text_sample = transcript_text[:3000] if len(transcript_text) > 3000 else transcript_text
        
        prompt = f"""
以下の決算説明会の英語テキストを日本語に翻訳し、重要なポイントを要約してください：

{text_sample}

以下の形式で出力してください：

## 📝 決算説明会 - 主要ポイント（日本語翻訳）

### 💡 業績ハイライト
### 📊 財務結果
### 🎯 今後の見通し
### ❓ Q&A重要ポイント
### 📋 投資家向け要約

翻訳は自然な日本語で、投資判断に役立つ情報を重視してください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.text if response.text else "翻訳に失敗しました。"
        
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return f"翻訳エラー: {str(e)}"

def extract_and_translate_earnings_transcript(ticker):
    """
    Generate quarterly business-focused earnings analysis with specific developments and events
    """
    try:
        import trafilatura
        import requests
        
        # Get comprehensive company data
        stock = yf.Ticker(ticker)
        info = stock.info
        financials = stock.financials
        quarterly_financials = stock.quarterly_financials
        quarterly_earnings = stock.quarterly_earnings
        
        company_name = info.get('longName', ticker)
        
        # Try to get recent earnings data from multiple sources
        earnings_data = {}
        
        # First try to scrape from SEC filings or investor relations
        website = info.get('website', '')
        transcript_content = ""
        
        # Use company-specific investor relations pages for better transcript access
        company_ir_pages = {
            'AAPL': 'https://investor.apple.com/investor-relations/',
            'MSFT': 'https://www.microsoft.com/en-us/Investor/',
            'GOOGL': 'https://abc.xyz/investor/',
            'GOOG': 'https://abc.xyz/investor/',
            'AMZN': 'https://ir.aboutamazon.com/',
            'TSLA': 'https://ir.tesla.com/',
            'META': 'https://investor.fb.com/',
            'NVDA': 'https://investor.nvidia.com/',
            'NFLX': 'https://ir.netflix.net/',
            'AMD': 'https://ir.amd.com/',
            'ORCL': 'https://investor.oracle.com/',
            'CRM': 'https://investor.salesforce.com/',
            'INTC': 'https://www.intc.com/investor-relations'
        }
        
        # Enhanced sources using real transcript sources
        potential_sources = []
        
        # Priority sources: Investing.com and Seeking Alpha (as user suggested)
        potential_sources.extend([
            f"https://www.investing.com/equities/{ticker.lower()}-earnings",
            f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts", 
            f"https://seekingalpha.com/symbol/{ticker}/earnings",
            f"https://www.investing.com/search/?q={ticker}+earnings+transcript",
        ])
        
        # Add company-specific IR pages for official transcripts
        if ticker in company_ir_pages:
            potential_sources.append(company_ir_pages[ticker])
        
        # Add additional financial data sources
        potential_sources.extend([
            f"https://finance.yahoo.com/quote/{ticker}/financials",
            f"https://www.marketwatch.com/investing/stock/{ticker}/financials",
            f"https://finance.yahoo.com/quote/{ticker}/key-statistics"
        ])
        
        # Add company website IR (for press releases)
        if website:
            potential_sources.extend([
                f"{website}/investor-relations",
                f"{website}/investors", 
                f"{website}/ir",
                f"{website}/news"
            ])
        
        # Try to extract from financial news and earnings sites
        for source_url in potential_sources:
            if not source_url:
                continue
            try:
                downloaded = trafilatura.fetch_url(source_url)
                if downloaded:
                    text = trafilatura.extract(downloaded)
                    if text and len(text) > 500:
                        # Look for earnings-related content
                        text_lower = text.lower()
                        if any(term in text_lower for term in ['earnings', 'revenue', 'profit', 'quarterly', 'ceo', 'cfo']):
                            transcript_content = text[:5000]  # Take first 5000 characters
                            break
            except:
                continue
        
        # If we found some earnings content, enhance it with financial data and translate
        if transcript_content and len(transcript_content) > 200:
            # Get latest financial metrics
            revenue = info.get('totalRevenue', 0)
            net_income = info.get('netIncomeToCommon', 0)
            revenue_growth = info.get('revenueGrowth', 0)
            profit_margins = info.get('profitMargins', 0)
            
            # Create enhanced business-focused analysis with real data
            sector = info.get('sector', 'Technology')
            industry = info.get('industry', 'Software')
            business_summary = info.get('longBusinessSummary', '')[:1500]
            
            # Get quarterly financial data for business analysis
            latest_quarter_data = {}
            if not quarterly_financials.empty:
                latest_quarter = quarterly_financials.columns[0]
                latest_quarter_data = {
                    'revenue': quarterly_financials.loc['Total Revenue', latest_quarter] if 'Total Revenue' in quarterly_financials.index else 0,
                    'operating_income': quarterly_financials.loc['Operating Income', latest_quarter] if 'Operating Income' in quarterly_financials.index else 0,
                    'net_income': quarterly_financials.loc['Net Income', latest_quarter] if 'Net Income' in quarterly_financials.index else 0
                }
            
            # Get previous quarter for comparison
            previous_quarter_data = {}
            if not quarterly_financials.empty and len(quarterly_financials.columns) > 1:
                previous_quarter = quarterly_financials.columns[1]
                previous_quarter_data = {
                    'revenue': quarterly_financials.loc['Total Revenue', previous_quarter] if 'Total Revenue' in quarterly_financials.index else 0,
                    'operating_income': quarterly_financials.loc['Operating Income', previous_quarter] if 'Operating Income' in quarterly_financials.index else 0,
                    'net_income': quarterly_financials.loc['Net Income', previous_quarter] if 'Net Income' in quarterly_financials.index else 0
                }
            
            # Calculate quarter-over-quarter changes
            qoq_revenue_change = 0
            qoq_operating_change = 0
            qoq_net_income_change = 0
            
            if previous_quarter_data.get('revenue', 0) != 0:
                try:
                    current_rev = float(latest_quarter_data.get('revenue', 0)) if latest_quarter_data.get('revenue', 0) else 0
                    prev_rev = float(previous_quarter_data.get('revenue', 0)) if previous_quarter_data.get('revenue', 0) else 1
                    qoq_revenue_change = ((current_rev - prev_rev) / prev_rev) * 100
                except:
                    qoq_revenue_change = 0
            
            if previous_quarter_data.get('operating_income', 0) != 0:
                try:
                    current_op = float(latest_quarter_data.get('operating_income', 0)) if latest_quarter_data.get('operating_income', 0) else 0
                    prev_op = float(previous_quarter_data.get('operating_income', 0)) if previous_quarter_data.get('operating_income', 0) else 1
                    qoq_operating_change = ((current_op - prev_op) / prev_op) * 100
                except:
                    qoq_operating_change = 0
            
            if previous_quarter_data.get('net_income', 0) != 0:
                try:
                    current_net = float(latest_quarter_data.get('net_income', 0)) if latest_quarter_data.get('net_income', 0) else 0
                    prev_net = float(previous_quarter_data.get('net_income', 0)) if previous_quarter_data.get('net_income', 0) else 1
                    qoq_net_income_change = ((current_net - prev_net) / prev_net) * 100
                except:
                    qoq_net_income_change = 0

            enhanced_content = f"""
{company_name} Quarterly Business Analysis & Earnings Insights

QUARTERLY BUSINESS PERFORMANCE:
Recent Quarter Revenue: ${latest_quarter_data.get('revenue', 0):,.0f}
Quarter-over-Quarter Revenue Change: {qoq_revenue_change:+.1f}%
Operating Income Change: {qoq_operating_change:+.1f}%
Net Income Change: {qoq_net_income_change:+.1f}%

BUSINESS DEVELOPMENTS & STRATEGIC INITIATIVES:
Sector: {sector} | Industry: {industry}
Business Summary: {business_summary}

QUARTERLY FINANCIAL HIGHLIGHTS:
- Revenue Growth: {"Strong growth" if qoq_revenue_change > 5 else "Moderate growth" if qoq_revenue_change > 0 else "Revenue decline"}
- Operational Efficiency: {"Improving margins" if qoq_operating_change > 0 else "Margin pressure"}
- Profitability Trend: {"Increasing profitability" if qoq_net_income_change > 0 else "Profitability challenges"}

MARKET POSITIONING & COMPETITIVE DYNAMICS:
Current Market Cap: ${info.get('marketCap', 0):,}
Trading Multiple: {info.get('trailingPE', 'N/A')}x P/E ratio
Book Value: {info.get('priceToBook', 'N/A')}x P/B ratio

BUSINESS INSIGHTS:
{transcript_content[:2000] if transcript_content else f"Analyzing {company_name}'s business fundamentals and quarterly performance trends based on financial data."}

KEY BUSINESS DRIVERS:
- Revenue drivers: {"Product sales growth" if qoq_revenue_change > 0 else "Market challenges affecting revenue"}
- Cost management: {"Operational efficiency gains" if qoq_operating_change > qoq_revenue_change else "Rising operational costs"}
- Market expansion: Business operating in {sector} with focus on {industry}

INVESTMENT PERSPECTIVE:
The quarterly results show {"positive business momentum" if qoq_revenue_change > 0 else "business headwinds"} with {"improving operational metrics" if qoq_operating_change > 0 else "operational challenges"}. The company's strategic position in {sector} provides {"competitive advantages" if info.get('returnOnEquity', 0) > 0.15 else "market positioning opportunities"}.
"""
            
            # Translate the enhanced content with focus on quarterly business developments
            prompt = f"""
以下の{company_name}の四半期決算分析を日本語に翻訳し、具体的なビジネス展開や事業変化に焦点を当てて要約してください：

{enhanced_content}

翻訳・分析の際は以下の点を重視してください：
- 四半期の具体的な業績変化とその原因
- 新製品、サービス、事業展開などの具体的な事業活動
- 市場環境や競争状況の変化が業績に与えた影響
- 経営陣の発言や今後の戦略的方向性
- 業界全体の動向と当社への影響

以下の形式で、具体的なビジネス情報を中心に分析してください：

## {company_name} 最新四半期ビジネス分析

### 📊 四半期業績の変化
[前四半期比での具体的な業績変化とその背景]

### 🚀 事業展開・新規取り組み
[新製品発表、市場参入、戦略的投資など具体的な事業活動]

### 📈 業績を押し上げた要因
[売上成長や利益改善の具体的な要因]

### ⚠️ 課題・懸念材料
[業績に悪影響を与えた要因や今後の懸念]

### 🎯 今後の展望・戦略
[経営陣の発言や今後の事業戦略]

### 💡 投資家への示唆
[これらの事業変化が投資判断に与える影響]
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            
            if response.text:
                return response.text
            else:
                return f"{company_name}の決算分析の翻訳に失敗しました。"
        
        else:
            # If no external content found, create analysis from available financial data
            revenue = info.get('totalRevenue', 0)
            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE', 0)
            
            basic_analysis = f"""
{company_name} Financial Analysis Summary

Current Financial Position:
- Market Capitalization: ${market_cap:,} if market_cap else 'N/A'
- Annual Revenue: ${revenue:,} if revenue else 'N/A'
- P/E Ratio: {pe_ratio} if pe_ratio else 'N/A'
- Sector: {info.get('sector', 'N/A')}
- Industry: {info.get('industry', 'N/A')}

Business Overview:
{info.get('longBusinessSummary', 'Business summary not available')[:1000]}

Key Investment Considerations:
The company operates in the {info.get('sector', 'technology')} sector and continues to maintain its market position with steady financial performance.
"""
            
            # Translate basic analysis
            prompt = f"""
以下の{company_name}の財務分析を日本語に翻訳してください：

{basic_analysis}

投資家向けの情報として、正確で理解しやすい日本語に翻訳してください。

## {company_name} 財務分析サマリー

[翻訳された財務分析内容]
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            
            if response.text:
                return response.text
            else:
                return f"{company_name}の財務分析を生成しました。詳細な決算説明会トランスクリプトについては、企業の投資家向けページをご確認ください。"
            
    except Exception as e:
        logging.error(f"Earnings analysis error: {e}")
        return f"決算分析の生成中にエラーが発生しました: {str(e)}"

def generate_business_insights(ticker):
    """
    Generate comprehensive business insights and financial analysis
    """
    try:
        # Get real financial data from Yahoo Finance
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get financial statements
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        
        # Extract comprehensive financial data
        company_data = {
            'name': info.get('longName', ticker),
            'ticker': ticker,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'enterprise_value': info.get('enterpriseValue', 0),
            'revenue': info.get('totalRevenue', 0),
            'revenue_growth': info.get('revenueGrowth', 0),
            'profit_margins': info.get('profitMargins', 0),
            'operating_margins': info.get('operatingMargins', 0),
            'ebitda_margins': info.get('ebitdaMargins', 0),
            'gross_margins': info.get('grossMargins', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'forward_pe': info.get('forwardPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
            'peg_ratio': info.get('pegRatio', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'current_ratio': info.get('currentRatio', 0),
            'quick_ratio': info.get('quickRatio', 0),
            'roe': info.get('returnOnEquity', 0),
            'roa': info.get('returnOnAssets', 0),
            'roic': info.get('returnOnCapital', 0),
            'free_cash_flow': info.get('freeCashflow', 0),
            'operating_cash_flow': info.get('operatingCashflow', 0),
            'total_cash': info.get('totalCash', 0),
            'total_debt': info.get('totalDebt', 0),
            'book_value': info.get('bookValue', 0),
            'earnings_growth': info.get('earningsGrowth', 0),
            'revenue_per_share': info.get('revenuePerShare', 0),
            'business_summary': info.get('longBusinessSummary', '')[:800]
        }
        
        prompt = f"""
以下の実際の財務データに基づいて、企業の包括的なビジネス洞察と財務分析を日本語で提供してください：

企業: {company_data['name']} ({company_data['ticker']})
セクター: {company_data['sector']}
業界: {company_data['industry']}

財務指標:
- 時価総額: ${company_data['market_cap']:,} if company_data['market_cap'] else 'N/A'
- 売上高: ${company_data['revenue']:,} if company_data['revenue'] else 'N/A'
- 売上成長率: {company_data['revenue_growth']:.1%} if company_data['revenue_growth'] else 'N/A'
- 利益率: {company_data['profit_margins']:.1%} if company_data['profit_margins'] else 'N/A'
- 営業利益率: {company_data['operating_margins']:.1%} if company_data['operating_margins'] else 'N/A'
- PER: {company_data['pe_ratio']:.2f} if company_data['pe_ratio'] else 'N/A'
- PBR: {company_data['pb_ratio']:.2f} if company_data['pb_ratio'] else 'N/A'
- ROE: {company_data['roe']:.1%} if company_data['roe'] else 'N/A'
- フリーキャッシュフロー: ${company_data['free_cash_flow']:,} if company_data['free_cash_flow'] else 'N/A'
- 負債比率: {company_data['debt_to_equity']:.2f} if company_data['debt_to_equity'] else 'N/A'
- 流動比率: {company_data['current_ratio']:.2f} if company_data['current_ratio'] else 'N/A'

事業概要: {company_data['business_summary']}

以下の構造で詳細なビジネス分析を提供してください：

## 🏢 事業の核心理解
## 💰 最新四半期の財務健全性
## 📈 成長性と収益性の評価
## ⚡ 競争力と市場ポジション
## 🎯 投資判断のポイント
## ⚠️ 注意すべきリスク要因
## 🔮 今後の事業展望

各セクションで具体的な数値を使用し、日本の個人投資家にとって実用的で理解しやすい分析を提供してください。この企業への投資を検討する際の重要な要因を明確に説明してください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.text if response.text else "ビジネス分析の生成に失敗しました。"
        
    except Exception as e:
        logging.error(f"Business insights generation error: {e}")
        return f"ビジネス分析エラー: {str(e)}"

def analyze_historical_metrics_insight(ticker, metrics_data):
    """
    Provide AI insights on historical metrics trends
    """
    try:
        if not metrics_data or len(metrics_data) == 0:
            return "分析対象のデータがありません。"
        
        # Calculate basic statistics
        latest_pe = metrics_data.get('PE_Ratio', [0])[-1] if metrics_data.get('PE_Ratio') else 0
        latest_pb = metrics_data.get('PB_Ratio', [0])[-1] if metrics_data.get('PB_Ratio') else 0
        avg_pe = sum(metrics_data.get('PE_Ratio', [])) / len(metrics_data.get('PE_Ratio', [1])) if metrics_data.get('PE_Ratio') else 0
        avg_pb = sum(metrics_data.get('PB_Ratio', [])) / len(metrics_data.get('PB_Ratio', [1])) if metrics_data.get('PB_Ratio') else 0
        
        prompt = f"""
{ticker}の過去10年間の財務指標データに基づいて、投資判断に役立つ洞察を提供してください：

現在のPER: {latest_pe:.2f}倍
10年平均PER: {avg_pe:.2f}倍
現在のPBR: {latest_pb:.2f}倍  
10年平均PBR: {avg_pb:.2f}倍

以下の観点から分析してください：

## 📊 バリュエーション分析
## 📈 トレンド評価
## ⚖️ 適正価格帯の考察
## 🎯 投資タイミングの示唆

簡潔で実用的な分析を提供してください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp", 
            contents=prompt
        )
        
        return response.text if response.text else "分析に失敗しました。"
        
    except Exception as e:
        logging.error(f"Metrics analysis error: {e}")
        return f"分析エラー: {str(e)}"

def generate_earnings_summary(ticker, financial_data):
    """
    Generate earnings analysis summary using Gemini
    """
    try:
        prompt = f"""
{ticker}の最新決算データに基づいて、包括的な決算分析レポートを作成してください：

財務データ概要:
- 企業名: {financial_data.get('name', ticker)}
- セクター: {financial_data.get('sector', 'N/A')}
- 現在株価: ${financial_data.get('current_price', 0):.2f}
- 時価総額: ${financial_data.get('market_cap', 0):,.0f}
- 売上成長率: {financial_data.get('historical_growth', 0):.1f}%

以下の構造でレポートを作成してください：

## 📊 決算ハイライト
## 💰 財務パフォーマンス  
## 📈 成長性分析
## 🎯 業績予想
## ⚠️ 注意すべきポイント
## 📋 投資判断への示唆

実用的で分かりやすい分析を提供してください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.text if response.text else "決算分析の生成に失敗しました。"
        
    except Exception as e:
        logging.error(f"Earnings analysis error: {e}")
        return f"分析エラー: {str(e)}"