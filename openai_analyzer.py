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


def extract_key_transcript_sections(transcript_text):
    """
    Extract and identify key sections from earnings transcript using ChatGPT API
    """
    try:
        prompt = f"""Analyze this earnings transcript and extract the key sections. Identify and separate:

1. Financial Highlights/Key Metrics
2. Executive Commentary/Management Discussion  
3. Q&A Section (most important)
4. Forward Guidance
5. Strategic Updates

Transcript:
{transcript_text[:8000]}  # Limit text size

Please provide ONLY a JSON response with these fields:
- financial_highlights: key financial data and metrics
- executive_commentary: management discussion and strategy
- qa_section: questions and answers (full content)
- forward_guidance: future outlook and guidance
- strategic_updates: business strategy and initiatives
- key_topics: list of main discussion topics

Format as valid JSON only."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst extracting key information from earnings transcripts."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logging.error(f"Error extracting transcript sections: {e}")
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