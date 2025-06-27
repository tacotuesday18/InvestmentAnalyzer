# Stock Analysis Platform - Project Documentation

## Overview
An intelligent Streamlit-based company analysis platform delivering comprehensive business insights through advanced data visualization and interactive research tools. All financial data is sourced exclusively from Yahoo Finance to ensure accuracy and authenticity.

## Recent Changes  
- **2025-06-27**: INTEGRATED CHATGPT API - Added comprehensive ChatGPT analysis for historical metrics and current stock evaluation
- **2025-06-27**: Enhanced earnings page with ChatGPT investment evaluation, target price analysis, and risk assessment
- **2025-06-27**: Created Japanese earnings transcript translation capability using ChatGPT API
- **2025-06-27**: Added ChatGPT-generated industry benchmark analysis when historical data unavailable
- **2025-06-27**: Fixed comparison page indentation errors preventing proper functionality
- **2025-06-27**: Enhanced earnings transcript sources to use Investing.com and Seeking Alpha as primary sources
- **2025-06-27**: Auto-generates individual stock comparison charts when clicking "比較を実行" (no separate button needed)
- **2025-06-27**: Enhanced earnings analysis to focus on specific quarterly business developments and actual events
- **2025-06-27**: Removed synthetic historical PE/PB/PS ratios that were showing inaccurate values (like Google PE 13.91)
- **2025-06-26**: FIXED NAVIGATION - Completely rebuilt app.py to enable proper Streamlit sidebar page navigation
- **2025-06-26**: Single hamburger button (☰) in top-left corner opens/closes sidebar with clickable page links
- **2025-06-26**: Removed all custom navigation logic that was preventing page switching
- **2025-06-26**: Styled sidebar navigation with proper hover effects and active page highlighting
- **2025-06-26**: Completely redesigned fundamental analysis page as research paper format (no numbers, business-focused)
- **2025-06-26**: Removed buy/sell recommendations from earnings page, replaced with objective financial scoring
- **2025-06-26**: Fixed income statement page indentation error and all page functionality
- **2025-06-26**: Added comprehensive USD/JPY currency converter for Japanese investors
- **2025-06-26**: Created new education page with investment fundamentals and platform tutorials
- **2025-06-26**: Integrated real-time currency conversion on stock analysis pages
- **2025-06-26**: Enhanced earnings page with comprehensive investment metrics (PE, PS, PB, PEG, Beta, Dividend)
- **2025-06-26**: Added company name search functionality across all pages
- **2025-06-26**: Implemented historical metrics charts (PE, PS, PB, PEG trends) across all pages

## Project Architecture

### Core Pages
1. **Business Model Analysis** - Deep dive into company fundamentals with live Yahoo Finance data
2. **Stock Comparison** - Multi-company financial comparison with authentic metrics
3. **Financial Statements** - Detailed financial data from Yahoo Finance
4. **DCF Calculator** - Discounted cash flow valuation tool
5. **Earnings Analysis** - Latest earnings data and trends
6. **Stock Discovery** - New screening tool for retail investors

### Key Features
- Live Yahoo Finance data integration
- Comprehensive financial health scoring
- Investment style presets (Growth, Value, Dividend, Stability)
- Real-time stock screening with customizable criteria
- USD/JPY currency conversion for Japanese investors
- Interactive investment education center
- Historical metrics trend analysis
- Multi-language support (Japanese/English)

### Technology Stack
- **Backend**: Python, Streamlit
- **Data Sources**: Yahoo Finance (yfinance)
- **Visualization**: Plotly, Chart.js
- **Database**: PostgreSQL for user data

## Data Integrity Policy
- All financial metrics sourced from Yahoo Finance
- No synthetic or placeholder data
- Real-time earnings data integration
- Proper error handling for unavailable data

## User Preferences
- Focus on authentic financial data accuracy
- Emphasis on retail investor accessibility
- Japanese language interface preferred
- Clean, professional UI without excessive emojis

## Navigation Structure
```
Home
├── Business Model Analysis (ビジネスモデル分析)
├── Stock Comparison (銘柄比較)
├── Financial Statements (財務諸表)
├── DCF Calculator (DCF価値計算機)
├── Stock Discovery (銘柄発見)
├── Earnings Analysis (決算分析)
└── Investment Education (投資教育) [NEW]
```

## Stock Discovery Tool Features
- Investment style presets for different investor types
- Customizable financial criteria screening
- Sector and market cap filtering
- Real-time data from Yahoo Finance
- Educational investment guidance
- Performance metrics visualization

## Recent Fixes
- Fixed KeyError in fundamental analysis growth calculations
- Resolved TypeError in stock comparison null value handling
- Updated all financial data to use live Yahoo Finance sources
- Added comprehensive null value handling across all pages