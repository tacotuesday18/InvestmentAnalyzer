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
        st.markdown("### AI Financial Assistant")
        
        # Toggle chatbot visibility
        chat_button_text = "💬 Open AI Chat" if not st.session_state.chatbot_visible else "❌ Close Chat"
        if st.button(chat_button_text, key="toggle_chat"):
            st.session_state.chatbot_visible = not st.session_state.chatbot_visible
            st.rerun()
        
        if st.session_state.chatbot_visible:
            st.markdown("---")
            
            # Display recent chat messages
            if st.session_state.chat_messages:
                st.markdown("**Recent Messages:**")
                for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                    if message["role"] == "user":
                        st.markdown(f"👤 **You:** {message['content'][:100]}...")
                    else:
                        st.markdown(f"🤖 **AI:** {message['content'][:100]}...")
                
                if st.button("Clear Chat History", key="clear_chat"):
                    st.session_state.chat_messages = []
                    st.rerun()
            
            # Chat input form
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_area(
                    "Ask about financial analysis:", 
                    height=80, 
                    placeholder="例: AAPLの財務状況は？"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Send", type="primary")
                with col2:
                    if st.form_submit_button("Quick DCF Help"):
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
                        st.success("Response generated!")
                    else:
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": "OpenAI API key required for AI responses. The chatbot needs proper API configuration to function."
                        })
                        st.warning("API key needed")
                except Exception as e:
                    error_msg = f"Chat error: {str(e)}"
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    st.error("Response failed")
                
                st.rerun()


def process_chat_message(message):
    """Process chat message and generate response"""
    if not openai_client:
        return "OpenAI API key not configured. Please set up your API key to use the chat feature."
    
    # Rate limiting check
    import time
    current_time = time.time()
    if 'last_api_call' not in st.session_state:
        st.session_state.last_api_call = 0
    
    # Limit to one call per 3 seconds to avoid rate limits
    if current_time - st.session_state.last_api_call < 3:
        return "Please wait a moment before sending another message to avoid rate limits."
    
    try:
        st.session_state.last_api_call = current_time
        
        # Create context about the financial analysis platform
        system_prompt = """You are an AI financial assistant for a Japanese stock analysis platform. 
        You help users with:
        - Stock analysis and valuation questions
        - DCF calculations and financial modeling
        - Market data interpretation
        - Investment strategy advice
        - Explaining financial ratios and metrics
        
        Respond in Japanese when users ask in Japanese, otherwise use English.
        Keep responses concise but informative. Focus on practical financial advice."""
        
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
        return f"Sorry, I encountered an error processing your request: {str(e)}"