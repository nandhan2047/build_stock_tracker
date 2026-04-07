"""
Streamlit Cloud Compatible Entry Point
Place this file in the root of your GitHub repository
This file imports and runs the main Streamlit app
"""

import sys
from pathlib import Path

# Get the root directory of the project
root_dir = Path(__file__).parent.absolute()

# Add root to Python path so we can import modules
sys.path.insert(0, str(root_dir))

# Now import everything from main.py
from main import *
