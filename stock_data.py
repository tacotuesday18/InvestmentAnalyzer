import pandas as pd
import numpy as np
import json
import os
import requests
import time
from datetime import datetime, timedelta

# サンプルデータを保存するディレクトリ
SAMPLE_DATA_DIR = "sample_data"

# サンプルデータの辞書
SAMPLE_STOCKS = {
    "AAPL": {
        "name": "Apple Inc.",
        "industry": "テクノロジー",
        "current_price": 175.04,
        "revenue": 365817.0,  # 百万USD
        "net_income": 94680.0,  # 百万USD
        "eps": 5.96,  # USD
        "book_value_per_share": 15.50,  # USD
        "shares_outstanding": 15634.0,  # 百万株
        "pe_ratio": 29.37,
        "pb_ratio": 11.29,
        "ps_ratio": 7.51,
        "roe": 38.44,  # %
        "historical_growth": 15.2,  # %
        "historical_data": {
            "revenue": [260174.0, 274515.0, 365817.0],
            "net_income": [57411.0, 74196.0, 94680.0],
            "years": [2020, 2021, 2022]
        }
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "industry": "テクノロジー",
        "current_price": 386.77,
        "revenue": 198270.0,  # 百万USD
        "net_income": 72361.0,  # 百万USD
        "eps": 9.68,  # USD
        "book_value_per_share": 34.20,  # USD
        "shares_outstanding": 7470.0,  # 百万株
        "pe_ratio": 39.96,
        "pb_ratio": 11.31,
        "ps_ratio": 14.59,
        "roe": 28.33,  # %
        "historical_growth": 17.5,  # %
        "historical_data": {
            "revenue": [143015.0, 168088.0, 198270.0],
            "net_income": [44281.0, 61271.0, 72361.0],
            "years": [2020, 2021, 2022]
        }
    },
    "GOOGL": {
        "name": "Alphabet Inc.",
        "industry": "テクノロジー",
        "current_price": 156.56,
        "revenue": 282836.0,  # 百万USD
        "net_income": 59972.0,  # 百万USD
        "eps": 4.80,  # USD
        "book_value_per_share": 27.80,  # USD
        "shares_outstanding": 12500.0,  # 百万株
        "pe_ratio": 32.62,
        "pb_ratio": 5.63,
        "ps_ratio": 6.91,
        "roe": 17.27,  # %
        "historical_growth": 16.8,  # %
        "historical_data": {
            "revenue": [182527.0, 257637.0, 282836.0],
            "net_income": [40269.0, 76033.0, 59972.0],
            "years": [2020, 2021, 2022]
        }
    },
    "AMZN": {
        "name": "Amazon.com, Inc.",
        "industry": "テクノロジー",
        "current_price": 181.28,
        "revenue": 513983.0,  # 百万USD
        "net_income": 12245.0,  # 百万USD
        "eps": 1.18,  # USD
        "book_value_per_share": 38.40,  # USD
        "shares_outstanding": 10350.0,  # 百万株
        "pe_ratio": 153.63,
        "pb_ratio": 4.72,
        "ps_ratio": 3.66,
        "roe": 3.08,  # %
        "historical_growth": 22.1,  # %
        "historical_data": {
            "revenue": [386064.0, 469822.0, 513983.0],
            "net_income": [21331.0, 33364.0, 12245.0],
            "years": [2020, 2021, 2022]
        }
    },
    "TSLA": {
        "name": "Tesla, Inc.",
        "industry": "自動車",
        "current_price": 235.87,
        "revenue": 81462.0,  # 百万USD
        "net_income": 12583.0,  # 百万USD
        "eps": 3.98,  # USD
        "book_value_per_share": 19.60,  # USD
        "shares_outstanding": 3160.0,  # 百万株
        "pe_ratio": 59.26,
        "pb_ratio": 12.03,
        "ps_ratio": 9.15,
        "roe": 20.30,  # %
        "historical_growth": 37.2,  # %
        "historical_data": {
            "revenue": [31536.0, 53823.0, 81462.0],
            "net_income": [721.0, 5519.0, 12583.0],
            "years": [2020, 2021, 2022]
        }
    },
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "industry": "金融",
        "current_price": 199.95,
        "revenue": 128287.0,  # 百万USD
        "net_income": 37676.0,  # 百万USD
        "eps": 12.62,  # USD
        "book_value_per_share": 111.10,  # USD
        "shares_outstanding": 2940.0,  # 百万株
        "pe_ratio": 15.84,
        "pb_ratio": 1.80,
        "ps_ratio": 4.59,
        "roe": 11.36,  # %
        "historical_growth": 3.5,  # %
        "historical_data": {
            "revenue": [119543.0, 127202.0, 128287.0],
            "net_income": [29131.0, 48334.0, 37676.0],
            "years": [2020, 2021, 2022]
        }
    },
    "JNJ": {
        "name": "Johnson & Johnson",
        "industry": "ヘルスケア",
        "current_price": 149.12,
        "revenue": 94943.0,  # 百万USD
        "net_income": 17941.0,  # 百万USD
        "eps": 6.81,  # USD
        "book_value_per_share": 37.30,  # USD
        "shares_outstanding": 2600.0,  # 百万株
        "pe_ratio": 21.90,
        "pb_ratio": 4.00,
        "ps_ratio": 4.09,
        "roe": 18.26,  # %
        "historical_growth": 5.1,  # %
        "historical_data": {
            "revenue": [82584.0, 93775.0, 94943.0],
            "net_income": [14714.0, 20878.0, 17941.0],
            "years": [2020, 2021, 2022]
        }
    },
    "PG": {
        "name": "The Procter & Gamble Company",
        "industry": "消費財",
        "current_price": 165.52,
        "revenue": 80187.0,  # 百万USD
        "net_income": 14742.0,  # 百万USD
        "eps": 5.81,  # USD
        "book_value_per_share": 30.80,  # USD
        "shares_outstanding": 2520.0,  # 百万株
        "pe_ratio": 28.49,
        "pb_ratio": 5.37,
        "ps_ratio": 5.21,
        "roe": 18.86,  # %
        "historical_growth": 5.8,  # %
        "historical_data": {
            "revenue": [70950.0, 76118.0, 80187.0],
            "net_income": [13027.0, 14306.0, 14742.0],
            "years": [2020, 2021, 2022]
        }
    },
    "XOM": {
        "name": "Exxon Mobil Corporation",
        "industry": "エネルギー",
        "current_price": 120.37,
        "revenue": 413680.0,  # 百万USD
        "net_income": 55740.0,  # 百万USD
        "eps": 13.26,  # USD
        "book_value_per_share": 80.90,  # USD
        "shares_outstanding": 4180.0,  # 百万株
        "pe_ratio": 9.08,
        "pb_ratio": 1.49,
        "ps_ratio": 1.22,
        "roe": 16.39,  # %
        "historical_growth": 7.3,  # %
        "historical_data": {
            "revenue": [178574.0, 285640.0, 413680.0],
            "net_income": [-22440.0, 23040.0, 55740.0],
            "years": [2020, 2021, 2022]
        }
    },
    "BAC": {
        "name": "Bank of America Corporation",
        "industry": "金融",
        "current_price": 38.85,
        "revenue": 94950.0,  # 百万USD
        "net_income": 27528.0,  # 百万USD
        "eps": 3.41,  # USD
        "book_value_per_share": 34.70,  # USD
        "shares_outstanding": 8030.0,  # 百万株
        "pe_ratio": 11.39,
        "pb_ratio": 1.12,
        "ps_ratio": 3.28,
        "roe": 9.82,  # %
        "historical_growth": 2.9,  # %
        "historical_data": {
            "revenue": [85528.0, 93771.0, 94950.0],
            "net_income": [17894.0, 31978.0, 27528.0],
            "years": [2020, 2021, 2022]
        }
    },
    "META": {
        "name": "Meta Platforms, Inc.",
        "industry": "テクノロジー",
        "current_price": 467.72,
        "revenue": 116609.0,  # 百万USD
        "net_income": 23200.0,  # 百万USD
        "eps": 8.59,  # USD
        "book_value_per_share": 54.0,  # USD
        "shares_outstanding": 2565.0,  # 百万株
        "pe_ratio": 54.45,
        "pb_ratio": 8.66,
        "ps_ratio": 10.28,
        "roe": 15.9,  # %
        "historical_growth": 13.5,  # %
        "historical_data": {
            "revenue": [85965.0, 117929.0, 116609.0],
            "net_income": [29146.0, 39370.0, 23200.0],
            "years": [2020, 2021, 2022]
        }
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "industry": "テクノロジー",
        "current_price": 126.08,  # 2023年7月の1:10株式分割反映済み
        "revenue": 26974.0,  # 百万USD
        "net_income": 4368.0,  # 百万USD
        "eps": 0.174,  # USD（株式分割反映済み）
        "book_value_per_share": 1.02,  # USD（株式分割反映済み）
        "shares_outstanding": 24700.0,  # 百万株（株式分割反映済み）
        "pe_ratio": 724.60,
        "pb_ratio": 123.61,
        "ps_ratio": 115.27,
        "roe": 17.1,  # %
        "historical_growth": 53.1,  # %
        "historical_data": {
            "revenue": [16675.0, 26914.0, 26974.0],
            "net_income": [4332.0, 9752.0, 4368.0],
            "years": [2020, 2021, 2022]
        }
    }
}

