import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
from database import get_session, SensitivityAnalysis
from financial_models import calculate_intrinsic_value

def generate_sensitivity_matrix(base_forecasted_data, base_discount_rate, terminal_multiple, 
                              shares_outstanding, growth_range, discount_range):
    """
    成長率と割引率の変動に基づく感度分析マトリックスを生成する
    
    Parameters:
    -----------
    base_forecasted_data : pandas.DataFrame
        基本シナリオの予測財務データ
    base_discount_rate : float
        基本シナリオの割引率
    terminal_multiple : float
        終末価値の計算に使用する倍率
    shares_outstanding : float
        発行済株式数（百万株）
    growth_range : list
        分析に使用する成長率の範囲 [最小値, 最大値, ステップ]
    discount_range : list
        分析に使用する割引率の範囲 [最小値, 最大値, ステップ]
        
    Returns:
    --------
    dict
        感度分析の結果を含む辞書
    """
    # 成長率と割引率の範囲を生成
    growth_rates = np.arange(growth_range[0], growth_range[1] + growth_range[2], growth_range[2])
    discount_rates = np.arange(discount_range[0], discount_range[1] + discount_range[2], discount_range[2])
    
    # 結果マトリックスの初期化
    matrix = []
    
    # 基本シナリオのデータを取得
    base_revenue = base_forecasted_data['売上高（百万USD）'].iloc[0]
    base_net_margin = base_forecasted_data['純利益率 (%)'].iloc[0]
    years = base_forecasted_data['年']
    
    # 各成長率と割引率の組み合わせについてDCF価値を計算
    for growth_rate in growth_rates:
        row = []
        for discount_rate in discount_rates:
            # 指定された成長率で売上高を予測
            forecasted_data = pd.DataFrame()
            forecasted_data['年'] = years
            
            # 売上高の予測
            forecasted_data['売上高（百万USD）'] = [base_revenue * ((1 + growth_rate/100) ** year) for year in years]
            
            # 純利益率は一定と仮定
            forecasted_data['純利益率 (%)'] = base_net_margin
            
            # 純利益の予測
            forecasted_data['純利益（百万USD）'] = forecasted_data['売上高（百万USD）'] * forecasted_data['純利益率 (%)'] / 100
            
            # DCF法による本質的価値の計算
            dcf_results = calculate_intrinsic_value(
                forecasted_data, 
                discount_rate, 
                terminal_multiple, 
                shares_outstanding
            )
            
            # 結果をマトリックスに追加
            row.append(dcf_results['dcf_per_share'])
        
        matrix.append(row)
    
    return {
        'growth_rates': growth_rates.tolist(),
        'discount_rates': discount_rates.tolist(),
        'matrix': matrix
    }

def save_sensitivity_analysis(analysis_id, growth_range, discount_range, matrix_data):
    """
    感度分析の結果をデータベースに保存する
    
    Parameters:
    -----------
    analysis_id : int
        関連する分析ID
    growth_range : list
        [最小値, 最大値, ステップ]
    discount_range : list
        [最小値, 最大値, ステップ]
    matrix_data : dict
        感度分析の結果マトリックス
        
    Returns:
    --------
    int or None
        成功した場合は感度分析IDを返す。失敗した場合はNone。
    """
    try:
        session = get_session()
        
        # データをJSON形式に変換
        matrix_json = json.dumps(matrix_data)
        
        # 感度分析データを作成
        sensitivity = SensitivityAnalysis(
            analysis_id=analysis_id,
            growth_range_min=growth_range[0],
            growth_range_max=growth_range[1],
            growth_step=growth_range[2],
            discount_range_min=discount_range[0],
            discount_range_max=discount_range[1],
            discount_step=discount_range[2],
            matrix_data=matrix_json
        )
        
        session.add(sensitivity)
        session.commit()
        
        sensitivity_id = sensitivity.id
        session.close()
        
        return sensitivity_id
    except Exception as e:
        if session:
            session.rollback()
            session.close()
        print(f"感度分析の保存中にエラーが発生しました: {e}")
        return None

def get_sensitivity_analysis(analysis_id):
    """
    指定された分析IDに関連する感度分析データを取得する
    
    Parameters:
    -----------
    analysis_id : int
        分析ID
        
    Returns:
    --------
    dict or None
        感度分析データを含む辞書。データがない場合はNone。
    """
    try:
        session = get_session()
        
        # 関連する感度分析を取得
        sensitivity = session.query(SensitivityAnalysis).filter(
            SensitivityAnalysis.analysis_id == analysis_id
        ).order_by(SensitivityAnalysis.created_at.desc()).first()
        
        if not sensitivity:
            session.close()
            return None
        
        # JSONデータをPythonオブジェクトに変換
        matrix_data = json.loads(sensitivity.matrix_data)
        
        result = {
            'id': sensitivity.id,
            'analysis_id': sensitivity.analysis_id,
            'growth_range': [sensitivity.growth_range_min, sensitivity.growth_range_max, sensitivity.growth_step],
            'discount_range': [sensitivity.discount_range_min, sensitivity.discount_range_max, sensitivity.discount_step],
            'matrix_data': matrix_data
        }
        
        session.close()
        return result
    except Exception as e:
        if 'session' in locals():
            session.close()
        print(f"感度分析データの取得中にエラーが発生しました: {e}")
        return None

def create_sensitivity_heatmap(sensitivity_data, current_stock_price=None):
    """
    感度分析の結果からヒートマップを作成する
    
    Parameters:
    -----------
    sensitivity_data : dict
        感度分析データ
    current_stock_price : float, optional
        現在の株価。指定された場合は上昇/下落の境界として表示される。
        
    Returns:
    --------
    plotly.graph_objects.Figure
        ヒートマップのFigureオブジェクト
    """
    growth_rates = sensitivity_data['matrix_data']['growth_rates']
    discount_rates = sensitivity_data['matrix_data']['discount_rates']
    matrix = sensitivity_data['matrix_data']['matrix']
    
    # デフォルトのカラースケール
    colorscale = 'RdBu_r'  # 赤から青への反転スケール
    
    # 現在の株価がある場合、その値を中心とするカラースケールを作成
    if current_stock_price:
        # マトリックスの最小値と最大値を取得
        flat_matrix = [item for sublist in matrix for item in sublist]
        min_val = min(flat_matrix)
        max_val = max(flat_matrix)
        
        # 現在の株価を基準としたカラースケールを作成
        zmin = min(min_val, current_stock_price * 0.5)  # 下限値
        zmax = max(max_val, current_stock_price * 1.5)  # 上限値
        
        # ヒートマップを作成
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=discount_rates,
            y=growth_rates,
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            colorbar=dict(title="DCF価値 (USD)"),
        ))
        
        # 現在の株価のラインを追加
        # X軸を横切る水平線
        fig.add_shape(
            type="line",
            x0=min(discount_rates),
            y0=current_stock_price,
            x1=max(discount_rates),
            y1=current_stock_price,
            line=dict(color="green", width=2, dash="dash"),
        )
    else:
        # 現在の株価がない場合は通常のヒートマップを作成
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=discount_rates,
            y=growth_rates,
            colorscale=colorscale,
            colorbar=dict(title="DCF価値 (USD)"),
        ))
    
    # グラフのレイアウトを設定
    fig.update_layout(
        title="DCF価値の感度分析",
        xaxis_title="割引率 (%)",
        yaxis_title="成長率 (%)",
        height=600,
        width=800,
    )
    
    return fig