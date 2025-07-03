import os
import json
import logging
from google import genai
from google.genai import types
import yfinance as yf

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
財務比率は一切使用せず、優れた投資家が重視する企業の本質的な競争力と持続的成長要因に焦点を当てた詳細分析を提供してください。

企業名: {company_data['name']} ({company_data['ticker']})
セクター: {company_data['sector']}
業界: {company_data['industry']}
事業概要: {company_data['business_summary']}

まず、魅力的な企業ビジョンのヘッドラインで分析レポートを開始してください：

## 📈 企業ビジョン・ヘッドライン
（この企業の核となるビジョンや野心的な目標を、投資家が興味を持つような魅力的なキャッチフレーズで表現してください）

続いて、以下の6つの領域について、具体例と最近の動向を含む投資判断に重要な要因分析を提供してください。
各セクションで、投資機会と潜在的リスクの両面から客観的な分析を行い、長期投資家が評価すべき重要な要因を明確にしてください：

## 🏰 A. 経済的堀と核心的競争力
**具体的な競争優位性の源泉：**
- **コア・コンピタンシー**: この企業独自の中核的能力と差別化要因を特定
- **コスト構造上の優位性**: 例：デジタル銀行の物理店舗コスト削減による高利回り提供能力
- **顧客獲得コスト vs 顧客維持コスト**: 既存顧客への新サービス提供の経済的優位性
- **技術的優位性**: 独自技術、プラットフォーム効果、データ活用能力
- **規制・参入障壁**: ライセンス、規制対応コスト、業界経験の必要性
- **ネットワーク効果とエコシステム**: プラットフォーム参加者間の相互作用による価値創出
- **ブランド力とカスタマーロイヤルティ**: 顧客のスイッチングコスト
- この堀は時間とともに強化されるのか、それとも弱体化するリスクがあるのか？
- 競合他社はこの堀をどのように攻撃しているか？具体例を挙げて説明

## 💼 B. ビジネスモデルと戦略
**収益構造と持続可能性：**
- 実際にどのように収益を上げているのか？このモデルの回復力は？
- 複数の収益源のバランスとリスク分散効果
- 景気循環や外部ショックに対する収益の安定性

**成長戦略の詳細分析：**
- **有機成長 vs 無機成長**: 内部開発と買収のバランス、過去のM&A実績評価
- **地理的拡張戦略**: 国際展開の手法、現地化への取り組み、文化的適応力
- **製品・サービス拡張**: 既存顧客への追加販売、新分野への参入戦略
- **垂直統合 vs パートナーシップ**: サプライチェーン戦略、協業関係の構築
- **プラットフォーム戦略**: エコシステム構築、サードパーティとの関係

**マーケティング戦略の深掘り：**
- **顧客獲得戦略**: CAC（顧客獲得コスト）効率性、チャネル別ROI分析
- **ブランド構築手法**: ブランド投資の効果測定、競合との差別化戦略
- **デジタルマーケティング**: SEO/SEM、ソーシャルメディア、コンテンツマーケティングの活用
- **顧客セグメンテーション**: ターゲット市場の明確化、ペルソナ戦略
- **リテンション戦略**: 顧客維持率、LTV（生涯価値）最大化の取り組み
- **価格戦略**: 価格決定権、競合価格への対応、価値ベース価格設定

**戦略実行力の評価：**
- 過去の成功にあぐらをかいているのか、それとも本当にイノベーションを続けているのか？
- 戦略は現実と一致しているか、それとも単なる美辞麗句か？具体的な執行例で判断
- 戦略変更の機敏性、市場変化への適応スピード

## 👥 C. 経営陣の質
**主要幹部の具体的な実績と資質評価：**
- **CEO**: 過去の経歴、実績、リーダーシップスタイル、戦略的ビジョンの実行能力を詳細分析
- **CFO**: 財務戦略、資本配分の巧拙、投資家との関係構築能力
- **CTO**: 技術戦略、イノベーション推進力、競合技術への対応力
- **COO**: オペレーション効率化、組織運営、実行力の評価
- 各幹部の前職での成功/失敗事例と現職での具体的な成果
- 資本配分の実績は良好か？M&A、設備投資、株主還元の判断事例を検証
- 株主や顧客に対するコミュニケーションは率直で現実的か？
- インセンティブは株主と一致しているか、それとも経営陣に偏重しているか？
- 帝国建設、誇大宣伝、問題隠蔽の兆候はないか？

## 🏢 D. 企業文化と人材
- 企業文化は健全か、それとも問題があるか？
- 優秀な人材は留まっているか、それとも離職しているか？
- 最高の人材を引き付けることができているか？
- 内部告発、訴訟、ガバナンス上の問題はないか？

## 🌍 E. 業界ポジションとマクロ環境
- 真の競合他社は誰か？市場シェアを獲得しているか、失っているか？
- どのような脅威が存在するか？（規制、新技術、顧客の嗜好変化）
- グローバルやマクロトレンドの中でどのような位置にあるか？

