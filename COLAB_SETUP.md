# 🚀 Google Colab Setup Guide

## Quick Start (3 Minutes)

### Cell 1: Install Dependencies & Clone Repo
```python
import subprocess, sys, os

# Install all required packages (idempotent - safe to run multiple times)
deps = ["yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"]
subprocess.run(["pip", "install", "-q"] + deps, capture_output=True)

# Clone repo (checks if already cloned)
repo_path = "/content/build_stock_tracker"
if not os.path.exists(repo_path):
    print("📥 Cloning repository...")
    subprocess.run(["git", "clone",
                    "https://github.com/YOUR_USERNAME/build_stock_tracker.git",
                    repo_path], capture_output=True)
else:
    print("✓ Repository already cloned")

# Setup Python path
sys.path.insert(0, repo_path)

print("✅ Environment ready!")
```

### Cell 2: Quick Test
```python
import sys
sys.path.insert(0, "/content/build_stock_tracker")

try:
    from src.agents.research_manager import ResearchManager
    from src.models.stock_data import AnalysisConfig
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Error: {e}\nRe-run Cell 1")
```

### Cell 3: Analyze a Stock
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

try:
    print("📊 Analyzing AAPL...")
    manager = ResearchManager(use_cache=False)
    config = AnalysisConfig(ticker="AAPL", num_peers=3)
    result = manager.analyze("AAPL", config)
    print(manager.generate_report(result))
    print("✅ Done!")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## Advanced: Run Multiple Stocks

```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

tickers = ["AAPL", "MSFT", "GOOGL"]
manager = ResearchManager(use_cache=False)

for ticker in tickers:
    try:
        print(f"\n{'='*50}\n📊 {ticker}\n{'='*50}")
        config = AnalysisConfig(ticker=ticker, num_peers=2)
        result = manager.analyze(ticker, config)
        print(manager.generate_report(result))
    except Exception as e:
        print(f"❌ {ticker} failed: {e}")
```

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'yfinance'` | Re-run Cell 1 |
| `No such file or directory: 'build_stock_tracker'` | Re-run Cell 1 |
| `ImportError: cannot import name 'ResearchManager'` | Check `sys.path.insert(0, ...)` in cell |
| `Network timeout` | Run again - autoretries built-in |
| `Ticker not found` | Use valid ticker (e.g., AAPL, MSFT, TSLA) |

---

## ⚡ Performance Tips

- **First run:** 15-25 seconds (API calls + analysis)
- **Subsequent runs:** <5 seconds (if cache enabled)
- **Colab tip:** Disable cache (`use_cache=False`) since /tmp clears between sessions
- **Fewer peers:** Use `num_peers=2` for faster analysis

---

## 📥 Update to Latest Version

```python
import subprocess
subprocess.run(["git", "-C", "/content/build_stock_tracker", "pull", "origin", "main"],
               capture_output=True)
print("✅ Updated!")
```

---

**🎯 Ready to analyze? Start with Cell 1!**
