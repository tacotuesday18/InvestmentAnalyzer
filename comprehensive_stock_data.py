"""
Comprehensive stock database with company names for search functionality
Includes S&P 500, NASDAQ, Dow Jones, Russell 2000, international stocks, and 500+ additional stocks
Now features 800+ stocks across all major markets and sectors
"""

# Import expanded database
from expanded_stock_database import get_expanded_stock_database

COMPREHENSIVE_STOCKS = {
    # S&P 500 Technology Leaders
    "AAPL": {"name": "Apple Inc.", "category": "Technology", "index": "S&P500"},
    "MSFT": {"name": "Microsoft Corporation", "category": "Technology", "index": "S&P500"},
    "GOOGL": {"name": "Alphabet Inc. Class A", "category": "Technology", "index": "S&P500"},
    "GOOG": {"name": "Alphabet Inc. Class C", "category": "Technology", "index": "S&P500"},
    "AMZN": {"name": "Amazon.com Inc.", "category": "Technology", "index": "S&P500"},
    "META": {"name": "Meta Platforms Inc.", "category": "Technology", "index": "S&P500"},
    "TSLA": {"name": "Tesla Inc.", "category": "Technology", "index": "S&P500"},
    "NFLX": {"name": "Netflix Inc.", "category": "Technology", "index": "S&P500"},
    "NVDA": {"name": "NVIDIA Corporation", "category": "Technology", "index": "S&P500"},
    "AMD": {"name": "Advanced Micro Devices", "category": "Technology", "index": "S&P500"},
    "INTC": {"name": "Intel Corporation", "category": "Technology", "index": "S&P500"},
    "CSCO": {"name": "Cisco Systems Inc.", "category": "Technology", "index": "S&P500"},
    "ORCL": {"name": "Oracle Corporation", "category": "Technology", "index": "S&P500"},
    "CRM": {"name": "Salesforce Inc.", "category": "Technology", "index": "S&P500"},
    "ADBE": {"name": "Adobe Inc.", "category": "Technology", "index": "S&P500"},
    "PYPL": {"name": "PayPal Holdings Inc.", "category": "Technology", "index": "S&P500"},
    "IBM": {"name": "International Business Machines", "category": "Technology", "index": "S&P500"},
    "QCOM": {"name": "QUALCOMM Incorporated", "category": "Technology", "index": "S&P500"},
    "TXN": {"name": "Texas Instruments Incorporated", "category": "Technology", "index": "S&P500"},
    "AVGO": {"name": "Broadcom Inc.", "category": "Technology", "index": "S&P500"},
    
    # Healthcare & Pharmaceuticals
    "JNJ": {"name": "Johnson & Johnson", "category": "Healthcare", "index": "S&P500"},
    "PFE": {"name": "Pfizer Inc.", "category": "Healthcare", "index": "S&P500"},
    "UNH": {"name": "UnitedHealth Group", "category": "Healthcare", "index": "S&P500"},
    "MRK": {"name": "Merck & Co Inc.", "category": "Healthcare", "index": "S&P500"},
    "ABT": {"name": "Abbott Laboratories", "category": "Healthcare", "index": "S&P500"},
    "TMO": {"name": "Thermo Fisher Scientific", "category": "Healthcare", "index": "S&P500"},
    "DHR": {"name": "Danaher Corporation", "category": "Healthcare", "index": "S&P500"},
    "ABBV": {"name": "AbbVie Inc.", "category": "Healthcare", "index": "S&P500"},
    "LLY": {"name": "Eli Lilly and Company", "category": "Healthcare", "index": "S&P500"},
    "BMY": {"name": "Bristol-Myers Squibb", "category": "Healthcare", "index": "S&P500"},
    "AMGN": {"name": "Amgen Inc.", "category": "Healthcare", "index": "S&P500"},
    "GILD": {"name": "Gilead Sciences Inc.", "category": "Healthcare", "index": "S&P500"},
    "VRTX": {"name": "Vertex Pharmaceuticals", "category": "Healthcare", "index": "S&P500"},
    "REGN": {"name": "Regeneron Pharmaceuticals", "category": "Healthcare", "index": "S&P500"},
    "BIIB": {"name": "Biogen Inc.", "category": "Healthcare", "index": "S&P500"},
    "HIMS": {"name": "Hims & Hers Health Inc.", "category": "Healthcare", "index": "NYSE"},
    
    # Financial Services
    "JPM": {"name": "JPMorgan Chase & Co.", "category": "Financial", "index": "S&P500"},
    "BAC": {"name": "Bank of America Corp", "category": "Financial", "index": "S&P500"},
    "WFC": {"name": "Wells Fargo & Company", "category": "Financial", "index": "S&P500"},
    "GS": {"name": "Goldman Sachs Group", "category": "Financial", "index": "S&P500"},
    "MS": {"name": "Morgan Stanley", "category": "Financial", "index": "S&P500"},
    "C": {"name": "Citigroup Inc.", "category": "Financial", "index": "S&P500"},
    "AXP": {"name": "American Express Company", "category": "Financial", "index": "S&P500"},
    "BLK": {"name": "BlackRock Inc.", "category": "Financial", "index": "S&P500"},
    "SCHW": {"name": "Charles Schwab Corporation", "category": "Financial", "index": "S&P500"},
    "SPGI": {"name": "S&P Global Inc.", "category": "Financial", "index": "S&P500"},
    "CME": {"name": "CME Group Inc.", "category": "Financial", "index": "S&P500"},
    "ICE": {"name": "Intercontinental Exchange", "category": "Financial", "index": "S&P500"},
    "COF": {"name": "Capital One Financial", "category": "Financial", "index": "S&P500"},
    "USB": {"name": "U.S. Bancorp", "category": "Financial", "index": "S&P500"},
    "PNC": {"name": "PNC Financial Services", "category": "Financial", "index": "S&P500"},
    
    # Consumer Discretionary
    "WMT": {"name": "Walmart Inc.", "category": "Consumer", "index": "S&P500"},
    "HD": {"name": "Home Depot Inc.", "category": "Consumer", "index": "S&P500"},
    "MCD": {"name": "McDonald's Corporation", "category": "Consumer", "index": "S&P500"},
    "NKE": {"name": "Nike Inc.", "category": "Consumer", "index": "S&P500"},
    "SBUX": {"name": "Starbucks Corporation", "category": "Consumer", "index": "S&P500"},
    "LOW": {"name": "Lowe's Companies Inc.", "category": "Consumer", "index": "S&P500"},
    "TGT": {"name": "Target Corporation", "category": "Consumer", "index": "S&P500"},
    "DIS": {"name": "Walt Disney Company", "category": "Consumer", "index": "S&P500"},
    "TJX": {"name": "TJX Companies Inc.", "category": "Consumer", "index": "S&P500"},
    "BKNG": {"name": "Booking Holdings Inc.", "category": "Consumer", "index": "S&P500"},
    
    # Consumer Staples
    "PG": {"name": "Procter & Gamble Company", "category": "Consumer", "index": "S&P500"},
    "KO": {"name": "Coca-Cola Company", "category": "Consumer", "index": "S&P500"},
    "PEP": {"name": "PepsiCo Inc.", "category": "Consumer", "index": "S&P500"},
    "COST": {"name": "Costco Wholesale Corporation", "category": "Consumer", "index": "S&P500"},
    "WBA": {"name": "Walgreens Boots Alliance", "category": "Consumer", "index": "S&P500"},
    "CVS": {"name": "CVS Health Corporation", "category": "Consumer", "index": "S&P500"},
    "CL": {"name": "Colgate-Palmolive Company", "category": "Consumer", "index": "S&P500"},
    "KMB": {"name": "Kimberly-Clark Corporation", "category": "Consumer", "index": "S&P500"},
    "GIS": {"name": "General Mills Inc.", "category": "Consumer", "index": "S&P500"},
    "K": {"name": "Kellogg Company", "category": "Consumer", "index": "S&P500"},
    
    # Energy
    "XOM": {"name": "Exxon Mobil Corporation", "category": "Energy", "index": "S&P500"},
    "CVX": {"name": "Chevron Corporation", "category": "Energy", "index": "S&P500"},
    "COP": {"name": "ConocoPhillips", "category": "Energy", "index": "S&P500"},
    "SLB": {"name": "Schlumberger Limited", "category": "Energy", "index": "S&P500"},
    "EOG": {"name": "EOG Resources Inc.", "category": "Energy", "index": "S&P500"},
    "KMI": {"name": "Kinder Morgan Inc.", "category": "Energy", "index": "S&P500"},
    "OXY": {"name": "Occidental Petroleum", "category": "Energy", "index": "S&P500"},
    "PSX": {"name": "Phillips 66", "category": "Energy", "index": "S&P500"},
    "VLO": {"name": "Valero Energy Corporation", "category": "Energy", "index": "S&P500"},
    "MPC": {"name": "Marathon Petroleum", "category": "Energy", "index": "S&P500"},
    
    # Industrials
    "BA": {"name": "Boeing Company", "category": "Industrial", "index": "S&P500"},
    "CAT": {"name": "Caterpillar Inc.", "category": "Industrial", "index": "S&P500"},
    "MMM": {"name": "3M Company", "category": "Industrial", "index": "S&P500"},
    "GE": {"name": "General Electric Company", "category": "Industrial", "index": "S&P500"},
    "HON": {"name": "Honeywell International", "category": "Industrial", "index": "S&P500"},
    "UPS": {"name": "United Parcel Service", "category": "Industrial", "index": "S&P500"},
    "FDX": {"name": "FedEx Corporation", "category": "Industrial", "index": "S&P500"},
    "LMT": {"name": "Lockheed Martin Corporation", "category": "Industrial", "index": "S&P500"},
    "RTX": {"name": "Raytheon Technologies", "category": "Industrial", "index": "S&P500"},
    "NOC": {"name": "Northrop Grumman Corporation", "category": "Industrial", "index": "S&P500"},
    
    # Utilities & Telecom
    "VZ": {"name": "Verizon Communications", "category": "Telecom", "index": "S&P500"},
    "T": {"name": "AT&T Inc.", "category": "Telecom", "index": "S&P500"},
    "NEE": {"name": "NextEra Energy Inc.", "category": "Utilities", "index": "S&P500"},
    "DUK": {"name": "Duke Energy Corporation", "category": "Utilities", "index": "S&P500"},
    "SO": {"name": "Southern Company", "category": "Utilities", "index": "S&P500"},
    "D": {"name": "Dominion Energy Inc.", "category": "Utilities", "index": "S&P500"},
    "AEP": {"name": "American Electric Power", "category": "Utilities", "index": "S&P500"},
    "EXC": {"name": "Exelon Corporation", "category": "Utilities", "index": "S&P500"},
    
    # Materials
    "LIN": {"name": "Linde plc", "category": "Materials", "index": "S&P500"},
    "APD": {"name": "Air Products and Chemicals", "category": "Materials", "index": "S&P500"},
    "ECL": {"name": "Ecolab Inc.", "category": "Materials", "index": "S&P500"},
    "FCX": {"name": "Freeport-McMoRan Inc.", "category": "Materials", "index": "S&P500"},
    "NEM": {"name": "Newmont Corporation", "category": "Materials", "index": "S&P500"},
    "DOW": {"name": "Dow Inc.", "category": "Materials", "index": "S&P500"},
    
    # NASDAQ Growth Stocks
    "SPOT": {"name": "Spotify Technology", "category": "Technology", "index": "NASDAQ"},
    "UBER": {"name": "Uber Technologies", "category": "Technology", "index": "NASDAQ"},
    "COIN": {"name": "Coinbase Global Inc.", "category": "Technology", "index": "NASDAQ"},
    "SQ": {"name": "Block Inc.", "category": "Technology", "index": "NASDAQ"},
    "ZM": {"name": "Zoom Video Communications", "category": "Technology", "index": "NASDAQ"},
    "SNOW": {"name": "Snowflake Inc.", "category": "Technology", "index": "NASDAQ"},
    "PLTR": {"name": "Palantir Technologies", "category": "Technology", "index": "NASDAQ"},
    "ROKU": {"name": "Roku Inc.", "category": "Technology", "index": "NASDAQ"},
    "DOCU": {"name": "DocuSign Inc.", "category": "Technology", "index": "NASDAQ"},
    "OKTA": {"name": "Okta Inc.", "category": "Technology", "index": "NASDAQ"},
    "TWLO": {"name": "Twilio Inc.", "category": "Technology", "index": "NASDAQ"},
    "ZS": {"name": "Zscaler Inc.", "category": "Technology", "index": "NASDAQ"},
    "CRWD": {"name": "CrowdStrike Holdings", "category": "Technology", "index": "NASDAQ"},
    "NET": {"name": "Cloudflare Inc.", "category": "Technology", "index": "NASDAQ"},
    "DDOG": {"name": "Datadog Inc.", "category": "Technology", "index": "NASDAQ"},
    "TEAM": {"name": "Atlassian Corporation", "category": "Technology", "index": "NASDAQ"},
    "WDAY": {"name": "Workday Inc.", "category": "Technology", "index": "NASDAQ"},
    "PANW": {"name": "Palo Alto Networks", "category": "Technology", "index": "NASDAQ"},
    "SPLK": {"name": "Splunk Inc.", "category": "Technology", "index": "NASDAQ"},
    "VEEV": {"name": "Veeva Systems Inc.", "category": "Technology", "index": "NASDAQ"},
    
    # International ADRs
    "BABA": {"name": "Alibaba Group Holding", "category": "International", "index": "NYSE"},
    "TSM": {"name": "Taiwan Semiconductor", "category": "International", "index": "NYSE"},
    "ASML": {"name": "ASML Holding N.V.", "category": "International", "index": "NASDAQ"},
    "NVO": {"name": "Novo Nordisk A/S", "category": "International", "index": "NYSE"},
    "TM": {"name": "Toyota Motor Corporation", "category": "International", "index": "NYSE"},
    "UL": {"name": "Unilever PLC", "category": "International", "index": "NYSE"},
    "SAP": {"name": "SAP SE", "category": "International", "index": "NYSE"},
    "SHOP": {"name": "Shopify Inc.", "category": "International", "index": "NYSE"},
    "SE": {"name": "Sea Limited", "category": "International", "index": "NYSE"},
    "BIDU": {"name": "Baidu Inc.", "category": "International", "index": "NASDAQ"},
    "JD": {"name": "JD.com Inc.", "category": "International", "index": "NASDAQ"},
    "PDD": {"name": "PDD Holdings Inc.", "category": "International", "index": "NASDAQ"},
    "NIO": {"name": "NIO Inc.", "category": "International", "index": "NYSE"},
    "XPEV": {"name": "XPeng Inc.", "category": "International", "index": "NYSE"},
    "LI": {"name": "Li Auto Inc.", "category": "International", "index": "NASDAQ"},
    
    # Russell 2000 Small Caps
    "UPST": {"name": "Upstart Holdings Inc.", "category": "Technology", "index": "Russell2000"},
    "FUBO": {"name": "fuboTV Inc.", "category": "Technology", "index": "Russell2000"},
    "SPCE": {"name": "Virgin Galactic Holdings", "category": "Technology", "index": "Russell2000"},
    "HOOD": {"name": "Robinhood Markets Inc.", "category": "Financial", "index": "Russell2000"},
    "SOFI": {"name": "SoFi Technologies Inc.", "category": "Financial", "index": "Russell2000"},
    
    # Mid-Cap Growth
    "ETSY": {"name": "Etsy Inc.", "category": "Technology", "index": "NASDAQ"},
    "PINS": {"name": "Pinterest Inc.", "category": "Technology", "index": "NYSE"},
    "SNAP": {"name": "Snap Inc.", "category": "Technology", "index": "NYSE"},
    "LYFT": {"name": "Lyft Inc.", "category": "Technology", "index": "NASDAQ"},
    "ABNB": {"name": "Airbnb Inc.", "category": "Technology", "index": "NASDAQ"},
    "DASH": {"name": "DoorDash Inc.", "category": "Technology", "index": "NYSE"},
    "RBLX": {"name": "Roblox Corporation", "category": "Technology", "index": "NYSE"},
    
    # Automotive
    "F": {"name": "Ford Motor Company", "category": "Automotive", "index": "NYSE"},
    "GM": {"name": "General Motors Company", "category": "Automotive", "index": "NYSE"},
    "LCID": {"name": "Lucid Group Inc.", "category": "Automotive", "index": "NASDAQ"},
    "RIVN": {"name": "Rivian Automotive Inc.", "category": "Automotive", "index": "NASDAQ"},
    
    # REITs
    "AMT": {"name": "American Tower Corporation", "category": "REIT", "index": "NYSE"},
    "PLD": {"name": "Prologis Inc.", "category": "REIT", "index": "NYSE"},
    "CCI": {"name": "Crown Castle International", "category": "REIT", "index": "NYSE"},
    "EQIX": {"name": "Equinix Inc.", "category": "REIT", "index": "NASDAQ"},
    "SPG": {"name": "Simon Property Group", "category": "REIT", "index": "NYSE"},
    
    # Additional Popular Stocks
    "CROX": {"name": "Crocs Inc.", "category": "Consumer", "index": "NASDAQ"},
    "ELF": {"name": "e.l.f. Beauty Inc.", "category": "Consumer", "index": "NYSE"},
    "LMND": {"name": "Lemonade Inc.", "category": "Financial", "index": "NYSE"},
    "FUBO": {"name": "fuboTV Inc.", "category": "Technology", "index": "NYSE"},
    "BYND": {"name": "Beyond Meat Inc.", "category": "Consumer", "index": "NASDAQ"},
    "PELOTON": {"name": "Peloton Interactive Inc.", "category": "Consumer", "index": "NASDAQ"},
    "ZOOM": {"name": "Zoom Video Communications", "category": "Technology", "index": "NASDAQ"},
    "DOCN": {"name": "DigitalOcean Holdings", "category": "Technology", "index": "NYSE"},
    "BILL": {"name": "Bill.com Holdings", "category": "Technology", "index": "NYSE"},
    "PATH": {"name": "UiPath Inc.", "category": "Technology", "index": "NYSE"},
    "OPEN": {"name": "Opendoor Technologies", "category": "Technology", "index": "NASDAQ"},
    "RKLB": {"name": "Rocket Lab USA Inc.", "category": "Technology", "index": "NASDAQ"},
    "BROS": {"name": "Dutch Bros Inc.", "category": "Consumer", "index": "NYSE"},
    "BIRD": {"name": "Bird Global Inc.", "category": "Technology", "index": "NYSE"},
    "GOGO": {"name": "Gogo Inc.", "category": "Technology", "index": "NASDAQ"},
    "SKLZ": {"name": "Skillz Inc.", "category": "Technology", "index": "NYSE"},
    "DKNG": {"name": "DraftKings Inc.", "category": "Technology", "index": "NASDAQ"},
    "PENN": {"name": "Penn Entertainment", "category": "Consumer", "index": "NASDAQ"},
    "MGM": {"name": "MGM Resorts International", "category": "Consumer", "index": "NYSE"},
    "WYNN": {"name": "Wynn Resorts Limited", "category": "Consumer", "index": "NASDAQ"},
    "CZR": {"name": "Caesars Entertainment", "category": "Consumer", "index": "NASDAQ"},
    "NCLH": {"name": "Norwegian Cruise Line", "category": "Consumer", "index": "NYSE"},
    "CCL": {"name": "Carnival Corporation", "category": "Consumer", "index": "NYSE"},
    "RCL": {"name": "Royal Caribbean Cruises", "category": "Consumer", "index": "NYSE"},
    "AAL": {"name": "American Airlines Group", "category": "Industrial", "index": "NASDAQ"},
    "DAL": {"name": "Delta Air Lines Inc.", "category": "Industrial", "index": "NYSE"},
    "UAL": {"name": "United Airlines Holdings", "category": "Industrial", "index": "NASDAQ"},
    "LUV": {"name": "Southwest Airlines Co.", "category": "Industrial", "index": "NYSE"},
    "ALK": {"name": "Alaska Air Group Inc.", "category": "Industrial", "index": "NYSE"},
    "JBLU": {"name": "JetBlue Airways Corporation", "category": "Industrial", "index": "NASDAQ"},
    "SAVE": {"name": "Spirit Airlines Inc.", "category": "Industrial", "index": "NYSE"},
    "HA": {"name": "Hawaiian Holdings Inc.", "category": "Industrial", "index": "NASDAQ"},
    
    # Biotechnology & Healthcare
    "MRNA": {"name": "Moderna Inc.", "category": "Healthcare", "index": "NASDAQ"},
    "BNTX": {"name": "BioNTech SE", "category": "Healthcare", "index": "NASDAQ"},
    "NVAX": {"name": "Novavax Inc.", "category": "Healthcare", "index": "NASDAQ"},
    "ILMN": {"name": "Illumina Inc.", "category": "Healthcare", "index": "NASDAQ"},
    "ISRG": {"name": "Intuitive Surgical Inc.", "category": "Healthcare", "index": "NASDAQ"},
    "DXCM": {"name": "DexCom Inc.", "category": "Healthcare", "index": "NASDAQ"},
    "TDOC": {"name": "Teladoc Health Inc.", "category": "Healthcare", "index": "NYSE"},
    "VEEV": {"name": "Veeva Systems Inc.", "category": "Healthcare", "index": "NYSE"},
    
    # Semiconductor & Hardware
    "TSM": {"name": "Taiwan Semiconductor", "category": "Technology", "index": "NYSE"},
    "ASML": {"name": "ASML Holding N.V.", "category": "Technology", "index": "NASDAQ"},
    "AMAT": {"name": "Applied Materials Inc.", "category": "Technology", "index": "NASDAQ"},
    "LRCX": {"name": "Lam Research Corporation", "category": "Technology", "index": "NASDAQ"},
    "KLAC": {"name": "KLA Corporation", "category": "Technology", "index": "NASDAQ"},
    "MRVL": {"name": "Marvell Technology Inc.", "category": "Technology", "index": "NASDAQ"},
    "XLNX": {"name": "Xilinx Inc.", "category": "Technology", "index": "NASDAQ"},
    "SWKS": {"name": "Skyworks Solutions Inc.", "category": "Technology", "index": "NASDAQ"},
    "QRVO": {"name": "Qorvo Inc.", "category": "Technology", "index": "NASDAQ"},
    "MCHP": {"name": "Microchip Technology", "category": "Technology", "index": "NASDAQ"},
    "MPWR": {"name": "Monolithic Power Systems", "category": "Technology", "index": "NASDAQ"},
    "ON": {"name": "ON Semiconductor Corporation", "category": "Technology", "index": "NASDAQ"},
    
    # Software & SaaS
    "NOW": {"name": "ServiceNow Inc.", "category": "Technology", "index": "NYSE"},
    "MDB": {"name": "MongoDB Inc.", "category": "Technology", "index": "NASDAQ"},
    "ESTC": {"name": "Elastic N.V.", "category": "Technology", "index": "NYSE"},
    "GTLB": {"name": "GitLab Inc.", "category": "Technology", "index": "NASDAQ"},
    "FROG": {"name": "JFrog Ltd.", "category": "Technology", "index": "NASDAQ"},
    "PD": {"name": "PagerDuty Inc.", "category": "Technology", "index": "NYSE"},
    "SUMO": {"name": "Sumo Logic Inc.", "category": "Technology", "index": "NASDAQ"},
    "AI": {"name": "C3.ai Inc.", "category": "Technology", "index": "NYSE"},
    "SMCI": {"name": "Super Micro Computer", "category": "Technology", "index": "NASDAQ"},
    
    # Media & Entertainment
    "DIS": {"name": "Walt Disney Company", "category": "Consumer", "index": "NYSE"},
    "CMCSA": {"name": "Comcast Corporation", "category": "Consumer", "index": "NASDAQ"},
    "PARA": {"name": "Paramount Global", "category": "Consumer", "index": "NASDAQ"},
    "WBD": {"name": "Warner Bros. Discovery", "category": "Consumer", "index": "NASDAQ"},
    "FOXA": {"name": "Fox Corporation Class A", "category": "Consumer", "index": "NASDAQ"},
    "FOX": {"name": "Fox Corporation Class B", "category": "Consumer", "index": "NASDAQ"},
    "IAC": {"name": "IAC/InterActiveCorp", "category": "Technology", "index": "NASDAQ"},
    "MTCH": {"name": "Match Group Inc.", "category": "Technology", "index": "NASDAQ"},
    "BMBL": {"name": "Bumble Inc.", "category": "Technology", "index": "NASDAQ"},
    
    # Missing Major Stocks - Restaurant & Consumer Brands
    "CMG": {"name": "Chipotle Mexican Grill", "category": "Consumer", "index": "NYSE"},
    "CAVA": {"name": "CAVA Group Inc.", "category": "Consumer", "index": "NYSE"},
    "LULU": {"name": "Lululemon Athletica", "category": "Consumer", "index": "NASDAQ"},
    "ONON": {"name": "ON Holding AG", "category": "Consumer", "index": "NYSE"},
    "SBUX": {"name": "Starbucks Corporation", "category": "Consumer", "index": "NASDAQ"},
    "MCD": {"name": "McDonald's Corporation", "category": "Consumer", "index": "NYSE"},
    "YUM": {"name": "Yum! Brands Inc.", "category": "Consumer", "index": "NYSE"},
    "QSR": {"name": "Restaurant Brands International", "category": "Consumer", "index": "NYSE"},
    "DPZ": {"name": "Domino's Pizza Inc.", "category": "Consumer", "index": "NYSE"},
    "WING": {"name": "Wingstop Inc.", "category": "Consumer", "index": "NASDAQ"},
    "SHAK": {"name": "Shake Shack Inc.", "category": "Consumer", "index": "NYSE"},
    "TXRH": {"name": "Texas Roadhouse Inc.", "category": "Consumer", "index": "NASDAQ"},
    "DNUT": {"name": "Krispy Kreme Inc.", "category": "Consumer", "index": "NASDAQ"},
    "BJRI": {"name": "BJ's Restaurants Inc.", "category": "Consumer", "index": "NASDAQ"},
    "CAKE": {"name": "Cheesecake Factory Inc.", "category": "Consumer", "index": "NASDAQ"},
    "DENN": {"name": "Denny's Corporation", "category": "Consumer", "index": "NASDAQ"},
    "EAT": {"name": "Brinker International", "category": "Consumer", "index": "NYSE"},
    "BLMN": {"name": "Bloomin' Brands Inc.", "category": "Consumer", "index": "NASDAQ"},
    "DRI": {"name": "Darden Restaurants Inc.", "category": "Consumer", "index": "NYSE"},
    
    # Athletic & Fashion Brands
    "NKE": {"name": "Nike Inc.", "category": "Consumer", "index": "NYSE"},
    "ADDYY": {"name": "Adidas AG", "category": "Consumer", "index": "OTC"},
    "UAA": {"name": "Under Armour Inc. Class A", "category": "Consumer", "index": "NYSE"},
    "UA": {"name": "Under Armour Inc. Class C", "category": "Consumer", "index": "NYSE"},
    "DECK": {"name": "Deckers Outdoor Corporation", "category": "Consumer", "index": "NYSE"},
    "SKX": {"name": "Skechers U.S.A. Inc.", "category": "Consumer", "index": "NYSE"},
    "FL": {"name": "Foot Locker Inc.", "category": "Consumer", "index": "NYSE"},
    "HIBB": {"name": "Hibbett Inc.", "category": "Consumer", "index": "NASDAQ"},
    "BOOT": {"name": "Boot Barn Holdings Inc.", "category": "Consumer", "index": "NYSE"},
    "ASO": {"name": "Academy Sports and Outdoors", "category": "Consumer", "index": "NASDAQ"},
    "BGFV": {"name": "Big 5 Sporting Goods", "category": "Consumer", "index": "NASDAQ"},
    "DKS": {"name": "Dick's Sporting Goods", "category": "Consumer", "index": "NYSE"},
    "SCVL": {"name": "Shoe Carnival Inc.", "category": "Consumer", "index": "NASDAQ"},
    "WWW": {"name": "Wolverine World Wide", "category": "Consumer", "index": "NYSE"},
    "CAL": {"name": "Caleres Inc.", "category": "Consumer", "index": "NYSE"},
    
    # Technology Hardware & Components
    "HPQ": {"name": "HP Inc.", "category": "Technology", "index": "NYSE"},
    "HPE": {"name": "Hewlett Packard Enterprise", "category": "Technology", "index": "NYSE"},
    "DELL": {"name": "Dell Technologies Inc.", "category": "Technology", "index": "NYSE"},
    "NTAP": {"name": "NetApp Inc.", "category": "Technology", "index": "NASDAQ"},
    "WDC": {"name": "Western Digital Corporation", "category": "Technology", "index": "NASDAQ"},
    "STX": {"name": "Seagate Technology Holdings", "category": "Technology", "index": "NASDAQ"},
    "SMTC": {"name": "Semtech Corporation", "category": "Technology", "index": "NASDAQ"},
    "FLEX": {"name": "Flex Ltd.", "category": "Technology", "index": "NASDAQ"},
    "SANM": {"name": "Sanmina Corporation", "category": "Technology", "index": "NASDAQ"},
    "PLXS": {"name": "Plexus Corp.", "category": "Technology", "index": "NASDAQ"},
    "JNPR": {"name": "Juniper Networks Inc.", "category": "Technology", "index": "NYSE"},
    "FFIV": {"name": "F5 Inc.", "category": "Technology", "index": "NASDAQ"},
    "CYBR": {"name": "CyberArk Software Ltd.", "category": "Technology", "index": "NASDAQ"},
    "PANW": {"name": "Palo Alto Networks Inc.", "category": "Technology", "index": "NASDAQ"},
    "FTNT": {"name": "Fortinet Inc.", "category": "Technology", "index": "NASDAQ"},
    "ZS": {"name": "Zscaler Inc.", "category": "Technology", "index": "NASDAQ"},
    "OKTA": {"name": "Okta Inc.", "category": "Technology", "index": "NASDAQ"},
    "CRWD": {"name": "CrowdStrike Holdings Inc.", "category": "Technology", "index": "NASDAQ"},
    "S": {"name": "SentinelOne Inc.", "category": "Technology", "index": "NYSE"},
    
    # Russell 2000 Small-Cap Growth Stocks
    "ROKU": {"name": "Roku Inc.", "category": "Technology", "index": "Russell2000", "business": "Streaming platform and digital advertising"},
    "PLUG": {"name": "Plug Power Inc.", "category": "Energy", "index": "Russell2000", "business": "Hydrogen fuel cell technology and clean energy solutions"},
    "RIOT": {"name": "Riot Platforms Inc.", "category": "Technology", "index": "Russell2000", "business": "Bitcoin mining and blockchain technology"},
    "MARA": {"name": "Marathon Digital Holdings", "category": "Technology", "index": "Russell2000", "business": "Digital asset technology and Bitcoin mining operations"},
    "PLTR": {"name": "Palantir Technologies", "category": "Technology", "index": "Russell2000", "business": "Big data analytics and software platforms"},
    "SPCE": {"name": "Virgin Galactic Holdings", "category": "Industrials", "index": "Russell2000", "business": "Commercial space travel and aerospace"},
    "SOFI": {"name": "SoFi Technologies Inc.", "category": "Financials", "index": "Russell2000", "business": "Digital financial services and student loans"},
    "AI": {"name": "C3.ai Inc.", "category": "Technology", "index": "Russell2000", "business": "Enterprise AI software applications"},
    "SMCI": {"name": "Super Micro Computer", "category": "Technology", "index": "Russell2000", "business": "High-performance computing and server solutions"},
    "PATH": {"name": "UiPath Inc.", "category": "Technology", "index": "Russell2000", "business": "Robotic process automation software"},
    "FIVN": {"name": "Five9 Inc.", "category": "Technology", "index": "Russell2000", "business": "Cloud contact center software"},
    "SMAR": {"name": "Smartsheet Inc.", "category": "Technology", "index": "Russell2000", "business": "Work management and automation platform"},
    "BILL": {"name": "Bill.com Holdings", "category": "Technology", "index": "Russell2000", "business": "Cloud-based payment software for businesses"},
    "ZEN": {"name": "Zendesk Inc.", "category": "Technology", "index": "Russell2000", "business": "Customer service and engagement platform"},
    "HUBS": {"name": "HubSpot Inc.", "category": "Technology", "index": "Russell2000", "business": "Inbound marketing and sales software"},
    "TEAM": {"name": "Atlassian Corporation", "category": "Technology", "index": "Russell2000", "business": "Team collaboration and productivity software"},
    "CFLT": {"name": "Confluent Inc.", "category": "Technology", "index": "Russell2000", "business": "Data streaming platform"},
    "NET": {"name": "Cloudflare Inc.", "category": "Technology", "index": "Russell2000", "business": "Web performance and security services"},
    "FSLY": {"name": "Fastly Inc.", "category": "Technology", "index": "Russell2000", "business": "Edge cloud platform services"},
    "U": {"name": "Unity Software Inc.", "category": "Technology", "index": "Russell2000", "business": "3D content creation platform"},
    "RBLX": {"name": "Roblox Corporation", "category": "Technology", "index": "Russell2000", "business": "Online gaming and metaverse platform"},
    "ZM": {"name": "Zoom Video Communications", "category": "Technology", "index": "Russell2000", "business": "Video conferencing and communication platform"},
    "DOCU": {"name": "DocuSign Inc.", "category": "Technology", "index": "Russell2000", "business": "Electronic signature and digital transaction management"},
    "COUP": {"name": "Coupa Software Inc.", "category": "Technology", "index": "Russell2000", "business": "Business spend management platform"},
    "ESTC": {"name": "Elastic N.V.", "category": "Technology", "index": "Russell2000", "business": "Search and data analytics platform"},
    "TWLO": {"name": "Twilio Inc.", "category": "Technology", "index": "Russell2000", "business": "Cloud communications and customer engagement"},
    "OKTA": {"name": "Okta Inc.", "category": "Technology", "index": "Russell2000", "business": "Identity and access management cloud software"},
    "ZS": {"name": "Zscaler Inc.", "category": "Technology", "index": "Russell2000", "business": "Cloud security platform"},
    "CRWD": {"name": "CrowdStrike Holdings", "category": "Technology", "index": "Russell2000", "business": "Cybersecurity and endpoint protection"},
    "SNOW": {"name": "Snowflake Inc.", "category": "Technology", "index": "Russell2000", "business": "Cloud-based data warehousing"},
    "DDOG": {"name": "Datadog Inc.", "category": "Technology", "index": "Russell2000", "business": "Monitoring and analytics platform"},
    "MDB": {"name": "MongoDB Inc.", "category": "Technology", "index": "Russell2000", "business": "Modern database platform"},
    
    # Russell 2000 Healthcare & Biotech
    "TDOC": {"name": "Teladoc Health Inc.", "category": "Healthcare", "index": "Russell2000", "business": "Virtual healthcare and telemedicine"},
    "EXAS": {"name": "Exact Sciences Corporation", "category": "Healthcare", "index": "Russell2000", "business": "Cancer screening and diagnostic tests"},
    "TWST": {"name": "Twist Bioscience Corporation", "category": "Healthcare", "index": "Russell2000", "business": "Synthetic DNA manufacturing"},
    "NVTA": {"name": "Invitae Corporation", "category": "Healthcare", "index": "Russell2000", "business": "Genetic testing and diagnostics"},
    "PACB": {"name": "Pacific Biosciences", "category": "Healthcare", "index": "Russell2000", "business": "DNA sequencing technology"},
    "RXRX": {"name": "Recursion Pharmaceuticals", "category": "Healthcare", "index": "Russell2000", "business": "AI-driven drug discovery"},
    "DNA": {"name": "Ginkgo Bioworks Holdings", "category": "Healthcare", "index": "Russell2000", "business": "Synthetic biology platform"},
    "CRSP": {"name": "CRISPR Therapeutics AG", "category": "Healthcare", "index": "Russell2000", "business": "Gene editing and cell therapy"},
    "EDIT": {"name": "Editas Medicine Inc.", "category": "Healthcare", "index": "Russell2000", "business": "Genome editing medicines"},
    "NTLA": {"name": "Intellia Therapeutics", "category": "Healthcare", "index": "Russell2000", "business": "CRISPR gene editing therapeutics"},
    "BEAM": {"name": "Beam Therapeutics Inc.", "category": "Healthcare", "index": "Russell2000", "business": "Base editing and gene therapy"},
    "PRIME": {"name": "Prime Medicine Inc.", "category": "Healthcare", "index": "Russell2000", "business": "Prime editing technology"},
    "MRNA": {"name": "Moderna Inc.", "category": "Healthcare", "index": "Russell2000", "business": "mRNA vaccines and therapeutics"},
    "BNTX": {"name": "BioNTech SE", "category": "Healthcare", "index": "Russell2000", "business": "Immunotherapy and mRNA vaccines"},
    
    # Russell 2000 Financial Services
    "UPST": {"name": "Upstart Holdings Inc.", "category": "Financials", "index": "Russell2000", "business": "AI-powered lending platform"},
    "LC": {"name": "LendingClub Corporation", "category": "Financials", "index": "Russell2000", "business": "Digital marketplace lending"},
    "OPEN": {"name": "Opendoor Technologies", "category": "Financials", "index": "Russell2000", "business": "Digital real estate platform"},
    "RKT": {"name": "Rocket Companies Inc.", "category": "Financials", "index": "Russell2000", "business": "Digital mortgage and real estate services"},
    "HOOD": {"name": "Robinhood Markets Inc.", "category": "Financials", "index": "Russell2000", "business": "Commission-free stock trading app"},
    "COIN": {"name": "Coinbase Global Inc.", "category": "Financials", "index": "Russell2000", "business": "Cryptocurrency exchange platform"},
    "MSTR": {"name": "MicroStrategy Incorporated", "category": "Technology", "index": "Russell2000", "business": "Business intelligence and Bitcoin treasury"},
    "SQ": {"name": "Block Inc.", "category": "Financials", "index": "Russell2000", "business": "Digital payments and financial services"},
    "AFRM": {"name": "Affirm Holdings Inc.", "category": "Financials", "index": "Russell2000", "business": "Buy now, pay later financial technology"},
    
    # Russell 2000 Consumer & E-commerce
    "PTON": {"name": "Peloton Interactive Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Connected fitness equipment and content"},
    "LULU": {"name": "Lululemon Athletica", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Athletic apparel and accessories"},
    "ETSY": {"name": "Etsy Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Online marketplace for handmade goods"},
    "W": {"name": "Wayfair Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Online home goods and furniture retailer"},
    "CHWY": {"name": "Chewy Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Online pet products and services"},
    "PETS": {"name": "PetMed Express Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Pet prescription medications online"},
    "BARK": {"name": "BARK Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Dog products and subscription services"},
    "SHOP": {"name": "Shopify Inc.", "category": "Technology", "index": "Russell2000", "business": "E-commerce platform and services"},
    "SPOT": {"name": "Spotify Technology SA", "category": "Communication Services", "index": "Russell2000", "business": "Audio streaming and podcast platform"},
    "DKNG": {"name": "DraftKings Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Sports betting and daily fantasy sports"},
    "PENN": {"name": "Penn Entertainment Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Gaming and sports betting"},
    
    # Russell 2000 Clean Energy & EVs
    "FSLR": {"name": "First Solar Inc.", "category": "Energy", "index": "Russell2000", "business": "Solar panels and renewable energy"},
    "ENPH": {"name": "Enphase Energy Inc.", "category": "Energy", "index": "Russell2000", "business": "Solar microinverters and energy management"},
    "SEDG": {"name": "SolarEdge Technologies", "category": "Energy", "index": "Russell2000", "business": "Solar power optimization and monitoring"},
    "RUN": {"name": "Sunrun Inc.", "category": "Energy", "index": "Russell2000", "business": "Residential solar energy services"},
    "BE": {"name": "Bloom Energy Corporation", "category": "Energy", "index": "Russell2000", "business": "Solid oxide fuel cell technology"},
    "FCEL": {"name": "FuelCell Energy Inc.", "category": "Energy", "index": "Russell2000", "business": "Fuel cell power generation"},
    "BLDP": {"name": "Ballard Power Systems", "category": "Energy", "index": "Russell2000", "business": "Hydrogen fuel cell technology"},
    "NKLA": {"name": "Nikola Corporation", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Electric and hydrogen commercial vehicles"},
    "RIDE": {"name": "Lordstown Motors Corp.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Electric pickup trucks"},
    "FSR": {"name": "Fisker Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Electric vehicle design and manufacturing"},
    "LCID": {"name": "Lucid Group Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Luxury electric vehicles"},
    "RIVN": {"name": "Rivian Automotive Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Electric pickup trucks and delivery vans"},
    
    # Russell 2000 Popular Meme Stocks
    "AMC": {"name": "AMC Entertainment Holdings", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Movie theater chain and entertainment"},
    "GME": {"name": "GameStop Corp.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Video game retailer and NFT marketplace"},
    "BB": {"name": "BlackBerry Limited", "category": "Technology", "index": "Russell2000", "business": "Cybersecurity and IoT software"},
    "NOK": {"name": "Nokia Corporation", "category": "Technology", "index": "Russell2000", "business": "Telecommunications equipment and 5G technology"},
    "SNDL": {"name": "Sundial Growers Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Cannabis cultivation and retail"},
    "CLOV": {"name": "Clover Health Investments", "category": "Healthcare", "index": "Russell2000", "business": "Medicare Advantage health insurance"},
    "WISH": {"name": "ContextLogic Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "E-commerce marketplace platform"},
    "TLRY": {"name": "Tilray Brands Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Cannabis products and beverages"},
    "ACB": {"name": "Aurora Cannabis Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Cannabis cultivation and distribution"},
    
    # Russell 2000 Transportation & Logistics
    "UBER": {"name": "Uber Technologies Inc.", "category": "Technology", "index": "Russell2000", "business": "Ride-sharing and food delivery platform"},
    "LYFT": {"name": "Lyft Inc.", "category": "Technology", "index": "Russell2000", "business": "Ride-sharing and transportation services"},
    "DASH": {"name": "DoorDash Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Food delivery and logistics platform"},
    "ABNB": {"name": "Airbnb Inc.", "category": "Consumer Discretionary", "index": "Russell2000", "business": "Vacation rental and travel platform"},
    
    # Russell 2000 Social Media & Entertainment
    "SNAP": {"name": "Snap Inc.", "category": "Communication Services", "index": "Russell2000", "business": "Multimedia messaging and AR platform"},
    "PINS": {"name": "Pinterest Inc.", "category": "Communication Services", "index": "Russell2000", "business": "Visual discovery and social media platform"},
    "TWTR": {"name": "Twitter Inc.", "category": "Communication Services", "index": "Russell2000", "business": "Social media and microblogging platform"},
    

}

def search_stocks_by_name(query):
    """Search stocks by company name or ticker including expanded database and discovered stocks"""
    # First try the enhanced search that includes discovered stocks
    try:
        from stock_universe_updater import search_all_stocks_including_discovered
        return search_all_stocks_including_discovered(query)
    except ImportError:
        # Fallback to traditional search if updater not available
        pass
    query = query.lower()
    results = []
    
    # Get combined stock database
    all_stocks = COMPREHENSIVE_STOCKS.copy()
    
    # Add expanded database
    try:
        expanded_stocks = get_expanded_stock_database()
        for ticker, info in expanded_stocks.items():
            if ticker not in all_stocks:
                all_stocks[ticker] = {
                    'name': info['name'],
                    'category': info['sector'],
                    'index': info.get('type', 'Stock')
                }
    except Exception:
        pass
    
    for ticker, info in all_stocks.items():
        # Search by ticker or company name
        if (query in ticker.lower() or 
            query in info['name'].lower()):
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'category': info['category']
            })
    
    return results[:50]  # Limit results

def get_all_tickers():
    """Get all available tickers including expanded database"""
    all_stocks = COMPREHENSIVE_STOCKS.copy()
    
    # Add expanded database (500+ additional stocks)
    try:
        expanded_stocks = get_expanded_stock_database()
        # Convert expanded format to comprehensive format
        for ticker, info in expanded_stocks.items():
            if ticker not in all_stocks:
                all_stocks[ticker] = {
                    'name': info['name'],
                    'category': info['sector'],
                    'index': info.get('type', 'Stock'),
                    'market_cap': info.get('market_cap', 'Unknown'),
                    'country': info.get('country', 'USA')
                }
    except Exception as e:
        pass  # Continue with original database if expanded fails
    
    return list(all_stocks.keys())

def get_stock_info(ticker):
    """Get stock information"""
    return COMPREHENSIVE_STOCKS.get(ticker, {"name": ticker, "category": "Unknown", "index": "Unknown"})

def get_stocks_by_category(category):
    """Get stocks by category"""
    return [ticker for ticker, info in COMPREHENSIVE_STOCKS.items() if info['category'] == category]

def get_stocks_by_index(index):
    """Get stocks by index"""
    return [ticker for ticker, info in COMPREHENSIVE_STOCKS.items() if info['index'] == index]

def get_all_categories():
    """Get all available categories"""
    return list(set(info['category'] for info in COMPREHENSIVE_STOCKS.values()))

def get_all_indices():
    """Get all available indices"""
    return list(set(info['index'] for info in COMPREHENSIVE_STOCKS.values()))