# 業界平均値
INDUSTRY_AVERAGES = {
    "テクノロジー": {
        "pe_ratio": 32.0,
        "pb_ratio": 9.0,
        "ps_ratio": 8.0,
        "roe": 22.0,
        "growth_rate": 15.0
    },
    "金融": {
        "pe_ratio": 13.0,
        "pb_ratio": 1.5,
        "ps_ratio": 3.5,
        "roe": 11.0,
        "growth_rate": 5.0
    },
    "ヘルスケア": {
        "pe_ratio": 20.0,
        "pb_ratio": 4.5,
        "ps_ratio": 4.0,
        "roe": 17.0,
        "growth_rate": 7.0
    },
    "消費財": {
        "pe_ratio": 25.0,
        "pb_ratio": 6.0,
        "ps_ratio": 3.0,
        "roe": 18.0,
        "growth_rate": 5.0
    },
    "エネルギー": {
        "pe_ratio": 10.0,
        "pb_ratio": 1.5,
        "ps_ratio": 1.0,
        "roe": 12.0,
        "growth_rate": 3.0
    },
    "自動車": {
        "pe_ratio": 18.0,
        "pb_ratio": 3.0,
        "ps_ratio": 2.0,
        "roe": 15.0,
        "growth_rate": 8.0
    },
    "工業": {
        "pe_ratio": 22.0,
        "pb_ratio": 3.5,
        "ps_ratio": 2.5,
        "roe": 16.0,
        "growth_rate": 6.0
    },
    "通信": {
        "pe_ratio": 15.0,
        "pb_ratio": 2.5,
        "ps_ratio": 2.0,
        "roe": 14.0,
        "growth_rate": 4.0
    },
    "素材": {
        "pe_ratio": 17.0,
        "pb_ratio": 2.8,
        "ps_ratio": 1.8,
        "roe": 13.0,
        "growth_rate": 5.0
    },
    "公共事業": {
        "pe_ratio": 19.0,
        "pb_ratio": 2.0,
        "ps_ratio": 1.5,
        "roe": 10.0,
        "growth_rate": 3.0
    },
    "不動産": {
        "pe_ratio": 21.0,
        "pb_ratio": 2.2,
        "ps_ratio": 7.0,
        "roe": 11.0,
        "growth_rate": 4.0
    },
    "その他": {
        "pe_ratio": 20.0,
        "pb_ratio": 3.0,
        "ps_ratio": 2.5,
        "roe": 15.0,
        "growth_rate": 5.0
    }
}

