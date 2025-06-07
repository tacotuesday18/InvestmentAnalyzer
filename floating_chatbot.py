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
    Render a floating chatbot in the bottom right corner
    """
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "chatbot_visible" not in st.session_state:
        st.session_state.chatbot_visible = False
    
    # Sidebar-based chatbot for better functionality
    with st.sidebar:
        st.markdown("### AI Financial Assistant")
        
        # Toggle chatbot visibility
        if st.button("💬 Open AI Chat" if not st.session_state.chatbot_visible else "❌ Close Chat"):
            st.session_state.chatbot_visible = not st.session_state.chatbot_visible
            st.rerun()
        
        if st.session_state.chatbot_visible:
            st.markdown("---")
            
            # Display chat messages
            for message in st.session_state.chat_messages[-5:]:  # Show last 5 messages
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
            
            # Chat input
            user_input = st.text_area("Ask about stocks, financial analysis, or market data:", 
                                    height=100, 
                                    placeholder="Type your financial question here...")
            
            if st.button("Send Message", type="primary") and user_input:
                # Add user message
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                
                # Generate AI response
                if openai_client:
                    try:
                        response = process_chat_message(user_input)
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": f"Error: {str(e)}"
                        })
                else:
                    st.session_state.chat_messages.append({
                        "role": "assistant", 
                        "content": "OpenAI API key not configured. Please set up your API key."
                    })
                
                st.rerun()
            
            if st.button("Clear Chat"):
                st.session_state.chat_messages = []
                st.rerun()


def process_chat_message(message):
    """Process chat message and generate response"""
    if not openai_client:
        return "OpenAI API key not configured. Please set up your API key to use the chat feature."
    
    try:
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