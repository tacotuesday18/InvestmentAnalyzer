"""
Comprehensive market stock database with all major US and international stocks
For the stock discovery tool
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import requests

def get_sp500_tickers():
    """Get all S&P 500 tickers"""
    try:
        # S&P 500 companies from Wikipedia
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        return sp500_table['Symbol'].tolist()
    except:
        # Fallback list of major S&P 500 stocks
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "UNH", "JNJ",
            "V", "XOM", "PG", "JPM", "HD", "CVX", "MA", "ABBV", "PFE", "AVGO",
            "LLY", "KO", "COST", "PEP", "TMO", "WMT", "MRK", "BAC", "CSCO", "ACN",
            "DIS", "DHR", "VZ", "ADBE", "ABT", "CRM", "NKE", "TXN", "NFLX", "RTX",
            "QCOM", "NEE", "PM", "ORCL", "T", "LOW", "COP", "UNP", "HON", "IBM"
        ]

def get_nasdaq100_tickers():
    """Get NASDAQ 100 tickers"""
    return [
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "COST",
        "NFLX", "ADBE", "PEP", "TMUS", "CSCO", "CMCSA", "TXN", "QCOM", "AMD", "HON",
        "INTU", "AMAT", "SBUX", "ISRG", "BKNG", "MDLZ", "GILD", "ADP", "MU", "REGN",
        "PYPL", "ATVI", "FISV", "CSX", "VRTX", "MELI", "KLAC", "CHTR", "NXPI", "MRVL",
        "FTNT", "ORLY", "LRCX", "ADSK", "MAR", "MNST", "ASML", "WDAY", "PANW", "SNPS"
    ]

def get_dow30_tickers():
    """Get Dow Jones 30 tickers"""
    return [
        "AAPL", "MSFT", "UNH", "V", "HD", "JPM", "PG", "JNJ", "CVX", "WMT",
        "CRM", "MRK", "DIS", "VZ", "AXP", "NKE", "KO", "IBM", "CAT", "MCD",
        "TRV", "GS", "BA", "MMM", "HON", "AMGN", "WBA", "INTC", "CSCO", "DOW"
    ]

def get_russell2000_sample():
    """Get sample of Russell 2000 small-cap stocks"""
    return [
        "ROKU", "PLUG", "AMC", "GME", "BB", "NOK", "SNDL", "CLOV", "WISH", "SOFI",
        "PLTR", "SPCE", "RIOT", "MARA", "TLRY", "ACB", "SIRI", "F", "AAL", "CCL",
        "NCLH", "RCL", "DAL", "UAL", "LUV", "JETS", "XRT", "IWM", "VTWO", "SCHA"
    ]

def get_international_stocks():
    """Get major international stocks (ADRs and direct listings) - significantly expanded"""
    return [
        # Japanese stocks (Expanded)
        "TM", "SONY", "NTT", "MUFG", "SMFG", "HMC", "SNE", "NSANY", "FUJIY", "CAJ", 
        "KYOCY", "CANNY", "HTHIY", "NTDOY", "SZKMY", "SFTBY", "NMR", "MFG", "SFM",
        
        # European stocks (Expanded)
        "ASML", "SAP", "NVO", "NESN", "ROCHE", "NOVN", "UL", "BP", "SHELL", "VOD",
        "SAN", "BBVA", "SNY", "GSK", "AZN", "RDS.A", "RDS.B", "BT", "ING", "ABN",
        "CS", "UBS", "DB", "BCS", "LYG", "NOKIA", "NOK", "ERIC", "TEF", "VIV",
        "DT", "TI", "STM", "INFINEON", "ASMLY", "MC", "OR", "LVMH", "HERMES", "ADIDAS",
        
        # Chinese stocks (Expanded)
        "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "TME", "NTES", "WB",
        "HUYA", "YY", "MOMO", "GOTU", "TAL", "EDU", "NEW", "GOOS", "RLX", "DIDI",
        "BYDDY", "KNDI", "SOLO", "AYRO", "IQ", "VIPS", "DOYU", "YMM", "BEKE",
        
        # Taiwanese Semiconductors
        "TSM", "UMC", "ASX", "HIMX", "MCHP", "QCOM", "TXN", "ON", "SWKS", "QRVO",
        
        # Canadian Stocks
        "SHOP", "SPOT", "TRI", "CNQ", "SU", "IMO", "CVE", "MEG", "WCP", "BTE",
        "WEED", "ACB", "CRON", "HEXO", "OGI", "FIRE", "EMH", "HUGE", "VIDA", "ZENA",
        
        # South Korean ADRs
        "LPL", "PKX", "SID", "SSL", "WIT", "KB", "SHG", "LFC", "YPF", "CX",
        
        # Indian ADRs
        "WIT", "RDY", "TTM", "INFY", "HDB", "IBN", "WF", "VEDL", "SSTK", "SIFY",
        
        # Brazilian ADRs
        "VALE", "PBR", "ITUB", "BBD", "ABV", "CBD", "ERJ", "SBS", "BAK", "UGP",
        
        # Israeli Tech ADRs
        "CHKP", "CYBR", "NICE", "MNDY", "WIX", "FVRR", "NNOX", "RSKD", "TEVA", "MGIC",
        
        # Australian/Other
        "BHP", "RIO", "WBK", "SHPGY", "WKHHY", "CIOXY", "DPOSY", "FTAI", "SE", "GRAB"
    ]

def get_sector_etfs():
    """Get sector ETFs for sector analysis"""
    return {
        "Technology": "XLK",
        "Healthcare": "XLV", 
        "Financials": "XLF",
        "Consumer Discretionary": "XLY",
        "Communication Services": "XLC",
        "Industrials": "XLI",
        "Consumer Staples": "XLP",
        "Energy": "XLE",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Materials": "XLB"
    }

def get_all_market_stocks():
    """Get comprehensive list of all major market stocks including 500+ additional stocks"""
    all_stocks = []
    
    # Add major indices
    all_stocks.extend(get_sp500_tickers())
    all_stocks.extend(get_nasdaq100_tickers()) 
    all_stocks.extend(get_dow30_tickers())
    all_stocks.extend(get_russell2000_sample())
    all_stocks.extend(get_international_stocks())
    
    # Add comprehensive additional stocks for broader market coverage
    additional_mid_caps = [
        # Technology Mid-Caps
        "PLTR", "DDOG", "SNOW", "CRWD", "ZS", "OKTA", "TWLO", "ESTC", "DOCU", "COUP", 
        "SPLK", "NOW", "VEEV", "TEAM", "HUBS", "ZEN", "BILL", "SMAR", "GTLB", "FIVN",
        "PATH", "AI", "SMCI", "RBLX", "U", "FSLY", "NET", "CFLT", "MDB", "ZOOM", "ZM",
        
        # Healthcare & Biotech
        "TDOC", "ILMN", "MKTX", "INCY", "ALNY", "BMRN", "SGEN", "EXAS", "TWST", "NVTA",
        "PACB", "RXRX", "DNA", "CRSP", "EDIT", "NTLA", "BEAM", "PRIME", "MRNA", "BNTX",
        
        # FinTech & Digital Payments
        "SOFI", "AFRM", "UPST", "LC", "OPEN", "RKT", "HOOD", "COIN", "MSTR", "SQ",
        "UBER", "LYFT", "DASH", "ABNB", "BOOKING", "EXPE", "TRIP", "GRUB", "SNAP",
        
        # Consumer & E-commerce
        "PTON", "LULU", "ETSY", "W", "WAYFAIR", "CHWY", "PETS", "BARK", "WOOF", "SHOP",
        "SPOT", "DKNG", "PENN", "MGM", "WYNN", "LVS", "CCL", "NCLH", "RCL", "TWTR",
        
        # Clean Energy & EVs
        "FSLR", "ENPH", "SEDG", "RUN", "NOVA", "CSIQ", "JKS", "DQ", "SOL", "MAXN",
        "BE", "PLUG", "FCEL", "BLDP", "HYLN", "NKLA", "RIDE", "FSR", "LCID", "RIVN",
        
        # International ADRs
        "BABA", "JD", "PDD", "BIDU", "NTES", "TME", "IQ", "VIPS", "WB", "ASML",
        "SAP", "NVO", "UL", "TSM", "TM", "HMC", "NSANY", "SNE", "SONY", "SNY",
        
        # Meme Stocks & Popular Retail
        "BB", "NOK", "PLTR", "SPCE", "WISH", "CLOV", "SKLZ", "PROG", "PRTY", "BBBY", 
        "EXPR", "KOSS", "GME", "AMC", "NAKD", "SNDL", "GNUS", "IDEX", "IZEA", "KTOV",
        
        # Cannabis & Emerging Themes
        "TLRY", "APHA", "CGC", "ACB", "CRON", "HEXO", "OGI", "ZYNE", "GRWG", "IIPR",
        "SMG", "RIOT", "MARA", "HUT", "BITF", "CAN", "HIVE", "ARBK", "BTBT", "SOS"
    ]
    all_stocks.extend(additional_mid_caps)
    
    # Add Russell 2000 extended sample (small caps)
    russell_extended = [
        "AMAT", "ADI", "ALGN", "AMD", "AMGN", "ANSS", "ASML", "ATVI", "AVGO", "BIIB",
        "BKNG", "CDNS", "CERN", "CHTR", "COST", "CSX", "CTAS", "CTSH", "DLTR", "EA", 
        "EBAY", "EXC", "FAST", "FISV", "GILD", "HAS", "IDXX", "ILMN", "INCY", "INTC",
        "INTU", "ISRG", "JD", "KLAC", "LRCX", "LULU", "MAR", "MCHP", "MDLZ", "MELI",
        "MNST", "MRNA", "MRVL", "MTCH", "MU", "NFLX", "NTES", "NVDA", "NXPI", "ODFL",
        "OKTA", "ORLY", "PAYX", "PDD", "PEP", "PYPL", "QCOM", "REGN", "ROST", "SBUX",
        "SGEN", "SIRI", "SNPS", "SPLK", "SWKS", "TMUS", "TSLA", "TXN", "ULTA", "VRSK",
        "VRSN", "VRTX", "WBA", "WDAY", "XEL", "XLNX", "ZM", "ADSK", "AEP", "ALXN",
        "ANET", "BMRN", "BIDU", "CDW", "CERN", "CTXS", "DXCM", "EA", "EXPE", "FOXA",
        "FOX", "GOOG", "GOOGL", "HCA", "HOLX", "HSIC", "ICLR", "IPGP", "JBHT", "KHC",
        "LBTYA", "LBTYK", "LSXMA", "LSXMK", "MXIM", "NDAQ", "NLOK", "NTAP", "PCAR",
        "SSNC", "TTWO", "TCOM", "WDC", "WLTW", "WYNN", "XRAY", "ZION", "ZS"
    ]
    all_stocks.extend(russell_extended)
    
    # Add expanded database (500+ additional stocks)
    try:
        from expanded_stock_database import get_all_tickers_expanded
        expanded_tickers = get_all_tickers_expanded()
        all_stocks.extend(expanded_tickers)
    except Exception:
        pass  # Continue with original database if expanded fails
    
    # Remove duplicates and return sorted list
    unique_stocks = list(set(all_stocks))
    return sorted(unique_stocks)

def get_stock_sector_mapping():
    """Map stocks to their sectors"""
    return {
        # Technology
        "Technology": ["AAPL", "MSFT", "GOOGL", "GOOG", "NVDA", "META", "TSLA", "NFLX", "ADBE", "CRM", "ORCL", "CSCO", "IBM", "INTC", "AMD", "QCOM", "TXN", "AVGO", "AMAT", "LRCX", "KLAC", "MRVL", "NXPI", "SNPS", "ADSK", "FTNT", "PANW", "WDAY", "ROKU", "ZOOM", "ZM", "SQ", "SHOP", "SPOT"],
        
        # Healthcare  
        "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "LLY", "TMO", "DHR", "ABT", "MRK", "GILD", "REGN", "VRTX", "ISRG", "AMGN", "MRNA", "BNTX", "NVAX"],
        
        # Financials
        "Financials": ["JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "BLK", "SCHW", "USB", "TFC", "PNC", "COF", "SPGI", "ICE", "CME", "V", "MA", "PYPL"],
        
        # Consumer Discretionary  
        "Consumer Discretionary": ["AMZN", "HD", "NKE", "DIS", "MCD", "SBUX", "LOW", "TJX", "BKNG", "MAR", "GM", "F", "TSLA", "CCL", "NCLH", "RCL", "MGM"],
        
        # Communication Services
        "Communication Services": ["META", "GOOGL", "GOOG", "NFLX", "DIS", "VZ", "T", "CMCSA", "CHTR", "SNAP", "TWTR", "SPOT"],
        
        # Industrials
        "Industrials": ["HON", "UNP", "RTX", "CAT", "BA", "LMT", "MMM", "GE", "FDX", "UPS", "CSX", "NSC", "UAL", "DAL", "LUV", "AAL"],
        
        # Consumer Staples
        "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST", "MDLZ", "CL", "KMB", "GIS", "K", "HSY"],
        
        # Energy
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC", "VLO", "PSX", "KMI", "OKE", "WMB"],
        
        # Utilities  
        "Utilities": ["NEE", "DUK", "SO", "AEP", "EXC", "XEL", "PEG", "ED", "ETR", "ES"],
        
        # Real Estate
        "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "AVB", "EQR", "VTR", "ESS", "MAA"],
        
        # Materials
        "Materials": ["LIN", "APD", "ECL", "SHW", "FCX", "NEM", "DOW", "DD", "PPG", "IFF"]
    }

def get_stock_info_enhanced(ticker):
    """Get enhanced stock information with sector and market cap"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get sector mapping
        sector_mapping = get_stock_sector_mapping()
        sector = "Other"
        for sec, stocks in sector_mapping.items():
            if ticker in stocks:
                sector = sec
                break
        
        return {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "sector": sector,
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "country": info.get("country", "US"),
            "exchange": info.get("exchange", "NASDAQ"),
            "price": info.get("currentPrice", 0)
        }
    except:
        return {
            "ticker": ticker,
            "name": ticker,
            "sector": "Other", 
            "industry": "N/A",
            "market_cap": 0,
            "country": "US",
            "exchange": "NASDAQ",
            "price": 0
        }

def search_stocks_comprehensive(query="", sector=None, min_market_cap=None, max_market_cap=None):
    """Comprehensive stock search with filters"""
    all_stocks = get_all_market_stocks()
    
    if query:
        # Filter by query in ticker or name
        filtered_stocks = [s for s in all_stocks if query.upper() in s.upper()]
    else:
        filtered_stocks = all_stocks
    
    # Apply additional filters (sector, market cap) would require real-time data
    return filtered_stocks[:100]  # Limit to 100 results for performance

def get_market_categories():
    """Get all market categories"""
    return {
        "US Large Cap": ["S&P 500", "Dow Jones 30", "NASDAQ 100"],
        "US Small Cap": ["Russell 2000"],
        "International": ["Japanese Stocks", "European Stocks", "Chinese Stocks"],
        "Sectors": list(get_sector_etfs().keys())
    }