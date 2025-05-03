def generate_swot_analysis(industry, growth_rate, current_margin, target_margin):
    """
    業界、成長率、利益率に基づいたSWOT分析を生成する
    
    Parameters:
    -----------
    industry : str
        企業の業界
    growth_rate : float
        予想売上成長率（%）
    current_margin : float
        現在の純利益率（%）
    target_margin : float
        目標純利益率（%）
        
    Returns:
    --------
    dict
        SWOT分析の結果を含む辞書
    """
    # 業界別の強みと弱みを定義
    industry_strengths = {
        "テクノロジー": "技術革新力とスケーラビリティの高さ",
        "金融": "安定した収益基盤と規模の経済",
        "ヘルスケア": "高い参入障壁と安定した需要",
        "消費財": "ブランド力と広範な流通ネットワーク",
        "工業": "生産技術と効率性の高さ",
        "通信": "インフラ基盤と顧客基盤の大きさ",
        "エネルギー": "資源へのアクセスと高い参入障壁",
        "素材": "原材料へのアクセスと製造技術",
        "公共事業": "安定した需要と規制による保護",
        "不動産": "物理的資産と立地の優位性",
        "その他": "多様なビジネスモデルと柔軟性"
    }
    
    industry_weaknesses = {
        "テクノロジー": "技術変化の速さによる陳腐化リスク",
        "金融": "規制の厳格化と低金利環境の影響",
        "ヘルスケア": "研究開発コストの高さと規制対応",
        "消費財": "消費者嗜好の変化への対応",
        "工業": "原材料価格の変動と設備投資負担",
        "通信": "技術更新コストの高さと価格競争",
        "エネルギー": "環境規制と代替エネルギーへの移行",
        "素材": "コモディティ価格の変動と環境負荷",
        "公共事業": "規制変更リスクと設備更新負担",
        "不動産": "金利変動と市場サイクルの影響",
        "その他": "業界固有の課題への対応"
    }
    
    # 成長率に基づく機会の分析
    if growth_rate > 15:
        opportunity = f"業界平均を大幅に上回る{growth_rate}%の成長率は、市場拡大または市場シェア獲得の強い機会を示唆しています。継続的な投資によりこの成長トレンドを維持できる可能性があります。"
    elif growth_rate > 5:
        opportunity = f"{growth_rate}%の安定した成長率は、業界内での競争優位性を構築する機会を提供します。新製品開発や市場拡大の余地があります。"
    else:
        opportunity = f"{growth_rate}%の成長率は限定的ですが、効率性の向上やコスト削減を通じて収益性を高める機会があります。また、業界再編の中での戦略的買収や合併の可能性も考えられます。"
    
    # 利益率変化に基づく脅威の分析
    margin_change = target_margin - current_margin
    if margin_change > 5:
        threat = f"純利益率を{current_margin:.2f}%から{target_margin:.2f}%へ大幅に向上させる目標は、競争環境の激化や原材料コストの上昇などの脅威に直面する可能性があります。目標達成のためには効率的なコスト管理と価格設定戦略が必要です。"
    elif margin_change > 0:
        threat = f"純利益率の穏やかな改善目標（{current_margin:.2f}%から{target_margin:.2f}%へ）は、競争環境の中でも達成可能ですが、原価上昇や市場シェア維持のための価格競争などの脅威に注意が必要です。"
    else:
        threat = f"純利益率が{current_margin:.2f}%から{target_margin:.2f}%へ低下する見通しは、競争激化や市場環境の変化による脅威が存在することを示唆しています。収益性の改善策や事業構造の見直しが必要かもしれません。"
    
    # SWOT分析の結果を辞書にまとめる
    swot = {
        "strengths": f"• {industry_strengths.get(industry, '業界での競争力')}\n• {current_margin:.2f}%の純利益率による安定した収益基盤\n• 将来の{growth_rate}%成長を支える経営基盤と戦略",
        "weaknesses": f"• {industry_weaknesses.get(industry, '業界特有の課題')}\n• 目標利益率{target_margin:.2f}%達成のための経営効率化の課題\n• 成長を支えるための資本・人材投資の必要性",
        "opportunities": opportunity,
        "threats": threat
    }
    
    return swot

