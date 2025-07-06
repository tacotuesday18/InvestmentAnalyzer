"""
Company logo utility functions for displaying logos throughout the website
"""
import streamlit as st
import requests
from PIL import Image
import io

def get_company_logo_url(ticker):
    """
    Get company logo URL from various sources
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
        
    Returns:
    --------
    str
        Logo URL or None if not found
    """
    # Primary logo sources with fallbacks
    logo_sources = [
        f"https://logo.clearbit.com/{get_company_domain(ticker)}",
        f"https://companiesmarketcap.com/img/company-logos/64/{ticker}.webp",
        f"https://assets.finnhub.io/logo/{ticker}.png",
        f"https://s3.polygon.io/logos/{ticker.lower()}/logo.png"
    ]
    
    for url in logo_sources:
        try:
            response = requests.head(url, timeout=3)
            if response.status_code == 200:
                return url
        except:
            continue
    
    return None

def get_company_domain(ticker):
    """
    Map ticker symbols to company domains for Clearbit logos
    """
    domain_mapping = {
        'AAPL': 'apple.com',
        'MSFT': 'microsoft.com',
        'GOOGL': 'google.com',
        'GOOG': 'google.com',
        'AMZN': 'amazon.com',
        'TSLA': 'tesla.com',
        'META': 'meta.com',
        'NVDA': 'nvidia.com',
        'BRK.B': 'berkshirehathaway.com',
        'JPM': 'jpmorganchase.com',
        'JNJ': 'jnj.com',
        'V': 'visa.com',
        'PG': 'pg.com',
        'UNH': 'unitedhealthgroup.com',
        'HD': 'homedepot.com',
        'MA': 'mastercard.com',
        'BAC': 'bankofamerica.com',
        'ABBV': 'abbvie.com',
        'PFE': 'pfizer.com',
        'KO': 'coca-cola.com',
        'AVGO': 'broadcom.com',
        'PEP': 'pepsico.com',
        'TMO': 'thermofisher.com',
        'COST': 'costco.com',
        'DIS': 'disney.com',
        'ABT': 'abbott.com',
        'ACN': 'accenture.com',
        'LLY': 'lilly.com',
        'VZ': 'verizon.com',
        'WMT': 'walmart.com',
        'NFLX': 'netflix.com',
        'ADBE': 'adobe.com',
        'DHR': 'danaher.com',
        'NKE': 'nike.com',
        'TXN': 'ti.com',
        'CVX': 'chevron.com',
        'XOM': 'exxonmobil.com',
        'ORCL': 'oracle.com',
        'WFC': 'wellsfargo.com',
        'BMY': 'bms.com',
        'LIN': 'linde.com',
        'AMGN': 'amgen.com',
        'HON': 'honeywell.com',
        'QCOM': 'qualcomm.com',
        'PM': 'pmi.com',
        'RTX': 'rtx.com',
        'NEE': 'nexteraenergy.com',
        'LOW': 'lowes.com',
        'T': 'att.com',
        'UPS': 'ups.com',
        'IBM': 'ibm.com',
        'SPGI': 'spglobal.com',
        'GS': 'goldmansachs.com',
        'MDT': 'medtronic.com',
        'CRM': 'salesforce.com',
        'BLK': 'blackrock.com',
        'CAT': 'caterpillar.com',
        'DE': 'deere.com',
        'GILD': 'gilead.com',
        'AXP': 'americanexpress.com',
        'MO': 'altria.com',
        'ISRG': 'intuitive.com',
        'SCHW': 'schwab.com',
        'AMD': 'amd.com',
        'TGT': 'target.com',
        'INTU': 'intuit.com',
        'ZTS': 'zoetis.com',
        'MU': 'micron.com',
        'MS': 'morganstanley.com',
        'NOW': 'servicenow.com',
        'C': 'citigroup.com',
        'BKNG': 'booking.com',
        'AMAT': 'appliedmaterials.com',
        'ELV': 'elevancehealth.com',
        'CVS': 'cvshealth.com',
        'PLD': 'prologis.com',
        'SYK': 'stryker.com',
        'TFC': 'truist.com',
        'REGN': 'regeneron.com',
        'MMM': '3m.com',
        'AON': 'aon.com',
        'CI': 'cigna.com',
        'DUK': 'duke-energy.com',
        'SO': 'southerncompany.com',
        'BSX': 'bostonscientific.com',
        'ICE': 'theice.com',
        'PYPL': 'paypal.com',
        'CME': 'cmegroup.c com',
        'WM': 'wm.com',
        'ITW': 'itw.com',
        'EQIX': 'equinix.com',
        'APD': 'airproducts.com',
        'USB': 'usbank.com',
        'GE': 'ge.com',
        'SHW': 'sherwin-williams.com',
        'CL': 'colgatepalmolive.com',
        'NSC': 'nscorp.com',
        'LRCX': 'lamresearch.com',
        'MCO': 'moodys.com',
        'EMR': 'emerson.com',
        'FDX': 'fedex.com',
        'CSX': 'csx.com',
        'MCD': 'mcdonalds.com',
        'ADI': 'analog.com',
        'MDLZ': 'mondelezinternational.com',
        'RCL': 'royalcaribbean.com',
        'NCLH': 'nclh.com',
        'CCL': 'carnival.com'
    }
    
    return domain_mapping.get(ticker, f"{ticker.lower()}.com")

