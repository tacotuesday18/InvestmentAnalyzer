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
企業の基本分析レポートを作成してください。以下の企業データに基づいて、包括的な分析を提供してください：

企業名: {company_data['name']} ({company_data['ticker']})
セクター: {company_data['sector']}
業界: {company_data['industry']}
時価総額: ${company_data['market_cap']:,} if company_data['market_cap'] else 'N/A'
売上高: ${company_data['revenue']:,} if company_data['revenue'] else 'N/A'
利益率: {company_data['profit_margins']:.2%} if company_data['profit_margins'] else 'N/A'
PER: {company_data['pe_ratio']:.2f} if company_data['pe_ratio'] else 'N/A'
PBR: {company_data['pb_ratio']:.2f} if company_data['pb_ratio'] else 'N/A'
負債比率: {company_data['debt_to_equity']:.2f} if company_data['debt_to_equity'] else 'N/A'
ROE: {company_data['roe']:.2%} if company_data['roe'] else 'N/A'

事業概要: {company_data['business_summary']}

以下の構造で詳細な分析レポートを作成してください：

## 📊 企業概要
## 💼 ビジネスモデル分析
## 📈 財務健全性評価
## 🎯 競合優位性
## ⚠️ リスク要因
## 🔮 将来展望
## 📋 投資判断の要点

各セクションで具体的で実用的な洞察を提供し、日本の投資家にとって理解しやすい形で説明してください。
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

def generate_earnings_call_analysis(ticker):
    """
    Generate realistic earnings call content based on actual financial data
    """
    try:
        # Get real financial data from Yahoo Finance
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get quarterly financials
        quarterly_financials = stock.quarterly_financials
        quarterly_income_stmt = stock.quarterly_income_stmt
        
        # Extract key financial data
        company_data = {
            'name': info.get('longName', ticker),
            'ticker': ticker,
            'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
            'market_cap': info.get('marketCap', 0),
            'revenue': info.get('totalRevenue', 0),
            'revenue_growth': info.get('revenueGrowth', 0),
            'profit_margins': info.get('profitMargins', 0),
            'operating_margins': info.get('operatingMargins', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'forward_pe': info.get('forwardPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'current_ratio': info.get('currentRatio', 0),
            'roe': info.get('returnOnEquity', 0),
            'roa': info.get('returnOnAssets', 0),
            'free_cash_flow': info.get('freeCashflow', 0),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'business_summary': info.get('longBusinessSummary', '')[:500]
        }
        
        prompt = f"""
以下の実際の財務データに基づいて、リアルな決算説明会の内容を生成してください：

企業: {company_data['name']} ({company_data['ticker']})
セクター: {company_data['sector']}
業界: {company_data['industry']}
時価総額: ${company_data['market_cap']:,} if company_data['market_cap'] else 'N/A'
売上高: ${company_data['revenue']:,} if company_data['revenue'] else 'N/A'
売上成長率: {company_data['revenue_growth']:.1%} if company_data['revenue_growth'] else 'N/A'
利益率: {company_data['profit_margins']:.1%} if company_data['profit_margins'] else 'N/A'
営業利益率: {company_data['operating_margins']:.1%} if company_data['operating_margins'] else 'N/A'
PER: {company_data['pe_ratio']:.2f} if company_data['pe_ratio'] else 'N/A'
PBR: {company_data['pb_ratio']:.2f} if company_data['pb_ratio'] else 'N/A'
ROE: {company_data['roe']:.1%} if company_data['roe'] else 'N/A'
流動比率: {company_data['current_ratio']:.2f} if company_data['current_ratio'] else 'N/A'

事業概要: {company_data['business_summary']}

この実際のデータに基づいて、以下の構造で本格的な決算説明会トランスクリプトを英語で作成してください：

Welcome to [Company Name]'s Latest Quarterly Earnings Call

CEO Opening Remarks:
- 実際の業績数値を使用した挨拶
- 四半期の主要成果
- 戦略的優先事項

CFO Financial Highlights:
- 実際の財務数値の詳細説明
- 前年同期比較
- バランスシート強度
- キャッシュフロー状況

Business Outlook:
- 将来の事業見通し
- 市場機会
- 潜在的課題

Q&A Session:
- アナリストからの典型的な質問
- 経営陣の回答
- 戦略的洞察

Forward-Looking Statements:
- 将来見通しに関する注意事項

実際のデータに基づいて、投資家にとって価値のある情報を含む本格的な内容を作成してください。数値は提供されたデータと一致させてください。
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.text if response.text else "決算説明会の生成に失敗しました。"
        
    except Exception as e:
        logging.error(f"Earnings call generation error: {e}")
        return f"決算説明会生成エラー: {str(e)}"

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