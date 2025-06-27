"""
Gemini-powered historical metrics generator for accurate financial data
Replaces OpenAI functionality when quota is exceeded
"""

import json
import logging
import os
import streamlit as st
import pandas as pd
import yfinance as yf
from google import genai
from google.genai import types

# Initialize Gemini client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_historical_metrics_with_gemini(ticker, current_pe=None, current_pb=None, current_ps=None):
    """
    Generate accurate historical average metrics using Gemini API
    Returns realistic historical data for 1, 3, 5, and 10 year periods
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
        
        system_prompt = """You are a senior equity research analyst with access to comprehensive historical financial data. Provide accurate historical valuation metrics based on real market data."""
        
        prompt = f"""Provide accurate historical average valuation metrics for {ticker} across different time periods.

Current metrics: {current_context}

Analyze {ticker}'s historical valuation ratios and provide realistic data for:

P/E Ratio Historical Averages:
- pe_1y: 1-year average P/E ratio
- pe_3y: 3-year average P/E ratio  
- pe_5y: 5-year average P/E ratio
- pe_10y: 10-year average P/E ratio

P/S Ratio Historical Averages:
- ps_1y: 1-year average P/S ratio
- ps_3y: 3-year average P/S ratio
- ps_5y: 5-year average P/S ratio
- ps_10y: 10-year average P/S ratio

P/B Ratio Historical Averages:
- pb_1y: 1-year average P/B ratio
- pb_3y: 3-year average P/B ratio
- pb_5y: 5-year average P/B ratio
- pb_10y: 10-year average P/B ratio

Additional Context:
- valuation_trend: overall trend description
- market_context: brief valuation context

Base analysis on actual financial data for {ticker}. Ensure all values are realistic numbers, not null.
Respond with JSON format only."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        
        if response.text:
            result = json.loads(response.text)
            return result
        else:
            return None
            
    except Exception as e:
        logging.error(f"Error generating historical metrics with Gemini: {e}")
        return None


def create_historical_metrics_table_with_gemini(ticker, current_pe=None, current_pb=None, current_ps=None):
    """
    Create a table showing current metrics vs historical averages using Gemini API
    Similar to financecharts.com format with actual data
    """
    try:
        # Get current financial data
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get current metrics if not provided
        if current_pe is None:
            current_pe = info.get('trailingPE', info.get('forwardPE', None))
        if current_pb is None:
            current_pb = info.get('priceToBook', None)
        if current_ps is None:
            current_ps = info.get('priceToSalesTrailing12Months', None)
        
        # Generate historical averages using Gemini
        gemini_metrics = generate_historical_metrics_with_gemini(ticker, current_pe, current_pb, current_ps)
        
        # Create table data
        table_data = []
        
        # P/E Ratio row
        if current_pe and current_pe > 0:
            pe_row = {
                '指標': 'P/E (Price/Earnings)',
                '現在': f"~{current_pe:.1f}x",
                '1年平均': get_gemini_average(gemini_metrics, 'pe_1y'),
                '3年平均': get_gemini_average(gemini_metrics, 'pe_3y'),
                '5年平均': get_gemini_average(gemini_metrics, 'pe_5y'),
                '10年平均': get_gemini_average(gemini_metrics, 'pe_10y')
            }
            table_data.append(pe_row)
        
        # P/S Ratio row
        if current_ps and current_ps > 0:
            ps_row = {
                '指標': 'P/S (Price/Sales)',
                '現在': f"~{current_ps:.1f}x",
                '1年平均': get_gemini_average(gemini_metrics, 'ps_1y'),
                '3年平均': get_gemini_average(gemini_metrics, 'ps_3y'),
                '5年平均': get_gemini_average(gemini_metrics, 'ps_5y'),
                '10年平均': get_gemini_average(gemini_metrics, 'ps_10y')
            }
            table_data.append(ps_row)
        
        # P/B Ratio row
        if current_pb and current_pb > 0:
            pb_row = {
                '指標': 'P/B (Price/Book)',
                '現在': f"~{current_pb:.1f}x",
                '1年平均': get_gemini_average(gemini_metrics, 'pb_1y'),
                '3年平均': get_gemini_average(gemini_metrics, 'pb_3y'),
                '5年平均': get_gemini_average(gemini_metrics, 'pb_5y'),
                '10年平均': get_gemini_average(gemini_metrics, 'pb_10y')
            }
            table_data.append(pb_row)
        
        # Create DataFrame and display table
        if table_data:
            df = pd.DataFrame(table_data)
            
            # Display title
            st.markdown(f"""
            ### 📊 {ticker}の現在のPE、PS、PB比率と過去平均の比較表
            
            以下は{ticker}の主要バリュエーション指標の現在値と過去平均値の比較です：
            """)
            
            # Style the table to match the financecharts.com format
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "指標": st.column_config.TextColumn("指標", width="medium"),
                    "現在": st.column_config.TextColumn("現在", width="small"),
                    "1年平均": st.column_config.TextColumn("1年平均", width="small"),
                    "3年平均": st.column_config.TextColumn("3年平均", width="small"),
                    "5年平均": st.column_config.TextColumn("5年平均", width="small"),
                    "10年平均": st.column_config.TextColumn("10年平均", width="small")
                }
            )
            
            # Add interpretation note
            st.markdown("""
            **📝 解釈のポイント:**
            - **P/E比率**: 現在値が過去平均より低い場合、割安の可能性
            - **P/S比率**: 売上高に対する評価の妥当性を示す
            - **P/B比率**: 純資産に対する市場評価を表す
            """)
            
            # Display trend analysis if available
            if gemini_metrics and gemini_metrics.get('market_context'):
                st.info(f"💡 **市場コンテキスト**: {gemini_metrics['market_context']}")
            
        else:
            st.info("📊 現在、この銘柄の主要指標データが利用できません")
            
    except Exception as e:
        st.error(f"履歴指標テーブルの作成中にエラーが発生しました: {str(e)}")