def generate_moat_analysis(industry, growth_rate, net_margin):
    """
    業界、成長率、利益率に基づいた競争優位性（モート）分析を生成する
    
    Parameters:
    -----------
    industry : str
        企業の業界
    growth_rate : float
        予想売上成長率（%）
    net_margin : float
        純利益率（%）
        
    Returns:
    --------
    dict
        モート分析の結果を含む辞書
    """
    # 業界別のモート（競争優位性）の特徴
    industry_moats = {
        "テクノロジー": {
            "primary": "ネットワーク効果と知的財産",
            "description": "技術特許、プラットフォーム効果、顧客データの蓄積による参入障壁"
        },
        "金融": {
            "primary": "規模の経済と切替コスト",
            "description": "大規模な顧客基盤、高い規制参入障壁、顧客の金融サービス切替の難しさ"
        },
        "ヘルスケア": {
            "primary": "特許と規制による保護",
            "description": "医薬品特許、医療機器の認可、専門知識に基づく参入障壁"
        },
        "消費財": {
            "primary": "ブランド力と流通網",
            "description": "消費者の高いブランド忠誠度、広範な小売流通ネットワークへのアクセス"
        },
        "工業": {
            "primary": "コスト優位性と規模の経済",
            "description": "効率的な生産プロセス、サプライチェーンの最適化、専門的な製造ノウハウ"
        },
        "通信": {
            "primary": "インフラ投資と切替コスト",
            "description": "通信インフラへの大規模投資による参入障壁、顧客の高い切替コスト"
        },
        "エネルギー": {
            "primary": "資産と地理的優位性",
            "description": "資源へのアクセス、エネルギーインフラ、地域独占的な地位"
        },
        "素材": {
            "primary": "原材料へのアクセスとコスト優位性",
            "description": "鉱山や原材料へのアクセス、効率的な生産工程、輸送の優位性"
        },
        "公共事業": {
            "primary": "規制による保護と地域独占",
            "description": "政府による規制保護、高い初期投資による参入障壁、地域独占"
        },
        "不動産": {
            "primary": "立地の優位性",
            "description": "プライムロケーションの物件所有、土地の希少性、開発許可の壁"
        },
        "その他": {
            "primary": "複合的な優位性",
            "description": "業界特有の参入障壁と差別化要因"
        }
    }
    
    # モートの評価基準
    # 成長率と利益率の組み合わせでモートの強さを評価
    moat_strength = "弱い"
    if growth_rate > 15 and net_margin > 20:
        moat_strength = "非常に強い"
    elif growth_rate > 10 and net_margin > 15:
        moat_strength = "強い"
    elif growth_rate > 5 and net_margin > 10:
        moat_strength = "中程度"
    elif growth_rate > 0 and net_margin > 5:
        moat_strength = "やや弱い"
    
    # 業界特有のモート情報を取得
    industry_moat = industry_moats.get(industry, industry_moats["その他"])
    
    # モート評価のテキスト生成
    evaluation = f"この企業は{moat_strength}競争優位性（モート）を持っていると評価されます。{growth_rate}%の成長率と{net_margin:.2f}%の純利益率を考慮すると、同業他社と比較して{moat_strength}競争力を維持していると考えられます。"
    
    # モート源泉のテキスト生成
    primary_moat = industry_moat["primary"]
    moat_description = industry_moat["description"]
    
    additional_moat_source = ""
    if net_margin > 20:
        additional_moat_source = "\n\n特に高い利益率（20%超）は、強力な価格決定力または極めて効率的な事業運営を示しており、これもモートの重要な源泉です。"
    elif net_margin > 15:
        additional_moat_source = "\n\n平均以上の利益率（15%超）は、一定の価格決定力または効率的な事業運営を示しており、これもモートの源泉となっています。"
    
    sources = f"{industry}業界では主に「{primary_moat}」が競争優位性の源泉となります。具体的には、{moat_description}などが挙げられます。{additional_moat_source}"
    
    return {
        "evaluation": evaluation,
        "sources": sources
    }
