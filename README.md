# 📈 Build Stock Tracker

A **multi-agent financial research system** that provides 360-degree analysis of any stock ticker, generating interactive dashboards and Google Colab-ready Python scripts.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Active Development](https://img.shields.io/badge/Status-Active-brightgreen)]()

## 🎯 Features

### Core Capabilities
- ✅ **Stock Information & Metrics** - Real-time data from Yahoo Finance
- ✅ **Peer Comparison Analysis** - Identify direct competitors and compare valuations
- ✅ **Macro Policy Impact Analysis** - Research interest rates, tariffs, regulations
- ✅ **Superinvestor Holdings** - Track what institutional investors are buying/selling
- ✅ **Interactive Dashboard** - Streamlit-powered web interface
- ✅ **Colab Script Generation** - Auto-generate self-contained Jupyter notebooks
- ✅ **Smart Caching** - SQLite-based caching with 7-day TTL
- ✅ **Fast & Lightweight** - No paid APIs, uses free data sources only

### Technical Highlights
- 🏗️ **Modular Architecture** - Clean separation of agents, scrapers, models
- 🔄 **Multi-Agent System** - Research Manager, Peer Agent, Macro Agent, Colab Agent
- 📊 **Plotly Visualizations** - Interactive charts like Google Finance
- 🗄️ **Type Safety** - Pydantic models for all data structures
- 🪵 **Structured Logging** - Track analysis workflow and errors
- 🚀 **Production Ready** - Error handling, retry logic, rate limiting

## 🚀 Quick Start

### Option A: Google Colab (Fastest - No Setup!)
```python
# Cell 1: Install & Clone
import subprocess, sys
subprocess.run(["pip", "install", "-q", "yfinance", "pandas", "requests", "beautifulsoup4", "pydantic", "plotly"], capture_output=True)
subprocess.run(["git", "clone", "https://github.com/YOUR_USERNAME/build_stock_tracker.git", "/content/build_stock_tracker"], capture_output=False)
sys.path.insert(0, '/content/build_stock_tracker')
print("✅ Setup complete!")

# Cell 2: Analyze
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig
manager = ResearchManager(use_cache=False)
result = manager.analyze('AAPL', AnalysisConfig(ticker='AAPL'))
print(manager.generate_report(result))
```

### Option B: Local Setup

## 📊 Analysis Output

### Executive Dossier
- Stock basic info (name, sector, industry)
- Key financial metrics (P/E, margins, debt ratios)
- Valuation verdict (Premium/Fair Value/Undervalued)

### Peer Comparison
- Direct industry competitors identified automatically
- Side-by-side metric comparison (Forward P/E, PEG, Margins, D/E)
- Percentile rankings within peer group
- Similarity scoring

### Macro Analysis
- 3+ sector-specific policy impacts
- Interest rate sensitivity
- Tariff & trade war exposure
- Regulatory impacts
- Overall macro sentiment score (-10 to +10)

### Interactive Visualizations
- Forward P/E comparison chart
- Valuation scatter plot
- Peer metrics heatmap
- Historical price chart (in Colab script)

### Downloadable Artifacts
- JSON export of full analysis
- CSV export of peer comparison
- Google Colab notebook (self-contained)

## 🏗️ Project Structure

```
build_stock_tracker/
├── main.py                          # 🚀 Streamlit entry point
├── config.py                        # ⚙️ Configuration & constants
├── requirements.txt                 # 📦 Dependencies
│
├── src/
│   ├── agents/
│   │   ├── research_manager.py      # 🎯 Main orchestrator
│   │   ├── peer_comparison.py       # 📈 Peer analysis agent
│   │   ├── macro_analyst.py         # 🌍 Macro research agent
│   │   └── colab_generator.py       # 📝 Colab script generation
│   │
│   ├── scrapers/
│   │   ├── base_scraper.py          # 🏗️ Abstract base class
│   │   ├── yahoo_scraper.py         # 📊 Yahoo Finance scraper
│   │   ├── dataroma_scraper.py      # 👥 Superinvestor data
│   │   └── macro_scraper.py         # 🌐 Macro trends (Phase 2)
│   │
│   ├── models/
│   │   └── stock_data.py            # 📋 Pydantic data models
│   │
│   ├── database/
│   │   └── cache.py                 # 💾 SQLite cache manager
│   │
│   ├── utils/
│   │   ├── logger.py                # 🪵 Structured logging
│   │   ├── data_cleaning.py         # 🧹 Data parsing & validation
│   │   └── calculations.py          # 🧮 Financial ratio calculations
│   │
│   └── visualizations/
│       └── (Phase 2 - Plotly charts)
│
├── notebooks/
│   ├── generated_scripts/           # 📥 Auto-generated Colab scripts
│   └── analysis_sample.ipynb        # 📚 Example notebook
│
├── data/
│   ├── cache/                       # 💾 Cache files
│   ├── scraped/                     # 📂 Raw data
│   └── stock_tracker.db             # 🗄️ SQLite database
│
├── tests/
│   └── (Phase 2 - Unit tests)
│
├── EXECUTION_PLAN.md                # 📋 Phase 1-2 roadmap
├── PHASE_2_ENHANCEMENTS.md          # 🚀 Future improvements
└── README.md                        # 📖 This file
```

## 🔄 How It Works

### Analysis Workflow
```
User Input (Ticker)
    ↓
Research Manager (Orchestrator)
    ├─→ Yahoo Scraper
    │   ├─ Fetch stock info
    │   ├─ Get financial metrics
    │   └─ Identify peers
    │
    ├─→ Peer Comparison Agent
    │   ├─ Fetch peer metrics
    │   ├─ Calculate ratios
    │   └─ Determine valuation
    │
    ├─→ Macro Analyst Agent
    │   ├─ Research policy impacts
    │   ├─ Assess sector exposure
    │   └─ Calculate macro score
    │
    └─→ Colab Generator
        └─ Create Jupyter notebook
    ↓
Cache Manager (SQLite)
    ↓
Streamlit Dashboard
    ├─ Display metrics
    ├─ Show charts
    └─ Enable downloads
```

## 💡 Key Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Web Framework | Streamlit | Fast prototyping, zero DevOps |
| Data Validation | Pydantic | Type safety, serialization |
| Data Manipulation | Pandas | Fast tabular operations |
| Web Scraping | BeautifulSoup4 | HTML parsing |
| Stock Data | yfinance | Free, reliable API |
| Visualization | Plotly | Interactive charts |
| Caching | SQLite | Built-in, lightweight |
| Logging | Python logging | Structured, file-based |

## 📈 Data Sources (All Free)

1. **Yahoo Finance** - Stock prices, metrics, fundamentals
2. **Dataroma** - Superinvestor holdings, insider trading
3. **Finviz** - Stock screening, sector data
4. **Federal Reserve FRED** (Phase 2) - Interest rates, macro data
5. **Trading Economics** (Phase 2) - Global macro indicators

## ⚙️ Configuration

Edit `config.py` to customize:
- API timeouts and retries
- Cache expiry (default 7 days)
- Financial metrics to track
- Macro sector sensitivities
- Peer identification parameters

## 🚨 Error Handling

The system handles:
- ✅ Ticker not found
- ✅ Network timeouts
- ✅ Parsing errors
- ✅ Missing data
- ✅ Cache misses
- ✅ Rate limiting

All errors are logged and returned gracefully to the user.

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EXECUTIVE RESEARCH DOSSIER                                ║
║                         Ticker: AAPL                              
╚══════════════════════════════════════════════════════════════════════════════╝

📌 COMPANY PROFILE
──────────────────────────────────────────────────────────────────────────────
Name:           Apple Inc.
Sector:         Technology
Industry:       Consumer Electronics

💰 KEY METRICS
──────────────────────────────────────────────────────────────────────────────
Current Price:  $175.50
Market Cap:     $2,758,750,000,000
P/E Ratio:      28.5
Forward P/E:    26.2
PEG Ratio:      2.1

📊 PEER COMPARISON
──────────────────────────────────────────────────────────────────────────────
Valuation:      Fair Value
Avg P/E (Peers): 25.3
Your P/E:       26.2
Number of Peers: 4

🌍 MACRO OUTLOOK
──────────────────────────────────────────────────────────────────────────────
Overall Sentiment: Positive

Tailwinds (Positive):
  • AI demand strong and accelerating
  • Semiconductor shortage easing
  • Services revenue growing

Headwinds (Risks):
  • China tariff exposure
  • Regulatory scrutiny on App Store
  • Consumer spending uncertainty
```

## 🔮 Phase 2 Enhancements (Roadmap)

See `PHASE_2_ENHANCEMENTS.md` for:
- ✨ Advanced LLM-based agents (Claude API, LangChain)
- ✨ FastAPI backend for production
- ✨ Supabase PostgreSQL integration
- ✨ Real-time macro data (FRED, Mirofish, Trading Economics)
- ✨ Railway/Vercel deployment
- ✨ Historical analysis tracking
- ✨ ML-based peer identification
- ✨ User alerts & portfolio tracking

## 🧪 Testing

```bash
# Run scraper tests
python -m pytest tests/test_scrapers.py -v

# Run agent tests
python -m pytest tests/test_agents.py -v

# Run utility tests
python -m pytest tests/test_utils.py -v
```

## 📝 Usage Examples

### Example 1: Analyze a Stock
```python
from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig

manager = ResearchManager(use_cache=True)
config = AnalysisConfig(ticker="TSLA", num_peers=4)
result = manager.analyze("TSLA", config)
print(manager.generate_report(result))
```

### Example 2: Custom Peer Comparison
```python
from src.agents.peer_comparison import PeerComparisonAgent
from src.scrapers.yahoo_scraper import YahooFinanceScraper

scraper = YahooFinanceScraper()
agent = PeerComparisonAgent(scraper)

data = scraper.scrape("NVDA")
result = agent.analyze(
    target_ticker="NVDA",
    target_metrics=data['metrics'],
    peer_tickers=data['peers'],
    num_peers=4
)
print(agent.format_comparison_table(result))
```

### Example 3: Macro Analysis
```python
from src.agents.macro_analyst import MacroAnalyst

analyst = MacroAnalyst()
result = analyst.analyze("MSFT", sector="Technology")
print(analyst.format_macro_report(result))
```

## 📚 Documentation

- **[EXECUTION_PLAN.md](EXECUTION_PLAN.md)** - Complete Phase 1-2 roadmap
- **[PHASE_2_ENHANCEMENTS.md](PHASE_2_ENHANCEMENTS.md)** - Future improvements
- **Inline code comments** - Every function documented
- **Docstrings** - Full API documentation

## 🐛 Known Limitations

1. **Peer identification** - Uses simple industry matching (Phase 2 will use ML embeddings)
2. **Macro data** - Hardcoded impacts (Phase 2 will integrate live APIs)
3. **Historical analysis** - Single snapshot only (Phase 2 will add tracking)
4. **Colab scripts** - Basic template (Phase 2 will have advanced visualizations)
5. **No user accounts** - Local use only (Phase 2 will add Supabase)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new code
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

- 📖 Check the docs in `EXECUTION_PLAN.md`
- 🐛 Report bugs on GitHub Issues
- 💬 Discuss features on GitHub Discussions
- 📧 Contact: [your email]

## 🎉 Acknowledgments

- **Yahoo Finance** for stock data
- **Dataroma** for superinvestor data
- **Streamlit** for amazing web framework
- **Plotly** for interactive visualizations
- **Pydantic** for data validation

---

**Built with ❤️ by [Your Name]**

⭐ If you find this useful, please star the repo!

**Last Updated:** April 2024  
**Version:** 1.0.0-beta
