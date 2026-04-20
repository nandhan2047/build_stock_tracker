# Graph Report - C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker  (2026-04-19)

## Corpus Check
- 24 files · ~44,267 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 288 nodes · 675 edges · 53 communities detected
- Extraction: 38% EXTRACTED · 62% INFERRED · 0% AMBIGUOUS · INFERRED: 417 edges (avg confidence: 0.55)
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
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]

## God Nodes (most connected - your core abstractions)
1. `StockMetrics` - 46 edges
2. `YahooFinanceScraper` - 37 edges
3. `StockInfo` - 36 edges
4. `AnalysisResult` - 34 edges
5. `BaseScraper` - 30 edges
6. `ResearchManager` - 27 edges
7. `PeerComparisonAgent` - 26 edges
8. `MacroAnalysisResult` - 26 edges
9. `MacroAnalyst` - 25 edges
10. `PeerAnalysisResult` - 24 edges

## Surprising Connections (you probably didn't know these)
- `BaseScraper` --uses--> `Extract superinvestor holdings from table with id='grid'.          Args:`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\scrapers\base_scraper.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\scrapers\dataroma_scraper.py
- `BaseScraper` --uses--> `Extract insider trading summary from table with id='ins_sum'.          Args:`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\scrapers\base_scraper.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\scrapers\dataroma_scraper.py
- `get_sample_analysis()` --calls--> `AnalysisResult`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `get_sample_analysis()` --calls--> `StockInfo`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py
- `get_sample_analysis()` --calls--> `StockMetrics`  [INFERRED]
  C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\local_mode.py → C:\Users\raghunandhan.palla\OneDrive - Accenture\Desktop\My_folder\project stock tracker\build_stock_tracker\src\models\stock_data.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (40): CacheManager, Cache management module using SQLite for local caching. Reduces API calls and im, Delete a cache entry.          Args:             key: Cache key          Returns, Delete all expired cache entries.          Returns:             Number of entrie, Clear all cache entries.          Returns:             True if successful, Get cache statistics.          Returns:             Dictionary with cache stats, Manages caching of analysis results using SQLite., Store data in cache.          Args:             key: Cache key             data: (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (29): ABC, BaseScraper, Base scraper class and common scraping utilities. Provides abstract base and hel, Custom exception for scraper errors., Exception raised when ticker is not found., Abstract base class for all scrapers., Create a requests session with proper headers., ScraperError (+21 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (20): demo_report(), get_sample_analysis(), Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m, Generate and display sample report, Generate sample analysis using ONLY local data - NO API CALLS, MacroAnalyst, Macro Analyst Agent - Researches policy and macro impacts on stocks. Analyzes gl, Identify relevant impacts for a specific sector.          Args:             sect (+12 more)

### Community 3 - "Community 3"
Cohesion: 0.22
Nodes (20): BaseScraper, FinancialCalculator, PeerAnalyzer, Analyzes peer comparison metrics., Performs financial ratio calculations., PeerComparisonAgent, Peer Comparison Agent - Analyzes target stock vs peers. Identifies peers and com, Calculate how similar a peer is to the target.          Simple scoring based on (+12 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (16): handle_consent_page(), Handle Yahoo Finance consent page.      Args:         response: Initial response, Retrieve data from cache.          Args:             key: Cache key          Ret, calculate_similarity_score(), identify_peer_characteristics(), clean_percentage(), normalize_ticker(), Data cleaning and normalization utilities. Handles parsing, validation, and norm (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (18): NoDataError, Exception raised when no data can be scraped., Add delay to respect server rate limits., Fetch a page with retry logic and error handling.          Args:             url, clean_numeric_value(), extract_range(), Extract numeric range from string like "1.5 - 2.5".      Args:         value: Ra, Clean and convert numeric values from various formats.     Handles: "1.2B", "500 (+10 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (4): calculate_average_metric(), calculate_peer_percentile(), calculate_valuation_verdict(), Financial calculations module. Provides utility classes for financial ratio calc

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (14): BaseModel, CacheEntry, Config, InsiderTransaction, Data models for the stock tracker application. Uses Pydantic for type validation, Superinvestor holding data from Dataroma., Insider trading transaction data., Shareholder/institutional investor data. (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (2): Initialize cache manager.          Args:             db_path: Path to SQLite dat, Initialize database schema if needed.

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (3): Logging configuration module. Sets up structured logging for the application., Setup and configure a logger for a module., setup_logger()

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Configuration module for Build Stock Tracker. Handles environment variables, pa

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Streamlit Cloud Compatible Entry Point Place this file in the root of your GitHu

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

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
Nodes (1): Main scraping method. Must be implemented by subclasses.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Calculate forward P/E ratio.

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Calculate PEG ratio.         PEG = P/E Ratio / Expected Annual Earnings Growth R

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Calculate debt-to-equity ratio.

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Calculate current ratio (liquidity).

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Calculate quick ratio (acid-test ratio).

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Calculate Return on Equity (ROE).

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Calculate Return on Assets (ROA).

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Calculate profit margin.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Calculate operating margin.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Calculate free cash flow.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Calculate free cash flow yield.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Calculate average of a list of metric values, ignoring None values.          Arg

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Calculate what percentile the target value falls in among peers.          Args:

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Determine if stock is overvalued, fairly valued, or undervalued vs peers.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Calculate how similar a peer is to the target based on key metrics.          Arg

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Identify key characteristics of a peer company.          Args:             peer_

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Scrapes stock data from Finviz for a specified country and a given number of pag

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Scrapes super investor holdings and insider trading summary data for a given tic

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Attempts to fetch a Yahoo Finance page, handling the consent page using a persis

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Helper function to scrape insider transactions data for a single ticker from Yah

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Scrapes insider transactions data for one or more ticker symbols from Yahoo Fina

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): Helper function to scrape detailed shareholder data for a single ticker from Yah

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Scrapes detailed shareholder data for one or more ticker symbols from Yahoo Fina

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Attempts to fetch a Yahoo Finance page, handling the consent page using a persis

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Cleans a string value by removing non-numeric characters (except for '-' and '.'

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): Scrapes Cash Flow statement data for a given ticker from Yahoo Finance.      A

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Scrapes Financial statement data (Income Statement) for a given ticker from Yaho

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): Attempts to fetch a Yahoo Finance page, handling the consent page using a persis

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Extracts data from the 'yf-kbx2lo' table on Yahoo Finance Key Statistics page.

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Scrapes Balance Sheet data for a given ticker from Yahoo Finance.      Args:

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Colab utility functions - Display website in Colab.

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Read HTML website file for display in Colab.      Args:         website_path: Pa

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Print website file path and usage instructions.      Args:         website_path:

## Knowledge Gaps
- **86 isolated node(s):** `Configuration module for Build Stock Tracker. Handles environment variables, pa`, `Streamlit Cloud Compatible Entry Point Place this file in the root of your GitHu`, `Cache management module using SQLite for local caching. Reduces API calls and im`, `Manages caching of analysis results using SQLite.`, `Initialize cache manager.          Args:             db_path: Path to SQLite dat` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `config.py`, `Configuration module for Build Stock Tracker. Handles environment variables, pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `Streamlit Cloud Compatible Entry Point Place this file in the root of your GitHu`, `app.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Main scraping method. Must be implemented by subclasses.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Calculate forward P/E ratio.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Calculate PEG ratio.         PEG = P/E Ratio / Expected Annual Earnings Growth R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Calculate debt-to-equity ratio.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Calculate current ratio (liquidity).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Calculate quick ratio (acid-test ratio).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Calculate Return on Equity (ROE).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Calculate Return on Assets (ROA).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Calculate profit margin.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Calculate operating margin.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Calculate free cash flow.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Calculate free cash flow yield.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Calculate average of a list of metric values, ignoring None values.          Arg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Calculate what percentile the target value falls in among peers.          Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Determine if stock is overvalued, fairly valued, or undervalued vs peers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Calculate how similar a peer is to the target based on key metrics.          Arg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Identify key characteristics of a peer company.          Args:             peer_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Scrapes stock data from Finviz for a specified country and a given number of pag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Scrapes super investor holdings and insider trading summary data for a given tic`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Attempts to fetch a Yahoo Finance page, handling the consent page using a persis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Helper function to scrape insider transactions data for a single ticker from Yah`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Scrapes insider transactions data for one or more ticker symbols from Yahoo Fina`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `Helper function to scrape detailed shareholder data for a single ticker from Yah`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Scrapes detailed shareholder data for one or more ticker symbols from Yahoo Fina`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Attempts to fetch a Yahoo Finance page, handling the consent page using a persis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Cleans a string value by removing non-numeric characters (except for '-' and '.'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `Scrapes Cash Flow statement data for a given ticker from Yahoo Finance.      A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Scrapes Financial statement data (Income Statement) for a given ticker from Yaho`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `Attempts to fetch a Yahoo Finance page, handling the consent page using a persis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Extracts data from the 'yf-kbx2lo' table on Yahoo Finance Key Statistics page.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Scrapes Balance Sheet data for a given ticker from Yahoo Finance.      Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Colab utility functions - Display website in Colab.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Read HTML website file for display in Colab.      Args:         website_path: Pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Print website file path and usage instructions.      Args:         website_path:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `CacheManager` connect `Community 0` to `Community 8`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `BaseScraper` connect `Community 1` to `Community 0`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 43 inferred relationships involving `StockMetrics` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`StockMetrics` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `YahooFinanceScraper` (e.g. with `COMPREHENSIVE TEST SUITE - Run this locally to catch errors BEFORE Colab Tests a` and `PeerComparisonAgent`) actually correct?**
  _`YahooFinanceScraper` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `StockInfo` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`StockInfo` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `AnalysisResult` (e.g. with `Local-Only Mode - Run analysis with ZERO external API calls All data is sample/m` and `Generate sample analysis using ONLY local data - NO API CALLS`) actually correct?**
  _`AnalysisResult` has 29 INFERRED edges - model-reasoned connections that need verification._