# Graph Report - C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker  (2026-04-19)

## Corpus Check
- 28 files · ~49,299 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 306 nodes · 681 edges · 38 communities detected
- Extraction: 46% EXTRACTED · 54% INFERRED · 0% AMBIGUOUS · INFERRED: 370 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]

## God Nodes (most connected - your core abstractions)
1. `StockMetrics` - 41 edges
2. `StockInfo` - 32 edges
3. `YahooFinanceScraper` - 31 edges
4. `AnalysisResult` - 30 edges
5. `BaseScraper` - 30 edges
6. `MacroAnalysisResult` - 27 edges
7. `ResearchManager` - 26 edges
8. `PeerAnalysisResult` - 24 edges
9. `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` - 23 edges
10. `PeerComparisonAgent` - 21 edges

## Surprising Connections (you probably didn't know these)
- `get_sample_analysis()` --calls--> `StockMetrics`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `get_sample_analysis()` --calls--> `PeerMetrics`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `get_sample_analysis()` --calls--> `MacroImpact`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` --uses--> `StockMetrics`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` --uses--> `PeerMetrics`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (43): BaseModel, ColabGenerator, _create_code_cell(), _create_markdown_cell(), Colab Script Generator - Creates self-contained Google Colab notebooks. Generate, Create a markdown cell., Generates Google Colab-ready Python scripts with analysis., Initialize Colab generator. (+35 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (31): CacheManager, Cache management module using SQLite for local caching. Reduces API calls and im, Delete a cache entry.          Args:             key: Cache key          Returns, Delete all expired cache entries.          Returns:             Number of entrie, Clear all cache entries.          Returns:             True if successful, Get cache statistics.          Returns:             Dictionary with cache stats, Manages caching of analysis results using SQLite., Initialize cache manager.          Args:             db_path: Path to SQLite dat (+23 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (23): ABC, BaseScraper, NoDataError, Base scraper class and common scraping utilities. Provides abstract base and hel, Exception raised when no data can be scraped., Abstract base class for all scrapers., Create a requests session with proper headers., Add delay to respect server rate limits. (+15 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (31): handle_consent_page(), Handle Yahoo Finance consent page.      Args:         response: Initial response, Retrieve data from cache.          Args:             key: Cache key          Ret, calculate_similarity_score(), identify_peer_characteristics(), clean_value(), extract_yf_quarterly_table_data(), get_yahoo_finance_page_with_session() (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (17): Custom exception for scraper errors., Exception raised when ticker is not found., ScraperError, TickerNotFoundError, normalize_ticker(), Normalize ticker to uppercase and strip whitespace.      Args:         ticker: R, Exception, Convert to dictionary. (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (13): MacroAnalyst, Macro Analyst Agent - Researches policy and macro impacts on stocks. Analyzes gl, Identify relevant impacts for a specific sector.          Args:             sect, Macro Analyst Agent.      Responsibilities:     1. Research sector-specific macr, Categorize impacts into tailwinds and headwinds.          Args:             impa, Calculate overall macro sentiment.          Args:             impacts: List of i, Calculate overall macro score (-10 to +10).          Args:             impacts:, Format macro analysis as readable report.          Args:             result: Mac (+5 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (4): calculate_average_metric(), calculate_peer_percentile(), calculate_valuation_verdict(), Financial calculations module. Provides utility classes for financial ratio calc

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (15): CacheEntry, Config, InsiderTransaction, InvestmentThesis, Data models for the stock tracker application. Uses Pydantic for type validation, Investment thesis combining all analysis., Superinvestor holding data from Dataroma., Insider trading transaction data. (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (9): clean_percentage(), extract_range(), Data cleaning and normalization utilities. Handles parsing, validation, and norm, Extract numeric range from string like "1.5 - 2.5".      Args:         value: Ra, Sanitize string by removing extra whitespace.      Args:         value: String t, Validate ticker format.      Args:         ticker: Ticker to validate      Retur, Clean percentage values.      Args:         value: Percentage value (with or wit, sanitize_string() (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (5): display_website_link(), open_website_in_colab(), Colab utility functions - Display website in Colab., Read HTML website file for display in Colab.      Args:         website_path: Pa, Print website file path and usage instructions.      Args:         website_path:

### Community 10 - "Community 10"
Cohesion: 0.5
Nodes (3): Logging configuration module. Sets up structured logging for the application., Setup and configure a logger for a module., setup_logger()

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Configuration module for Build Stock Tracker. Handles environment variables, pa

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Streamlit Cloud Compatible Entry Point Place this file in the root of your GitHu

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Main scraping method. Must be implemented by subclasses.

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Calculate forward P/E ratio.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Calculate PEG ratio.         PEG = P/E Ratio / Expected Annual Earnings Growth R

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Calculate debt-to-equity ratio.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Calculate current ratio (liquidity).

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Calculate quick ratio (acid-test ratio).

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Calculate Return on Equity (ROE).

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Calculate Return on Assets (ROA).

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Calculate profit margin.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Calculate operating margin.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Calculate free cash flow.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Calculate free cash flow yield.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Calculate average of a list of metric values, ignoring None values.          Arg

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Calculate what percentile the target value falls in among peers.          Args:

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Determine if stock is overvalued, fairly valued, or undervalued vs peers.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Calculate how similar a peer is to the target based on key metrics.          Arg

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Identify key characteristics of a peer company.          Args:             peer_

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **86 isolated node(s):** `Configuration module for Build Stock Tracker. Handles environment variables, pa`, `Scrapes stock data from Finviz for a specified country and a given number of pag`, `Scrapes super investor holdings and insider trading summary data for a given tic`, `Attempts to fetch a Yahoo Finance page, handling the consent page using a persis`, `Helper function to scrape insider transactions data for a single ticker from Yah` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (2 nodes): `config.py`, `Configuration module for Build Stock Tracker. Handles environment variables, pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `Streamlit Cloud Compatible Entry Point Place this file in the root of your GitHu`, `app.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Main scraping method. Must be implemented by subclasses.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Calculate forward P/E ratio.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Calculate PEG ratio.         PEG = P/E Ratio / Expected Annual Earnings Growth R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Calculate debt-to-equity ratio.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Calculate current ratio (liquidity).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Calculate quick ratio (acid-test ratio).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Calculate Return on Equity (ROE).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Calculate Return on Assets (ROA).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Calculate profit margin.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Calculate operating margin.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Calculate free cash flow.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Calculate free cash flow yield.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Calculate average of a list of metric values, ignoring None values.          Arg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Calculate what percentile the target value falls in among peers.          Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Determine if stock is overvalued, fairly valued, or undervalued vs peers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Calculate how similar a peer is to the target based on key metrics.          Arg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Identify key characteristics of a peer company.          Args:             peer_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `CacheManager` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `StockMetrics` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`StockMetrics` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `StockInfo` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`StockInfo` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `YahooFinanceScraper` (e.g. with `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` and `PeerComparisonAgent`) actually correct?**
  _`YahooFinanceScraper` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `AnalysisResult` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`AnalysisResult` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `BaseScraper` (e.g. with `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` and `DataromaScraper`) actually correct?**
  _`BaseScraper` has 20 INFERRED edges - model-reasoned connections that need verification._