## 📊 G. 製品・サービス成功度分析
**製品ポートフォリオの詳細評価：**
- **成功製品・サービスの特定**: 収益貢献度、成長率、市場シェア、顧客満足度が高い製品/サービス
- **失敗・苦戦製品の分析**: 期待を下回った製品、撤退・縮小した事業の原因分析
- **製品ライフサイクル段階**: 各製品の導入期・成長期・成熟期・衰退期における位置づけ
- **製品間のシナジー効果**: クロスセル、バンドリング、エコシステム効果の実績
- **イノベーション成功率**: 新製品開発の投資対効果、市場投入成功率
- **収益化パターン**: 製品別の収益構造、利益率、成長性の違い

**具体的な製品・サービス実績：**
- **主力製品の進化**: コア製品の機能改善、市場適応、競合対応の歴史
- **新規事業の成否**: 新分野参入の成果、失敗事例から学んだ教訓
- **顧客セグメント別適合度**: B2B vs B2C、企業規模別、地域別の製品受容度
- **技術革新の商業化**: R&D投資が実際の製品・収益に結びついた成功事例
- **パートナーシップ製品**: 他社との協業による製品・サービスの成果

## 📊 H. 成長エンジンと顧客戦略
**顧客ライフサイクル管理：**
- **顧客獲得**: 新規顧客獲得チャネルの効率性、CAC（顧客獲得コスト）トレンド
- **オンボーディング**: 新規顧客の定着率、アクティベーション戦略
- **エンゲージメント**: 顧客参加度向上施策、使用頻度・深度の改善
- **リテンション**: 解約率（チャーン率）削減戦略、顧客維持の取り組み
- **拡張**: アップセル・クロスセル戦略、既存顧客からの収益拡大
- **アドボカシー**: 顧客による紹介・推薦の活用、NPS（ネットプロモータースコア）向上

**成長指標の実績評価：**
- **ユニットエコノミクス**: LTV/CAC比率、投資回収期間（ペイバック期間）
- **コホート分析**: 世代別顧客行動、長期的な価値創出パターン
- **市場浸透度**: TAM/SAM/SOMにおける現在のポジション、成長余地
- **バイラル係数**: 顧客による自然な拡散効果、紹介プログラムの効果

## 📊 H. 成功・苦戦要因の根本分析
**企業の業績を左右する核心的要因：**
- **成功要因**: 過去5年間で企業が成功した具体的な理由（戦略、実行、市場環境、運）
- **苦戦・失敗要因**: 業績低迷や戦略失敗の根本原因と学習能力
- **外部環境 vs 内部要因**: 成功/失敗がコントロール可能な要因によるものか
- **再現性**: 成功パターンが持続可能で再現可能か、それとも一時的なものか
- **危機対応力**: 過去の危機や逆境をどのように乗り越えたか
- **機会捕捉力**: 市場機会を見つけて活用する組織的能力

## 🤝 F. ステークホルダーとの信頼関係
- 顧客は企業を愛しているのか、それとも我慢しているのか？
- サプライヤーやパートナーは忠実か、それとも代替案を探しているか？
- 規制当局は味方と見なしているか、それとも標的と見なしているか？

各セクションで：
- 具体的な事例、実名、数値、最近の動向を豊富に含める
- 懐疑的な視点を保ち、表面的な評価を避ける
- 自分自身の結論に挑戦し、反対意見も考慮する
- 投資家が見落としがちな重要なリスクを特定する
- 経営陣については、個人名、経歴、具体的な成果・失敗事例を詳述
- 競合他社との比較を具体的に行い、優劣を明確化
- 業界特有の課題や機会について具体例で説明

**成長・マーケティング戦略については特に詳細に：**
- 具体的なマーケティングキャンペーン事例、チャネル別の成果
- 顧客獲得コスト（CAC）や顧客生涯価値（LTV）の実際の数値やトレンド
- A/Bテスト、パーソナライゼーション、データドリブンマーケティングの実例
- パートナーシップ、インフルエンサーマーケティング、コンテンツ戦略の具体例
- 地域別・セグメント別の成長戦略の違いと成果
- ブランド認知度調査、市場シェア推移、競合比較の具体的データ

**製品・サービス成功分析については：**
- 具体的な製品名、サービス名、ローンチ時期、成果指標
- 収益貢献度の数値（売上構成比、成長率、利益率）
- 市場シェア、ユーザー数、採用率などの具体的データ
- 顧客満足度調査、NPS、レビュー評価などの品質指標
- 競合製品との比較優位性、差別化ポイント
- 失敗製品の具体的な撤退理由、損失額、学んだ教訓

**重要**: この分析は長期投資家が投資判断を行う際の参考資料として使用されます。
表面的な一般論ではなく、この企業特有の詳細な洞察を提供してください。
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