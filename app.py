#!/usr/bin/env python3
"""
Main entry point for the Stock Analysis Platform
This file provides compatibility for deployment systems that expect app.py
The actual main application is in ホーム.py (Home in Japanese)
"""

import sys
import os
import streamlit as st

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point that loads and executes the home page application"""
    try:
        # Import the main home page module using exec
        # This approach works better for Streamlit applications
        home_file_path = os.path.join(os.path.dirname(__file__), "ホーム.py")
        
        if not os.path.exists(home_file_path):
            st.error("メインアプリケーションファイル 'ホーム.py' が見つかりません。")
            st.write("Main application file 'ホーム.py' not found.")
            return
        
        # Read and execute the home page file
        with open(home_file_path, 'r', encoding='utf-8') as f:
            home_code = f.read()
        
        # Execute the home page code in the current namespace
        exec(home_code)
        
    except Exception as e:
        st.error(f"アプリケーションの読み込み中にエラーが発生しました: {e}")
        st.error(f"Error loading main application: {e}")
        st.write("ホーム.py ファイルが正しく設定されていることを確認してください。")
        st.write("Please ensure ホーム.py exists and is properly configured.")
        
        # Show debug information
        st.write("**Debug Information:**")
        st.write(f"Current working directory: {os.getcwd()}")
        st.write(f"Python path: {sys.path}")
        st.write(f"Looking for file: {home_file_path}")
        st.write(f"File exists: {os.path.exists(home_file_path)}")

if __name__ == "__main__":
    main()