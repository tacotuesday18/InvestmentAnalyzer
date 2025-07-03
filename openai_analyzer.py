"""
Fixed OpenAI analyzer with proper JSON handling to prevent the JSON parsing errors
"""

import json
import logging
import os
from openai import OpenAI
from twitter_sentiment_analyzer import TwitterDueDiligenceAnalyzer

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def safe_json_parse(response):
    """Safely parse JSON response with null checking"""
    try:
        content = response.choices[0].message.content
        if content and content.strip():
            return json.loads(content)
        else:
            return None
    except (json.JSONDecodeError, AttributeError, IndexError) as e:
        logging.error(f"JSON parsing error: {e}")
        return None


def generate_historical_metrics_with_ai(ticker, current_pe=None, current_pb=None, current_ps=None):
    """
    Generate accurate historical average metrics for multiple time periods using ChatGPT API
    """
    try:
        # Prepare current metrics context
        current_context = ""
        if current_pe:
            current_context += f"Current P/E: {current_pe:.2f}, "
        if current_pb:
            current_context += f"Current P/B: {current_pb:.2f}, "
        if current_ps:
            current_context += f"Current P/S: {current_ps:.2f}"
        
        prompt = f"""Provide accurate historical average valuation metrics for {ticker} across different time periods.

Current metrics: {current_context}

Analyze {ticker}'s historical valuation ratios and provide ONLY a JSON response with these specific fields:

P/E Ratio Historical Averages:
- pe_1y: 1-year average P/E ratio
- pe_3y: 3-year average P/E ratio  
- pe_5y: 5-year average P/E ratio
- pe_10y: 10-year average P/E ratio (if available)

P/S Ratio Historical Averages:
- ps_1y: 1-year average P/S ratio
- ps_3y: 3-year average P/S ratio
- ps_5y: 5-year average P/S ratio
- ps_10y: 10-year average P/S ratio (if available)

P/B Ratio Historical Averages:
- pb_1y: 1-year average P/B ratio
- pb_3y: 3-year average P/B ratio
- pb_5y: 5-year average P/B ratio
- pb_10y: 10-year average P/B ratio (if available)

Additional Context:
- valuation_trend: overall trend in company's valuation over time
- market_context: brief context about the company's valuation patterns (write in Japanese)

Base analysis on actual financial data for {ticker}. Ensure all values are realistic and reflect the company's actual trading history.
The market_context field must be written in Japanese. Provide professional analysis of historical valuation trends.
If data for a specific period is not available, use null.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior equity research analyst with access to comprehensive historical financial data. Provide accurate historical valuation metrics based on real market data. Write the market_context field in Japanese only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        return safe_json_parse(response)
        
    except Exception as e:
        logging.error(f"Error generating historical metrics with AI: {e}")
        return None


def generate_current_stock_metrics_with_ai(ticker, financial_data):
    """
    Generate current stock evaluation using AI API
    """
    try:
        prompt = f"""As an expert financial analyst, evaluate {ticker} stock based on the provided financial metrics.

Financial Data:
{financial_data}

Provide ONLY a JSON response with these fields:
- investment_recommendation: "Buy", "Hold", or "Sell"
- target_price_range: estimated 12-month price target range
- key_strengths: list of 3 main strengths
- key_risks: list of 3 main risks
- valuation_assessment: overall valuation commentary
- growth_outlook: growth prospects assessment
- financial_health_score: score from 1-10
- market_position: competitive position analysis

Base your analysis on actual financial fundamentals and market conditions.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior equity research analyst providing investment analysis based on financial data."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return safe_json_parse(response)
        
    except Exception as e:
        logging.error(f"Error generating stock metrics: {e}")
        return None


def translate_earnings_transcript_to_japanese(earnings_data):
    """
    Translate earnings information to Japanese using ChatGPT API
    """
    try:
        prompt = f"""Translate and summarize the following earnings information into professional Japanese for Japanese investors:

{earnings_data}

Provide ONLY a JSON response with these fields:
- japanese_summary: comprehensive Japanese summary of earnings highlights
- key_financial_metrics: key financial metrics in Japanese
- management_commentary: management commentary in Japanese
- outlook: forward guidance in Japanese
- investor_takeaways: key takeaways for Japanese investors

Write in professional business Japanese suitable for financial analysis.
Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional financial translator specializing in Japanese business communication."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return safe_json_parse(response)
        
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
        
        return safe_json_parse(response)
        
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
        
        return safe_json_parse(response)
        
    except Exception as e:
        logging.error(f"Error analyzing Q&A section: {e}")
        return None