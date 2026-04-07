# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd build_stock_tracker
pip install -r requirements.txt
```

### Step 2: Run Streamlit App
```bash
streamlit run main.py
```

The app will automatically open at `http://localhost:8501`

### Step 3: Analyze a Stock
1. In the sidebar, type a stock ticker (e.g., `AAPL`, `TSLA`, `MSFT`)
2. Configure options:
   - ☑️ Peer Analysis (compare to competitors)
   - ☑️ Macro Analysis (policy impacts)
3. Click **"Analyze Stock"**
4. Explore the results!

---

## Google Colab Quick Start (Recommended for Testing)

### 🚀 One-Cell Colab Setup
```python
# Cell 1: Clone & Setup (Copy-paste this entire cell)
import subprocess
import sys

# Clone repo (skip if already cloned)
try:
    import build_stock_tracker
except ImportError:
    print("📦 Installing project...")
    subprocess.run(["git", "clone", "https://github.com/YOUR_USERNAME/build_stock_tracker.git",
                    "/content/build_stock_tracker"], check=False)

# Install dependencies
subprocess.run(["pip", "install", "-q", "yfinance", "pandas", "requests", "beautifulsoup4",
                "pydantic", "plotly"], capture_output=True)

# Add to path
sys.path.insert(0, '/content/build_stock_tracker')

print("✅ Setup complete!")
```

### 📊 Run Analysis in Colab
```python
# Cell 2: Analyze a stock
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

try:
    manager = ResearchManager(use_cache=False)  # Disable cache in Colab
    result = manager.analyze('AAPL', AnalysisConfig(ticker='AAPL', num_peers=3))
    print(manager.generate_report(result))
    print("✅ Analysis complete!")
except Exception as e:
    print(f"❌ Error: {e}")
```

### 🔧 Local Command Line Usage

```bash
# Run analysis script
python fetch_data_for_given_stock.py

# Or use Python directly
python -c "
import sys
sys.path.insert(0, '.')
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig
manager = ResearchManager()
result = manager.analyze('TSLA', AnalysisConfig(ticker='TSLA'))
print(manager.generate_report(result))
"
```

---

## What Each Module Does

| Module | Purpose | Key Functions |
|--------|---------|---|
| `main.py` | Streamlit web interface | Entry point, dashboard UI |
| `research_manager.py` | Orchestrates analysis | Coordinates all agents |
| `yahoo_scraper.py` | Stock & peer data | Fetches metrics, identifies peers |
| `dataroma_scraper.py` | Superinvestor data | Insider holdings, trades |
| `peer_comparison.py` | Peer analysis agent | Valuations, comparisons |
| `macro_analyst.py` | Macro research agent | Policy impacts, tailwinds/headwinds |
| `colab_generator.py` | Notebook generation | Creates Jupyter scripts |
| `cache.py` | Caching system | SQLite-based persistence |

---

## Example Workflows

### Workflow 1: Quick Stock Check (5 minutes)
1. Open Streamlit: `streamlit run main.py`
2. Type ticker: `NVDA`
3. Click "Analyze Stock"
4. View peer comparison and macro analysis
5. Download JSON if needed

### Workflow 2: Detailed Analysis (15 minutes)
1. Run full analysis for 4 different tickers
2. Compare results across tabs
3. Download peer comparison CSVs
4. Export JSON for further analysis

### Workflow 3: Automation (For Developers)
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

manager = ResearchManager(use_cache=True)

# Analyze multiple stocks
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
for ticker in tickers:
    config = AnalysisConfig(ticker=ticker)
    result = manager.analyze(ticker, config)
    print(f"✓ Analyzed {ticker}")
    # Save results to database, file, etc.
```

---

## Troubleshooting

### Issue: "Ticker not found"
- **Solution:** Check ticker spelling (e.g., use `BRK-B` not `BRK-BRK`)
- Some stocks may not have complete data on Yahoo Finance

### Issue: "Network timeout"
- **Solution:** Check internet connection
- Script will retry 3 times automatically
- Wait a few seconds and try again

### Issue: "No peer data found"
- **Solution:** Try a different, more popular ticker
- Peer matching requires sector classification

### Issue: "Cache not working"
- **Solution:** Check `data/stock_tracker.db` exists
- Clear cache: Click "🔄 Clear Cache" in Streamlit sidebar
- Or delete the file and restart

### Issue: "Import errors"
- **Solution:** Make sure you're in the right directory:
  ```bash
  cd build_stock_tracker
  pip install -r requirements.txt
  ```

---

## Performance Tips

1. **Enable Caching** (default ON)
   - First run: ~15-20 seconds
   - Cached run: <1 second

2. **Limit Peers**
   - Default: 4 peers (fast)
   - Maximum: 8 peers (slower)

3. **Disable Optional Analysis**
   - Disable macro if only need valuations
   - Disable peer if analyzing single stock

4. **Batch Processing**
   - Analyze multiple stocks in sequence
   - Cache builds up, subsequent runs faster

---

## File Locations

```
build_stock_tracker/
├── main.py                      ← Run this file
├── config.py                    ← Edit settings here
├── requirements.txt             ← Python dependencies
│
├── data/
│   ├── stock_tracker.db         ← Cache database (auto-created)
│   ├── cache/                   ← Cache files
│   └── scraped/                 ← Downloaded data
│
├── notebooks/
│   └── generated_scripts/       ← Generated Colab scripts
│
├── logs/
│   └── app.log                  ← Application logs
│
├── src/                         ← Source code
│   ├── agents/                  ← Analysis agents
│   ├── scrapers/                ← Web scrapers
│   ├── models/                  ← Data models
│   ├── database/                ← Cache & DB
│   └── utils/                   ← Helper functions
```

---

## Next Steps

1. **Explore the Dashboard**
   - Try different tickers
   - Compare peers
   - Check macro impacts

2. **Download Results**
   - Export JSON for backup
   - Export CSV for spreadsheet analysis
   - Download Colab notebook for coding

3. **Customize** (`config.py`)
   - Adjust peer matching sensitivity
   - Change cache TTL
   - Add custom sectors/industries

4. **Integrate** (For developers)
   - Use as Python library
   - Build custom analysis workflows
   - Extend with more data sources

5. **Deploy** (Phase 2)
   - Host on Vercel/Railway
   - Add database backend
   - Enable multi-user access

---

## Getting Help

- 📖 **Documentation:** Read `README.md` and `EXECUTION_PLAN.md`
- 🐛 **Bugs:** Check GitHub Issues
- 💡 **Ideas:** Open GitHub Discussions
- 📧 **Contact:** [Your email]

---

## Key Shortcuts

| Shortcut | Purpose |
|----------|---------|
| `Ctrl+C` | Stop Streamlit server |
| Sidebar toggle | Hide/show options |
| Refresh browser | Reset dashboard |
| Clear cache button | Delete cached analyses |

---

## Common Analysis Times

| Analysis | Time |
|----------|------|
| First run (no cache) | 15-20 seconds |
| Cached run | <1 second |
| Full peer analysis | 25-30 seconds |
| With macro analysis | 30-35 seconds |
| Colab generation | 5-10 seconds |

---

**Enjoy analyzing! 📈**

Start with `streamlit run main.py` and explore!
