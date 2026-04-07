# Build Stock Tracker - Complete Reference

## 📁 Folder Structure
```
build_stock_tracker/
├── main.py                          # Streamlit entry point
├── config.py                        # Configuration (50+ settings)
├── requirements.txt                 # Dependencies
├── app.py                           # Streamlit Cloud entry point
│
├── src/
│   ├── agents/
│   │   ├── research_manager.py      # Orchestrator (ticker → analysis)
│   │   ├── peer_comparison.py       # Peer analysis agent
│   │   ├── macro_analyst.py         # Macro policy impact agent
│   │   └── colab_generator.py       # Jupyter notebook generation
│   │
│   ├── scrapers/
│   │   ├── base_scraper.py          # Abstract base + error handling
│   │   ├── yahoo_scraper.py         # Stock metrics & peer identification
│   │   └── dataroma_scraper.py      # Superinvestor holdings
│   │
│   ├── models/
│   │   └── stock_data.py            # 15+ Pydantic models (type safety)
│   │
│   ├── database/
│   │   └── cache.py                 # SQLite cache (7-day TTL)
│   │
│   ├── utils/
│   │   ├── logger.py                # Structured logging
│   │   ├── data_cleaning.py         # Parse 1.2B, 500M, percentages, ranges
│   │   └── calculations.py          # Financial ratios + peer analysis
│   │
│   └── visualizations/              # (Phase 2)
│
├── data/
│   ├── cache/                       # Cache files
│   ├── scraped/                     # Raw data
│   └── stock_tracker.db             # SQLite database
│
├── notebooks/generated_scripts/     # Auto-generated Colab notebooks
├── logs/                            # Application logs
│
├── .md files (documentation)
└── .git/
```

## 🔑 Core Functionality

### Data Flow
```
User Ticker
↓
Research Manager (validate ticker)
├→ Cache Check (SQLite)
│  ├ HIT → return cached + execution_time
│  └ MISS → proceed
├→ YahooFinanceScraper
│  ├ fetch stock info (name, sector, industry)
│  ├ fetch metrics (P/E, PEG, margins, ROE, D/E)
│  └ identify peers (4+ competitors by sector/industry)
├→ PeerComparisonAgent
│  ├ fetch peer metrics
│  ├ calculate ratios
│  ├ determine valuation (Premium/Fair/Undervalued)
│  └ percentile rankings
├→ MacroAnalyst
│  ├ research sector-specific impacts
│  ├ interest rate sensitivity
│  ├ tariff/regulatory exposure
│  └ macro sentiment (-10 to +10)
├→ ColabGenerator
│  └ create self-contained Jupyter notebook
└→ Store in Cache + Display Dashboard
```

### Key Classes & Methods

**ResearchManager**
- `analyze(ticker, config)` → AnalysisResult
- `generate_report(result)` → formatted ASCII report

**YahooFinanceScraper**
- `scrape(ticker)` → {"info": StockInfo, "metrics": StockMetrics, "peers": [tickers]}

**PeerComparisonAgent**
- `analyze(target_ticker, target_metrics, peer_tickers, num_peers)` → PeerAnalysisResult

**MacroAnalyst**
- `analyze(ticker, sector)` → MacroAnalysisResult

**FinancialCalculator** (static methods)
- calculate_pe_ratio, calculate_forward_pe, calculate_peg_ratio
- calculate_debt_to_equity, calculate_current_ratio, calculate_quick_ratio
- calculate_roe, calculate_roa, calculate_profit_margin, calculate_operating_margin
- calculate_free_cash_flow, calculate_fcf_yield

**PeerAnalyzer** (static methods)
- calculate_average_metric(values) → float
- calculate_peer_percentile(target, peers) → int (0-100)
- calculate_valuation_verdict(target_pe, avg_peer_pe) → "Premium"/"Fair Value"/"Undervalued"
- calculate_similarity_score(target_metrics, peer_metrics) → float (0-1)
- identify_peer_characteristics(metrics) → dict

**DataCleaning** (utility functions)
- normalize_ticker(ticker) → uppercase + strip
- validate_ticker(ticker) → bool
- clean_numeric_value(value) → float (parses "1.2B", "500M", "1.5K")
- clean_percentage(value) → float
- extract_range(value) → (min, max) tuple
- sanitize_string(value) → string

**CacheManager**
- `get(key)` → cached data or None
- `set(key, data)` → store with TTL
- `delete(key)` → remove entry
- `clear_expired()` → cleanup

### Data Models (src/models/stock_data.py)
- StockInfo, StockMetrics
- PeerMetrics, PeerAnalysisResult
- MacroImpact, MacroAnalysisResult
- AnalysisResult, AnalysisConfig
- CacheEntry, SuperinvestorHolding

