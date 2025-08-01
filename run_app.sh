#!/bin/bash

# Set up environment variables
export OPENAI_API_KEY="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"
export GOOGLE_API_KEY="AIzaSyDCDsN9rI19z3O_MbePuimzKI76zrl7UEg"

# Add uv to PATH if not already there
export PATH="$HOME/.local/bin:$PATH"

# Run the app
echo "Starting Investment Analyzer app..."
echo "App will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

uv run streamlit run app_fixed.py --server.port 8501 