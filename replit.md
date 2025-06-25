# Stock Analysis Platform - Project Documentation

## Overview
An intelligent Streamlit-based company analysis platform delivering comprehensive business insights through advanced data visualization and interactive research tools. All financial data is sourced exclusively from Yahoo Finance to ensure accuracy and authenticity.

## Recent Changes
- **2025-06-25**: Added comprehensive stock discovery tool for retail investors
- **2025-06-25**: Fixed business model analysis to use only live Yahoo Finance data
- **2025-06-25**: Enhanced financial health metrics with proper null handling
- **2025-06-25**: Replaced all hardcoded financial data with authentic earnings data

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
├── Stock Discovery (銘柄発見) [NEW]
└── Earnings Analysis (決算分析)
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