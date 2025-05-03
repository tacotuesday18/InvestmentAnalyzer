import pandas as pd
import numpy as np

def calculate_intrinsic_value(forecasted_data, discount_rate, terminal_multiple, shares_outstanding):
    """
    DCF法を用いた企業の本質的価値を計算する
    
    Parameters:
    -----------
    forecasted_data : pandas.DataFrame
        予測財務データを含むデータフレーム
    discount_rate : float
        割引率（%）
    terminal_multiple : float
        終末価値算出に使用する倍率（通常はPE倍率）
    shares_outstanding : float
        発行済株式数（百万株）
        
    Returns:
    --------
    dict
        本質的価値の計算結果を含む辞書
    """
    # 割引率をパーセンテージから小数に変換
    discount_rate_decimal = discount_rate / 100
    
    # 予測期間の純利益の現在価値を計算
    present_values = []
    
    for i, year in enumerate(forecasted_data['年']):
        if i == 0:  # 初年度（現在）はスキップ
            continue
            
        future_value = forecasted_data['純利益（百万円）'].iloc[i]
        present_value = future_value / ((1 + discount_rate_decimal) ** i)
        present_values.append(present_value)
    
    # 予測期間の純利益の現在価値合計
    total_pv_forecast_period = sum(present_values)
    
    # 終末価値の計算（最終年の純利益 × ターミナル倍率）
    terminal_profit = forecasted_data['純利益（百万円）'].iloc[-1]
    terminal_value = terminal_profit * terminal_multiple
    
    # 終末価値の現在価値
    terminal_year = forecasted_data['年'].iloc[-1]
    present_value_of_terminal_value = terminal_value / ((1 + discount_rate_decimal) ** terminal_year)
    
    # 企業価値（エンタープライズバリュー）の計算
    enterprise_value = total_pv_forecast_period + present_value_of_terminal_value
    
    # 1株あたりの企業価値
    equity_value_per_share = enterprise_value / shares_outstanding
    
    return {
        'total_pv_forecast_period': total_pv_forecast_period,
        'terminal_value': terminal_value,
        'present_value_of_terminal_value': present_value_of_terminal_value,
        'enterprise_value': enterprise_value,
        'dcf_per_share': equity_value_per_share
    }

def calculate_financial_ratios(market_cap, revenue, net_income, book_value, shares_outstanding):
    """
    主要な財務指標を計算する
    
    Parameters:
    -----------
    market_cap : float
        時価総額（百万円）
    revenue : float
        売上高（百万円）
    net_income : float
        純利益（百万円）
    book_value : float
        純資産（百万円）
    shares_outstanding : float
        発行済株式数（百万株）
        
    Returns:
    --------
    dict
        財務指標の計算結果を含む辞書
    """
    # 各指標の計算
    eps = (net_income * 1000000) / (shares_outstanding * 1000000) if shares_outstanding > 0 else 0
    
    pe_ratio = market_cap / net_income if net_income > 0 else float('inf')
    pb_ratio = market_cap / book_value if book_value > 0 else float('inf')
    ps_ratio = market_cap / revenue if revenue > 0 else float('inf')
    
    return {
        'eps': eps,
        'pe_ratio': pe_ratio,
        'pb_ratio': pb_ratio,
        'ps_ratio': ps_ratio
    }