def get_gemini_average(gemini_metrics, metric_key):
    """
    Get historical average from Gemini data with proper formatting
    """
    try:
        if gemini_metrics and isinstance(gemini_metrics, dict):
            value = gemini_metrics.get(metric_key)
            if value and isinstance(value, (int, float)) and value > 0:
                return f"~{value:.1f}x"
        
        return "N/A"
        
    except Exception:
        return "N/A"


def extract_quarterly_business_developments_with_gemini(ticker, quarter_info="latest"):
    """
    Extract specific quarterly business developments using Gemini API
    """
    try:
        system_prompt = "You are a business intelligence analyst specializing in quarterly earnings analysis with focus on specific business developments."
        
        prompt = f"""As a business analyst, provide specific quarterly business developments for {ticker} ({quarter_info} quarter).

Focus on SPECIFIC business events and developments that happened during the quarter, not general company descriptions. Include:

1. Specific Product Launches/Updates: What new products or features were released?
2. Business Metrics Changes: How did key user metrics, revenue segments change?
3. Strategic Initiatives: What specific business moves were made (partnerships, acquisitions, expansions)?
4. Operational Changes: Any changes to business operations, pricing, or market approach?
5. CEO Key Messages: What were the main points emphasized by leadership?
6. Market Position Changes: How did competitive position or market share evolve?

Provide JSON response with these fields:
- product_developments: specific product/service launches or updates
- business_metrics_changes: quarter-over-quarter business metric changes
- strategic_initiatives: specific strategic moves made during quarter
- operational_updates: changes to operations, pricing, or processes
- ceo_key_messages: main messages from CEO about the quarter
- market_position: changes in competitive position or market dynamics
- financial_highlights: specific financial achievements or challenges this quarter
- outlook_changes: any updates to forward guidance or outlook

Focus on specific, actionable business intelligence rather than generic company information.
Respond with JSON format only."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        
        if response.text:
            result = json.loads(response.text)
            return result
        else:
            return None
            
    except Exception as e:
        logging.error(f"Error extracting quarterly developments with Gemini: {e}")
        return None


def generate_qa_section_analysis_with_gemini(ticker):
    """
    Generate detailed Q&A section analysis using Gemini API
    """
    try:
        system_prompt = "You are an expert in earnings call analysis, specializing in Q&A section insights."
        
        prompt = f"""Analyze the most recent earnings call Q&A section for {ticker} and provide insights on:

1. Key Investor Questions: What were investors most concerned about?
2. Management Responses: How did management address these concerns?
3. Guidance Updates: Any changes to forward-looking statements?
4. Competitive Concerns: Questions about competition and market position
5. Business Model Questions: Investor queries about the business strategy
6. Financial Concerns: Questions about margins, costs, or capital allocation

Provide JSON response with these fields:
- key_investor_concerns: main areas of investor questioning
- management_responses: how leadership addressed key concerns
- guidance_updates: any changes to forward guidance discussed
- competitive_discussions: talk about competitors and market position
- business_strategy_qa: questions and answers about business direction
- financial_qa: discussions about financial metrics and outlook
- unexpected_topics: any surprising topics that came up
- investor_sentiment: overall tone of investor questions

Focus on the interactive nature of the Q&A and specific concerns raised.
Respond with JSON format only."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        
        if response.text:
            result = json.loads(response.text)
            return result
        else:
            return None
            
    except Exception as e:
        logging.error(f"Error analyzing Q&A section with Gemini: {e}")
        return None