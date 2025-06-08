"""
Comprehensive stock universe for Kabu2Easy platform
Contains hundreds of major stocks from various exchanges and sectors
"""

# S&P 500 Major Stocks
SP500_STOCKS = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE",
    "CRM", "INTC", "AMD", "CSCO", "ORCL", "IBM", "QCOM", "TXN", "AVGO", "INTU",
    "NOW", "SNOW", "PLTR", "ZM", "DOCU", "OKTA", "TWLO", "DDOG", "NET", "CRWD",
    
    # Healthcare & Biotechnology
    "JNJ", "PFE", "UNH", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY", "LLY",
    "AMGN", "GILD", "BIIB", "REGN", "VRTX", "ISRG", "ZTS", "ILMN", "MRNA", "BNTX",
    
    # Financial Services
    "BRK-B", "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "V", "MA",
    "PYPL", "SQ", "COIN", "HOOD", "SOFI", "AFRM", "UPST", "LC", "ALLY", "COF",
    
    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "TJX", "BKNG",
    "ABNB", "UBER", "LYFT", "DIS", "NFLX", "ROKU", "SPOT", "ETSY", "EBAY", "SHOP",
    
    # Consumer Staples
    "PG", "KO", "PEP", "WMT", "COST", "CL", "KMB", "GIS", "K", "CPB",
    "CAG", "TSN", "HSY", "MDLZ", "MNST", "KHC", "SJM", "HRL", "MKC", "CHD",
    
    # Energy
    "XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "OXY", "DVN",
    "FANG", "EQT", "AR", "SM", "CNX", "RRC", "CHK", "WPX", "COG", "NFG",
    
    # Industrials
    "BA", "CAT", "DE", "GE", "HON", "MMM", "UPS", "FDX", "LMT", "RTX",
    "NOC", "GD", "TDG", "PH", "ETN", "EMR", "ITW", "CMI", "DOV", "ROK",
    
    # Materials
    "LIN", "APD", "ECL", "SHW", "FCX", "NEM", "FMC", "ALB", "CE", "VMC",
    "MLM", "NUE", "STLD", "X", "AA", "CF", "MOS", "IFF", "PPG", "RPM",
    
    # Real Estate
    "AMT", "PLD", "CCI", "EQIX", "PSA", "WELL", "DLR", "O", "SBAC", "EXR",
    "AVB", "EQR", "MAA", "UDR", "CPT", "ESS", "AIV", "BXP", "VTR", "PEAK",
    
    # Utilities
    "NEE", "DUK", "SO", "D", "EXC", "XEL", "SRE", "AEP", "PCG", "ED",
    "AWK", "ES", "FE", "ETR", "PPL", "AES", "NI", "LNT", "PNW", "CNP",
    
    # Communication Services
    "GOOGL", "META", "NFLX", "DIS", "VZ", "T", "TMUS", "CHTR", "CMCSA", "FOXA",
    "PARA", "WBD", "NWSA", "IPG", "OMC", "TTWO", "EA", "ATVI", "ZM", "TWTR"
]

# NASDAQ 100 Additional Stocks
NASDAQ_STOCKS = [
    "TSLA", "NVDA", "AMZN", "GOOGL", "META", "AAPL", "MSFT", "NFLX", "ADBE", "INTC",
    "CSCO", "PEP", "COST", "QCOM", "TXN", "AVGO", "INTU", "AMD", "SBUX", "GILD",
    "AMGN", "ISRG", "BKNG", "REGN", "MRNA", "MDLZ", "ADP", "FISV", "CSX", "ABNB",
    "PYPL", "NXPI", "KLAC", "MRVL", "ORLY", "LRCX", "DXCM", "CRWD", "FTNT", "WDAY",
    "MNST", "IDXX", "ILMN", "BIIB", "ZS", "TEAM", "OKTA", "DOCU", "ZM", "PTON"
]

# Popular International Stocks (ADRs)
INTERNATIONAL_STOCKS = [
    # Chinese Stocks
    "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "TME", "BILI", "IQ",
    "NTES", "WB", "VIPS", "YMM", "DADA", "KC", "TIGR", "FUTU", "TAL", "EDU",
    
    # European Stocks
    "ASML", "SAP", "NVO", "UL", "NESN", "RHHBY", "TM", "SNY", "GSK", "AZN",
    "BP", "RDS-A", "BCS", "DB", "ING", "SAN", "BBVA", "TEF", "VOD", "BT",
    
    # Japanese Stocks
    "TM", "SONY", "TSM", "NTT", "SFM", "SMFG", "MFG", "HMC", "SNE", "FUJIY",
    
    # Other International
    "TSM", "VALE", "IBN", "ITUB", "PBR", "SID", "GGB", "BBD", "CIG", "LFC"
]

# Growth Stocks
GROWTH_STOCKS = [
    "SHOP", "SQ", "ROKU", "ZOOM", "SNOW", "PLTR", "RBLX", "U", "PATH", "DDOG",
    "NET", "CRWD", "ZS", "OKTA", "TWLO", "DOCU", "FVRR", "UPWK", "ETSY", "PINS",
    "SNAP", "TWTR", "HOOD", "COIN", "RIVN", "LCID", "SOFI", "AFRM", "UPST", "OPEN"
]

# Dividend Stocks
DIVIDEND_STOCKS = [
    "KO", "PEP", "JNJ", "PG", "MCD", "WMT", "VZ", "T", "IBM", "INTC",
    "XOM", "CVX", "MO", "PM", "BTI", "O", "MAIN", "STAG", "NLY", "AGNC",
    "IRM", "WPC", "ADC", "MPW", "STOR", "LAND", "EPR", "NNN", "SRC", "FCPT"
]

# All available stocks combined
ALL_STOCKS = list(set(SP500_STOCKS + NASDAQ_STOCKS + INTERNATIONAL_STOCKS + 
                     GROWTH_STOCKS + DIVIDEND_STOCKS))

# Stock categories for filtering
STOCK_CATEGORIES = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", 
                   "ADBE", "CRM", "INTC", "AMD", "CSCO", "ORCL", "IBM", "QCOM"],
    "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK", "TMO", "ABT", "DHR", 
                   "BMY", "LLY", "AMGN", "GILD", "BIIB", "REGN", "VRTX"],
    "Financial": ["BRK-B", "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "V", "MA"],
    "Consumer": ["HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "TJX", "BKNG", "DIS"],
    "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "OXY"],
    "International": INTERNATIONAL_STOCKS,
    "Growth": GROWTH_STOCKS,
    "Dividend": DIVIDEND_STOCKS
}

def get_all_available_stocks():
    """Return all available stocks"""
    return sorted(ALL_STOCKS)

def get_stocks_by_category(category):
    """Get stocks filtered by category"""
    return STOCK_CATEGORIES.get(category, [])

def get_stock_categories():
    """Get all available categories"""
    return list(STOCK_CATEGORIES.keys())

def search_stocks(query):
    """Search stocks by ticker symbol"""
    query = query.upper()
    return [stock for stock in ALL_STOCKS if query in stock]

def get_popular_stocks():
    """Get most popular stocks for quick access"""
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", 
            "BABA", "TSM", "V", "JNJ", "WMT", "JPM", "UNH"]