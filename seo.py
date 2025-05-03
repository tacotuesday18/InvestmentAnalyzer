def generate_seo_metadata(company_name, industry, dcf_price, current_price, recommendation):
    """
    企業分析に基づいたSEO最適化されたメタデータを生成する
    
    Parameters:
    -----------
    company_name : str
        企業名
    industry : str
        業界
    dcf_price : float
        DCF法による株価
    current_price : float
        現在の株価
    recommendation : str
        投資推奨度
        
    Returns:
    --------
    dict
        SEOメタデータを含む辞書
    """
    # 投資推奨度に基づいたキーワード
    if recommendation in ["強い買い", "買い"]:
        sentiment = "買い"
        investment_keywords = "投資推奨,買い推奨,割安株,成長株"
    elif recommendation in ["様子見", "中立"]:
        sentiment = "中立"
        investment_keywords = "投資検討,値動き注視,適正株価"
    else:
        sentiment = "売り"
        investment_keywords = "投資注意,売り推奨,割高株"
    
    # 業界特有のキーワード
    industry_keywords = {
        "テクノロジー": "テクノロジー株,IT企業,ハイテク,AI,デジタル化",
        "金融": "金融株,銀行株,フィンテック,金融サービス",
        "ヘルスケア": "ヘルスケア株,医療,製薬,バイオテック",
        "消費財": "消費財,小売,eコマース,消費者ブランド",
        "工業": "工業株,製造,重機,インフラ,建設",
        "通信": "通信株,テレコム,5G,ネットワーク",
        "エネルギー": "エネルギー株,石油,再生可能エネルギー,電力",
        "素材": "素材株,鉱業,化学,コモディティ",
        "公共事業": "公共事業株,ユーティリティ,電力,水道,ガス",
        "不動産": "不動産株,REIT,不動産開発",
        "その他": "株式投資,企業分析,バリュー投資"
    }
    
    # 価格差に基づいたフレーズ
    price_diff_percent = ((dcf_price / current_price) - 1) * 100
    if price_diff_percent > 20:
        price_phrase = f"大幅な上昇余地({price_diff_percent:.1f}%)あり"
    elif price_diff_percent > 5:
        price_phrase = f"上昇余地({price_diff_percent:.1f}%)あり"
    elif price_diff_percent > -5:
        price_phrase = "ほぼ適正な株価水準"
    else:
        price_phrase = f"割高な可能性({-price_diff_percent:.1f}%)"
    
    # タイトルの生成
    title = f"{company_name}の株価分析: DCF法による本質的価値と{sentiment}推奨 | 企業価値分析プロ"
    
    # 説明文の生成
    description = f"{company_name}（{industry}）の株価分析結果。DCF法による本質的価値は{dcf_price:.2f}円で現在株価に対して{price_phrase}。{recommendation}の投資判断が示されています。成長率や割引率の感度分析も提供。"
    
    # キーワードの生成
    keywords = f"{company_name},株価分析,企業価値,DCF法,本質的価値,投資判断,{sentiment}推奨,{price_phrase},{industry_keywords.get(industry, '')},{investment_keywords}"
    
    return {
        "title": title,
        "description": description,
        "keywords": keywords
    }