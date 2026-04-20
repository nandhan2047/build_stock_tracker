"""
Configuration module for Build Stock Tracker.
Handles environment variables, paths, and global settings.
"""

import os
from pathlib import Path
from typing import Dict, List

# ==================== PATH CONFIGURATION ====================
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
SCRAPED_DIR = DATA_DIR / "scraped"
DB_PATH = DATA_DIR / "stock_tracker.db"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
SCRAPED_DIR.mkdir(exist_ok=True)

# ==================== DATABASE CONFIGURATION ====================
DATABASE_URL = f"sqlite:///{DB_PATH}"
CACHE_EXPIRY_DAYS = 7
CACHE_EXPIRY_SECONDS = CACHE_EXPIRY_DAYS * 24 * 60 * 60

# ==================== API & SCRAPING CONFIGURATION ====================
REQUEST_TIMEOUT = 10
REQUEST_RETRY_COUNT = 3
REQUEST_DELAY_SECONDS = 2

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ==================== DATA SOURCES ====================
YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com/quote/"
DATAROMA_BASE_URL = "https://www.dataroma.com/m/stock.php"
FINVIZ_BASE_URL = "https://finviz.com/screener.ashx"

# ==================== FINANCIAL METRICS ====================
KEY_FINANCIAL_METRICS = [
    "Forward P/E",
    "PEG Ratio",
    "Profit Margin",
    "Debt-to-Equity",
    "ROE",
    "ROA",
    "Current Ratio",
    "Quick Ratio",
    "Operating Margin",
    "Free Cash Flow",
]

# ==================== SECTOR CLASSIFICATION ====================
SECTOR_INDUSTRY_MAP: Dict[str, List[str]] = {
    "Technology": [
        "Software",
        "IT Services",
        "Semiconductors",
        "Computer Hardware",
        "Electronics",
    ],
    "Healthcare": [
        "Pharmaceuticals",
        "Biotech",
        "Medical Devices",
        "Healthcare Services",
        "Health Insurers",
    ],
    "Financials": [
        "Banks",
        "Insurance",
        "Financial Services",
        "Investment Banking",
    ],
    "Energy": [
        "Oil & Gas",
        "Renewable Energy",
        "Utilities",
    ],
    "Consumer": [
        "Retail",
        "Consumer Goods",
        "Food & Beverage",
        "Entertainment",
    ],
    "Industrials": [
        "Aerospace & Defense",
        "Machinery",
        "Industrial Distribution",
        "Construction",
    ],
    "Materials": [
        "Chemicals",
        "Metals & Mining",
        "Paper & Forest Products",
    ],
    "Real Estate": [
        "REITs",
        "Real Estate Services",
    ],
    "Communication": [
        "Telecom",
        "Media",
        "Broadcasting",
    ],
}

