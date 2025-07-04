"""
Stock Universe Updater - Ensures all discovered stocks are searchable throughout the platform
"""
import pickle
import os
from datetime import datetime

class StockUniverseUpdater:
    def __init__(self):
        self.stock_universe_file = "discovered_stocks_universe.pkl"
        self.discovered_stocks = self.load_discovered_stocks()
    
    def load_discovered_stocks(self):
        """Load previously discovered stocks from file"""
        try:
            if os.path.exists(self.stock_universe_file):
                with open(self.stock_universe_file, 'rb') as f:
                    return pickle.load(f)
            return {}
        except Exception:
            return {}
    
    def save_discovered_stocks(self):
        """Save discovered stocks to file"""
        try:
            with open(self.stock_universe_file, 'wb') as f:
                pickle.dump(self.discovered_stocks, f)
        except Exception:
            pass
    
    def add_discovered_stocks(self, stock_list):
        """Add newly discovered stocks to the universe"""
        for stock in stock_list:
            ticker = stock.get('ticker', '').upper()
            if ticker and ticker not in self.discovered_stocks:
                self.discovered_stocks[ticker] = {
                    'name': stock.get('name', ticker),
                    'sector': stock.get('sector', 'Unknown'),
                    'description': stock.get('description', ''),
                    'market_cap': stock.get('market_cap', 0),
                    'discovered_date': datetime.now().isoformat(),
                    'category': self._categorize_stock(stock)
                }
        
        self.save_discovered_stocks()
    
    def _categorize_stock(self, stock):
        """Categorize stock based on market cap and sector"""
        market_cap = stock.get('market_cap', 0)
        sector = stock.get('sector', 'Unknown')
        
        if market_cap > 200000:  # >200B
            return "Large Cap"
        elif market_cap > 10000:  # 10B-200B
            return "Mid Cap"
        elif market_cap > 2000:  # 2B-10B
            return "Small Cap"
        else:
            return "Micro Cap"
    
    def get_all_discovered_stocks(self):
        """Get all discovered stocks in format compatible with comprehensive_stock_data"""
        return self.discovered_stocks
    
    def search_discovered_stocks(self, query):
        """Search discovered stocks by name or ticker"""
        query = query.lower()
        results = []
        
        for ticker, info in self.discovered_stocks.items():
            if (query in ticker.lower() or 
                query in info['name'].lower() or 
                query in info.get('description', '').lower()):
                results.append({
                    'ticker': ticker,
                    'name': info['name'],
                    'sector': info['sector'],
                    'category': info['category']
                })
        
        return results

# Global instance
stock_universe_updater = StockUniverseUpdater()

def update_stock_universe_with_discoveries(discovered_stocks):
    """Function to be called from stock discovery to update universe"""
    stock_universe_updater.add_discovered_stocks(discovered_stocks)

def search_all_stocks_including_discovered(query):
    """Enhanced search that includes discovered stocks"""
    from comprehensive_stock_data import search_stocks_by_name
    
    # Search traditional database
    traditional_results = search_stocks_by_name(query)
    
    # Search discovered stocks
    discovered_results = stock_universe_updater.search_discovered_stocks(query)
    
    # Combine and deduplicate
    all_results = traditional_results.copy()
    existing_tickers = {stock['ticker'] for stock in traditional_results}
    
    for stock in discovered_results:
        if stock['ticker'] not in existing_tickers:
            all_results.append(stock)
    
    return all_results

def get_total_stock_count():
    """Get total count of all searchable stocks"""
    from comprehensive_stock_data import get_all_tickers
    traditional_count = len(get_all_tickers())
    discovered_count = len(stock_universe_updater.discovered_stocks)
    return traditional_count + discovered_count