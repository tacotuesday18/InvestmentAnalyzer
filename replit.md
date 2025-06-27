# Stock Analysis Platform - Project Documentation

## Overview
An intelligent Streamlit-based company analysis platform delivering comprehensive business insights through advanced data visualization and interactive research tools. All financial data is sourced exclusively from Yahoo Finance to ensure accuracy and authenticity.

## Recent Changes
- **2025-06-27**: STREAMLINED USER EXPERIENCE - Removed duplicate functionality to reduce confusion across pages
- **2025-06-27**: Enhanced industry benchmarks with realistic multiples for AI/tech vs traditional sectors
- **2025-06-27**: Fixed session state management to prevent page resets when changing comparison periods
- **2025-06-27**: Removed OpenAI API key requirements and implemented comprehensive earnings analysis
- **2025-06-27**: Improved earnings transcript extraction with company-specific investor relations sources
- **2025-06-27**: Simplified fundamental analysis page by removing redundant historical metrics section
- **2025-06-27**: Added individual stock comparison charts to comparison page for direct performance analysis
- **2025-06-27**: Created market comparison module for stock vs index performance visualization
- **2025-06-27**: Enhanced earnings page with business-focused fundamental analysis and improved formatting
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