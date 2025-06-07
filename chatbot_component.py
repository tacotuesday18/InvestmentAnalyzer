import streamlit as st
from streamlit_chat import message
import json
from real_time_data import financial_chatbot, get_live_stock_data, get_industry_averages, get_company_cagr

def render_chatbot():
    """
    Render the floating chatbot component
    """
    # CSS for floating chatbot
    st.markdown("""
    <style>
    .chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        border: 1px solid #e0e0e0;
    }
    
    .chatbot-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px 15px 0 0;
        font-weight: 600;
        font-size: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chatbot-toggle {
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
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        z-index: 1001;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .chatbot-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .chatbot-messages {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        background: #f8f9fa;
    }
    
    .chatbot-input {
        padding: 15px;
        border-top: 1px solid #e0e0e0;
        background: white;
        border-radius: 0 0 15px 15px;
    }
    
    .chat-message {
        margin-bottom: 10px;
        padding: 10px 15px;
        border-radius: 20px;
        max-width: 80%;
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
    
    .quick-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 10px;
    }
    
    .quick-action-btn {
        background: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 5px 10px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action-btn:hover {
        background: #667eea;
        color: white;
    }
    
    @media (max-width: 768px) {
        .chatbot-container {
            width: 100%;
            height: 100%;
            bottom: 0;
            right: 0;
            border-radius: 0;
        }
        
        .chatbot-toggle {
            bottom: 70px;
            right: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'chatbot_open' not in st.session_state:
        st.session_state.chatbot_open = False
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""
    
    # Toggle button
    if not st.session_state.chatbot_open:
        if st.button("💬", key="chatbot_toggle", help="AIアシスタントに質問"):
            st.session_state.chatbot_open = True
            st.rerun()
    
    # Chatbot container
    if st.session_state.chatbot_open:
        with st.container():
            st.markdown("""
            <div class="chatbot-container">
                <div class="chatbot-header">
                    💹 AIファイナンシャルアシスタント
                    <button onclick="window.parent.document.querySelector('[data-testid=\"stButton\"] button').click()" style="background:none;border:none;color:white;font-size:18px;cursor:pointer;">×</button>
                </div>
                <div class="chatbot-messages" id="chat-messages">
            """, unsafe_allow_html=True)
            
            # Display chat messages
            for i, msg in enumerate(st.session_state.chat_messages):
                if msg['role'] == 'user':
                    st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Initial welcome message
            if not st.session_state.chat_messages:
                welcome_msg = """
                こんにちは！AIファイナンシャルアシスタントです。
                
                以下のような質問にお答えできます：
                • 業界平均の財務指標
                • 企業のCAGR（年平均成長率）
                • 収益性指標の分析
                • 財務比率の説明
                
                何かご質問はありますか？
                """
                st.markdown(f'<div class="chat-message bot-message">{welcome_msg}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick action buttons
            st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("業界平均を教えて", key="industry_avg"):
                    handle_quick_question("テクノロジー業界の平均PE、PB、ROEを教えてください")
                if st.button("CAGR計算", key="cagr_calc"):
                    handle_quick_question("AAPLの過去5年間のCAGRを教えてください")
            
            with col2:
                if st.button("収益性分析", key="profitability"):
                    handle_quick_question("収益性指標のROE、ROA、純利益率について説明してください")
                if st.button("財務比率説明", key="ratios"):
                    handle_quick_question("PER、PBR、PEGの違いと意味を教えてください")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input
            st.markdown('<div class="chatbot-input">', unsafe_allow_html=True)
            user_input = st.text_input("質問を入力してください...", key="chat_input_field", placeholder="例: AAPLの業界平均と比較した収益性は？")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("送信", key="send_message") and user_input:
                    handle_user_message(user_input)
            with col2:
                if st.button("閉じる", key="close_chatbot"):
                    st.session_state.chatbot_open = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def handle_user_message(message):
    """Handle user message and generate AI response"""
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": message})
    
    # Determine if we need to fetch specific data
    context_data = {}
    
    # Check if user is asking about specific company
    import re
    ticker_match = re.search(r'\b([A-Z]{2,5})\b', message.upper())
    if ticker_match:
        ticker = ticker_match.group(1)
        live_data = get_live_stock_data(ticker)
        if live_data.get('success'):
            context_data['company_data'] = live_data
    
    # Check for industry-related questions
    if '業界' in message or 'industry' in message.lower():
        # Extract industry or use technology as default
        industry = 'Technology'  # Default
        if 'テクノロジー' in message or 'technology' in message.lower():
            industry = 'Technology'
        elif '金融' in message or 'financial' in message.lower():
            industry = 'Financial'
        elif 'ヘルスケア' in message or 'healthcare' in message.lower():
            industry = 'Healthcare'
        
        industry_data = get_industry_averages(industry)
        context_data['industry_data'] = industry_data
    
    # Check for CAGR questions
    if 'CAGR' in message.upper() or '成長率' in message:
        if ticker_match:
            cagr_data = get_company_cagr(ticker_match.group(1))
            context_data['cagr_data'] = cagr_data
    
    # Generate AI response
    ai_response = financial_chatbot(message, context_data)
    
    # Add AI response
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
    
    # Rerun to show new messages
    st.rerun()

def handle_quick_question(question):
    """Handle quick action button clicks"""
    handle_user_message(question)