"""
Comprehensive Due Diligence Analyzer
Integrates Gemini AI, OpenAI, and Twitter sentiment analysis for best-in-class investment research
"""

import os
import json
import logging
import yfinance as yf
from typing import Dict, Any
from twitter_sentiment_analyzer import TwitterDueDiligenceAnalyzer
from gemini_analyzer import analyze_company_fundamentals
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveDueDiligenceAnalyzer:
    """
    Master analyzer that orchestrates multiple AI systems and data sources
    for comprehensive investment due diligence
    """
    
    def __init__(self):
        """Initialize all AI clients and analyzers"""
        try:
            # Initialize OpenAI client
            self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            # Initialize Twitter analyzer
            self.twitter_analyzer = TwitterDueDiligenceAnalyzer()
            
            logger.info("Comprehensive Due Diligence Analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize comprehensive analyzer: {e}")
            raise
    
    def generate_comprehensive_due_diligence_report(self, ticker: str) -> Dict[str, Any]:
        """
        Generate the most comprehensive due diligence report possible
        using Gemini, OpenAI, and Twitter sentiment analysis
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
            
        Returns:
        --------
        Dict[str, Any]
            Comprehensive due diligence report combining all data sources
        """
        logger.info(f"Starting comprehensive due diligence analysis for {ticker}")
        
        try:
            # Get basic company information
            stock = yf.Ticker(ticker)
            info = stock.info
            company_name = info.get('longName', ticker)
            
            # 1. Get Twitter sentiment analysis first (provides social context)
            logger.info(f"Gathering social media sentiment for {ticker}")
            social_analysis = self.twitter_analyzer.generate_social_due_diligence_summary(ticker, company_name)
            
            # 2. Generate Gemini fundamental analysis (with Twitter integration)
            logger.info(f"Generating Gemini AI fundamental analysis for {ticker}")
            gemini_analysis = analyze_company_fundamentals(ticker)
            
            # 3. Generate OpenAI cross-verification analysis
            logger.info(f"Generating OpenAI cross-verification analysis for {ticker}")
            openai_analysis = self._generate_openai_cross_verification(ticker, company_name, social_analysis)
            
            # 4. Synthesize final comprehensive report
            logger.info(f"Synthesizing comprehensive report for {ticker}")
            comprehensive_report = self._synthesize_comprehensive_report(
                ticker, company_name, info, social_analysis, gemini_analysis, openai_analysis
            )
            
            logger.info(f"Comprehensive due diligence analysis completed for {ticker}")
            return comprehensive_report
            
        except Exception as e:
            logger.error(f"Error in comprehensive due diligence analysis for {ticker}: {e}")
            return self._create_error_report(ticker, str(e))
    
    def _generate_openai_cross_verification(self, ticker: str, company_name: str, social_analysis: Dict) -> str:
        """
        Generate OpenAI analysis that cross-verifies and adds insights to other analyses
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        company_name : str
            Company name
        social_analysis : Dict
            Twitter sentiment analysis results
            
        Returns:
        --------
        str
            OpenAI analysis focused on cross-verification and additional insights
        """
        try:
            # Get company data for context
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Create focused prompt for OpenAI cross-verification
            prompt = f"""
As an experienced investment analyst, provide a focused cross-verification analysis for {company_name} ({ticker}) that complements our existing research.

Company Context:
- Name: {company_name}
- Sector: {info.get('sector', 'N/A')}
- Industry: {info.get('industry', 'N/A')}
- Business: {info.get('longBusinessSummary', 'N/A')[:800]}

Social Media Intelligence Summary:
- Overall Sentiment: {social_analysis.get('sentiment_analysis', {}).get('overall_sentiment', 'neutral')}
- Discussion Volume: {social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0)} discussions
- Key Themes: {', '.join(social_analysis.get('sentiment_analysis', {}).get('key_themes', [])[:3])}
- Bullish Signals: {', '.join(social_analysis.get('sentiment_analysis', {}).get('bullish_signals', [])[:3])}
- Risk Signals: {', '.join(social_analysis.get('sentiment_analysis', {}).get('bearish_signals', [])[:3])}

Provide analysis in the following areas that adds unique value and cross-verification:

## 🔍 Alternative Perspective Analysis
- What alternative viewpoints might challenge the mainstream narrative about this company?
- Are there overlooked risks or opportunities that social sentiment might be missing?
- How do different stakeholder groups (retail vs institutional) view this company?

## 📊 Market Positioning Verification
- How does this company's competitive position align with social media discussion themes?
- Are the social media "bullish signals" supported by fundamental business strengths?
- Do the "risk signals" represent real business concerns or short-term market noise?

## 🎯 Investment Thesis Stress Testing
- What are the key assumptions underlying the bull case that need verification?
- Which risk factors could most significantly impact the investment thesis?
- How resilient is the business model under different economic scenarios?

## 🔮 Forward-Looking Insights
- What emerging trends or catalysts might not be fully reflected in current discussions?
- How might regulatory, technological, or competitive changes affect this company?
- What should long-term investors monitor most closely?

## ⚖️ Balanced Recommendation Framework
- Synthesize the investment attractiveness considering both quantitative factors and social sentiment
- What type of investor profile would this company best suit?
- What are the key monitoring metrics for ongoing investment decisions?

Focus on providing insights that complement rather than repeat the fundamental analysis. Be objective, balanced, and specific. Respond in Japanese with 1500+ characters for each section.
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in OpenAI cross-verification for {ticker}: {e}")
            return f"OpenAI分析でエラーが発生しました: {str(e)}"
    
    def _synthesize_comprehensive_report(self, ticker: str, company_name: str, info: Dict, 
                                       social_analysis: Dict, gemini_analysis: str, 
                                       openai_analysis: str) -> Dict[str, Any]:
        """
        Synthesize all analyses into a comprehensive final report
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        company_name : str
            Company name
        info : Dict
            Yahoo Finance company info
        social_analysis : Dict
            Twitter sentiment analysis
        gemini_analysis : str
            Gemini fundamental analysis
        openai_analysis : str
            OpenAI cross-verification analysis
            
        Returns:
        --------
        Dict[str, Any]
            Comprehensive synthesized report
        """
        return {
            'report_metadata': {
                'ticker': ticker,
                'company_name': company_name,
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'analysis_timestamp': social_analysis.get('analysis_date'),
                'data_sources': ['Yahoo Finance', 'Twitter API', 'Gemini AI', 'OpenAI GPT-4o'],
                'report_type': 'Comprehensive Multi-Source Due Diligence'
            },
            
            'executive_summary': {
                'social_sentiment_score': social_analysis.get('social_media_score', 50),
                'discussion_volume': social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0),
                'key_themes': social_analysis.get('sentiment_analysis', {}).get('key_themes', []),
                'primary_opportunities': social_analysis.get('opportunity_signals', [])[:3],
                'primary_risks': social_analysis.get('risk_signals', [])[:3]
            },
            
            'social_media_intelligence': {
                'sentiment_analysis': social_analysis.get('sentiment_analysis', {}),
                'institutional_insights': social_analysis.get('institutional_insights', {}),
                'key_findings': social_analysis.get('key_findings', []),
                'data_quality_score': min(100, social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0) * 2)
            },
            
            'fundamental_analysis': {
                'source': 'Gemini AI with Social Media Integration',
                'analysis_type': 'Comprehensive Qualitative Due Diligence',
                'report_content': gemini_analysis,
                'integrated_social_insights': True
            },
            
            'cross_verification_analysis': {
                'source': 'OpenAI GPT-4o',
                'analysis_type': 'Alternative Perspective & Stress Testing',
                'report_content': openai_analysis,
                'focus_areas': ['Alternative Perspectives', 'Thesis Stress Testing', 'Forward-Looking Insights']
            },
            
            'investment_grade_assessment': self._calculate_investment_grade(social_analysis, info),
            
            'data_confidence_metrics': {
                'social_data_volume': social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0),
                'institutional_discussion_count': len(social_analysis.get('institutional_insights', {}).get('insights', [])),
                'analysis_comprehensiveness': 'High' if len(gemini_analysis) > 5000 else 'Medium',
                'multi_source_verification': True
            }
        }
    
    def _calculate_investment_grade(self, social_analysis: Dict, info: Dict) -> Dict[str, Any]:
        """Calculate overall investment grade based on multiple factors"""
        sentiment_score = social_analysis.get('social_media_score', 50)
        discussion_volume = social_analysis.get('sentiment_analysis', {}).get('tweet_count', 0)
        
        # Calculate grade based on multiple factors
        volume_score = min(100, discussion_volume * 5)  # More discussion = higher interest
        sentiment_weight = 0.4
        volume_weight = 0.3
        diversification_weight = 0.3
        
        # Company size factor
        market_cap = info.get('marketCap', 0)
        size_factor = 1.0
        if market_cap > 100e9:  # Large cap
            size_factor = 1.1
        elif market_cap < 1e9:  # Small cap
            size_factor = 0.9
        
        overall_score = (sentiment_score * sentiment_weight + 
                        volume_score * volume_weight + 
                        50 * diversification_weight) * size_factor
        
        # Determine grade
        if overall_score >= 80:
            grade = 'A'
            grade_description = 'Strong Investment Interest'
        elif overall_score >= 65:
            grade = 'B'
            grade_description = 'Positive Investment Sentiment'
        elif overall_score >= 50:
            grade = 'C'
            grade_description = 'Neutral Investment Outlook'
        elif overall_score >= 35:
            grade = 'D'
            grade_description = 'Below Average Interest'
        else:
            grade = 'F'
            grade_description = 'Poor Investment Sentiment'
        
        return {
            'overall_grade': grade,
            'numeric_score': round(overall_score, 1),
            'grade_description': grade_description,
            'sentiment_component': round(sentiment_score, 1),
            'volume_component': round(volume_score, 1),
            'size_adjustment': size_factor
        }
    
    def _create_error_report(self, ticker: str, error_message: str) -> Dict[str, Any]:
        """Create error report when analysis fails"""
        return {
            'report_metadata': {
                'ticker': ticker,
                'status': 'error',
                'error_message': error_message,
                'data_sources': ['Error Handler']
            },
            'error_details': {
                'message': f"包括的な分析中にエラーが発生しました: {error_message}",
                'recommendation': "しばらく待ってから再試行してください。問題が続く場合は、ティッカーシンボルを確認してください。"
            }
        }

def get_comprehensive_due_diligence_report(ticker: str) -> Dict[str, Any]:
    """
    Main function to get comprehensive due diligence report
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
        
    Returns:
    --------
    Dict[str, Any]
        Comprehensive due diligence report
    """
    analyzer = ComprehensiveDueDiligenceAnalyzer()
    return analyzer.generate_comprehensive_due_diligence_report(ticker)