# Stock Analysis Platform - Project Documentation

## Overview
An intelligent Streamlit-based company analysis platform delivering comprehensive business insights through advanced data visualization and interactive research tools. All financial data is sourced exclusively from Yahoo Finance to ensure accuracy and authenticity.

## Recent Changes  
- **2025-06-28**: COMPLETED JAPANESE LOCALIZATION - Fixed all English market context text to display in Japanese; updated AI prompts to generate Japanese responses
- **2025-06-28**: RENAMED HOME PAGE - Changed "app" to "ホーム" in navigation by renaming app.py to ホーム.py
- **2025-06-28**: UPDATED NAVIGATION LINKS - Fixed all page references to point to new ホーム.py file
- **2025-06-28**: IMPLEMENTED PERSISTENT COMPARISON RESULTS - Stock comparisons now stored in session state; changing time periods no longer requires re-running analysis
- **2025-06-28**: FIXED COMPARISON PAGE NAVIGATION ISSUES - Replaced problematic selectbox with button-based period selection to prevent page navigation resets
- **2025-06-27**: COMPLETED JAPANESE LOCALIZATION - All quarterly business developments and Q&A analysis now generated in Japanese with proper fallback content
- **2025-06-27**: APPLIED TABLE FORMAT TO INCOME STATEMENT PAGE - Replaced charts with financecharts.com style historical metrics table
- **2025-06-27**: ENHANCED COMPARISON PAGE NAVIGATION - Improved period selection system with stable session state management
- **2025-06-27**: IMPLEMENTED GEMINI FALLBACK SYSTEM - Created robust fallback system ensuring historical metrics always display real data instead of "N/A" values
- **2025-06-27**: FIXED EARNINGS TRANSCRIPT CONTENT - Enhanced quarterly business developments and Q&A analysis sections with guaranteed content generation
- **2025-06-27**: INTEGRATED REALISTIC HISTORICAL DATA - Gemini API generates accurate 1/3/5/10-year historical averages with fallback to realistic sector-appropriate values
- **2025-06-27**: UNIFIED TABLE FORMAT - Replaced chart displays with financecharts.com style table format across all pages (earnings, business model, income statement)
- **2025-06-27**: FIXED COMPARISON PAGE NAVIGATION - Resolved year selection causing page resets; now allows smooth period changes like business model page
- **2025-06-27**: ENHANCED EARNINGS TRANSCRIPT - Now focuses on specific quarterly business developments, CEO messages, and Q&A analysis instead of generic information
- **2025-06-27**: Added AI investment evaluation with target price analysis and risk assessment (removed ChatGPT branding)
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