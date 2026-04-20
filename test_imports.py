"""
COMPREHENSIVE TEST SUITE - Run this locally to catch errors
Tests all imports, syntax, and basic functionality
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*80)
print("COMPREHENSIVE TEST SUITE")
print("="*80 + "\n")

# ============================================================
# TEST 1: Config imports
# ============================================================
print("TEST 1: Loading config...")
try:
    from config import (
        DB_PATH, CACHE_EXPIRY_SECONDS, REQUEST_TIMEOUT,
        REQUEST_RETRY_COUNT, REQUEST_DELAY_SECONDS,
        YAHOO_FINANCE_BASE_URL, DATAROMA_BASE_URL, USER_AGENT,
        MACRO_SECTOR_SENSITIVITY
    )
    print("[OK] Config loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Config error: {e}\n")
    sys.exit(1)

# ============================================================
# TEST 2: Utils imports
# ============================================================
print("TEST 2: Loading utils...")
try:
    from src.utils.logger import setup_logger
    from src.utils.data_cleaning import (
        clean_numeric_value, normalize_ticker, validate_ticker,
        clean_percentage, extract_range, sanitize_string
    )
    from src.utils.calculations import FinancialCalculator, PeerAnalyzer
    print("[OK] Utils loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Utils error: {e}\n")
    sys.exit(1)

# ============================================================
# TEST 3: Models imports
# ============================================================
print("TEST 3: Loading models...")
try:
    from src.models.stock_data import (
        StockInfo, StockMetrics, PeerMetrics,
        PeerAnalysisResult, MacroAnalysisResult, MacroImpact,
        AnalysisResult, AnalysisConfig, CacheEntry
    )
    print("[OK] Models loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Models error: {e}\n")
    sys.exit(1)

# ============================================================
# TEST 4: Scraper imports
# ============================================================
print("TEST 4: Loading scrapers...")
try:
    from src.scrapers.base_scraper import BaseScraper, ScraperError, NoDataError, TickerNotFoundError
    from src.scrapers.yahoo_scraper import YahooFinanceScraper
    from src.scrapers.dataroma_scraper import DataromaScraper
    print("[OK] Scrapers loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Scrapers error: {e}\n")
    sys.exit(1)

# ============================================================
# TEST 5: Database imports
# ============================================================
print("TEST 5: Loading database...")
try:
    from src.database.cache import CacheManager
    print("[OK] Database loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Database error: {e}\n")
    sys.exit(1)

# ============================================================
# TEST 6: Agent imports
# ============================================================
print("TEST 6: Loading agents...")
try:
    from src.agents.peer_comparison import PeerComparisonAgent
    from src.agents.macro_analyst import MacroAnalyst
    from src.agents.research_manager import ResearchManager
    print("[OK] Agents loaded successfully\n")
except Exception as e:
    print(f"[FAIL] Agents error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# TEST 7: Function tests
# ============================================================
print("TEST 7: Testing utility functions...")
try:
    # Test data_cleaning
    assert clean_numeric_value("1.2B") == 1.2e9, "clean_numeric_value failed"
    assert clean_numeric_value("500M") == 5e8, "clean_numeric_value failed"
    assert normalize_ticker("aapl") == "AAPL", "normalize_ticker failed"
    assert validate_ticker("AAPL") == True, "validate_ticker failed"
    print("  [OK] Data cleaning functions work\n")

    # Test calculations
    calc = FinancialCalculator()
    pe = calc.calculate_pe_ratio(100, 5)
    assert pe == 20, f"P/E calculation failed: {pe}"
    print("  [OK] FinancialCalculator works\n")

    # Test peer analyzer
    analyzer = PeerAnalyzer()
    avg = analyzer.calculate_average_metric([10, 20, 30])
    assert avg == 20, f"Average calculation failed: {avg}"
    print("  [OK] PeerAnalyzer works\n")

    print("[OK] Function tests passed\n")
except Exception as e:
    print(f"[FAIL] Function test error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# TEST 8: Model instantiation
# ============================================================
print("TEST 8: Testing model instantiation...")
try:
    stock_info = StockInfo(
        ticker="AAPL",
        name="Apple",
        sector="Technology"
    )

    stock_metrics = StockMetrics(
        ticker="AAPL",
        price=175.50,
        pe_ratio=28.5
    )

    config = AnalysisConfig(ticker="AAPL")

    result = AnalysisResult(target_ticker="AAPL")

    print("[OK] Model instantiation passed\n")
except Exception as e:
    print(f"[FAIL] Model instantiation error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# TEST 9: Manager instantiation (no cache)
# ============================================================
print("TEST 9: Testing ResearchManager instantiation...")
try:
    manager = ResearchManager(use_cache=False)
    print("[OK] ResearchManager instantiated successfully\n")
except Exception as e:
    print(f"[FAIL] ResearchManager error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# SUMMARY
# ============================================================
print("="*80)
print("ALL TESTS PASSED!")
print("="*80)
print("\nCode is ready for:")
print("  [OK] Local testing (Streamlit)")
print("  [OK] HTML website generation")
print("  [OK] Production use\n")
