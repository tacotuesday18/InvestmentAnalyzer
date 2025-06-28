#!/usr/bin/env python3
"""
Main entry point for the Stock Analysis Platform
This file provides compatibility for deployment systems that expect app.py
The actual main application is in ホーム.py (Home in Japanese)
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application from ホーム.py
try:
    # Import the main home page module
    import importlib.util
    
    # Load ホーム.py as a module
    spec = importlib.util.spec_from_file_location("home", "ホーム.py")
    home_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(home_module)
    
except Exception as e:
    import streamlit as st
    st.error(f"Error loading main application: {e}")
    st.write("Please ensure ホーム.py exists and is properly configured.")