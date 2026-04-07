# 🚀 Google Colab - Quick Reference (Copy-Paste These 3 Cells)

## Cell 1: Download & Extract (Import Fix Applied!)
```python
import os, zipfile, subprocess, sys, shutil

# Download ZIP
subprocess.run(["curl", "-L", "-o", "/tmp/repo.zip",
                "https://github.com/YOUR_USERNAME/build_stock_tracker/archive/refs/heads/main.zip"],
               capture_output=True)

# Extract
extract_dir = '/content/build_stock_tracker'
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile('/tmp/repo.zip', 'r') as z:
    z.extractall(extract_dir)

# Fix folder structure
extracted = os.path.join(extract_dir, [f for f in os.listdir(extract_dir) if 'build_stock_tracker' in f][0])
for item in os.listdir(extracted):
    shutil.move(os.path.join(extracted, item), os.path.join(extract_dir, item))
shutil.rmtree(extracted)

# Install deps
subprocess.run(["pip", "install", "-q", "yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"],
               capture_output=True)
sys.path.insert(0, extract_dir)
print("✅ Ready!")
```

## Cell 2: Verify (Import Test)
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

## Cell 3: Analyze
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

manager = ResearchManager(use_cache=False)
result = manager.analyze("AAPL", AnalysisConfig(ticker="AAPL", num_peers=3))
print(manager.generate_report(result))
```

---

**Done! 5 minutes to your first analysis! 🎉**
