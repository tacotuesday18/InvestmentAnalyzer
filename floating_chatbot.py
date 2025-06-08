import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

def render_floating_chatbot():
    """
    Render a financial AI assistant in the sidebar
    """
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "chatbot_visible" not in st.session_state:
        st.session_state.chatbot_visible = False
    
    # Sidebar-based chatbot
    with st.sidebar:
        st.markdown("### 💬 AI金融アシスタント")
        
        # Toggle chatbot visibility
        chat_button_text = "💬 AIチャットを開く" if not st.session_state.chatbot_visible else "❌ チャットを閉じる"
        if st.button(chat_button_text, key="toggle_chat"):
            st.session_state.chatbot_visible = not st.session_state.chatbot_visible
            st.rerun()
        
        if st.session_state.chatbot_visible:
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
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("送信", type="primary")
                with col2:
                    if st.form_submit_button("DCFヘルプ"):
                        user_input = "DCF計算について教えて"
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
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": "AI回答にはOpenAI APIキーが必要です。チャットボット機能を使用するには適切なAPI設定が必要です。"
                        })
                        st.warning("APIキーが必要です")
                except Exception as e:
                    error_msg = f"チャットエラー: {str(e)}"
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    st.error("回答の生成に失敗しました")
                
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
        
        # Create context about the financial analysis platform
        system_prompt = """あなたは日本の株式分析プラットフォームのAI金融アシスタントです。
        ユーザーを以下の点でサポートしてください：
        - 株式分析と企業価値評価の質問
        - DCF計算と財務モデリング
        - 市場データの解釈
        - 投資戦略のアドバイス
        - 財務比率と指標の説明
        
        常に日本語で回答してください。簡潔でありながら情報量の多い回答を心がけ、実用的な金融アドバイスに焦点を当ててください。
        専門用語を使う場合は、分かりやすく説明を加えてください。"""
        
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
        return f"申し訳ございませんが、リクエストの処理中にエラーが発生しました: {str(e)}"