# ==================== MACRO POLICY IMPACTS BY SECTOR ====================
MACRO_SECTOR_SENSITIVITY: Dict[str, Dict[str, float]] = {
    "Technology": {
        "interest_rates": 0.85,  # High sensitivity
        "inflation": 0.60,
        "tariffs": 0.75,
        "regulations": 0.70,  # AI/data privacy regulations
        "trade_policy": 0.80,
    },
    "Healthcare": {
        "interest_rates": 0.50,
        "inflation": 0.65,
        "tariffs": 0.40,
        "regulations": 0.90,  # FDA, healthcare policy
        "trade_policy": 0.35,
    },
    "Financials": {
        "interest_rates": 0.95,  # Ultra-high sensitivity
        "inflation": 0.55,
        "tariffs": 0.20,
        "regulations": 0.85,  # Banking regulations
        "trade_policy": 0.15,
    },
    "Energy": {
        "interest_rates": 0.70,
        "inflation": 0.75,
        "tariffs": 0.50,
        "regulations": 0.80,  # Climate/environmental policy
        "trade_policy": 0.85,
        "oil_prices": 0.95,
    },
    "Consumer": {
        "interest_rates": 0.65,  # Discretionary spending
        "inflation": 0.85,  # Direct cost impact
        "tariffs": 0.70,  # Imported goods
        "regulations": 0.50,
        "trade_policy": 0.75,
    },
    "Industrials": {
        "interest_rates": 0.75,
        "inflation": 0.70,
        "tariffs": 0.90,  # Supply chain heavy
        "regulations": 0.65,
        "trade_policy": 0.85,
    },
    "Materials": {
        "interest_rates": 0.70,
        "inflation": 0.80,
        "tariffs": 0.85,
        "regulations": 0.75,  # Environmental
        "trade_policy": 0.80,
    },
    "Real Estate": {
        "interest_rates": 0.95,  # Mortgage rates critical
        "inflation": 0.70,
        "tariffs": 0.30,
        "regulations": 0.75,  # Zoning, building codes
        "trade_policy": 0.25,
    },
    "Communication": {
        "interest_rates": 0.60,
        "inflation": 0.65,
        "tariffs": 0.40,
        "regulations": 0.85,  # FCC, data privacy
        "trade_policy": 0.50,
    },
}

# ==================== MACRO DATA SOURCES (Phase 1) ====================
MACRO_DATA_SOURCES = {
    "fed_rates": "https://fred.stlouisfed.org/",  # Will be implemented in Phase 2
    "trade_news": "https://www.reuters.com/business/",
    "policy_announcements": "https://www.whitehouse.gov/briefing-room/",
}

# ==================== PEER IDENTIFICATION ====================
NUM_PEERS_TO_IDENTIFY = 4
PEER_COMPARISON_METRICS = [
    "Forward P/E",
    "PEG Ratio",
    "Profit Margin",
    "Debt-to-Equity",
    "ROE",
]

# ==================== VALUATION THRESHOLDS ====================
VALUATION_PREMIUM_THRESHOLD = 0.15  # 15% above peer average = premium
VALUATION_UNDERVALUED_THRESHOLD = -0.15  # 15% below peer average = undervalued

# ==================== COLAB TEMPLATE ====================
COLAB_SCRIPT_TEMPLATE_PATH = BASE_DIR / "notebooks" / "colab_template.ipynb"

# ==================== LOGGING CONFIGURATION ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# ==================== STREAMLIT CONFIGURATION ====================
STREAMLIT_CONFIG = {
    "page_title": "Build Stock Tracker",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ==================== FEATURE FLAGS ====================
ENABLE_CACHING = True
ENABLE_DATABASE = True
ENABLE_MACRO_SCRAPING = True
ENABLE_PEER_ANALYSIS = True
ENABLE_COLAB_GENERATION = True

# ==================== ERROR MESSAGES ====================
ERROR_MESSAGES = {
    "ticker_not_found": "Ticker '{ticker}' not found. Please check the symbol and try again.",
    "scraper_error": "Error scraping data from {source}. Please try again later.",
    "network_error": "Network error. Please check your connection and try again.",
    "invalid_input": "Invalid input. Please provide a valid stock ticker symbol.",
    "no_data": "No data available for {ticker}. Please try a different ticker.",
}

# ==================== SUCCESS MESSAGES ====================
SUCCESS_MESSAGES = {
    "analysis_complete": "Analysis completed successfully for {ticker}!",
    "cache_hit": "Data loaded from cache for {ticker}.",
    "cache_miss": "Fetching fresh data for {ticker}...",
    "data_saved": "Data saved successfully.",
}

# ==================== ENVIRONMENT VARIABLES ====================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
DEMO_MODE = os.getenv("DEMO_MODE", "False").lower() == "true"

if DEBUG_MODE:
    LOG_LEVEL = "DEBUG"

print(f"[OK] Configuration loaded from {__file__}")
print(f"[OK] Base directory: {BASE_DIR}")
print(f"[OK] Database: {DB_PATH}")
