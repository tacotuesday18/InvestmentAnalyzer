import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# データベース接続
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# モデル定義
class Company(Base):
    """企業情報モデル"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(20), unique=True)
    industry = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # リレーションシップ
    financial_data = relationship("FinancialData", back_populates="company", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(name='{self.name}', symbol='{self.symbol}', industry='{self.industry}')>"


class FinancialData(Base):
    """企業の財務データモデル"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    year = Column(Integer, nullable=False)
    revenue = Column(Float)  # 売上高（百万USD）
    net_income = Column(Float)  # 純利益（百万USD）
    eps = Column(Float)  # 1株あたり利益（USD）
    book_value_per_share = Column(Float)  # 1株あたり純資産（USD）
    shares_outstanding = Column(Float)  # 発行済株式数（百万株）
    current_stock_price = Column(Float)  # 現在の株価（USD）
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # リレーションシップ
    company = relationship("Company", back_populates="financial_data")
    
    def __repr__(self):
        return f"<FinancialData(company_id={self.company_id}, year={self.year}, revenue={self.revenue})>"


class Analysis(Base):
    """企業の価値分析結果モデル"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 分析パラメータ
    revenue_growth_rate = Column(Float)  # 予想売上成長率（%）
    target_net_margin = Column(Float)  # 目標純利益率（%）
    discount_rate = Column(Float)  # 割引率（%）
    forecast_years = Column(Integer)  # 予測期間（年）
    
    # 業界平均指標
    industry_pe = Column(Float)  # 業界平均PER
    industry_pb = Column(Float)  # 業界平均PBR
    industry_ps = Column(Float)  # 業界平均PSR
    
    # 分析結果
    dcf_price = Column(Float)  # DCF法による株価（USD）
    upside_potential = Column(Float)  # 上昇余地（%）
    recommendation = Column(String(50))  # 投資推奨度
    
    # SWOT分析とモート分析結果
    swot_strengths = Column(Text)
    swot_weaknesses = Column(Text)
    swot_opportunities = Column(Text)
    swot_threats = Column(Text)
    moat_evaluation = Column(Text)
    moat_sources = Column(Text)
    
    # リレーションシップ
    company = relationship("Company", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(company_id={self.company_id}, dcf_price={self.dcf_price}, recommendation='{self.recommendation}')>"


class User(Base):
    """ユーザー情報モデル"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    subscription_plan = Column(String(20), default="basic")  # basic, professional, enterprise
    analysis_count = Column(Integer, default=0)  # 分析実行回数
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<User(username='{self.username}', subscription='{self.subscription_plan}')>"


# データベーステーブル作成
def init_db():
    Base.metadata.create_all(engine)


# サンプルデータ挿入
def insert_sample_data():
    session = Session()
    
    # サンプル企業データ
    sample_companies = [
        {"name": "Apple Inc.", "symbol": "AAPL", "industry": "テクノロジー"},
        {"name": "Microsoft Corporation", "symbol": "MSFT", "industry": "テクノロジー"},
        {"name": "Amazon.com, Inc.", "symbol": "AMZN", "industry": "消費財"},
        {"name": "JPMorgan Chase & Co.", "symbol": "JPM", "industry": "金融"},
        {"name": "Johnson & Johnson", "symbol": "JNJ", "industry": "ヘルスケア"}
    ]
    
    # 企業データ挿入
    for company_data in sample_companies:
        company = Company(**company_data)
        session.add(company)
    
    session.commit()
    
    # 財務データ挿入
    financial_data = [
        {"company_id": 1, "year": 2023, "revenue": 394328, "net_income": 96995, "eps": 6.14, "book_value_per_share": 15.38, "shares_outstanding": 15814, "current_stock_price": 175.04},
        {"company_id": 2, "year": 2023, "revenue": 211915, "net_income": 72361, "eps": 9.71, "book_value_per_share": 34.96, "shares_outstanding": 7453, "current_stock_price": 386.77},
        {"company_id": 3, "year": 2023, "revenue": 574785, "net_income": 30425, "eps": 2.96, "book_value_per_share": 51.54, "shares_outstanding": 10384, "current_stock_price": 178.32},
        {"company_id": 4, "year": 2023, "revenue": 156554, "net_income": 49547, "eps": 16.96, "book_value_per_share": 106.54, "shares_outstanding": 2921, "current_stock_price": 195.43},
        {"company_id": 5, "year": 2023, "revenue": 85160, "net_income": 17941, "eps": 6.93, "book_value_per_share": 28.65, "shares_outstanding": 2602, "current_stock_price": 148.90}
    ]
    
    for data in financial_data:
        financial = FinancialData(**data)
        session.add(financial)
    
    session.commit()
    session.close()


# 企業データの取得
def get_companies():
    session = Session()
    companies = session.query(Company).all()
    result = [{"id": c.id, "name": c.name, "symbol": c.symbol, "industry": c.industry} for c in companies]
    session.close()
    return result


# 企業の財務データ取得
def get_company_financial_data(company_id, year=None):
    session = Session()
    query = session.query(FinancialData).filter(FinancialData.company_id == company_id)
    
    if year:
        query = query.filter(FinancialData.year == year)
    
    data = query.order_by(FinancialData.year.desc()).first()
    session.close()
    return data


# 分析結果の保存
def save_analysis(analysis_data):
    session = Session()
    analysis = Analysis(**analysis_data)
    session.add(analysis)
    session.commit()
    session.close()
    return analysis.id


# ユーザーのサブスクリプションプラン更新
def update_user_subscription(username, plan):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    
    if not user:
        user = User(username=username, subscription_plan=plan)
        session.add(user)
    else:
        user.subscription_plan = plan
    
    session.commit()
    session.close()
    return True


# 分析カウントの増加
def increment_analysis_count(username):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    
    if user:
        user.analysis_count += 1
        session.commit()
    
    session.close()
    return True if user else False


# 初期化
if __name__ == "__main__":
    init_db()
    # 既存のサンプルデータがあるか確認
    session = Session()
    count = session.query(Company).count()
    session.close()
    
    if count == 0:
        insert_sample_data()
        print("サンプルデータが挿入されました。")
    else:
        print(f"既存の企業データが {count} 件あります。")