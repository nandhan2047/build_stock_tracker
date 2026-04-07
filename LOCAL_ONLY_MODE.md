# 🔒 Local-Only Mode - Run Without External APIs

Run the stock tracker completely locally with **zero external data fetches** - no data breaches, no privacy concerns.

## 🚀 Quick Start - Local Mode (3 Steps)

### Step 1: Create `local_mode.py`
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.stock_data import (
    AnalysisResult, AnalysisConfig, StockInfo, StockMetrics,
    PeerMetrics, PeerAnalysisResult, MacroAnalysisResult, MacroImpact
)
from datetime import datetime

def get_sample_analysis(ticker: str = "AAPL") -> AnalysisResult:
    """Generate sample analysis using ONLY local data - NO API CALLS"""

    result = AnalysisResult(target_ticker=ticker)

    # Sample Stock Info (no API call)
    result.stock_info = StockInfo(
        name="Apple Inc." if ticker == "AAPL" else f"Company {ticker}",
        sector="Technology" if ticker in ["AAPL", "MSFT", "GOOGL"] else "Finance",
        industry="Consumer Electronics" if ticker == "AAPL" else "Software",
        website="https://apple.com" if ticker == "AAPL" else "https://example.com",
        employees=161000,
        description="Sample company data - NOT from live API"
    )

    # Sample Stock Metrics (no API call)
    result.stock_metrics = StockMetrics(
        price=175.50,
        market_cap=2758750000000,
        pe_ratio=28.5,
        forward_pe=26.2,
        peg_ratio=2.1,
        profit_margin=26.5,
        operating_margin=30.1,
        roe=89.2,
        debt_to_equity=0.48,
        current_ratio=1.08,
        quick_ratio=1.04
    )

    # Sample Peer Analysis (no API call)
    result.peer_analysis = PeerAnalysisResult(
        target_ticker=ticker,
        peers=[
            PeerMetrics(
                ticker="MSFT",
                name="Microsoft",
                similarity_score=0.91,
                forward_pe=25.3,
                profit_margin=35.2,
                roe=42.1,
                debt_to_equity=0.32,
                current_ratio=1.89,
                percentile_rank=75
            ),
            PeerMetrics(
                ticker="GOOGL",
                name="Alphabet",
                similarity_score=0.88,
                forward_pe=23.1,
                profit_margin=21.8,
                roe=15.3,
                debt_to_equity=0.08,
                current_ratio=2.71,
                percentile_rank=65
            ),
        ],
        avg_pe_ratio=25.3,
        valuation_verdict="Fair Value",
        recommendation_score=7.5
    )

    # Sample Macro Analysis (no API call)
    result.macro_analysis = MacroAnalysisResult(
        target_ticker=ticker,
        sector="Technology",
        overall_sentiment="Positive",
        macro_score=6,
        tailwinds=[
            "AI demand strong and accelerating",
            "Semiconductor supply improving",
            "Services revenue growing"
        ],
        headwinds=[
            "China tariff exposure",
            "Regulatory scrutiny on App Store",
            "Consumer spending uncertainty"
        ],
        impacts=[
            MacroImpact(factor="Interest Rates", sensitivity=0.8, direction="Negative", explanation="Higher rates reduce consumer spending"),
            MacroImpact(factor="AI Adoption", sensitivity=0.9, direction="Positive", explanation="AI demand driving hardware sales"),
            MacroImpact(factor="Tariffs", sensitivity=0.7, direction="Negative", explanation="China tariffs affect imports"),
        ]
    )

    result.analysis_date = datetime.now()
    result.execution_time_seconds = 0.05  # Local - instant!
    result.cache_hit = False

    return result


def demo_local_analysis():
    """Run analysis using ONLY local data"""
    print("\n" + "="*80)
    print("🔒 LOCAL-ONLY MODE - NO EXTERNAL APIS")
    print("="*80 + "\n")

    result = get_sample_analysis("AAPL")

    # Print results
    print(f"📊 Ticker: {result.target_ticker}")
    print(f"   Company: {result.stock_info.name}")
    print(f"   Sector: {result.stock_info.sector}")
    print(f"   Price: ${result.stock_metrics.price}")
    print(f"   P/E Ratio: {result.stock_metrics.pe_ratio}")
    print(f"   Valuation: {result.peer_analysis.valuation_verdict}")
    print(f"   Macro Sentiment: {result.macro_analysis.overall_sentiment}")
    print(f"\n   ⏱️  Execution: {result.execution_time_seconds:.3f}s (NO API CALLS)")
    print(f"   🔒 Privacy: 100% LOCAL\n")


