import re

def format_ja_number(number, suffix="", include_raw=False):
    """
    数値を日本語での単位表記（兆、億、万）に変換する

    Parameters:
    -----------
    number : float または int
        変換する数値
    suffix : str, optional
        単位の接尾辞（例: "円", "ドル", "$"など）
    include_raw : bool, optional
        元の数値を括弧内に含めるかどうか

    Returns:
    --------
    str
        日本語単位で表記された文字列
    """
    abs_number = abs(number)
    sign = "-" if number < 0 else ""
    
    # 兆（10^12）
    if abs_number >= 1_0000_0000_0000:
        value = abs_number / 1_0000_0000_0000
        unit = "兆"
    # 億（10^8）
    elif abs_number >= 1_0000_0000:
        value = abs_number / 1_0000_0000
        unit = "億"
    # 万（10^4）
    elif abs_number >= 1_0000:
        value = abs_number / 1_0000
        unit = "万"
    else:
        value = abs_number
        unit = ""
    
    # 数値のフォーマット（小数点以下が0の場合は整数表示）
    if value == int(value):
        formatted = f"{sign}{int(value):,}{unit}{suffix}"
    else:
        # 小数点以下が少ない場合は小数点以下を調整
        decimal_places = 2
        if value < 10:
            decimal_places = 2
        elif value < 100:
            decimal_places = 1
        formatted = f"{sign}{value:,.{decimal_places}f}{unit}{suffix}"
    
    # 元の生の数値を含める場合
    if include_raw:
        formatted += f" (${number:,.2f})"
    
    return formatted


def format_currency(value, currency="$", use_ja_format=True, include_raw=False):
    """
    通貨値を指定された形式でフォーマットする

    Parameters:
    -----------
    value : float
        フォーマットする通貨値
    currency : str, optional
        通貨記号（デフォルトは"$"）
    use_ja_format : bool, optional
        日本語形式（兆、億、万）を使用するかどうか
    include_raw : bool, optional
        元の数値を括弧内に含めるかどうか

    Returns:
    --------
    str
        フォーマットされた通貨文字列
    """
    if use_ja_format:
        return format_ja_number(value, currency, include_raw)
    else:
        if include_raw:
            return f"{currency}{value:,.2f}"
        else:
            return f"{currency}{value:,.2f}"


def format_large_number(value, use_ja_format=True, include_raw=False):
    """
    大きな数値を指定された形式でフォーマットする

    Parameters:
    -----------
    value : float
        フォーマットする数値
    use_ja_format : bool, optional
        日本語形式（兆、億、万）を使用するかどうか
    include_raw : bool, optional
        元の数値を括弧内に含めるかどうか

    Returns:
    --------
    str
        フォーマットされた数値文字列
    """
    if use_ja_format:
        return format_ja_number(value, "", include_raw)
    else:
        if value == int(value):
            return f"{int(value):,}" + (f" ({value:,})" if include_raw else "")
        else:
            return f"{value:,.2f}" + (f" ({value:,})" if include_raw else "")