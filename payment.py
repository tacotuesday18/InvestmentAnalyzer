import datetime
import hashlib
import os
import uuid
from database import get_session, User

class PaymentProcessor:
    """決済処理を管理するクラス"""
    
    @staticmethod
    def generate_payment_id():
        """一意の決済IDを生成する"""
        return f"pay_{uuid.uuid4().hex[:16]}"
    
    @staticmethod
    def get_plan_details(plan_name):
        """
        プラン名に基づいて料金と機能を取得する
        
        Parameters:
        -----------
        plan_name : str
            プラン名（free, basic, premium）
            
        Returns:
        --------
        dict
            プランの詳細情報
        """
        plans = {
            "free": {
                "name": "無料プラン",
                "price": 0,
                "currency": "JPY",
                "period": "月額",
                "analysis_limit": 3,
                "features": [
                    "基本的な企業分析",
                    "DCF法による株価評価",
                    "シンプルなSWOT分析",
                ]
            },
            "basic": {
                "name": "ベーシックプラン",
                "price": 2500,
                "currency": "JPY",
                "period": "月額",
                "analysis_limit": 20,
                "features": [
                    "基本的な企業分析",
                    "DCF法による株価評価",
                    "詳細なSWOT分析",
                    "決算情報の詳細分析",
                    "財務指標の詳細比較"
                ]
            },
            "premium": {
                "name": "プレミアムプラン",
                "price": 4900,
                "currency": "JPY",
                "period": "月額",
                "analysis_limit": 999999,  # 実質無制限
                "features": [
                    "基本的な企業分析",
                    "DCF法による株価評価",
                    "詳細なSWOT分析",
                    "決算情報の詳細分析",
                    "財務指標の詳細比較",
                    "業界詳細レポート",
                    "感度分析",
                    "DCF価値の感度分析",
                    "優先カスタマーサポート",
                    "分析結果のエクスポート機能"
                ]
            }
        }
        
        return plans.get(plan_name, plans["free"])
    
    @staticmethod
    def process_payment(user_id, plan_name, payment_method, payment_details):
        """
        支払いを処理する
        
        Parameters:
        -----------
        user_id : int
            ユーザーID
        plan_name : str
            プラン名（basic, premium）
        payment_method : str
            支払い方法（credit_card, bank_transfer, convenience_store）
        payment_details : dict
            支払い詳細情報
            
        Returns:
        --------
        dict
            処理結果
        """
        try:
            # 実際の実装ではここで決済プロバイダのAPIを呼び出す
            # このサンプルでは成功したと仮定
            
            session = get_session()
            
            # ユーザーを検索
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                session.close()
                return {
                    "success": False,
                    "message": "ユーザーが見つかりません。"
                }
            
            # プラン詳細を取得
            plan_details = PaymentProcessor.get_plan_details(plan_name)
            
            # サブスクリプション期間を設定（1ヶ月）
            current_date = datetime.datetime.utcnow()
            end_date = current_date + datetime.timedelta(days=30)
            
            # ユーザー情報を更新
            user.subscription_plan = plan_name
            user.subscription_end_date = end_date
            user.payment_status = "active"
            
            session.commit()
            
            # 処理結果を返す
            result = {
                "success": True,
                "message": f"{plan_details['name']}へのアップグレードが完了しました。",
                "payment_id": PaymentProcessor.generate_payment_id(),
                "plan": plan_name,
                "amount": plan_details["price"],
                "currency": plan_details["currency"],
                "subscription_end_date": end_date.strftime("%Y-%m-%d")
            }
            
            session.close()
            return result
            
        except Exception as e:
            if 'session' in locals():
                session.rollback()
                session.close()
            return {
                "success": False,
                "message": f"決済処理中にエラーが発生しました: {str(e)}"
            }
    
    @staticmethod
    def cancel_subscription(user_id):
        """
        サブスクリプションをキャンセルする
        
        Parameters:
        -----------
        user_id : int
            ユーザーID
            
        Returns:
        --------
        dict
            処理結果
        """
        try:
            session = get_session()
            
            # ユーザーを検索
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                session.close()
                return {
                    "success": False,
                    "message": "ユーザーが見つかりません。"
                }
            
            # サブスクリプションをキャンセル
            user.payment_status = "cancelled"
            
            # 無料プランに戻す（現在の期間が終了したら）
            # 実際のアプリケーションでは、サブスクリプション終了日まで
            # 有料機能を使用できるようにするロジックを追加する
            
            session.commit()
            
            session.close()
            
            return {
                "success": True,
                "message": "サブスクリプションが正常にキャンセルされました。現在の期間が終了するまで引き続き機能をご利用いただけます。"
            }
            
        except Exception as e:
            if 'session' in locals():
                session.rollback()
                session.close()
            return {
                "success": False,
                "message": f"サブスクリプションのキャンセル中にエラーが発生しました: {str(e)}"
            }
    
    @staticmethod
    def check_subscription_status(user_id):
        """
        ユーザーのサブスクリプション状態を確認する
        
        Parameters:
        -----------
        user_id : int
            ユーザーID
            
        Returns:
        --------
        dict
            サブスクリプション情報
        """
        try:
            session = get_session()
            
            # ユーザーを検索
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                session.close()
                return {
                    "success": False,
                    "message": "ユーザーが見つかりません。"
                }
            
            # プラン詳細を取得
            plan_details = PaymentProcessor.get_plan_details(user.subscription_plan)
            
            # サブスクリプションが有効かチェック
            is_active = True
            status_message = "有効"
            
            # 終了日が設定されている場合、現在日付と比較
            if user.subscription_end_date:
                if user.subscription_end_date < datetime.datetime.utcnow():
                    # 無料プラン以外で期限切れの場合
                    if user.subscription_plan != "free":
                        is_active = False
                        status_message = "期限切れ"
            
            # サブスクリプション情報を返す
            subscription_info = {
                "success": True,
                "user_id": user.id,
                "plan": user.subscription_plan,
                "plan_name": plan_details["name"],
                "is_active": is_active,
                "status": status_message,
                "payment_status": user.payment_status,
                "features": plan_details["features"],
                "analysis_limit": plan_details["analysis_limit"],
                "analysis_count": user.analysis_count
            }
            
            # 有料プランの場合、終了日も返す
            if user.subscription_plan != "free" and user.subscription_end_date:
                subscription_info["end_date"] = user.subscription_end_date.strftime("%Y-%m-%d")
            
            session.close()
            
            return subscription_info
            
        except Exception as e:
            if 'session' in locals():
                session.close()
            return {
                "success": False,
                "message": f"サブスクリプション状態の確認中にエラーが発生しました: {str(e)}"
            }