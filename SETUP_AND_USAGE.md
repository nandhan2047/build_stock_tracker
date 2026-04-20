# Stock Tracker - Complete Setup & Usage Guide

## What This Does

Multi-agent financial research system that analyzes stocks and generates an **interactive HTML website** you can view locally on your browser.

**Main Features:**
- Fetch stock data & identify peers
- Compare valuation vs peers
- Analyze macro economic impacts
- Generate **interactive HTML dashboard with 7 tabs**
- Works locally on Windows/Mac/Linux
- 7-day caching for speed

---

## Quick Start (Choose One)

### Option 1: Local (Recommended)

**Fastest way to get started:**

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/build_stock_tracker.git
cd build_stock_tracker

# Install dependencies
pip install -r requirements.txt

# Run analysis (Python script)
python3 -c "
from src.agents.research_manager import ResearchManager
manager = ResearchManager()
result = manager.analyze('AAPL')
print(manager.generate_report(result))
print(f'View HTML: {result.website_path}')
# Open file:// URL in browser
"

# OR use Streamlit dashboard
streamlit run main.py
```

**What you get:**
- `analysis_AAPL.html` file in `/websites/` directory
- Open in any browser
- Interactive charts, 7 data-rich tabs

### Option 2: Google Colab (Advanced - Requires Upload)

---

## Website Features (7 Interactive Tabs)

The generated HTML dashboard includes:

1. **Overview** - Key metrics (Market Cap, P/E, 52-week high/low)
2. **Metrics** - Financial ratios (ROE, D/E, Current Ratio, Profit Margin)
3. **Peer Comparison** - P/E comparison chart vs competitors
4. **Macro Analysis** - Economic impact analysis
5. **Investment Thesis** - AI-generated rating, conviction, strengths/weaknesses, catalysts, risks
6. **Percentile Rankings** - Where stock ranks vs peers on key metrics (P/E, PEG, Profit Margin, ROE, FCF)
7. **Financial Health** - Operating Margin, ROA, Quick Ratio, Free Cash Flow, Revenue, Net Income

**All Charts Interactive:**
- Hover for details
- Zoom/pan functionality
- Responsive design
- Dark theme

---

## Project Structure

```
build_stock_tracker/
├── main.py                          # Streamlit dashboard
├── config.py                        # Global settings
├── requirements.txt                 # Dependencies
│
├── src/
│   ├── agents/
│   │   ├── research_manager.py      # Main orchestrator
│   │   ├── website_generator.py     # HTML website generator
│   │   ├── peer_comparison.py       # Peer analysis
│   │   └── macro_analyst.py         # Macro economic analysis
│   │
│   ├── scrapers/
│   │   ├── yahoo_scraper.py         # Stock data
│   │   └── dataroma_scraper.py      # Superinvestor holdings
│   │
│   ├── models/
│   │   └── stock_data.py            # Pydantic data models
│   │
│   ├── database/
│   │   └── cache.py                 # SQLite cache (7-day TTL)
│   │
│   └── utils/
│       ├── logger.py                # Logging
│       ├── data_cleaning.py         # Data parsing functions
│       └── calculations.py          # Financial ratios
│
├── websites/                        # Generated HTML files
└── data/
    ├── stock_tracker.db             # SQLite cache
    └── cache/
```

---

## Core Workflow

ResearchManager orchestrates everything:

```
User Input (ticker)
      |
Validate ticker
      |
Check cache (SQLite)
      |
      +- HIT   → Return cached result (< 1 second)
      +- MISS  → Continue
      |
Fetch stock info (Yahoo)
      |
Identify & fetch peer metrics (Yahoo)
      |
Peer comparison analysis + percentile rankings
      |
Macro economic impact analysis
      |
Generate investment thesis (AI-generated rating, conviction level, catalysts, risks)
      |
Generate HTML website (7 tabs with Plotly interactive charts)
      |
Cache result (7-day TTL)
      |
Return AnalysisResult
```

---

## Usage Examples

### Example 1: Basic Analysis
```python
from src.agents.research_manager import ResearchManager

manager = ResearchManager()
result = manager.analyze("TSLA")

if result and result.website_path:
    print(f"HTML dashboard generated: {result.website_path}")
    print(f"Open in browser: file://{result.website_path}")
    print(manager.generate_report(result))
```

### Example 2: Custom Configuration
```python
from src.models.stock_data import AnalysisConfig

config = AnalysisConfig(
    ticker="MSFT",
    num_peers=5,                      # Compare vs 5 competitors
    include_peer_analysis=True,
    include_macro_analysis=True,
)

manager = ResearchManager()
result = manager.analyze("MSFT", config)
print(manager.generate_report(result))

# Open websites/analysis_MSFT.html in browser
```

### Example 3: Zero-API Testing (Local Mode)
```python
# Run local_mode.py - generates sample analysis without API calls
python local_mode.py
```

---

## ⚙️ Configuration (config.py)

Key settings to customize:

```python
# Timeouts & retries
REQUEST_TIMEOUT = 10              # seconds
REQUEST_RETRY_COUNT = 3
REQUEST_DELAY_SECONDS = 0.5

