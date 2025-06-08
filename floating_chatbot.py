import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

def get_platform_context():
    """Get current platform context for personalized responses"""
    context = []
    
    # Check what page user is currently on
    if hasattr(st, 'session_state'):
        if 'selected_company' in st.session_state:
            company = st.session_state.selected_company
            context.append(f"現在選択企業: {company.get('name', 'N/A')} ({company.get('ticker', 'N/A')})")
        
        if 'current_price' in st.session_state:
            context.append(f"最新株価データ: 利用可能")
        
        if 'live_data' in st.session_state:
            context.append(f"リアルタイムデータ: 取得済み")
    
    # Available analysis features
    context.append("ファンダメンタル分析対応: AAPL, MSFT, AMZN, GOOGL, META, TSLA, NVDA")
    
    context.append("利用可能機能: DCF計算、財務諸表分析、銘柄比較、決算分析")
    
    return "\n".join(context) if context else "プラットフォーム準備完了"

def get_specialized_response(user_input):
    """Provide specialized platform responses without API dependency"""
    input_lower = user_input.lower()
    
    # DCF Analysis responses
    if "dcf" in input_lower or "割引" in input_lower or "価値計算" in input_lower:
        return """📊 **DCF価値計算機の使用方法**

1. **04_DCF価値計算機** ページにアクセス
2. 企業を選択（AAPL, MSFT, AMZN等対応）
3. 以下のパラメータを調整：
   - 売上成長率（5-15%が一般的）
   - 純利益率（業界平均を参考）
   - 割引率（7-10%が標準）
   - 予測期間（5-10年）

**重要ポイント：**
- 成長率は過去実績と業界トレンドを考慮
- 割引率はリスクフリーレート+リスクプレミアム
- 複数シナリオで感度分析を実施

現在の企業データがあれば、具体的な数値で分析可能です。"""

    # Investment decision responses
    elif "投資判断" in input_lower or "買い" in input_lower or "売り" in input_lower:
        current_company = get_current_company_context()
        return f"""💰 **投資判断フレームワーク**

{current_company}

**判断基準：**
1. **ファンダメンタル分析**
   - PER: 業界平均と比較
   - 成長率: 5年CAGR 10%以上が理想
   - ROE: 15%以上が優良

2. **ビジネスモデル評価**
   - 競争優位性（モート）の強さ
   - 収益の安定性・成長性
   - 市場シェアと拡大可能性

3. **リスク要因**
   - 業界トレンド変化
   - 規制リスク
   - 地政学リスク

**推奨アクション：**
ビジネスモデル分析ページで詳細なSWOT分析を確認してください。"""

    # Growth analysis responses
    elif "成長" in input_lower or "cagr" in input_lower:
        return """📈 **CAGR成長率評価ガイド**

**優秀な成長率基準：**
- 売上CAGR: 10-20%（テック企業）
- 利益CAGR: 15-25%（理想的）
- 配当CAGR: 5-10%（安定企業）

**業界別ベンチマーク：**
- テクノロジー: 売上15%+
- ヘルスケア: 売上8-12%
- 金融: 売上5-10%
- 消費財: 売上3-8%

**注意点：**
- 単年度の異常値に注意
- 市場成熟度を考慮
- 競合他社との比較必須

財務諸表ページで具体的な数値を確認し、業界平均と比較してください。"""

    # Risk analysis responses
    elif "リスク" in input_lower or "危険" in input_lower or "注意" in input_lower:
        return """🔍 **投資リスク分析チェックリスト**

**市場リスク：**
- 金利変動の影響
- 為替リスク（海外企業）
- 景気サイクルの影響

**企業固有リスク：**
- 売上集中度（特定顧客・製品）
- 競合他社の脅威
- 技術革新による陳腐化

**財務リスク：**
- 債務比率の高さ
- キャッシュフロー不安定
- 資金調達能力

**評価方法：**
1. SWOT分析で脅威を特定
2. 財務指標で健全性確認
3. 業界動向との照合

決算分析ページで最新の業績トレンドも確認することをお勧めします。"""

    # Company-specific responses
    elif any(ticker in input_lower for ticker in ["aapl", "apple", "アップル"]):
        return """🍎 **Apple (AAPL) 分析サマリー**

**強み：**
- エコシステムによる顧客囲い込み
- 高い利益率（純利益率25%+）
- 強固なブランド力

**注意点：**
- iPhone依存度（売上の50%）
- 中国市場リスク
- 成長率鈍化の可能性

**推奨分析：**
1. ビジネスモデル分析で詳細SWOT確認
2. DCF計算機でサービス事業成長を織り込んだ価値算出
3. 財務諸表で最新の収益構造確認

プラットフォーム内で包括的な分析データが利用できます。"""

    # General platform guidance
    else:
        return """💡 **1000x Stocks プラットフォーム活用ガイド**

**利用可能な分析ツール：**
1. **ビジネスモデル分析** - SWOT・競争優位性
2. **銘柄比較** - 複数企業の並列分析
3. **財務諸表** - 詳細な財務指標
4. **DCF価値計算機** - 本質的価値算出
5. **決算分析** - 事業セグメント別分析

**対応企業：**
AAPL, MSFT, AMZN, GOOGL, META, TSLA, NVDA等

**投資分析の流れ：**
1. ビジネスモデル理解
2. 財務健全性確認  
3. 成長性評価
4. 適正価値算出
5. リスク要因検討

具体的な企業名やティッカーをお教えいただければ、より詳細な分析をご案内します。"""

