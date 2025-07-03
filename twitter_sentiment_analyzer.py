"""
Twitter Sentiment Analysis for Stock Due Diligence
Integrates social media insights with Gemini and OpenAI analysis
"""

import tweepy
import pandas as pd
import re
import logging
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterDueDiligenceAnalyzer:
    """
    Comprehensive Twitter analysis for stock due diligence research
    """
    
    def __init__(self):
        """Initialize Twitter API client with authentication"""
        try:
            # Twitter API v2 Bearer Token authentication
            self.client = tweepy.Client(
                consumer_key=os.environ.get("TWITTER_API_KEY", "vRfP0OgECWCn6GgF9vnLLgOPV"),
                consumer_secret=os.environ.get("TWITTER_API_SECRET", "4YbOl1l1aeCgIsxatY9PSumJ8Q5iByFnvpSzC1xz14wOvVaUvT"),
                wait_on_rate_limit=True
            )
            
            self.vader_analyzer = SentimentIntensityAnalyzer()
            logger.info("Twitter API client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            self.client = None
    
    def search_stock_discussions(self, ticker: str, company_name: str, days_back: int = 7) -> List[Dict]:
        """
        Search for relevant stock discussions and due diligence content
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        company_name : str
            Company name for broader search
        days_back : int
            Number of days to search back
            
        Returns:
        --------
        List[Dict]
            List of relevant tweets with metadata
        """
        if not self.client:
            logger.warning("Twitter API not available")
            return []
        
        try:
            # Build comprehensive search query for due diligence content
            search_queries = [
                f"${ticker} due diligence OR analysis OR research",
                f"${ticker} fundamentals OR valuation OR investment",
                f'"{company_name}" financial analysis OR DD',
                f"${ticker} bullish OR bearish thesis",
                f"${ticker} competitive advantage OR moat",
                f'"{company_name}" revenue OR earnings OR growth'
            ]
            
            all_tweets = []
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days_back)
            
            for query in search_queries:
                try:
                    tweets = tweepy.Paginator(
                        self.client.search_recent_tweets,
                        query=query,
                        tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations'],
                        user_fields=['username', 'verified', 'public_metrics'],
                        expansions=['author_id'],
                        start_time=start_time,
                        end_time=end_time,
                        max_results=50
                    ).flatten(limit=100)
                    
                    for tweet in tweets:
                        # Filter for quality content (longer, more engagement)
                        if len(tweet.text) > 100 and tweet.public_metrics['like_count'] > 1:
                            all_tweets.append({
                                'id': tweet.id,
                                'text': self.clean_tweet_text(tweet.text),
                                'created_at': tweet.created_at,
                                'likes': tweet.public_metrics['like_count'],
                                'retweets': tweet.public_metrics['retweet_count'],
                                'replies': tweet.public_metrics['reply_count'],
                                'author_id': tweet.author_id,
                                'query_type': query
                            })
                    
                    # Rate limiting protection
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Search query failed: {query} - {e}")
                    continue
            
            # Remove duplicates and sort by engagement
            unique_tweets = {tweet['id']: tweet for tweet in all_tweets}.values()
            sorted_tweets = sorted(unique_tweets, 
                                 key=lambda x: x['likes'] + x['retweets'] * 2, 
                                 reverse=True)
            
            logger.info(f"Found {len(sorted_tweets)} relevant tweets for {ticker}")
            return list(sorted_tweets)[:50]  # Return top 50 most engaged tweets
            
        except Exception as e:
            logger.error(f"Error searching Twitter for {ticker}: {e}")
            return []
    
    def clean_tweet_text(self, text: str) -> str:
        """Clean and normalize tweet text"""
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Remove Twitter handles and hashtags for cleaner analysis
        text = re.sub(r'@\w+|#\w+', '', text)
        return text.strip()
    
    def analyze_sentiment_trends(self, tweets: List[Dict]) -> Dict:
        """
        Analyze sentiment trends from tweets using multiple methods
        
        Parameters:
        -----------
        tweets : List[Dict]
            List of tweet data
            
        Returns:
        --------
        Dict
            Comprehensive sentiment analysis results
        """
        if not tweets:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'confidence': 0.0,
                'tweet_count': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
                'key_themes': [],
                'top_concerns': [],
                'bullish_signals': [],
                'bearish_signals': []
            }
        
        sentiments = []
        themes = []
        concerns = []
        bullish_signals = []
        bearish_signals = []
        
        for tweet in tweets:
            text = tweet['text']
            
            # VADER sentiment analysis
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_polarity = blob.sentiment.polarity
            
            # Combined sentiment score (weighted average)
            combined_score = (vader_scores['compound'] + textblob_polarity) / 2
            sentiments.append(combined_score)
            
            # Extract themes and concerns
            self._extract_themes_and_signals(text, themes, concerns, bullish_signals, bearish_signals)
        
        # Calculate overall metrics
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        # Classify sentiment distribution
        positive_count = sum(1 for s in sentiments if s > 0.1)
        negative_count = sum(1 for s in sentiments if s < -0.1)
        neutral_count = len(sentiments) - positive_count - negative_count
        
        # Determine overall sentiment
        if avg_sentiment > 0.2:
            overall_sentiment = 'positive'
        elif avg_sentiment < -0.2:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'sentiment_score': avg_sentiment,
            'confidence': abs(avg_sentiment),
            'tweet_count': len(tweets),
            'sentiment_distribution': {
                'positive': positive_count,
                'neutral': neutral_count,
                'negative': negative_count
            },
            'key_themes': self._get_top_themes(themes),
            'top_concerns': self._get_top_themes(concerns),
            'bullish_signals': self._get_top_themes(bullish_signals),
            'bearish_signals': self._get_top_themes(bearish_signals)
        }
    
    def _extract_themes_and_signals(self, text: str, themes: List, concerns: List, 
                                   bullish_signals: List, bearish_signals: List):
        """Extract investment themes and signals from tweet text"""
        text_lower = text.lower()
        
        # Bullish keywords and phrases
        bullish_keywords = [
            'strong fundamentals', 'great earnings', 'beat estimates', 'revenue growth',
            'expanding market', 'competitive advantage', 'undervalued', 'strong moat',
            'innovation', 'market leader', 'growing demand', 'excellent management'
        ]
        
        # Bearish keywords and phrases
        bearish_keywords = [
            'overvalued', 'declining revenue', 'missed estimates', 'competition threat',
            'regulatory risk', 'high debt', 'management issues', 'market saturation',
            'losing market share', 'weak fundamentals', 'accounting concerns'
        ]
        
        # Key investment themes
        theme_keywords = [
            'digital transformation', 'ai artificial intelligence', 'electric vehicle',
            'renewable energy', 'fintech', 'cloud computing', 'subscription model',
            'vertical integration', 'platform business', 'network effects'
        ]
        
        for keyword in bullish_keywords:
            if keyword in text_lower:
                bullish_signals.append(keyword)
        
        for keyword in bearish_keywords:
            if keyword in text_lower:
                bearish_signals.append(keyword)
        
        for keyword in theme_keywords:
            if keyword in text_lower:
                themes.append(keyword)
        
        # Extract concerns (risk-related keywords)
        concern_keywords = [
            'regulation', 'lawsuit', 'investigation', 'debt', 'competition',
            'market risk', 'economic downturn', 'supply chain'
        ]
        
        for keyword in concern_keywords:
            if keyword in text_lower:
                concerns.append(keyword)
    
    def _get_top_themes(self, themes_list: List, top_n: int = 5) -> List[str]:
        """Get top themes by frequency"""
        if not themes_list:
            return []
        
        theme_counts = {}
        for theme in themes_list:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, count in sorted_themes[:top_n]]
    
    def get_institutional_discussions(self, ticker: str, company_name: str) -> Dict:
        """
        Search for institutional-quality discussions and analysis
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        company_name : str
            Company name
            
        Returns:
        --------
        Dict
            Institutional-quality insights and analysis
        """
        if not self.client:
            return {'insights': [], 'analyst_opinions': [], 'institutional_signals': []}
        
        try:
            # Search for high-quality analysis from verified accounts or finance professionals
            institutional_queries = [
                f"${ticker} analysis from:verified_finance_accounts",
                f'"{company_name}" thesis OR investment case',
                f"${ticker} institutional OR hedge fund OR analyst",
                f"${ticker} DCF OR valuation model OR price target"
            ]
            
            insights = []
            analyst_opinions = []
            institutional_signals = []
            
            for query in institutional_queries:
                try:
                    tweets = self.client.search_recent_tweets(
                        query=query,
                        tweet_fields=['created_at', 'author_id', 'public_metrics'],
                        max_results=20
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data:
                            # Filter for high-quality content
                            if (len(tweet.text) > 200 and 
                                tweet.public_metrics['like_count'] > 5):
                                
                                cleaned_text = self.clean_tweet_text(tweet.text)
                                
                                if 'analyst' in cleaned_text.lower() or 'target' in cleaned_text.lower():
                                    analyst_opinions.append(cleaned_text)
                                elif 'institutional' in cleaned_text.lower() or 'hedge fund' in cleaned_text.lower():
                                    institutional_signals.append(cleaned_text)
                                else:
                                    insights.append(cleaned_text)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Institutional search failed for query: {query} - {e}")
                    continue
            
            return {
                'insights': insights[:10],
                'analyst_opinions': analyst_opinions[:5],
                'institutional_signals': institutional_signals[:5]
            }
            
        except Exception as e:
            logger.error(f"Error getting institutional discussions for {ticker}: {e}")
            return {'insights': [], 'analyst_opinions': [], 'institutional_signals': []}
    
    def generate_social_due_diligence_summary(self, ticker: str, company_name: str) -> Dict:
        """
        Generate comprehensive social media due diligence summary
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        company_name : str
            Company name
            
        Returns:
        --------
        Dict
            Comprehensive social media analysis for due diligence
        """
        logger.info(f"Starting social media due diligence analysis for {ticker}")
        
        # Search for relevant discussions
        tweets = self.search_stock_discussions(ticker, company_name)
        
        # Analyze sentiment trends
        sentiment_analysis = self.analyze_sentiment_trends(tweets)
        
        # Get institutional-quality discussions
        institutional_analysis = self.get_institutional_discussions(ticker, company_name)
        
        # Compile comprehensive summary
        summary = {
            'ticker': ticker,
            'company_name': company_name,
            'analysis_date': datetime.utcnow().isoformat(),
            'data_sources': ['Twitter'],
            'sentiment_analysis': sentiment_analysis,
            'institutional_insights': institutional_analysis,
            'social_media_score': self._calculate_social_media_score(sentiment_analysis),
            'key_findings': self._generate_key_findings(sentiment_analysis, institutional_analysis),
            'risk_signals': sentiment_analysis.get('bearish_signals', []),
            'opportunity_signals': sentiment_analysis.get('bullish_signals', [])
        }
        
        logger.info(f"Completed social media analysis for {ticker}")
        return summary
    
    def _calculate_social_media_score(self, sentiment_analysis: Dict) -> float:
        """Calculate overall social media sentiment score (0-100)"""
        if sentiment_analysis['tweet_count'] == 0:
            return 50.0  # Neutral score when no data
        
        # Base score from sentiment
        sentiment_score = sentiment_analysis['sentiment_score']
        base_score = 50 + (sentiment_score * 25)  # Convert -1 to 1 range to 25-75
        
        # Adjust for confidence
        confidence = sentiment_analysis['confidence']
        adjusted_score = base_score + (confidence * 10)  # Add up to 10 points for high confidence
        
        # Ensure score is within 0-100 range
        return max(0, min(100, adjusted_score))
    
    def _generate_key_findings(self, sentiment_analysis: Dict, institutional_analysis: Dict) -> List[str]:
        """Generate key findings from social media analysis"""
        findings = []
        
        # Sentiment findings
        if sentiment_analysis['overall_sentiment'] == 'positive':
            findings.append(f"Social sentiment is positive with {sentiment_analysis['tweet_count']} discussions analyzed")
        elif sentiment_analysis['overall_sentiment'] == 'negative':
            findings.append(f"Social sentiment shows concerns with {sentiment_analysis['tweet_count']} discussions analyzed")
        else:
            findings.append(f"Social sentiment is neutral across {sentiment_analysis['tweet_count']} discussions")
        
        # Theme findings
        if sentiment_analysis['key_themes']:
            findings.append(f"Key investment themes: {', '.join(sentiment_analysis['key_themes'][:3])}")
        
        # Risk findings
        if sentiment_analysis['top_concerns']:
            findings.append(f"Main concerns discussed: {', '.join(sentiment_analysis['top_concerns'][:3])}")
        
        # Institutional findings
        if institutional_analysis['analyst_opinions']:
            findings.append(f"Found {len(institutional_analysis['analyst_opinions'])} analyst-related discussions")
        
        if institutional_analysis['institutional_signals']:
            findings.append(f"Identified {len(institutional_analysis['institutional_signals'])} institutional investor signals")
        
        return findings