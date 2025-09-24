#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your Flask app
from enhanced_app_optimized import app

# Vercel entry point
def handler(event, context):
    return app

# For local development
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)