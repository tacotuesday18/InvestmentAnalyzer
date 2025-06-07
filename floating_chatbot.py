import streamlit as st
import json
from real_time_data import financial_chatbot, get_live_stock_data, get_industry_averages, get_company_cagr

def render_floating_chatbot():
    """
    Render a floating chatbot in the bottom right corner
    """
    # Initialize session state
    if 'chatbot_open' not in st.session_state:
        st.session_state.chatbot_open = False
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # CSS for floating chatbot
    st.markdown("""
    <style>
    .floating-chat-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .floating-chat-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    .floating-chat-container {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        height: 450px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        z-index: 999;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        font-weight: 600;
        text-align: center;
        font-size: 16px;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        background: #f8f9fa;
    }
    
    .chat-input-area {
        padding: 15px;
        border-top: 1px solid #e0e0e0;
        background: white;
    }
    
    .chat-message {
        margin-bottom: 12px;
        padding: 8px 12px;
        border-radius: 15px;
        max-width: 85%;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .user-message {
        background: #667eea;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: white;
        color: #333;
        border: 1px solid #e0e0e0;
    }
    
    .quick-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }
    
    .quick-btn {
        background: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-btn:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    @media (max-width: 768px) {
        .floating-chat-container {
            width: calc(100vw - 40px);
            height: 60vh;
            bottom: 90px;
            right: 20px;
            left: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Chat toggle button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("💬", key="chat_toggle", help="AIアシスタント"):
            st.session_state.chatbot_open = not st.session_state.chatbot_open
            st.rerun()
    
    # Chat container
    if st.session_state.chatbot_open:
        # Create chat interface
        with st.container():
            st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
            st.markdown('<div class="chat-header">💹 AIファイナンシャルアシスタント</div>', unsafe_allow_html=True)
            
            # Messages container
            st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
            
            # Display messages
            if not st.session_state.chat_messages:
                welcome_msg = """こんにちは！財務分析のお手伝いをします。

以下のような質問にお答えできます：
• 企業の財務指標分析
• 業界平均との比較
• CAGR計算
• 投資判断のアドバイス

何かご質問はありますか？"""
                st.markdown(f'<div class="chat-message bot-message">{welcome_msg}</div>', unsafe_allow_html=True)
            
            for msg in st.session_state.chat_messages:
                if msg['role'] == 'user':
                    st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick action buttons
            st.markdown('<div class="quick-buttons">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("AAPL分析", key="quick_aapl", use_container_width=True):
                    process_chat_message("AAPLの最新の財務指標を教えてください")
                if st.button("業界平均", key="quick_industry", use_container_width=True):
                    process_chat_message("テクノロジー業界の平均PERを教えてください")
            
            with col2:
                if st.button("CAGR計算", key="quick_cagr", use_container_width=True):
                    process_chat_message("MSFTの過去5年のCAGRを計算してください")
                if st.button("投資判断", key="quick_advice", use_container_width=True):
                    process_chat_message("現在の市場状況での投資戦略を教えてください")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input area
            st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input("質問を入力...", key="chat_input", placeholder="例: AAPLの現在の株価は？")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("送信", key="send_btn", use_container_width=True) and user_input:
                    process_chat_message(user_input)
            with col2:
                if st.button("閉じる", key="close_btn", use_container_width=True):
                    st.session_state.chatbot_open = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def process_chat_message(message):
    """Process chat message and generate response"""
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": message})
    
    # Get context data if needed
    context_data = {}
    
    # Check for specific company mentions
    import re
    ticker_match = re.search(r'\b([A-Z]{2,5})\b', message.upper())
    if ticker_match:
        ticker = ticker_match.group(1)
        try:
            live_data = get_live_stock_data(ticker)
            if live_data.get('success'):
                context_data['company_data'] = live_data
        except:
            pass
    
    # Check for industry questions
    if '業界' in message or 'industry' in message.lower():
        industry = 'Technology'
        try:
            industry_data = get_industry_averages(industry)
            context_data['industry_data'] = industry_data
        except:
            pass
    
    # Generate AI response
    try:
        ai_response = financial_chatbot(message, context_data)
    except Exception as e:
        ai_response = f"申し訳ございません。エラーが発生しました: {str(e)}"
    
    # Add AI response
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
    
    # Rerun to update display
    st.rerun()