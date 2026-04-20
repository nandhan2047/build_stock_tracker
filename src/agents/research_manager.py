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
from src.models.stock_data import AnalysisResult, AnalysisConfig, StockInfo, StockMetrics, InvestmentThesis
from src.scrapers.yahoo_scraper import YahooFinanceScraper
from src.scrapers.dataroma_scraper import DataromaScraper
from src.agents.peer_comparison import PeerComparisonAgent
from src.agents.macro_analyst import MacroAnalyst
from src.agents.website_generator import HTMLWebsiteGenerator
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
                try:
                    if cached_result and isinstance(cached_result, dict):
                        result.stock_info = StockInfo(**cached_result.get("stock_info")) if cached_result.get("stock_info") else None
                        result.stock_metrics = StockMetrics(**cached_result.get("stock_metrics")) if cached_result.get("stock_metrics") else None
                        result.peer_analysis = cached_result.get("peer_analysis")
                        result.macro_analysis = cached_result.get("macro_analysis")
                        result.cache_hit = True
                        result.execution_time_seconds = time.time() - start_time
                        return result
                except Exception as e:
                    logger.warning(f"⚠️ Failed to deserialize cache: {e}, refetching")
            else:
                logger.info(f"📥 Cache miss for {ticker}")

        # Initialize result
        result = AnalysisResult(target_ticker=ticker)

        # Step 1: Fetch stock info
        logger.info(f"📊 Step 1/4: Fetching stock information for {ticker}")
        try:
            yahoo_data = self.yahoo_scraper.scrape(ticker)
            if yahoo_data:
                stock_info_dict = yahoo_data.get("info")
                stock_metrics_dict = yahoo_data.get("metrics")

                if stock_info_dict:
                    result.stock_info = StockInfo(**stock_info_dict) if isinstance(stock_info_dict, dict) else stock_info_dict
                if stock_metrics_dict:
                    result.stock_metrics = StockMetrics(**stock_metrics_dict) if isinstance(stock_metrics_dict, dict) else stock_metrics_dict

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
            logger.info(f"Step 3/4: Analyzing macro impacts for {ticker}")
            try:
                macro_agent = MacroAnalyst()
                macro_analysis = macro_agent.analyze(
                    target_ticker=ticker,
                    sector=result.stock_info.sector if result.stock_info else None,
                )
                result.macro_analysis = macro_analysis
                logger.info(f"Macro analysis completed for {ticker}")
            except Exception as e:
                logger.warning(f"Macro analysis failed: {e}")

        # Step 4: Generate Investment Thesis
        logger.info(f"Step 4/5: Generating investment thesis for {ticker}")
        try:
            thesis = self._generate_investment_thesis(result)
            result.investment_thesis = thesis
            logger.info(f"Investment thesis generated for {ticker}")
        except Exception as e:
            logger.warning(f"Investment thesis generation failed: {e}")

        # Step 5: Generate Website
        logger.info(f"Step 5/5: Generating website for {ticker}")
        try:
            website_gen = HTMLWebsiteGenerator()
            website_path = website_gen.generate(analysis_result=result)
            result.website_path = website_path
            logger.info(f"✓ Website generated: {website_path}")
        except Exception as e:
            logger.warning(f"⚠️ Website generation failed: {e}")

        # Finalize
        result.analysis_date = datetime.now()
        result.execution_time_seconds = time.time() - start_time

        # Cache result
        if self.use_cache and self.cache_manager:
            self.cache_manager.set(f"analysis_{ticker}", result.to_dict())
            logger.info(f"💾 Analysis cached for {ticker}")

        logger.info(f"Analysis complete for {ticker} in {result.execution_time_seconds:.2f}s")

        return result

    def _generate_investment_thesis(self, result: AnalysisResult) -> InvestmentThesis:
        """
        Generate investment thesis from analysis results.

        Args:
            result: AnalysisResult object with peer and macro analysis

        Returns:
            InvestmentThesis object
        """
        thesis = InvestmentThesis(target_ticker=result.target_ticker)

        # Rating based on valuation verdict
        if result.peer_analysis and result.peer_analysis.valuation_verdict:
            verdict = result.peer_analysis.valuation_verdict.lower()
            if "undervalued" in verdict or "bargain" in verdict:
                thesis.rating = "Buy"
            elif "overvalued" in verdict or "premium" in verdict:
                thesis.rating = "Sell"
            else:
                thesis.rating = "Hold"

        # Conviction level based on macro score
        if result.macro_analysis:
            macro_score = result.macro_analysis.macro_score or 0
            if abs(macro_score) >= 7:
                thesis.conviction_level = "High"
            elif abs(macro_score) >= 4:
                thesis.conviction_level = "Medium"
            else:
                thesis.conviction_level = "Low"
        else:
            thesis.conviction_level = "Low"

        # Key strengths and weaknesses from peer analysis
        if result.peer_analysis:
            if result.peer_analysis.valuation_verdict and "undervalued" in result.peer_analysis.valuation_verdict.lower():
                thesis.key_strengths.append("Trading below peer valuation")
            if result.stock_metrics and result.stock_metrics.roe and result.stock_metrics.roe > 15:
                thesis.key_strengths.append(f"Strong ROE ({result.stock_metrics.roe:.1f}%)")
            if result.stock_metrics and result.stock_metrics.debt_to_equity and result.stock_metrics.debt_to_equity > 2:
                thesis.key_weaknesses.append(f"High debt levels (D/E: {result.stock_metrics.debt_to_equity:.1f})")

        # Catalysts and risks from macro analysis
        if result.macro_analysis:
            thesis.catalysts = [impact.description for impact in result.macro_analysis.impacts if impact.impact_direction == "Positive"][:3]
            thesis.risks = [impact.description for impact in result.macro_analysis.impacts if impact.impact_direction == "Negative"][:3]

        # Price target (simplified: based on peer average P/E)
        if result.peer_analysis and result.peer_analysis.avg_forward_pe and result.stock_metrics and result.stock_metrics.net_income:
            estimated_eps = result.stock_metrics.earnings_per_share or (result.stock_metrics.net_income / 1_000_000)
            if estimated_eps and estimated_eps > 0:
                thesis.price_target = estimated_eps * result.peer_analysis.avg_forward_pe

        # Summary thesis
        if thesis.rating and result.stock_info:
            thesis.thesis_summary = f"{result.stock_info.name} ({result.target_ticker}) is rated {thesis.rating} with {thesis.conviction_level} conviction based on valuation and macro outlook."

        # Set other fields
        thesis.time_horizon = "6-12 months"
        thesis.confidence_score = 65 if thesis.rating else 40

        return thesis

    def generate_report(self, result: AnalysisResult) -> str:
        """
        Generate executive summary report.

        Args:
            result: AnalysisResult object

        Returns:
            Formatted report string
        """
        # Handle both dict and Pydantic model formats
        if isinstance(result.stock_info, dict):
            stock_name = result.stock_info.get("name", "N/A")
            stock_sector = result.stock_info.get("sector", "N/A")
            stock_industry = result.stock_info.get("industry", "N/A")
        else:
            stock_name = result.stock_info.name if result.stock_info else 'N/A'
            stock_sector = result.stock_info.sector if result.stock_info else 'N/A'
            stock_industry = result.stock_info.industry if result.stock_info else 'N/A'

        if isinstance(result.stock_metrics, dict):
            current_price = result.stock_metrics.get("price", "N/A")
            market_cap = result.stock_metrics.get("market_cap", "N/A")
            pe_ratio = result.stock_metrics.get("pe_ratio", "N/A")
            forward_pe = result.stock_metrics.get("forward_pe", "N/A")
            peg_ratio = result.stock_metrics.get("peg_ratio", "N/A")
        else:
            current_price = result.stock_metrics.price if result.stock_metrics else 'N/A'
            market_cap = result.stock_metrics.market_cap if result.stock_metrics else 'N/A'
            pe_ratio = result.stock_metrics.pe_ratio if result.stock_metrics else 'N/A'
            forward_pe = result.stock_metrics.forward_pe if result.stock_metrics else 'N/A'
            peg_ratio = result.stock_metrics.peg_ratio if result.stock_metrics else 'N/A'

        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EXECUTIVE RESEARCH DOSSIER                                ║
║                         Ticker: {result.target_ticker}
╚══════════════════════════════════════════════════════════════════════════════╝

📌 COMPANY PROFILE
{'─' * 80}
Name:           {stock_name}
Sector:         {stock_sector}
Industry:       {stock_industry}

💰 KEY METRICS
{'─' * 80}
Current Price:  ${current_price}
Market Cap:     {f"${market_cap:,.0f}" if isinstance(market_cap, (int, float)) else market_cap}
P/E Ratio:      {pe_ratio}
Forward P/E:    {forward_pe}
PEG Ratio:      {peg_ratio}

📊 PEER COMPARISON
{'─' * 80}
"""

        if result.peer_analysis:
            report += f"""
Valuation:      {result.peer_analysis.valuation_verdict or 'N/A'}
Avg P/E (Peers): {result.peer_analysis.avg_pe_ratio or 'N/A'}
Your P/E:       {pe_ratio}
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