## ⚙️ Configuration (config.py)
- REQUEST_TIMEOUT, REQUEST_RETRY_COUNT, REQUEST_DELAY_SECONDS
- USER_AGENT, DB_PATH, CACHE_EXPIRY_SECONDS
- YAHOO_FINANCE_BASE_URL, DATAROMA_BASE_URL
- Financial metrics to track
- MACRO_SECTOR_SENSITIVITY dict

## 🐛 Critical Fixes Applied

1. **Missing Files Created**
   - src/utils/data_cleaning.py (all parsing functions)
   - src/utils/calculations.py (FinancialCalculator + PeerAnalyzer)

2. **Hardcoded Paths Fixed** (8 files)
   - Changed from: `sys.path.insert(0, '/home/claude/build_stock_tracker')`
   - Changed to: `sys.path.insert(0, str(Path(__file__).parent.parent.parent))`
   - Applied to all agents, scrapers, database, and main.py

3. **Colab Setup Fixed**
   - Git clone creates double nesting: `/content/build_stock_tracker/build_stock_tracker/`
   - Solution: Use ZIP extraction method (see QUICK_COLAB_3_CELLS.md)

## 🚀 Google Colab (ZIP Method - Works!)

**Cell 1: Download & Extract**
```python
import os, zipfile, subprocess, sys, shutil

subprocess.run(["curl", "-L", "-o", "/tmp/repo.zip",
                "https://github.com/YOUR_USERNAME/build_stock_tracker/archive/refs/heads/main.zip"],
               capture_output=True)

extract_dir = '/content/build_stock_tracker'
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile('/tmp/repo.zip', 'r') as z:
    z.extractall(extract_dir)

extracted = os.path.join(extract_dir, [f for f in os.listdir(extract_dir) if 'build_stock_tracker' in f][0])
for item in os.listdir(extracted):
    shutil.move(os.path.join(extracted, item), os.path.join(extract_dir, item))
shutil.rmtree(extracted)

subprocess.run(["pip", "install", "-q", "yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"],
               capture_output=True)
sys.path.insert(0, extract_dir)
print("✅ Ready!")
```

**Cell 2: Verify**
```python
import sys
sys.path.insert(0, "/content/build_stock_tracker")

try:
    from src.agents.research_manager import ResearchManager
    from src.utils.data_cleaning import clean_numeric_value
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Error: {e}")
```

**Cell 3: Analyze**
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

manager = ResearchManager(use_cache=False)
result = manager.analyze("AAPL", AnalysisConfig(ticker="AAPL", num_peers=3))
print(manager.generate_report(result))
```

## 📊 Performance
- First run (no cache): 15-25 seconds
- Cached run: <1 second
- Full peer analysis: 25-30 seconds
- Analysis + macro: 30-35 seconds

## 🔄 Workflow Example
```
User: "Analyze AAPL"
1. Validate ticker: ✓ AAPL
2. Check cache: MISS
3. Fetch from Yahoo: Stock info + 4 peers (MSFT, GOOGL, META, NVDA)
4. Fetch peer metrics from Yahoo
5. Calculate ratios (P/E, PEG, ROE, margins, etc)
6. Determine valuation (Fair Value vs peers)
7. Analyze macro impacts (tech sector, interest rates, AI demand)
8. Generate Colab notebook
9. Cache result (7-day TTL)
10. Display dashboard (tabs: Peer | Macro | Financials | Download)
```

## 📦 Dependencies
```
yfinance           - Stock data
pandas             - Data manipulation
requests           - HTTP requests
beautifulsoup4     - HTML parsing
pydantic           - Type validation
plotly             - Interactive charts
streamlit          - Web dashboard
```

## 🎯 Quick Commands

**Local**: `streamlit run main.py` → `http://localhost:8501`

**Python**:
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig
manager = ResearchManager()
result = manager.analyze('AAPL', AnalysisConfig(ticker='AAPL'))
print(manager.generate_report(result))
```

## 🔗 Key Files for Refactoring
- research_manager.py - Main orchestrator (add new analysis here)
- config.py - Change settings here
- stock_data.py - Add new Pydantic models here
- base_scraper.py - Add new scrapers here
- data_cleaning.py - Add new parsing functions here
- calculations.py - Add new financial ratios here

## ⚠️ Common Issues & Fixes
| Issue | Fix |
|-------|-----|
| ImportError: module not found | Check sys.path.insert(0, ...) at module top |
| "Ticker not found" | Use valid ticker (AAPL, MSFT, TSLA) |
| Network timeout | Retry logic built-in, retries 3x with backoff |
| Cache database locked | Delete stock_tracker.db and restart |
| Double-nested folder in Colab | Use ZIP extraction (Cell 1), not git clone |
