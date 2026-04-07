# 🚀 Google Colab - Quick Reference (Copy-Paste These 3 Cells)

## Cell 1: Install & Clone (30 seconds)
```python
import subprocess, sys, os

deps = ["yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"]
subprocess.run(["pip", "install", "-q"] + deps, capture_output=True)

repo_path = "/content/build_stock_tracker"
if not os.path.exists(repo_path):
    subprocess.run(["git", "clone", "https://github.com/YOUR_USERNAME/build_stock_tracker.git", repo_path], capture_output=True)

sys.path.insert(0, repo_path)
print("✅ Environment ready!")
```

## Cell 2: Verify Imports (5 seconds)
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

## Cell 3: Analyze Stock (15-25 seconds)
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

## Multiple Stocks (Add New Cell)
```python
for ticker in ["AAPL", "MSFT", "GOOGL"]:
    try:
        config = AnalysisConfig(ticker=ticker, num_peers=2)
        result = manager.analyze(ticker, config)
        print(f"\n{'='*50}\n{ticker}\n{'='*50}")
        print(manager.generate_report(result))
    except Exception as e:
        print(f"❌ {ticker}: {e}")
```

---

**That's it! You're done in 5 minutes! 🎉**

For detailed guide: See **COLAB_SETUP.md**