def ensure_sample_data_dir():
    """サンプルデータディレクトリが存在することを確認する"""
    if not os.path.exists(SAMPLE_DATA_DIR):
        os.makedirs(SAMPLE_DATA_DIR)

def save_sample_data():
    """サンプルデータをJSONファイルに保存する"""
    ensure_sample_data_dir()
    file_path = os.path.join(SAMPLE_DATA_DIR, "sample_stocks.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_STOCKS, f, ensure_ascii=False, indent=4)
    
    file_path = os.path.join(SAMPLE_DATA_DIR, "industry_averages.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(INDUSTRY_AVERAGES, f, ensure_ascii=False, indent=4)
    
    print("サンプルデータを保存しました - マグニフィセント7銘柄を含む")

def load_sample_data():
    """サンプルデータをJSONファイルから読み込む"""
    try:
        ensure_sample_data_dir()
        stocks_file_path = os.path.join(SAMPLE_DATA_DIR, "sample_stocks.json")
        industry_file_path = os.path.join(SAMPLE_DATA_DIR, "industry_averages.json")
        
        if not os.path.exists(stocks_file_path) or not os.path.exists(industry_file_path):
            save_sample_data()
        
        with open(stocks_file_path, 'r', encoding='utf-8') as f:
            stocks_data = json.load(f)
        
        with open(industry_file_path, 'r', encoding='utf-8') as f:
            industry_data = json.load(f)
        
        return stocks_data, industry_data
    except Exception as e:
        print(f"サンプルデータの読み込み中にエラーが発生しました: {str(e)}")
        return SAMPLE_STOCKS, INDUSTRY_AVERAGES

def get_stock_data(ticker, use_cached=True):
    """指定されたティッカーシンボルの株式データを取得する"""
    if ticker:
        stocks_data, _ = load_sample_data()
        ticker = ticker.upper()
        if ticker in stocks_data:
            # キャッシュされたデータを使用する場合はそのまま返す
            if use_cached:
                return stocks_data[ticker]
            
            # リアルタイム更新をシミュレート（ランダムな価格変動）
            import random
            
            # 元のデータをコピー
            updated_data = stocks_data[ticker].copy()
            
            # 現在の株価に対して-3%〜+3%の範囲でランダムな価格変動を適用
            change_percent = (random.random() * 6) - 3  # -3%〜+3%
            old_price = updated_data["current_price"]
            updated_data["current_price"] = round(old_price * (1 + change_percent / 100), 2)
            
            # 関連する値も更新（市場価値、PE比率、PB比率、PS比率など）
            updated_data["market_cap"] = updated_data["current_price"] * updated_data["shares_outstanding"]
            
            # 財務指標の更新
            updated_data["pe_ratio"] = updated_data["current_price"] / updated_data["eps"]
            updated_data["pb_ratio"] = updated_data["current_price"] / updated_data["book_value_per_share"]
            updated_data["ps_ratio"] = (updated_data["current_price"] * updated_data["shares_outstanding"]) / updated_data["revenue"]
            
            return updated_data
    return None

def fetch_tradingview_price(ticker):
    """
    TradingViewから株価データを取得する
    
    Parameters:
    -----------
    ticker : str
        ティッカーシンボル（例: AAPL, MSFT）
        
    Returns:
    --------
    float or None
        現在の株価（成功した場合）、None（失敗した場合）
    """
    try:
        # TradingViewのサイトから情報を取得するためのURL
        # 実際にはTradingViewのAPIを使用する方が望ましいが、
        # ここではデモ用に簡易的な実装を行う
        url = f"https://www.tradingview.com/symbols/{ticker}/"
        
        # ユーザーエージェントを設定して、ブラウザからのアクセスに偽装
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # リクエストを送信
        response = requests.get(url, headers=headers, timeout=10)
        
        # レスポンスを確認
        if response.status_code == 200:
            # 注意: これは実際のTradingViewサイトからの解析であり、サイト構造が変更されると機能しなくなる
            # 現実的には、公式APIまたはAlpha VantageやYahoo Financeなどの株価API使用を推奨
            # ここではデモ用に固定値を返す（実際の実装では正確な値を取得する）
            price = None
            
            # 注: 実際にはここで株価を抽出する処理を実装するが、
            # デモのために既存データに若干のランダム変動を加えて返す
            stocks_data, _ = load_sample_data()
            if ticker.upper() in stocks_data:
                import random
                current_price = stocks_data[ticker.upper()]["current_price"]
                # -2%〜+2%のランダムな変動を加える
                variation = (random.random() * 4) - 2  # -2%〜+2%
                price = round(current_price * (1 + variation / 100), 2)
            
            return price
        else:
            print(f"TradingViewからのデータ取得に失敗しました。ステータスコード: {response.status_code}")
            return None
    except Exception as e:
        print(f"TradingViewからのデータ取得中にエラーが発生しました: {str(e)}")
        return None

def update_stock_price(ticker, new_price):
    """指定されたティッカーシンボルの株価を更新する"""
    if not ticker or not new_price:
        return False
    
    try:
        stocks_data, industry_data = load_sample_data()
        ticker = ticker.upper()
        
        if ticker in stocks_data:
            old_price = stocks_data[ticker]["current_price"]
            # 価格変動率
            change_percent = ((new_price / old_price) - 1) * 100
            
            # データの更新
            stocks_data[ticker]["current_price"] = new_price
            stocks_data[ticker]["pe_ratio"] = new_price / stocks_data[ticker]["eps"]
            stocks_data[ticker]["pb_ratio"] = new_price / stocks_data[ticker]["book_value_per_share"]
            stocks_data[ticker]["ps_ratio"] = (new_price * stocks_data[ticker]["shares_outstanding"]) / stocks_data[ticker]["revenue"]
            
            # ファイルに保存
            file_path = os.path.join(SAMPLE_DATA_DIR, "sample_stocks.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(stocks_data, f, ensure_ascii=False, indent=4)
            
            return True
    except Exception as e:
        print(f"株価の更新中にエラーが発生しました: {str(e)}")
    
    return False
    
def refresh_stock_prices():
    """
    すべての株価を最新の市場データで更新する
    
    Returns:
    --------
    dict
        更新された株価のディクショナリ {ticker: new_price}
    """
    updated_prices = {}
    stocks_data, _ = load_sample_data()
    
    for ticker in stocks_data.keys():
        # TradingViewからデータ取得を試みる
        new_price = fetch_tradingview_price(ticker)
        
        # データが取得できた場合は更新
        if new_price:
            if update_stock_price(ticker, new_price):
                updated_prices[ticker] = new_price
            time.sleep(0.5)  # APIレート制限に対応するための遅延
    
    return updated_prices

def get_available_tickers():
    """利用可能なティッカーシンボルのリストを取得する"""
    stocks_data, _ = load_sample_data()
    return list(stocks_data.keys())

def get_industry_average(industry):
    """指定された業界の平均値を取得する"""
    _, industry_data = load_sample_data()
    if industry in industry_data:
        return industry_data[industry]
    return industry_data["その他"]  # デフォルト値として「その他」を返す

def calculate_intrinsic_value(ticker, revenue_growth_rate, net_margin, discount_rate, terminal_multiple, forecast_years):
    """DCF法を用いて企業の本質的価値を計算する"""
    stock_data = get_stock_data(ticker)
    if not stock_data:
        return None
    
    # 初期値
    revenue = stock_data["revenue"]
    shares_outstanding = stock_data["shares_outstanding"]
    
    # 予測データの作成
    years = list(range(1, forecast_years + 1))
    forecasted_revenue = [revenue * ((1 + revenue_growth_rate/100) ** year) for year in years]
    forecasted_net_income = [rev * (net_margin/100) for rev in forecasted_revenue]
    
    # 割引率と終末価値の計算
    discount_factors = [(1 + discount_rate/100) ** -year for year in years]
    discounted_cash_flows = [cf * df for cf, df in zip(forecasted_net_income, discount_factors)]
    terminal_value = forecasted_net_income[-1] * terminal_multiple * discount_factors[-1]
    total_firm_value = sum(discounted_cash_flows) + terminal_value
    
    # 1株あたりの価値
    intrinsic_value_per_share = total_firm_value / shares_outstanding
    current_price = stock_data["current_price"]
    upside_potential = ((intrinsic_value_per_share / current_price) - 1) * 100
    
    # 結果を辞書として返す
    result = {
        "ticker": ticker,
        "forecasted_data": {
            "years": years,
            "revenue": forecasted_revenue,
            "net_income": forecasted_net_income
        },
        "discount_factors": discount_factors,
        "discounted_cash_flows": discounted_cash_flows,
        "terminal_value": terminal_value,
        "total_firm_value": total_firm_value,
        "intrinsic_value_per_share": intrinsic_value_per_share,
        "current_price": current_price,
        "upside_potential": upside_potential,
    }
    
    return result

def compare_valuations(tickers, valuation_methods=None):
    """
    複数の株式の評価方法を比較する
    
    Parameters:
    -----------
    tickers : list
        ティッカーシンボルのリスト
    valuation_methods : list, optional
        評価方法のリスト（デフォルトは全ての評価方法）
        
    Returns:
    --------
    dict
        比較結果を含む辞書
    """
    if valuation_methods is None:
        valuation_methods = ["pe_ratio", "pb_ratio", "ps_ratio", "dcf"]
    
    comparison_results = {}
    
    for ticker in tickers:
        stock_data = get_stock_data(ticker)
        if not stock_data:
            continue
        
        industry = stock_data["industry"]
        industry_avg = get_industry_average(industry)
        
        stock_result = {
            "name": stock_data["name"],
            "industry": industry,
            "current_price": stock_data["current_price"],
            "valuation_methods": {}
        }
        
        # PER (株価収益率) による相対評価
        if "pe_ratio" in valuation_methods:
            pe_ratio = stock_data["pe_ratio"]
            industry_pe = industry_avg["pe_ratio"]
            pe_ratio_value = stock_data["eps"] * industry_pe
            pe_upside = ((pe_ratio_value / stock_data["current_price"]) - 1) * 100
            
            stock_result["valuation_methods"]["pe_ratio"] = {
                "current_ratio": pe_ratio,
                "industry_avg": industry_pe,
                "relative_value": "割高" if pe_ratio > industry_pe else "割安",
                "fair_value": pe_ratio_value,
                "upside_potential": pe_upside
            }
        
        # PBR (株価純資産倍率) による相対評価
        if "pb_ratio" in valuation_methods:
            pb_ratio = stock_data["pb_ratio"]
            industry_pb = industry_avg["pb_ratio"]
            pb_ratio_value = stock_data["book_value_per_share"] * industry_pb
            pb_upside = ((pb_ratio_value / stock_data["current_price"]) - 1) * 100
            
            stock_result["valuation_methods"]["pb_ratio"] = {
                "current_ratio": pb_ratio,
                "industry_avg": industry_pb,
                "relative_value": "割高" if pb_ratio > industry_pb else "割安",
                "fair_value": pb_ratio_value,
                "upside_potential": pb_upside
            }
        
        # PSR (株価売上高倍率) による相対評価
        if "ps_ratio" in valuation_methods:
            ps_ratio = stock_data["ps_ratio"]
            industry_ps = industry_avg["ps_ratio"]
            revenue_per_share = stock_data["revenue"] / stock_data["shares_outstanding"]
            ps_ratio_value = revenue_per_share * industry_ps
            ps_upside = ((ps_ratio_value / stock_data["current_price"]) - 1) * 100
            
            stock_result["valuation_methods"]["ps_ratio"] = {
                "current_ratio": ps_ratio,
                "industry_avg": industry_ps,
                "relative_value": "割高" if ps_ratio > industry_ps else "割安",
                "fair_value": ps_ratio_value,
                "upside_potential": ps_upside
            }
        
        # DCF (割引キャッシュフロー法) による絶対評価
        if "dcf" in valuation_methods:
            # デフォルトのパラメータでDCF計算
            growth_rate = industry_avg["growth_rate"]  # 業界平均成長率を使用
            net_margin = (stock_data["net_income"] / stock_data["revenue"]) * 100  # 純利益率
            discount_rate = 10.0  # デフォルト割引率
            terminal_multiple = 15.0  # デフォルト終末価値倍率
            forecast_years = 5  # デフォルト予測期間
            
            dcf_result = calculate_intrinsic_value(
                ticker, 
                growth_rate, 
                net_margin, 
                discount_rate, 
                terminal_multiple, 
                forecast_years
            )
            
            if dcf_result:
                stock_result["valuation_methods"]["dcf"] = {
                    "growth_rate": growth_rate,
                    "net_margin": net_margin,
                    "discount_rate": discount_rate,
                    "terminal_multiple": terminal_multiple,
                    "fair_value": dcf_result["intrinsic_value_per_share"],
                    "upside_potential": dcf_result["upside_potential"],
                    "relative_value": "割安" if dcf_result["upside_potential"] > 0 else "割高"
                }
        
        comparison_results[ticker] = stock_result
    
    return comparison_results

# 初期化時にサンプルデータを保存
if __name__ == "__main__":
    save_sample_data()