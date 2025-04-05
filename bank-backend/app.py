#!/usr/bin/env python

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the app
from src.main import app

if __name__ == "__main__":
    app.run(debug=True, port=8000) 