if __name__ == "__main__":
    demo_local_analysis()
```

### Step 2: Run Locally (No Internet Needed)
```bash
python local_mode.py
```

Output:
```
================================================================================
🔒 LOCAL-ONLY MODE - NO EXTERNAL APIS
================================================================================

📊 Ticker: AAPL
   Company: Apple Inc.
   Sector: Technology
   Price: $175.5
   P/E Ratio: 28.5
   Valuation: Fair Value
   Macro Sentiment: Positive

   ⏱️  Execution: 0.050s (NO API CALLS)
   🔒 Privacy: 100% LOCAL
```

---

## 🔐 Complete Privacy Setup

### Option 1: No Cache Database
```python
# Disable SQLite cache entirely
manager = ResearchManager(use_cache=False)
result = manager.analyze("AAPL", AnalysisConfig(ticker="AAPL"))
# Result stored ONLY in memory, never touches disk
```

### Option 2: Encrypt Cache Database
```bash
# On Linux/Mac - encrypt SQLite db file
openssl enc -aes-256-cbc -salt -in data/stock_tracker.db -out data/stock_tracker.db.enc -pass pass:YOUR_PASSWORD

# Delete unencrypted file
rm data/stock_tracker.db
```

### Option 3: RAM-Only Database
```python
import sqlite3
# Connect to in-memory database instead of disk
conn = sqlite3.connect(':memory:')
# All data lost when process ends - maximum privacy
```

---

## 🌐 Minimal API Mode (Optional)

To use live APIs **but minimize data transfer**:

```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

# Disable everything except basic metrics
config = AnalysisConfig(
    ticker="AAPL",
    include_peer_analysis=False,  # No peer API calls
    include_macro_analysis=False,  # No macro data fetches
    include_colab_generation=False  # No notebook generation
)

manager = ResearchManager(use_cache=True)
result = manager.analyze("AAPL", config)
print(manager.generate_report(result))
```

---

## 🔒 Data Safety Checklist

- [ ] Running `local_mode.py` for sample data only
- [ ] Cache disabled (`use_cache=False`) or encrypted
- [ ] No peer analysis enabled (reduces API calls)
- [ ] No macro analysis enabled (reduces API calls)
- [ ] Database is local SQLite (not cloud)
- [ ] No authentication tokens stored
- [ ] Results never leave your machine

---

## 🚨 What APIs Do We Call?

**If you use live mode**, we call:

| API | Data | Purpose | Frequency |
|-----|------|---------|-----------|
| yfinance | Stock prices, metrics | Valuation | 1 per ticker |
| Yahoo Finance | Peer tickers | Identification | 1 per ticker |
| Yahoo Finance | Peer metrics | Comparison | 1 per peer |
| Dataroma | Superinvestor holdings | Research | Optional |

**Data sent to them:** Only ticker symbol + HTTP request

---

## ✅ Safe Local Usage

```python
# Complete offline analysis - no internet needed
from local_mode import get_sample_analysis

# Generate sample data
result = get_sample_analysis("AAPL")

# All analysis stays local
print(f"Company: {result.stock_info.name}")
print(f"P/E: {result.stock_metrics.pe_ratio}")
print(f"Valuation: {result.peer_analysis.valuation_verdict}")
print(f"Macro Sentiment: {result.macro_analysis.overall_sentiment}")

# No data left the machine ✅
```

---

## 🎯 Recommended Setup

**For maximum privacy:**
1. Use `local_mode.py` (sample data, zero APIs)
2. Disable cache: `use_cache=False`
3. Never enable external APIs
4. Delete SQLite database after use
5. Run in isolated environment (don't share results)

**Data stays 100% local** ✅
