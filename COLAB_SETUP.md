# 🚀 Google Colab Setup Guide (Fixed!)

## ⚡ Quick Start (3 Minutes - Zip Method)

### Cell 1: Download & Extract Repo
```python
import os, zipfile, subprocess, sys

# Download ZIP from GitHub
subprocess.run(["curl", "-L", "-o", "/tmp/repo.zip",
                "https://github.com/YOUR_USERNAME/build_stock_tracker/archive/refs/heads/main.zip"],
               capture_output=True)

# Extract
extract_dir = '/content/build_stock_tracker'
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile('/tmp/repo.zip', 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Move extracted content to correct level (remove 'main' subfolder)
import shutil
extracted = os.path.join(extract_dir, [f for f in os.listdir(extract_dir) if 'build_stock_tracker' in f][0])
for item in os.listdir(extracted):
    shutil.move(os.path.join(extracted, item), os.path.join(extract_dir, item))
shutil.rmtree(extracted)

# Install dependencies
deps = ["yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"]
subprocess.run(["pip", "install", "-q"] + deps, capture_output=True)

# Setup path
sys.path.insert(0, extract_dir)
print("✅ Environment ready!")
```

### Cell 2: Verify Imports
```python
import sys
sys.path.insert(0, '/content/build_stock_tracker')

try:
    from src.agents.research_manager import ResearchManager
    from src.models.stock_data import AnalysisConfig
    from src.utils.data_cleaning import clean_numeric_value
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Error: {e}")
```

### Cell 3: Analyze Stock
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

try:
    manager = ResearchManager(use_cache=False)
    result = manager.analyze("AAPL", AnalysisConfig(ticker="AAPL", num_peers=3))
    print(manager.generate_report(result))
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
