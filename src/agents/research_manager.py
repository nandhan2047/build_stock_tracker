"""
Research Manager Agent - Orchestrates the multi-agent analysis workflow.
Coordinates all other agents and produces the final analysis result.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from typing import Optional, Dict, Any
from datetime import datetime
import time

from src.utils.logger import setup_logger
from src.utils.data_cleaning import normalize_ticker, validate_ticker
from src.models.stock_data import AnalysisResult, AnalysisConfig
from src.scrapers.yahoo_scraper import YahooFinanceScraper
from src.scrapers.dataroma_scraper import DataromaScraper
from src.agents.peer_comparison import PeerComparisonAgent
from src.agents.macro_analyst import MacroAnalyst
from src.agents.colab_generator import ColabGenerator
from src.database.cache import CacheManager

logger = setup_logger(__name__)


class ResearchManager:
    """
    Lead Research Manager Agent.

    Coordinates the workflow:
    1. Receive ticker and validate
    2. Fetch basic stock info
    3. Delegate to peer comparison agent
    4. Delegate to macro analyst
    5. Generate Colab script
    6. Compile final report
    """

    def __init__(self, use_cache: bool = True):
        """Initialize the research manager."""
        self.yahoo_scraper = YahooFinanceScraper()
        self.dataroma_scraper = DataromaScraper()
        self.cache_manager = CacheManager() if use_cache else None
        self.use_cache = use_cache

    def analyze(self, ticker: str, config: Optional[AnalysisConfig] = None) -> Optional[AnalysisResult]:
        """
        Execute complete analysis for a stock.

        Args:
            ticker: Stock ticker symbol
            config: Analysis configuration

        Returns:
            AnalysisResult object with all analysis data
        """
        start_time = time.time()

        # Normalize and validate ticker
        ticker = normalize_ticker(ticker)
        if not validate_ticker(ticker):
            logger.error(f"Invalid ticker format: {ticker}")
            return None

        logger.info(f"🔍 Starting analysis for {ticker}")

        # Create config if not provided
        if config is None:
            config = AnalysisConfig(ticker=ticker)

        # Check cache
        cache_hit = False
        if self.use_cache and self.cache_manager:
            cached_result = self.cache_manager.get(f"analysis_{ticker}")
            if cached_result:
                logger.info(f"✅ Cache hit for {ticker}")
                cached_result.cache_hit = True
                cached_result.execution_time_seconds = time.time() - start_time
                return cached_result
            logger.info(f"📥 Cache miss for {ticker}")

        # Initialize result
        result = AnalysisResult(target_ticker=ticker)

        # Step 1: Fetch stock info
        logger.info(f"📊 Step 1/4: Fetching stock information for {ticker}")
        try:
            yahoo_data = self.yahoo_scraper.scrape(ticker)
            if yahoo_data:
                result.stock_info = yahoo_data.get("info")
                result.stock_metrics = yahoo_data.get("metrics")
                logger.info(f"✓ Stock info retrieved for {ticker}")
            else:
                logger.warning(f"⚠️ No stock info found for {ticker}")
                return None

        except Exception as e:
            logger.error(f"❌ Error fetching stock info: {e}")
            return None

        # Step 2: Peer Analysis
        if config.include_peer_analysis:
            logger.info(f"📈 Step 2/4: Performing peer comparison for {ticker}")
            try:
                peer_agent = PeerComparisonAgent(self.yahoo_scraper)
                peer_analysis = peer_agent.analyze(
                    target_ticker=ticker,
                    target_metrics=result.stock_metrics,
                    peer_tickers=yahoo_data.get("peers"),
                    num_peers=config.num_peers,
                )
                result.peer_analysis = peer_analysis
                logger.info(f"✓ Peer analysis completed for {ticker}")
            except Exception as e:
                logger.warning(f"⚠️ Peer analysis failed: {e}")

        # Step 3: Macro Analysis
        if config.include_macro_analysis:
            logger.info(f"🌍 Step 3/4: Analyzing macro impacts for {ticker}")
            try:
                macro_agent = MacroAnalyst()
                macro_analysis = macro_agent.analyze(
                    target_ticker=ticker,
                    sector=result.stock_info.sector if result.stock_info else None,
                )
                result.macro_analysis = macro_analysis
                logger.info(f"✓ Macro analysis completed for {ticker}")
            except Exception as e:
                logger.warning(f"⚠️ Macro analysis failed: {e}")

        # Step 4: Generate Colab Script
        if config.include_colab_generation:
            logger.info(f"📝 Step 4/4: Generating Colab script for {ticker}")
            try:
                colab_gen = ColabGenerator()
                script_path = colab_gen.generate(
                    analysis_result=result,
                    output_dir=None,  # Uses default path from ColabGenerator
                )
                result.colab_script_path = script_path
                logger.info(f"✓ Colab script generated: {script_path}")
            except Exception as e:
                logger.warning(f"⚠️ Colab generation failed: {e}")

        # Finalize
        result.analysis_date = datetime.now()
        result.execution_time_seconds = time.time() - start_time

        # Cache result
        if self.use_cache and self.cache_manager:
            self.cache_manager.set(f"analysis_{ticker}", result.to_dict())
            logger.info(f"💾 Analysis cached for {ticker}")

        logger.info(f"✅ Analysis complete for {ticker} in {result.execution_time_seconds:.2f}s")

        return result

    def generate_report(self, result: AnalysisResult) -> str:
        """
        Generate executive summary report.

        Args:
            result: AnalysisResult object

        Returns:
            Formatted report string
        """
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EXECUTIVE RESEARCH DOSSIER                                ║
║                         Ticker: {result.target_ticker}                              
╚══════════════════════════════════════════════════════════════════════════════╝

📌 COMPANY PROFILE
{'─' * 80}
Name:           {result.stock_info.name if result.stock_info else 'N/A'}
Sector:         {result.stock_info.sector if result.stock_info else 'N/A'}
Industry:       {result.stock_info.industry if result.stock_info else 'N/A'}

💰 KEY METRICS
{'─' * 80}
Current Price:  ${result.stock_metrics.price if result.stock_metrics else 'N/A'}
Market Cap:     {f"${result.stock_metrics.market_cap:,.0f}" if result.stock_metrics and result.stock_metrics.market_cap else 'N/A'}
P/E Ratio:      {result.stock_metrics.pe_ratio if result.stock_metrics else 'N/A'}
Forward P/E:    {result.stock_metrics.forward_pe if result.stock_metrics else 'N/A'}
PEG Ratio:      {result.stock_metrics.peg_ratio if result.stock_metrics else 'N/A'}

📊 PEER COMPARISON
{'─' * 80}
"""

        if result.peer_analysis:
            report += f"""
Valuation:      {result.peer_analysis.valuation_verdict or 'N/A'}
Avg P/E (Peers): {result.peer_analysis.avg_pe_ratio or 'N/A'}
Your P/E:       {result.stock_metrics.pe_ratio if result.stock_metrics else 'N/A'}
Number of Peers: {len(result.peer_analysis.peers) if result.peer_analysis.peers else 0}
"""
        else:
            report += "No peer data available\n"

        if result.macro_analysis:
            report += f"""
🌍 MACRO OUTLOOK
{'─' * 80}
Overall Sentiment: {result.macro_analysis.overall_sentiment or 'N/A'}

Tailwinds (Positive):
"""
            for tailwind in result.macro_analysis.tailwinds:
                report += f"  • {tailwind}\n"

            report += "\nHeadwinds (Risks):\n"
            for headwind in result.macro_analysis.headwinds:
                report += f"  • {headwind}\n"
        else:
            report += "\n🌍 MACRO OUTLOOK\nNo macro data available\n"

        report += f"""
⏱️  ANALYSIS METADATA
{'─' * 80}
Analysis Date:  {result.analysis_date}
Execution Time: {result.execution_time_seconds:.2f} seconds
Cache Hit:      {'Yes' if result.cache_hit else 'No'}

"""

        return report

    def close(self):
        """Close all scrapers."""
        self.yahoo_scraper.close()
        self.dataroma_scraper.close()


if __name__ == "__main__":
    print("\n✅ Testing Research Manager\n")

    manager = ResearchManager(use_cache=False)

    try:
        config = AnalysisConfig(
            ticker="AAPL",
            num_peers=4,
            include_peer_analysis=True,
            include_macro_analysis=True,
            include_colab_generation=False,  # Skip for testing
        )

        result = manager.analyze("AAPL", config=config)

        if result:
            print(manager.generate_report(result))
            print("\n✓ Analysis successful!")
        else:
            print("✗ Analysis failed")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        manager.close()