# Paths
DB_PATH = "data/stock_tracker.db"
CACHE_EXPIRY_SECONDS = 604800     # 7 days

# API endpoints
YAHOO_FINANCE_BASE_URL = "https://query1.finance.yahoo.com"
DATAROMA_BASE_URL = "https://www.dataroma.com"

# User agent (required for scraping)
USER_AGENT = "Mozilla/5.0..."
```

---

## 📊 Data Models (Pydantic)

Main classes:

- **AnalysisResult**: Complete analysis output with website path
- **StockInfo**: ticker, name, sector, industry
- **StockMetrics**: P/E, forward P/E, PEG, ROE, D/E, margins, etc
- **PeerAnalysisResult**: peers, valuation verdict, percentile rankings
- **MacroAnalysisResult**: tailwinds, headwinds, overall sentiment
- **AnalysisConfig**: Control what gets analyzed

---

## 🧰 Key Classes & Methods

### ResearchManager
- `analyze(ticker, config)` → AnalysisResult (generates website!)
- `generate_report(result)` → ASCII report string
- `close()` → cleanup

### HTMLWebsiteGenerator (NEW!)
- `generate(analysis_result)` → Path to HTML file
- Generates interactive Plotly charts
- Dark theme by default
- Mobile responsive

### FinancialCalculator
All static methods:
- `calculate_pe_ratio(price, eps)`
- `calculate_roe(net_income, equity)`
- `calculate_debt_to_equity(debt, equity)`
- 12+ more metrics

### PeerAnalyzer
All static methods:
- `calculate_average_metric(values)`
- `calculate_peer_percentile(target, peers)`
- `calculate_valuation_verdict(target_pe, avg_peer_pe)`
- `calculate_similarity_score(target_metrics, peer_metrics)`

### DataCleaning
Utility functions:
- `normalize_ticker(ticker)` → uppercase + strip
- `validate_ticker(ticker)` → bool
- `clean_numeric_value(value)` → float (parses "1.2B", "500M")
- `clean_percentage(value)` → float
- `extract_range(value)` → (min, max) tuple

---

## 📦 Dependencies

```
yfinance           - Stock data fetching
pandas             - Data manipulation
requests           - HTTP requests
beautifulsoup4     - HTML parsing
pydantic           - Type validation
plotly             - Interactive charts
```

---

## ✅ Critical Fixes Done

✓ **Syntax errors** - Fixed f-string braces in research_manager.py
✓ **Missing imports** - Added Dict to colab_generator.py
✓ **Hardcoded paths** - All use dynamic Path(__file__) now
✓ **Missing files** - Created data_cleaning.py + calculations.py
✓ **Colab setup** - Use ZIP extraction (not git clone)
✓ **Website generation** - NEW HTMLWebsiteGenerator class (Plotly charts)
✓ **Colab utils** - NEW colab_utils.py for public URLs + display
✓ **Website format string** - Fixed template syntax in website_generator.py (Apr 7)
✓ **JavaScript escaping** - Fixed Plotly chart generation in HTML output (Apr 7)
✓ **Return statement** - Added missing return in _create_html() (Apr 7)
✓ **Ngrok removed** - Simplified to display HTML directly in Colab (Apr 7)

---

## 🐛 Troubleshooting

### "Website file not found"
- Make sure analysis completed successfully (result.website_path not None)
- Check websites/ folder exists

### "ImportError: No module named X"
- Run Cell 1 setup in Colab first
- Check sys.path.insert() is at top of each file

### "Ticker not found"
- Use valid ticker (AAPL, MSFT, TSLA, etc)
- Check Yahoo Finance has data for that ticker

### "Cache database locked"
- Delete `data/stock_tracker.db`
- Restart Python/Colab

### Colab website not displaying
- Use Cell 3 with `open_website_in_colab()` and `display(HTML(...))`
- Or download the HTML file to view locally in browser
- No ngrok auth token needed!

---

## 🔗 Quick Navigation

**For Developers:**
- Extend analysis: Edit `research_manager.py` analyze() method
- Add metrics: Edit `calculations.py` FinancialCalculator class
- Change theme: Edit `website_generator.py` CSS section
- Add scraper: Create new class inheriting from `base_scraper.py`

**For Users:**
- Analyze: Copy-paste Colab cells above
- Customize: Modify AnalysisConfig before calling analyze()
- Export: Open generated HTML in any browser

---

## ⏱️ Performance

- **First run** (no cache): 15-25 seconds
- **Cached run**: <1 second
- **Website generation**: Instant
- **TTL**: 7 days (then cache refreshes)

---

## 📝 Version Info

- **Entry point**: `main.py` (Streamlit) or Colab cells
- **Latest**: Includes HTML website generation
- **Status**: All errors fixed, ready for production
- **Tested on**: Windows, Mac, Linux, Google Colab

---

**Generated**: Stock data dashboard system
**Author**: Multi-agent financial research pipeline
**License**: MIT (modify as needed)