def display_company_logo(ticker, company_name="", size="small"):
    """
    Display company logo in Streamlit
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    company_name : str, optional
        Company name to display alongside logo
    size : str
        Logo size - "small", "medium", or "large"
    """
    logo_url = get_company_logo_url(ticker)
    
    if logo_url:
        try:
            # Set size parameters
            size_mapping = {
                "small": 40,
                "medium": 60,
                "large": 80
            }
            logo_size = size_mapping.get(size, 40)
            
            # Display logo with company info
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.image(logo_url, width=logo_size)
            
            with col2:
                if company_name:
                    st.markdown(f"**{company_name} ({ticker})**")
                else:
                    st.markdown(f"**{ticker}**")
                    
        except Exception as e:
            # Fallback to text display if logo fails
            if company_name:
                st.markdown(f"**{company_name} ({ticker})**")
            else:
                st.markdown(f"**{ticker}**")
    else:
        # No logo found, display text only
        if company_name:
            st.markdown(f"**{company_name} ({ticker})**")
        else:
            st.markdown(f"**{ticker}**")

def display_logo_header(ticker, company_name="", subtitle=""):
    """
    Display a header with company logo and information
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    company_name : str, optional
        Company name
    subtitle : str, optional
        Additional subtitle text
    """
    logo_url = get_company_logo_url(ticker)
    
    if logo_url:
        try:
            col1, col2 = st.columns([1, 6])
            
            with col1:
                st.image(logo_url, width=60)
            
            with col2:
                if company_name:
                    st.markdown(f"# {company_name} ({ticker})")
                else:
                    st.markdown(f"# {ticker}")
                
                if subtitle:
                    st.markdown(f"*{subtitle}*")
                    
        except Exception as e:
            # Fallback to text header
            if company_name:
                st.markdown(f"# {company_name} ({ticker})")
            else:
                st.markdown(f"# {ticker}")
            
            if subtitle:
                st.markdown(f"*{subtitle}*")
    else:
        # No logo, display text header
        if company_name:
            st.markdown(f"# {company_name} ({ticker})")
        else:
            st.markdown(f"# {ticker}")
        
        if subtitle:
            st.markdown(f"*{subtitle}*")

def get_logo_html(ticker, size=40):
    """
    Get HTML for company logo (for use in markdown)
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    size : int
        Logo size in pixels
        
    Returns:
    --------
    str
        HTML string for logo or empty string if not found
    """
    logo_url = get_company_logo_url(ticker)
    
    if logo_url:
        return f'<img src="{logo_url}" width="{size}" style="vertical-align: middle; margin-right: 10px;">'
    
    return ""