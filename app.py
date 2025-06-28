#!/usr/bin/env python3
"""
Main entry point for the Stock Analysis Platform
This file provides compatibility for deployment systems that expect app.py
The actual main application is in ホーム.py (Home in Japanese)
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set up the environment for deployment
os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
os.environ.setdefault('STREAMLIT_SERVER_PORT', '5000')
os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')

# Execute the home page content directly
home_file_path = os.path.join(current_dir, "ホーム.py")

if os.path.exists(home_file_path):
    # Read and execute the home page file content
    with open(home_file_path, 'r', encoding='utf-8') as f:
        home_code = f.read()
    
    # Execute the home page code in the global namespace
    exec(home_code, globals())
else:
    import streamlit as st
    st.error("メインアプリケーションファイル 'ホーム.py' が見つかりません。")
    st.error("Main application file 'ホーム.py' not found.")
    st.write(f"Looking for file: {home_file_path}")
    st.write(f"Current directory: {os.getcwd()}") 
    st.write(f"Files in directory: {os.listdir(current_dir)}")