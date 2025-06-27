import json
import os
import logging
from openai import OpenAI
import streamlit as st

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_historical_metrics_with_chatgpt(ticker, current_pe=None, current_pb=None, current_ps=None):
    """
    Generate realistic historical average metrics using ChatGPT API based on industry and company size
    """
    try:
        prompt = f"""As a financial analyst, provide realistic historical average metrics for {ticker} stock based on industry benchmarks and company characteristics.

Please provide ONLY a JSON response with these fields:
- historical_pe_avg: realistic 5-year average PE ratio
- historical_pb_avg: realistic 5-year average PB ratio  
- historical_ps_avg: realistic 5-year average PS ratio
- current_vs_historical_pe: comparison analysis
- current_vs_historical_pb: comparison analysis
- current_vs_historical_ps: comparison analysis

Consider:
- Industry sector and typical valuation multiples
- Company size and growth stage
- Market conditions over past 5 years
- Current metrics if provided: PE={current_pe}, PB={current_pb}, PS={current_ps}

Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing realistic valuation metrics based on industry standards."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error generating historical metrics with ChatGPT: {e}")
        return None


def generate_current_stock_metrics_with_chatgpt(ticker, financial_data):
    """
    Generate comprehensive current stock metrics analysis using ChatGPT API
    """
    try:
        prompt = f"""As a financial analyst, analyze the current financial metrics for {ticker} and provide comprehensive insights.

Financial Data Available:
{json.dumps(financial_data, indent=2, default=str)}

Please provide ONLY a JSON response with these fields:
- valuation_assessment: current valuation level (undervalued/fairly_valued/overvalued)
- key_strengths: list of 3-4 financial strengths
- key_concerns: list of 3-4 potential concerns  
- growth_prospects: growth outlook assessment
- risk_factors: main risk considerations
- investment_thesis: concise investment case
- target_price_range: estimated fair value range
- recommendation: buy/hold/sell with reasoning

Base analysis on provided financial data and current market conditions.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior equity research analyst providing objective stock analysis."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error generating current metrics with ChatGPT: {e}")
        return None


def translate_earnings_transcript_to_japanese(english_text, section_type="general"):
    """
    Translate earnings transcript sections to high-quality Japanese using ChatGPT API
    Focus on Q&A, financial highlights, and executive commentary
    """
    try:
        # Different prompts based on section type
        if section_type == "qa":
            system_prompt = """あなたは金融専門の翻訳者です。決算説明会のQ&Aセクションを自然で正確な日本語に翻訳してください。
- 投資家の質問と経営陣の回答を明確に区別
- 財務用語は適切な日本語に翻訳
- ビジネス戦略や数値は正確に保持
- 自然な日本語の流れを重視"""
        elif section_type == "highlights":
            system_prompt = """あなたは金融専門の翻訳者です。決算ハイライトを自然で正確な日本語に翻訳してください。
- 財務数値と業績指標を正確に翻訳
- ビジネス成果を明確に表現
- 投資家向けの専門的な日本語を使用"""
        else:
            system_prompt = """あなたは金融専門の翻訳者です。決算説明会の内容を自然で正確な日本語に翻訳してください。
- 財務・ビジネス用語を適切に翻訳
- 経営陣の発言を自然な日本語に
- 数値データは正確に保持"""

        user_prompt = f"""以下の英語の決算説明会テキストを日本語に翻訳してください：

{english_text}

高品質で自然な日本語翻訳を提供してください。"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error translating transcript to Japanese: {e}")
        return None


def extract_quarterly_business_developments(ticker, quarter_info="latest"):
    """
    Extract specific quarterly business developments using ChatGPT API
    Focus on what actually happened in the business during the quarter
    """
    try:
        prompt = f"""As a business analyst, provide specific quarterly business developments for {ticker} ({quarter_info} quarter).

Focus on SPECIFIC business events and developments that happened during the quarter, not general company descriptions. Include:

1. Specific Product Launches/Updates: What new products or features were released?
2. Business Metrics Changes: How did key user metrics, revenue segments change?
3. Strategic Initiatives: What specific business moves were made (partnerships, acquisitions, expansions)?
4. Operational Changes: Any changes to business operations, pricing, or market approach?
5. CEO Key Messages: What were the main points emphasized by leadership?
6. Market Position Changes: How did competitive position or market share evolve?

Please provide ONLY a JSON response with these fields:
- product_developments: specific product/service launches or updates
- business_metrics_changes: quarter-over-quarter business metric changes
- strategic_initiatives: specific strategic moves made during quarter
- operational_updates: changes to operations, pricing, or processes
- ceo_key_messages: main messages from CEO about the quarter
- market_position: changes in competitive position or market dynamics
- financial_highlights: specific financial achievements or challenges this quarter
- outlook_changes: any updates to forward guidance or outlook

Focus on specific, actionable business intelligence rather than generic company information.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business intelligence analyst specializing in quarterly earnings analysis with focus on specific business developments."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error extracting quarterly developments: {e}")
        return None


def generate_qa_section_analysis(ticker):
    """
    Generate detailed Q&A section analysis focusing on investor concerns and management responses
    """
    try:
        prompt = f"""Analyze the most recent earnings call Q&A section for {ticker} and provide insights on:

1. Key Investor Questions: What were investors most concerned about?
2. Management Responses: How did management address these concerns?
3. Guidance Updates: Any changes to forward-looking statements?
4. Competitive Concerns: Questions about competition and market position
5. Business Model Questions: Investor queries about the business strategy
6. Financial Concerns: Questions about margins, costs, or capital allocation

Please provide ONLY a JSON response with these fields:
- key_investor_concerns: main areas of investor questioning
- management_responses: how leadership addressed key concerns
- guidance_updates: any changes to forward guidance discussed
- competitive_discussions: talk about competitors and market position
- business_strategy_qa: questions and answers about business direction
- financial_qa: discussions about financial metrics and outlook
- unexpected_topics: any surprising topics that came up
- investor_sentiment: overall tone of investor questions

Focus on the interactive nature of the Q&A and specific concerns raised.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in earnings call analysis, specializing in Q&A section insights."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error analyzing Q&A section: {e}")
        return None


def generate_japanese_earnings_summary(ticker, extracted_sections):
    """
    Generate comprehensive Japanese earnings summary from extracted sections
    """
    try:
        prompt = f"""{ticker}の決算内容について、以下の抽出された情報から包括的な日本語サマリーを作成してください：

抽出されたセクション:
{json.dumps(extracted_sections, indent=2, ensure_ascii=False)}

以下の形式でJSONレスポンスを提供してください：
- 決算概要: 全体的な業績サマリー
- 主要業績指標: 重要な財務数値とその分析
- 経営陣コメント: 戦略と見通しの要約
- qa重要ポイント: Q&Aセクションの主要な質問と回答
- 今後の注目点: 投資家が注目すべきポイント
- リスク要因: 懸念事項や課題

投資家向けの専門的で分かりやすい日本語で記述してください。"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは日本の機関投資家向けに企業分析レポートを作成する金融アナリストです。"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error generating Japanese earnings summary: {e}")
        return None