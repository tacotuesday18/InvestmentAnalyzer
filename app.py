#!/usr/bin/env python3
"""
Main entry point for the Stock Analysis Platform
This file provides compatibility for deployment systems that expect app.py
The actual main application is in ホーム.py (Home in Japanese)
"""

import sys
import os
import streamlit as st
import importlib.util

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def load_home_module():
    """Load and execute the home page module using importlib"""
    home_file_path = os.path.join(current_dir, "ホーム.py")
    
    try:
        if not os.path.exists(home_file_path):
            st.error("メインアプリケーションファイル 'ホーム.py' が見つかりません。")
            st.error("Main application file 'ホーム.py' not found.")
            return False
        
        # Use importlib to load the module properly
        spec = importlib.util.spec_from_file_location("home", home_file_path)
        if spec is None or spec.loader is None:
            st.error("モジュールの読み込みに失敗しました。")
            st.error("Failed to load module specification.")
            return False
            
        home_module = importlib.util.module_from_spec(spec)
        
        # Add the module to sys.modules to prevent import issues
        sys.modules["home"] = home_module
        
        # Execute the module
        spec.loader.exec_module(home_module)
        
        return True
        
    except UnicodeDecodeError as e:
        st.error(f"ファイルエンコーディングエラー: {e}")
        st.error(f"File encoding error: {e}")
        return False
    except ImportError as e:
        st.error(f"モジュールインポートエラー: {e}")
        st.error(f"Module import error: {e}")
        return False
    except Exception as e:
        st.error(f"アプリケーションの読み込み中にエラーが発生しました: {e}")
        st.error(f"Error loading main application: {e}")
        
        # Show debug information in development
        with st.expander("デバッグ情報 / Debug Information"):
            st.write(f"Current working directory: {os.getcwd()}")
            st.write(f"Python path: {sys.path}")
            st.write(f"Looking for file: {home_file_path}")
            st.write(f"File exists: {os.path.exists(home_file_path)}")
            st.write(f"Exception type: {type(e).__name__}")
            st.write(f"Exception details: {str(e)}")
        
        return False

def main():
    """Main entry point that loads and executes the home page application"""
    # Set up the environment for deployment
    os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
    os.environ.setdefault('STREAMLIT_SERVER_PORT', '5000')
    os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')
    
    # Load the main application
    success = load_home_module()
    
    if not success:
        st.write("---")
        st.info("アプリケーションの起動に問題が発生しました。サポートにお問い合わせください。")
        st.info("There was an issue starting the application. Please contact support.")

if __name__ == "__main__":
    main()