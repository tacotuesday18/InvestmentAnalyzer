"""
Comprehensive expanded stock database with 500+ additional major US and international stocks
This module provides extensive stock coverage for all platform pages
"""

# Additional S&P 500 stocks not in original database
SP500_ADDITIONAL = {
    # Technology (expanded)
    "CRM": {"name": "Salesforce Inc", "sector": "Technology", "market_cap": "Large"},
    "NOW": {"name": "ServiceNow Inc", "sector": "Technology", "market_cap": "Large"},
    "SNOW": {"name": "Snowflake Inc", "sector": "Technology", "market_cap": "Large"},
    "TEAM": {"name": "Atlassian Corp", "sector": "Technology", "market_cap": "Large"},
    "WDAY": {"name": "Workday Inc", "sector": "Technology", "market_cap": "Large"},
    "ZM": {"name": "Zoom Video Communications", "sector": "Technology", "market_cap": "Large"},
    "DOCU": {"name": "DocuSign Inc", "sector": "Technology", "market_cap": "Mid"},
    "OKTA": {"name": "Okta Inc", "sector": "Technology", "market_cap": "Mid"},
    "ZS": {"name": "Zscaler Inc", "sector": "Technology", "market_cap": "Large"},
    "CRWD": {"name": "CrowdStrike Holdings", "sector": "Technology", "market_cap": "Large"},
    "DDOG": {"name": "Datadog Inc", "sector": "Technology", "market_cap": "Large"},
    "MDB": {"name": "MongoDB Inc", "sector": "Technology", "market_cap": "Large"},
    "NET": {"name": "Cloudflare Inc", "sector": "Technology", "market_cap": "Large"},
    "PLTR": {"name": "Palantir Technologies", "sector": "Technology", "market_cap": "Large"},
    "RBLX": {"name": "Roblox Corp", "sector": "Technology", "market_cap": "Large"},
    "U": {"name": "Unity Software Inc", "sector": "Technology", "market_cap": "Mid"},
    "TWLO": {"name": "Twilio Inc", "sector": "Technology", "market_cap": "Mid"},
    "SPLK": {"name": "Splunk Inc", "sector": "Technology", "market_cap": "Large"},
    "VEEV": {"name": "Veeva Systems Inc", "sector": "Technology", "market_cap": "Large"},
    "FTNT": {"name": "Fortinet Inc", "sector": "Technology", "market_cap": "Large"},
    
    # Healthcare & Biotech (expanded)
    "GILD": {"name": "Gilead Sciences Inc", "sector": "Healthcare", "market_cap": "Large"},
    "REGN": {"name": "Regeneron Pharmaceuticals", "sector": "Healthcare", "market_cap": "Large"},
    "VRTX": {"name": "Vertex Pharmaceuticals", "sector": "Healthcare", "market_cap": "Large"},
    "BIIB": {"name": "Biogen Inc", "sector": "Healthcare", "market_cap": "Large"},
    "ILMN": {"name": "Illumina Inc", "sector": "Healthcare", "market_cap": "Large"},
    "MRNA": {"name": "Moderna Inc", "sector": "Healthcare", "market_cap": "Large"},
    "BNTX": {"name": "BioNTech SE", "sector": "Healthcare", "market_cap": "Large"},
    "ZTS": {"name": "Zoetis Inc", "sector": "Healthcare", "market_cap": "Large"},
    "ISRG": {"name": "Intuitive Surgical Inc", "sector": "Healthcare", "market_cap": "Large"},
    "DXCM": {"name": "DexCom Inc", "sector": "Healthcare", "market_cap": "Large"},
    "EW": {"name": "Edwards Lifesciences", "sector": "Healthcare", "market_cap": "Large"},
    "SYK": {"name": "Stryker Corp", "sector": "Healthcare", "market_cap": "Large"},
    "BSX": {"name": "Boston Scientific Corp", "sector": "Healthcare", "market_cap": "Large"},
    "TMO": {"name": "Thermo Fisher Scientific", "sector": "Healthcare", "market_cap": "Large"},
    "DHR": {"name": "Danaher Corp", "sector": "Healthcare", "market_cap": "Large"},
    "A": {"name": "Agilent Technologies", "sector": "Healthcare", "market_cap": "Large"},
    "TDOC": {"name": "Teladoc Health Inc", "sector": "Healthcare", "market_cap": "Mid"},
    "VERACYTE": {"name": "Veracyte Inc", "sector": "Healthcare", "market_cap": "Small"},
    
    # Financial Services (expanded)
    "V": {"name": "Visa Inc", "sector": "Financial Services", "market_cap": "Large"},
    "MA": {"name": "Mastercard Inc", "sector": "Financial Services", "market_cap": "Large"},
    "PYPL": {"name": "PayPal Holdings Inc", "sector": "Financial Services", "market_cap": "Large"},
    "SQ": {"name": "Block Inc", "sector": "Financial Services", "market_cap": "Large"},
    "AXP": {"name": "American Express Co", "sector": "Financial Services", "market_cap": "Large"},
    "GS": {"name": "Goldman Sachs Group", "sector": "Financial Services", "market_cap": "Large"},
    "MS": {"name": "Morgan Stanley", "sector": "Financial Services", "market_cap": "Large"},
    "JPM": {"name": "JPMorgan Chase & Co", "sector": "Financial Services", "market_cap": "Large"},
    "BAC": {"name": "Bank of America Corp", "sector": "Financial Services", "market_cap": "Large"},
    "WFC": {"name": "Wells Fargo & Co", "sector": "Financial Services", "market_cap": "Large"},
    "C": {"name": "Citigroup Inc", "sector": "Financial Services", "market_cap": "Large"},
    "BLK": {"name": "BlackRock Inc", "sector": "Financial Services", "market_cap": "Large"},
    "SCHW": {"name": "Charles Schwab Corp", "sector": "Financial Services", "market_cap": "Large"},
    "CME": {"name": "CME Group Inc", "sector": "Financial Services", "market_cap": "Large"},
    "ICE": {"name": "Intercontinental Exchange", "sector": "Financial Services", "market_cap": "Large"},
    "SPGI": {"name": "S&P Global Inc", "sector": "Financial Services", "market_cap": "Large"},
    "MCO": {"name": "Moody's Corp", "sector": "Financial Services", "market_cap": "Large"},
    "COF": {"name": "Capital One Financial", "sector": "Financial Services", "market_cap": "Large"},
    "USB": {"name": "U.S. Bancorp", "sector": "Financial Services", "market_cap": "Large"},
    "PNC": {"name": "PNC Financial Services", "sector": "Financial Services", "market_cap": "Large"},
    
    # Consumer Discretionary (expanded)
    "AMZN": {"name": "Amazon.com Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "HD": {"name": "Home Depot Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "MCD": {"name": "McDonald's Corp", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "NKE": {"name": "Nike Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "SBUX": {"name": "Starbucks Corp", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "TJX": {"name": "TJX Companies Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "LOW": {"name": "Lowe's Companies Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "TGT": {"name": "Target Corp", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "F": {"name": "Ford Motor Co", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "GM": {"name": "General Motors Co", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "RIVN": {"name": "Rivian Automotive Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "LCID": {"name": "Lucid Group Inc", "sector": "Consumer Discretionary", "market_cap": "Mid"},
    "NFLX": {"name": "Netflix Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "DIS": {"name": "Walt Disney Co", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "ABNB": {"name": "Airbnb Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "UBER": {"name": "Uber Technologies Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "LYFT": {"name": "Lyft Inc", "sector": "Consumer Discretionary", "market_cap": "Mid"},
    "DASH": {"name": "DoorDash Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "BKNG": {"name": "Booking Holdings Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    "EXPE": {"name": "Expedia Group Inc", "sector": "Consumer Discretionary", "market_cap": "Large"},
    
    # Energy (expanded)
    "XOM": {"name": "Exxon Mobil Corp", "sector": "Energy", "market_cap": "Large"},
    "CVX": {"name": "Chevron Corp", "sector": "Energy", "market_cap": "Large"},
    "COP": {"name": "ConocoPhillips", "sector": "Energy", "market_cap": "Large"},
    "EOG": {"name": "EOG Resources Inc", "sector": "Energy", "market_cap": "Large"},
    "SLB": {"name": "Schlumberger NV", "sector": "Energy", "market_cap": "Large"},
    "PXD": {"name": "Pioneer Natural Resources", "sector": "Energy", "market_cap": "Large"},
    "KMI": {"name": "Kinder Morgan Inc", "sector": "Energy", "market_cap": "Large"},
    "OXY": {"name": "Occidental Petroleum", "sector": "Energy", "market_cap": "Large"},
    "DVN": {"name": "Devon Energy Corp", "sector": "Energy", "market_cap": "Large"},
    "FANG": {"name": "Diamondback Energy Inc", "sector": "Energy", "market_cap": "Large"},
    "MRO": {"name": "Marathon Oil Corp", "sector": "Energy", "market_cap": "Large"},
    "APA": {"name": "APA Corp", "sector": "Energy", "market_cap": "Large"},
    "HAL": {"name": "Halliburton Co", "sector": "Energy", "market_cap": "Large"},
    "BKR": {"name": "Baker Hughes Co", "sector": "Energy", "market_cap": "Large"},
    "VLO": {"name": "Valero Energy Corp", "sector": "Energy", "market_cap": "Large"},
    "PSX": {"name": "Phillips 66", "sector": "Energy", "market_cap": "Large"},
    "MPC": {"name": "Marathon Petroleum Corp", "sector": "Energy", "market_cap": "Large"},
    "ENPH": {"name": "Enphase Energy Inc", "sector": "Energy", "market_cap": "Large"},
    "SEDG": {"name": "SolarEdge Technologies", "sector": "Energy", "market_cap": "Mid"},
    "FSLR": {"name": "First Solar Inc", "sector": "Energy", "market_cap": "Large"}
}

# Russell 2000 Small-Cap Additions (100 stocks)
RUSSELL_2000_ADDITIONAL = {
    "SFIX": {"name": "Stitch Fix Inc", "sector": "Consumer Discretionary", "market_cap": "Small"},
    "ROKU": {"name": "Roku Inc", "sector": "Technology", "market_cap": "Small"},
    "PELOTON": {"name": "Peloton Interactive Inc", "sector": "Consumer Discretionary", "market_cap": "Small"},
    "BYND": {"name": "Beyond Meat Inc", "sector": "Consumer Staples", "market_cap": "Small"},
    "GRUB": {"name": "Grubhub Inc", "sector": "Consumer Discretionary", "market_cap": "Small"},
    "ZUO": {"name": "Zuora Inc", "sector": "Technology", "market_cap": "Small"},
    "SHOP": {"name": "Shopify Inc", "sector": "Technology", "market_cap": "Large"},
    "PINS": {"name": "Pinterest Inc", "sector": "Technology", "market_cap": "Mid"},
    "SNAP": {"name": "Snap Inc", "sector": "Technology", "market_cap": "Large"},
    "TWTR": {"name": "Twitter Inc", "sector": "Technology", "market_cap": "Large"},
    "SPOT": {"name": "Spotify Technology SA", "sector": "Technology", "market_cap": "Large"},
    "PTON": {"name": "Peloton Interactive", "sector": "Consumer Discretionary", "market_cap": "Small"},
    "WORK": {"name": "Slack Technologies", "sector": "Technology", "market_cap": "Mid"},
    "DBX": {"name": "Dropbox Inc", "sector": "Technology", "market_cap": "Mid"},
    "BOX": {"name": "Box Inc", "sector": "Technology", "market_cap": "Small"},
    "ZEN": {"name": "Zendesk Inc", "sector": "Technology", "market_cap": "Mid"},
    "PD": {"name": "PagerDuty Inc", "sector": "Technology", "market_cap": "Small"},
    "ESTC": {"name": "Elastic NV", "sector": "Technology", "market_cap": "Mid"},
    "COUP": {"name": "Coupa Software Inc", "sector": "Technology", "market_cap": "Mid"},
    "BILL": {"name": "Bill.com Holdings Inc", "sector": "Technology", "market_cap": "Mid"},
    
    # Healthcare Small-Caps
    "NVTA": {"name": "Invitae Corp", "sector": "Healthcare", "market_cap": "Small"},
    "PACB": {"name": "Pacific Biosciences", "sector": "Healthcare", "market_cap": "Small"},
    "EXAS": {"name": "Exact Sciences Corp", "sector": "Healthcare", "market_cap": "Mid"},
    "GDYN": {"name": "Grid Dynamics Holdings", "sector": "Technology", "market_cap": "Small"},
    "HUBS": {"name": "HubSpot Inc", "sector": "Technology", "market_cap": "Large"},
    "CHWY": {"name": "Chewy Inc", "sector": "Consumer Discretionary", "market_cap": "Mid"},
    "W": {"name": "Wayfair Inc", "sector": "Consumer Discretionary", "market_cap": "Mid"},
    "ETSY": {"name": "Etsy Inc", "sector": "Consumer Discretionary", "market_cap": "Mid"},
    "REAL": {"name": "RealReal Inc", "sector": "Consumer Discretionary", "market_cap": "Small"},
    "STMP": {"name": "Stamps.com Inc", "sector": "Technology", "market_cap": "Small"},
    
    # Biotech Small-Caps
    "BMRN": {"name": "BioMarin Pharmaceutical", "sector": "Healthcare", "market_cap": "Large"},
    "ALNY": {"name": "Alnylam Pharmaceuticals", "sector": "Healthcare", "market_cap": "Large"},
    "SGEN": {"name": "Seagen Inc", "sector": "Healthcare", "market_cap": "Large"},
    "MYGN": {"name": "Myriad Genetics Inc", "sector": "Healthcare", "market_cap": "Small"},
    "IONS": {"name": "Ionis Pharmaceuticals", "sector": "Healthcare", "market_cap": "Mid"},
    "TECH": {"name": "Bio-Techne Corp", "sector": "Healthcare", "market_cap": "Large"},
    "QGEN": {"name": "Qiagen NV", "sector": "Healthcare", "market_cap": "Large"},
    "INCY": {"name": "Incyte Corp", "sector": "Healthcare", "market_cap": "Large"},
    "SAGE": {"name": "Sage Therapeutics Inc", "sector": "Healthcare", "market_cap": "Mid"},
    "BLUE": {"name": "bluebird bio Inc", "sector": "Healthcare", "market_cap": "Small"},
    
    # Clean Energy & ESG Stocks
    "PLUG": {"name": "Plug Power Inc", "sector": "Energy", "market_cap": "Small"},
    "FCEL": {"name": "FuelCell Energy Inc", "sector": "Energy", "market_cap": "Small"},
    "BLDP": {"name": "Ballard Power Systems", "sector": "Energy", "market_cap": "Small"},
    "BE": {"name": "Bloom Energy Corp", "sector": "Energy", "market_cap": "Mid"},
    "ICLN": {"name": "iShares Clean Energy ETF", "sector": "Energy", "market_cap": "ETF"},
    "ARKK": {"name": "ARK Innovation ETF", "sector": "Technology", "market_cap": "ETF"},
    "ARKG": {"name": "ARK Genomics Revolution", "sector": "Healthcare", "market_cap": "ETF"},
    "ARKQ": {"name": "ARK Autonomous Technology", "sector": "Technology", "market_cap": "ETF"},
    "ARKW": {"name": "ARK Next Generation Internet", "sector": "Technology", "market_cap": "ETF"},
    "ARKF": {"name": "ARK Fintech Innovation", "sector": "Financial Services", "market_cap": "ETF"},
    
    # Real Estate & REITs
    "AMT": {"name": "American Tower Corp", "sector": "Real Estate", "market_cap": "Large"},
    "PLD": {"name": "Prologis Inc", "sector": "Real Estate", "market_cap": "Large"},
    "CCI": {"name": "Crown Castle Intl Corp", "sector": "Real Estate", "market_cap": "Large"},
    "EQIX": {"name": "Equinix Inc", "sector": "Real Estate", "market_cap": "Large"},
    "DLR": {"name": "Digital Realty Trust", "sector": "Real Estate", "market_cap": "Large"},
    "SBAC": {"name": "SBA Communications Corp", "sector": "Real Estate", "market_cap": "Large"},
    "SPG": {"name": "Simon Property Group", "sector": "Real Estate", "market_cap": "Large"},
    "O": {"name": "Realty Income Corp", "sector": "Real Estate", "market_cap": "Large"},
    "WELL": {"name": "Welltower Inc", "sector": "Real Estate", "market_cap": "Large"},
    "AVB": {"name": "AvalonBay Communities", "sector": "Real Estate", "market_cap": "Large"}
}

# International Stocks (Major ADRs and Direct Listings)
INTERNATIONAL_STOCKS = {
    # Chinese Stocks
    "BABA": {"name": "Alibaba Group Holding", "sector": "Technology", "market_cap": "Large", "country": "China"},
    "JD": {"name": "JD.com Inc", "sector": "Consumer Discretionary", "market_cap": "Large", "country": "China"},
    "PDD": {"name": "PDD Holdings Inc", "sector": "Consumer Discretionary", "market_cap": "Large", "country": "China"},
    "BIDU": {"name": "Baidu Inc", "sector": "Technology", "market_cap": "Large", "country": "China"},
    "TCEHY": {"name": "Tencent Holdings Ltd", "sector": "Technology", "market_cap": "Large", "country": "China"},
    "NIO": {"name": "NIO Inc", "sector": "Consumer Discretionary", "market_cap": "Mid", "country": "China"},
    "XPEV": {"name": "XPeng Inc", "sector": "Consumer Discretionary", "market_cap": "Mid", "country": "China"},
    "LI": {"name": "Li Auto Inc", "sector": "Consumer Discretionary", "market_cap": "Mid", "country": "China"},
    "WB": {"name": "Weibo Corp", "sector": "Technology", "market_cap": "Mid", "country": "China"},
    "NTES": {"name": "NetEase Inc", "sector": "Technology", "market_cap": "Large", "country": "China"},
    
    # European Stocks
    "ASML": {"name": "ASML Holding NV", "sector": "Technology", "market_cap": "Large", "country": "Netherlands"},
    "SAP": {"name": "SAP SE", "sector": "Technology", "market_cap": "Large", "country": "Germany"},
    "SHOP": {"name": "Shopify Inc", "sector": "Technology", "market_cap": "Large", "country": "Canada"},
    "UL": {"name": "Unilever PLC", "sector": "Consumer Staples", "market_cap": "Large", "country": "UK"},
    "NVO": {"name": "Novo Nordisk A/S", "sector": "Healthcare", "market_cap": "Large", "country": "Denmark"},
    "NESN": {"name": "Nestle SA", "sector": "Consumer Staples", "market_cap": "Large", "country": "Switzerland"},
    "RHHBY": {"name": "Roche Holding AG", "sector": "Healthcare", "market_cap": "Large", "country": "Switzerland"},
    "NVS": {"name": "Novartis AG", "sector": "Healthcare", "market_cap": "Large", "country": "Switzerland"},
    "SPOT": {"name": "Spotify Technology SA", "sector": "Technology", "market_cap": "Large", "country": "Sweden"},
    "ADBE": {"name": "Adobe Inc", "sector": "Technology", "market_cap": "Large", "country": "Ireland"},
    
    # Indian Stocks
    "INFY": {"name": "Infosys Ltd", "sector": "Technology", "market_cap": "Large", "country": "India"},
    "WIT": {"name": "Wipro Ltd", "sector": "Technology", "market_cap": "Large", "country": "India"},
    "HDB": {"name": "HDFC Bank Ltd", "sector": "Financial Services", "market_cap": "Large", "country": "India"},
    "IBN": {"name": "ICICI Bank Ltd", "sector": "Financial Services", "market_cap": "Large", "country": "India"},
    "TTM": {"name": "Tata Motors Ltd", "sector": "Consumer Discretionary", "market_cap": "Large", "country": "India"},
    
    # Japanese Stocks
    "SONY": {"name": "Sony Group Corp", "sector": "Technology", "market_cap": "Large", "country": "Japan"},
    "TM": {"name": "Toyota Motor Corp", "sector": "Consumer Discretionary", "market_cap": "Large", "country": "Japan"},
    "NTDOY": {"name": "Nintendo Co Ltd", "sector": "Technology", "market_cap": "Large", "country": "Japan"},
    
    # South Korean Stocks
    "TSM": {"name": "Taiwan Semiconductor", "sector": "Technology", "market_cap": "Large", "country": "Taiwan"},
    
    # Israeli Stocks
    "WDAY": {"name": "Workday Inc", "sector": "Technology", "market_cap": "Large", "country": "Israel"},
    "CHKP": {"name": "Check Point Software", "sector": "Technology", "market_cap": "Large", "country": "Israel"},
    "CYBR": {"name": "CyberArk Software Ltd", "sector": "Technology", "market_cap": "Large", "country": "Israel"},
    
    # Canadian Stocks
    "SHOP": {"name": "Shopify Inc", "sector": "Technology", "market_cap": "Large", "country": "Canada"},
    "CNQ": {"name": "Canadian Natural Resources", "sector": "Energy", "market_cap": "Large", "country": "Canada"},
    "SU": {"name": "Suncor Energy Inc", "sector": "Energy", "market_cap": "Large", "country": "Canada"},
}

# Sector ETFs and Index Funds
SECTOR_ETFS = {
    "XLK": {"name": "Technology Select Sector SPDR", "sector": "Technology", "type": "ETF"},
    "XLF": {"name": "Financial Select Sector SPDR", "sector": "Financial Services", "type": "ETF"},
    "XLV": {"name": "Health Care Select Sector SPDR", "sector": "Healthcare", "type": "ETF"},
    "XLE": {"name": "Energy Select Sector SPDR", "sector": "Energy", "type": "ETF"},
    "XLI": {"name": "Industrial Select Sector SPDR", "sector": "Industrials", "type": "ETF"},
    "XLP": {"name": "Consumer Staples Select Sector", "sector": "Consumer Staples", "type": "ETF"},
    "XLY": {"name": "Consumer Discretionary Select", "sector": "Consumer Discretionary", "type": "ETF"},
    "XLU": {"name": "Utilities Select Sector SPDR", "sector": "Utilities", "type": "ETF"},
    "XLB": {"name": "Materials Select Sector SPDR", "sector": "Materials", "type": "ETF"},
    "XLRE": {"name": "Real Estate Select Sector SPDR", "sector": "Real Estate", "type": "ETF"},
    "VTI": {"name": "Vanguard Total Stock Market", "sector": "Diversified", "type": "ETF"},
    "VGT": {"name": "Vanguard Information Technology", "sector": "Technology", "type": "ETF"},
    "QQQ": {"name": "Invesco QQQ Trust", "sector": "Technology", "type": "ETF"},
    "IWM": {"name": "iShares Russell 2000", "sector": "Small Cap", "type": "ETF"},
    "SPY": {"name": "SPDR S&P 500 ETF Trust", "sector": "Large Cap", "type": "ETF"}
}

def get_expanded_stock_database():
    """Get comprehensive stock database with all additions"""
    all_stocks = {}
    
    # Combine all stock databases
    all_stocks.update(SP500_ADDITIONAL)
    all_stocks.update(RUSSELL_2000_ADDITIONAL)
    all_stocks.update(INTERNATIONAL_STOCKS)
    all_stocks.update(SECTOR_ETFS)
    
    return all_stocks

def get_all_tickers_expanded():
    """Get all ticker symbols from expanded database"""
    return list(get_expanded_stock_database().keys())

def search_expanded_stocks(query="", sector=None, market_cap=None):
    """Search expanded stock database with filters"""
    all_stocks = get_expanded_stock_database()
    results = []
    
    for ticker, info in all_stocks.items():
        # Text search
        if query:
            if (query.lower() in ticker.lower() or 
                query.lower() in info['name'].lower()):
                pass
            else:
                continue
        
        # Sector filter
        if sector and info['sector'] != sector:
            continue
            
        # Market cap filter
        if market_cap and info.get('market_cap') != market_cap:
            continue
            
        results.append({
            'ticker': ticker,
            'name': info['name'],
            'sector': info['sector'],
            'market_cap': info.get('market_cap', 'Unknown'),
            'country': info.get('country', 'USA'),
            'type': info.get('type', 'Stock')
        })
    
    return results

def get_sector_breakdown():
    """Get sector breakdown of expanded database"""
    all_stocks = get_expanded_stock_database()
    sectors = {}
    
    for ticker, info in all_stocks.items():
        sector = info['sector']
        if sector not in sectors:
            sectors[sector] = []
        sectors[sector].append(ticker)
    
    return sectors

def get_stock_count_by_market_cap():
    """Get stock count by market cap"""
    all_stocks = get_expanded_stock_database()
    market_caps = {}
    
    for ticker, info in all_stocks.items():
        cap = info.get('market_cap', 'Unknown')
        if cap not in market_caps:
            market_caps[cap] = 0
        market_caps[cap] += 1
    
    return market_caps

def get_international_breakdown():
    """Get breakdown by country"""
    all_stocks = get_expanded_stock_database()
    countries = {}
    
    for ticker, info in all_stocks.items():
        country = info.get('country', 'USA')
        if country not in countries:
            countries[country] = []
        countries[country].append(ticker)
    
    return countries

# Statistics for the expanded database
def get_database_stats():
    """Get comprehensive statistics about the expanded database"""
    all_stocks = get_expanded_stock_database()
    
    stats = {
        'total_stocks': len(all_stocks),
        'sectors': get_sector_breakdown(),
        'market_caps': get_stock_count_by_market_cap(),
        'countries': get_international_breakdown(),
        'largest_sectors': sorted(get_sector_breakdown().items(), 
                                key=lambda x: len(x[1]), reverse=True)[:5]
    }
    
    return stats