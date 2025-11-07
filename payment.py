import streamlit as st
import datetime

class PaymentProcessor:
    """
    決済処理クラス
    """
    
    def __init__(self):
        self.plans = {
            "free": {
                "name": "無料プラン",
                "price": 0,
                "analysis_limit": 5,
                "features": [
                    "月5回まで分析可能",
                    "基本的な財務分析",
                    "DCF計算機能"
                ]
            },
            "basic": {
                "name": "ベーシックプラン",
                "price": 980,
                "analysis_limit": 50,
                "features": [
                    "月50回まで分析可能",
                    "詳細な財務分析",
                    "DCF計算機能",
                    "企業比較機能",
                    "感度分析"
                ]
            },
            "premium": {
                "name": "プレミアムプラン",
                "price": 2980,
                "analysis_limit": -1,  # 無制限
                "features": [
                    "無制限の分析",
                    "全機能利用可能",
                    "優先サポート",
                    "API アクセス",
                    "カスタムレポート"
                ]
            }
        }
    
    def get_plan_info(self, plan_name):
        """
        プラン情報を取得
        """
        return self.plans.get(plan_name, self.plans["free"])
    
    def check_analysis_limit(self, user, analysis_count):
        """
        ユーザーの分析回数制限をチェック
        
        Parameters:
        -----------
        user : dict
            ユーザー情報
        analysis_count : int
            現在の分析回数
            
        Returns:
        --------
        bool
            制限内ならTrue、超過ならFalse
        """
        if not user:
            return False
        
        plan = user.get('subscription_plan', 'free')
        plan_info = self.get_plan_info(plan)
        limit = plan_info['analysis_limit']
        
        # 無制限の場合
        if limit == -1:
            return True
        
        return analysis_count < limit
    
    def process_payment(self, user_id, plan_name, payment_method="credit_card"):
        """
        決済処理（デモ版）
        
        実際の実装では、Stripe、PayPalなどの決済APIを使用します
        
        Parameters:
        -----------
        user_id : int
            ユーザーID
        plan_name : str
            プラン名
        payment_method : str
            決済方法
            
        Returns:
        --------
        dict
            決済結果
        """
        plan = self.get_plan_info(plan_name)
        
        if plan_name == "free":
            return {
                "success": True,
                "message": "無料プランを選択しました。",
                "plan": plan_name
            }
        
        # デモ版のため、常に成功を返す
        return {
            "success": True,
            "message": f"{plan['name']}の決済が完了しました。",
            "plan": plan_name,
            "amount": plan['price'],
            "transaction_id": f"DEMO_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
    
    def cancel_subscription(self, user_id):
        """
        サブスクリプションキャンセル
        
        Parameters:
        -----------
        user_id : int
            ユーザーID
            
        Returns:
        --------
        dict
            キャンセル結果
        """
        return {
            "success": True,
            "message": "サブスクリプションがキャンセルされました。"
        }
    
    def display_pricing_table(self):
        """
        料金プランテーブルを表示
        """
        st.markdown("### 💳 料金プラン")
        
        cols = st.columns(3)
        
        for idx, (plan_key, plan_info) in enumerate(self.plans.items()):
            with cols[idx]:
                # プランカード
                if plan_key == "premium":
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 2rem; border-radius: 15px; color: white; text-align: center;
                                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);">
                        <div style="font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">おすすめ</div>
                        <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{plan_info['name']}</h3>
                        <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">¥{plan_info['price']:,}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 1.5rem;">/月</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: white; padding: 2rem; border-radius: 15px; 
                                border: 2px solid #e2e8f0; text-align: center;">
                        <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #1a202c;">{plan_info['name']}</h3>
                        <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: #667eea;">¥{plan_info['price']:,}</div>
                        <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 1.5rem;">/月</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("**機能:**")
                for feature in plan_info['features']:
                    st.markdown(f"✓ {feature}")
                
                if st.button(f"{plan_info['name']}を選択", key=f"select_{plan_key}", use_container_width=True):
                    st.success(f"{plan_info['name']}を選択しました！")
                
                st.markdown("---")


# 使用例
if __name__ == "__main__":
    processor = PaymentProcessor()
    
    # プラン情報取得
    premium_plan = processor.get_plan_info("premium")
    print(f"Premium Plan: {premium_plan}")
    
    # 決済処理（デモ）
    result = processor.process_payment(user_id=1, plan_name="basic")
    print(f"Payment Result: {result}")
