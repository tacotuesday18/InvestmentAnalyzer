import hashlib
import os
import uuid
import datetime
from database import get_session, User, Base, engine

def hash_password(password, salt=None):
    """
    パスワードをハッシュ化する関数
    
    Parameters:
    -----------
    password : str
        ハッシュ化したいパスワード
    salt : str, optional
        ソルト値（省略時は新しく生成）
        
    Returns:
    --------
    tuple
        (ハッシュ化されたパスワード, ソルト)
    """
    if salt is None:
        salt = uuid.uuid4().hex
    
    # パスワードとソルトを組み合わせてハッシュ化
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt


def create_user(username, email, password, subscription_plan="free"):
    """
    新しいユーザーを作成する関数
    
    Parameters:
    -----------
    username : str
        ユーザー名
    email : str
        メールアドレス
    password : str
        パスワード
    subscription_plan : str, optional
        サブスクリプションプラン（free, basic, premium）
        
    Returns:
    --------
    dict
        作成結果と情報を含む辞書
    """
    try:
        session = get_session()
        
        # ユーザー名またはメールアドレスが既に存在するか確認
        existing_user = session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            session.close()
            return {
                "success": False,
                "message": "ユーザー名またはメールアドレスが既に登録されています。"
            }
        
        # パスワードのハッシュ化
        hashed_password, salt = hash_password(password)
        
        # 新しいユーザーを作成
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            password_salt=salt,
            subscription_plan=subscription_plan,
            created_at=datetime.datetime.utcnow()
        )
        
        session.add(new_user)
        session.commit()
        
        user_id = new_user.id
        session.close()
        
        return {
            "success": True,
            "message": "ユーザーが正常に作成されました。",
            "user_id": user_id
        }
    except Exception as e:
        session.rollback()
        session.close()
        return {
            "success": False,
            "message": f"ユーザー作成中にエラーが発生しました: {str(e)}"
        }


def authenticate_user(username, password):
    """
    ユーザーを認証する関数
    
    Parameters:
    -----------
    username : str
        ユーザー名またはメールアドレス
    password : str
        パスワード
        
    Returns:
    --------
    dict
        認証結果とユーザー情報を含む辞書
    """
    try:
        session = get_session()
        
        # ユーザー名またはメールアドレスでユーザーを検索
        user = session.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            session.close()
            return {
                "success": False,
                "message": "ユーザーが見つかりません。"
            }
        
        # パスワードを検証
        hashed_password, _ = hash_password(password, user.password_salt)
        
        if hashed_password != user.password_hash:
            session.close()
            return {
                "success": False,
                "message": "パスワードが正しくありません。"
            }
        
        # 認証成功
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "subscription_plan": user.subscription_plan,
            "analysis_count": user.analysis_count
        }
        
        session.close()
        
        return {
            "success": True,
            "message": "認証に成功しました。",
            "user": user_data
        }
    except Exception as e:
        session.close()
        return {
            "success": False,
            "message": f"認証中にエラーが発生しました: {str(e)}"
        }


def update_subscription(user_id, new_plan):
    """
    ユーザーのサブスクリプションプランを更新する関数
    
    Parameters:
    -----------
    user_id : int
        ユーザーID
    new_plan : str
        新しいサブスクリプションプラン（free, basic, premium）
        
    Returns:
    --------
    dict
        更新結果を含む辞書
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
        
        # サブスクリプションプランを更新
        user.subscription_plan = new_plan
        session.commit()
        
        session.close()
        
        return {
            "success": True,
            "message": f"サブスクリプションプランが{new_plan}に更新されました。"
        }
    except Exception as e:
        session.rollback()
        session.close()
        return {
            "success": False,
            "message": f"サブスクリプション更新中にエラーが発生しました: {str(e)}"
        }


def increment_user_analysis_count(user_id):
    """
    ユーザーの分析回数カウンターをインクリメントする
    
    Parameters:
    -----------
    user_id : int
        ユーザーID
        
    Returns:
    --------
    dict
        更新結果と現在のカウント数を含む辞書
    """
    try:
        session = get_session()
        
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            session.close()
            return {
                "success": False,
                "message": "ユーザーが見つかりません。"
            }
        
        user.analysis_count += 1
        session.commit()
        
        count = user.analysis_count
        session.close()
        
        return {
            "success": True,
            "message": "分析カウントが更新されました。",
            "count": count
        }
    except Exception as e:
        session.rollback()
        session.close()
        return {
            "success": False,
            "message": f"カウント更新中にエラーが発生しました: {str(e)}"
        }


def get_user_by_id(user_id):
    """
    IDからユーザー情報を取得する
    
    Parameters:
    -----------
    user_id : int
        ユーザーID
        
    Returns:
    --------
    dict
        ユーザー情報を含む辞書
    """
    try:
        session = get_session()
        
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            session.close()
            return {
                "success": False,
                "message": "ユーザーが見つかりません。"
            }
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "subscription_plan": user.subscription_plan,
            "analysis_count": user.analysis_count
        }
        
        session.close()
        
        return {
            "success": True,
            "user": user_data
        }
    except Exception as e:
        session.close()
        return {
            "success": False,
            "message": f"ユーザー情報取得中にエラーが発生しました: {str(e)}"
        }


def setup_auth_tables():
    """認証関連のテーブルを作成する"""
    try:
        # User モデルのテーブルが存在しなければ作成
        Base.metadata.create_all(engine, tables=[User.__table__])
        return {"success": True, "message": "認証テーブルが正常に作成されました。"}
    except Exception as e:
        return {"success": False, "message": f"テーブル作成エラー: {str(e)}"}