def get_current_company_context():
    """Get current company context for responses"""
    if hasattr(st, 'session_state') and 'selected_company' in st.session_state:
        company = st.session_state.selected_company
        return f"**現在選択中企業:** {company.get('name', 'N/A')} ({company.get('ticker', 'N/A')})"
    return "**企業選択:** まず分析したい企業を選択してください"

def render_floating_chatbot():
    """
    Render AI financial assistant as part of navigation menu
    """
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    st.markdown("### 💬 AI金融アシスタント KOJI")
    st.markdown("株式分析とDCF計算に特化したAIアシスタント")
    st.markdown("---")
    
    # Display recent chat messages
    if st.session_state.chat_messages:
        st.markdown("**最近のメッセージ:**")
        for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
            if message["role"] == "user":
                st.markdown(f"👤 **あなた:** {message['content'][:100]}...")
            else:
                st.markdown(f"🤖 **AI:** {message['content'][:100]}...")
        
        if st.button("チャット履歴をクリア", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "金融分析について質問してください:", 
            height=80, 
            placeholder="例: AAPLの財務状況は？"
        )
        
        # Specialized quick action buttons for this platform
        st.markdown("**🚀 クイックアクション:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dcf_clicked = st.form_submit_button("📊 DCF分析")
        with col2:
            invest_clicked = st.form_submit_button("💰 投資判断")
        with col3:
            growth_clicked = st.form_submit_button("📈 成長性分析")
        
        col4, col5 = st.columns(2)
        with col4:
            risk_clicked = st.form_submit_button("🔍 リスク分析")
        with col5:
            submit = st.form_submit_button("送信", type="primary")
        
        # Handle quick action clicks
        if dcf_clicked:
            user_input = "DCF価値計算機の使い方と、適正株価の算出方法を教えて"
            submit = True
        elif invest_clicked:
            user_input = "現在選択中の企業の投資判断をファンダメンタル分析に基づいて教えて"
            submit = True
        elif growth_clicked:
            user_input = "この企業の5年CAGR成長率をどう評価すべきか分析して"
            submit = True
        elif risk_clicked:
            user_input = "この銘柄の主要リスク要因と注意点を教えて"
            submit = True
    
    if submit and user_input:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        try:
            if openai_client:
                response = process_chat_message(user_input)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.success("回答を生成しました！")
            else:
                # Fallback to specialized platform responses
                fallback_response = get_specialized_response(user_input)
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": fallback_response
                })
                st.info("プラットフォーム専用回答")
        except Exception as e:
            # Even if API fails, provide specialized guidance
            fallback_response = get_specialized_response(user_input)
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": fallback_response
            })
            st.warning("APIエラーのため、プラットフォーム専用回答を表示")
        
        st.rerun()


def process_chat_message(message):
    """Process chat message and generate response"""
    if not openai_client:
        return "OpenAI APIキーが設定されていません。チャット機能を使用するにはAPIキーを設定してください。"
    
    # Rate limiting check
    import time
    current_time = time.time()
    if 'last_api_call' not in st.session_state:
        st.session_state.last_api_call = 0
    
    # Limit to one call per 3 seconds to avoid rate limits
    if current_time - st.session_state.last_api_call < 3:
        return "レート制限を避けるため、少しお待ちください。"
    
    try:
        st.session_state.last_api_call = current_time
        
        # Get context from current session for personalized responses
        context_info = get_platform_context()
        
        # Create specialized system prompt with platform integration
        system_prompt = f"""あなたは「1000x Stocks」プラットフォームの専門AI金融アシスタント「KOJI」です。

以下の特別な機能を持っています：
- プラットフォーム内の分析データとの連携
- 日本市場に特化した投資アドバイス
- リアルタイム財務データの解釈
- DCF、ファンダメンタル分析の専門サポート

現在のプラットフォーム状況：
{context_info}

回答ルール：
1. 常に日本語で実用的なアドバイスを提供
2. 具体的な数値や計算式を含める
3. リスク要因も必ず言及
4. プラットフォーム内の他のページへの誘導も行う
5. 一般的な金融知識ではなく、実際の投資判断に役立つ情報を優先

ユーザーが企業名やティッカーを言及した場合、そのデータがプラットフォームにあるかを確認し、具体的な分析を提案してください。"""
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg or "429" in error_msg:
            return "現在、OpenAI APIの利用枠に制限があります。APIキーの課金設定をご確認ください。詳細については OpenAI のドキュメントをご参照ください。"
        elif "401" in error_msg or "invalid" in error_msg:
            return "APIキーが無効です。正しいOpenAI APIキーを設定してください。"
        else:
            return f"申し訳ございませんが、リクエストの処理中にエラーが発生しました: {error_msg}"