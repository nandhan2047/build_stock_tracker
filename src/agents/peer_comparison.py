"""
Peer Comparison Agent - Analyzes target stock vs peers.
Identifies peers and compares key financial metrics.
"""

import sys
sys.path.insert(0, '/home/claude/build_stock_tracker')

from typing import Optional, List, Dict
from src.utils.logger import setup_logger
from src.utils.calculations import PeerAnalyzer, FinancialCalculator
from src.models.stock_data import (
    PeerAnalysisResult,
    PeerMetrics,
    StockMetrics,
)
from src.scrapers.yahoo_scraper import YahooFinanceScraper

logger = setup_logger(__name__)


class PeerComparisonAgent:
    """
    Peer Comparison Agent.

    Responsibilities:
    1. Identify direct industry competitors
    2. Fetch metrics for target and peers
    3. Compare on key ratios (P/E, PEG, margins, D/E)
    4. Determine if target is "Premium", "Fair Value", or "Undervalued"
    5. Calculate percentile rankings
    """

    COMPARISON_METRICS = [
        "Forward P/E",
        "PEG Ratio",
        "Profit Margin",
        "Debt-to-Equity",
        "ROE",
    ]

    def __init__(self, yahoo_scraper: Optional[YahooFinanceScraper] = None):
        """Initialize peer comparison agent."""
        self.scraper = yahoo_scraper or YahooFinanceScraper()
        self.analyzer = PeerAnalyzer()

    def analyze(
        self,
        target_ticker: str,
        target_metrics: Optional[StockMetrics],
        peer_tickers: Optional[List[str]],
        num_peers: int = 4,
    ) -> Optional[PeerAnalysisResult]:
        """
        Perform comprehensive peer analysis.

        Args:
            target_ticker: Target stock ticker
            target_metrics: Target stock metrics
            peer_tickers: List of peer ticker candidates
            num_peers: Number of peers to include

        Returns:
            PeerAnalysisResult with comparison data
        """
        logger.info(f"🔍 Analyzing peers for {target_ticker}")

        if not target_metrics:
            logger.warning(f"No target metrics for {target_ticker}")
            return None

        # Use provided peers or identify new ones
        if not peer_tickers:
            logger.info(f"No peer tickers provided, identifying peers for {target_ticker}")
            peer_tickers = self.scraper.identify_peers(target_ticker, num_peers)

        if not peer_tickers:
            logger.warning(f"Could not identify peers for {target_ticker}")
            return None

        logger.info(f"Fetching metrics for {len(peer_tickers)} peers")

        # Fetch peer metrics
        peers_data = []
        for peer_ticker in peer_tickers[:num_peers]:
            try:
                peer_metrics = self.scraper.get_stock_metrics(peer_ticker)
                if peer_metrics:
                    peer_metrics["ticker"] = peer_ticker

                    # Calculate similarity score (simplified)
                    similarity = self._calculate_similarity_score(target_metrics, peer_metrics)

                    peer_data = PeerMetrics(
                        ticker=peer_ticker,
                        metrics=StockMetrics(**peer_metrics),
                        similarity_score=similarity,
                    )
                    peers_data.append(peer_data)
                    logger.info(f"✓ Fetched metrics for {peer_ticker}")
                else:
                    logger.warning(f"⚠️ Could not fetch metrics for {peer_ticker}")

            except Exception as e:
                logger.warning(f"Error fetching metrics for {peer_ticker}: {e}")

        if not peers_data:
            logger.warning(f"Could not fetch data for any peers")
            return None

        # Calculate comparative metrics
        result = self._calculate_comparison(target_ticker, target_metrics, peers_data)

        logger.info(f"✓ Peer analysis completed for {target_ticker}")

        return result

    def _calculate_similarity_score(
        self, target_metrics: StockMetrics, peer_metrics: Dict
    ) -> float:
        """
        Calculate how similar a peer is to the target.

        Simple scoring based on metrics proximity.

        Args:
            target_metrics: Target stock metrics
            peer_metrics: Peer stock metrics dictionary

        Returns:
            Similarity score (0-1, higher is more similar)
        """
        similarity_components = []

        # Compare P/E ratios
        if target_metrics.forward_pe and peer_metrics.get("forward_pe"):
            pe_diff = abs(target_metrics.forward_pe - peer_metrics["forward_pe"])
            pe_score = max(0, 1 - (pe_diff / max(target_metrics.forward_pe, 1)))
            similarity_components.append(pe_score * 0.3)  # Weight 30%

        # Compare profit margins
        if target_metrics.profit_margin and peer_metrics.get("profit_margin"):
            margin_diff = abs(target_metrics.profit_margin - peer_metrics["profit_margin"])
            margin_score = max(0, 1 - (margin_diff / 100))
            similarity_components.append(margin_score * 0.3)  # Weight 30%

        # Compare ROE
        if target_metrics.roe and peer_metrics.get("roe"):
            roe_diff = abs(target_metrics.roe - peer_metrics["roe"])
            roe_score = max(0, 1 - (roe_diff / 100))
            similarity_components.append(roe_score * 0.2)  # Weight 20%

        # Compare market cap (size similarity)
        if target_metrics.market_cap and peer_metrics.get("market_cap"):
            cap_ratio = peer_metrics["market_cap"] / target_metrics.market_cap
            cap_score = max(0, 1 - abs(1 - cap_ratio) / 2)  # Prefer 0.5x - 2x ratio
            similarity_components.append(cap_score * 0.2)  # Weight 20%

        avg_score = sum(similarity_components) / len(similarity_components) if similarity_components else 0.5

        return round(avg_score, 3)

    def _calculate_comparison(
        self,
        target_ticker: str,
        target_metrics: StockMetrics,
        peers_data: List[PeerMetrics],
    ) -> PeerAnalysisResult:
        """
        Calculate comparative metrics and valuation verdict.

        Args:
            target_ticker: Target ticker
            target_metrics: Target metrics
            peers_data: List of peer metrics

        Returns:
            PeerAnalysisResult
        """
        result = PeerAnalysisResult(target_ticker=target_ticker, peers=peers_data)

        # Extract peer values for each metric
        peer_forward_pes = [p.metrics.forward_pe for p in peers_data if p.metrics.forward_pe]
        peer_pegs = [p.metrics.peg_ratio for p in peers_data if p.metrics.peg_ratio]
        peer_margins = [p.metrics.profit_margin for p in peers_data if p.metrics.profit_margin]
        peer_de = [p.metrics.debt_to_equity for p in peers_data if p.metrics.debt_to_equity]
        peer_roes = [p.metrics.roe for p in peers_data if p.metrics.roe]

        # Calculate averages
        result.avg_forward_pe = self.analyzer.calculate_average_metric(peer_forward_pes)
        result.avg_peg_ratio = self.analyzer.calculate_average_metric(peer_pegs)
        result.avg_profit_margin = self.analyzer.calculate_average_metric(peer_margins)
        result.avg_debt_to_equity = self.analyzer.calculate_average_metric(peer_de)

        # Determine valuation verdict
        if result.avg_forward_pe and target_metrics.forward_pe:
            verdict = self.analyzer.calculate_valuation_verdict(
                target_metrics.forward_pe,
                result.avg_forward_pe,
                premium_threshold=0.15,
            )
            result.valuation_verdict = verdict
            logger.info(f"Valuation verdict for {target_ticker}: {verdict}")

        # Calculate percentile rankings
        result.percentile_ranking = {}

        if target_metrics.forward_pe and peer_forward_pes:
            percentile = self.analyzer.calculate_peer_percentile(
                target_metrics.forward_pe, peer_forward_pes
            )
            result.percentile_ranking["Forward P/E"] = percentile

        if target_metrics.peg_ratio and peer_pegs:
            percentile = self.analyzer.calculate_peer_percentile(
                target_metrics.peg_ratio, peer_pegs
            )
            result.percentile_ranking["PEG Ratio"] = percentile

        if target_metrics.profit_margin and peer_margins:
            percentile = self.analyzer.calculate_peer_percentile(
                target_metrics.profit_margin, peer_margins
            )
            result.percentile_ranking["Profit Margin"] = percentile

        if target_metrics.roe and peer_roes:
            percentile = self.analyzer.calculate_peer_percentile(target_metrics.roe, peer_roes)
            result.percentile_ranking["ROE"] = percentile

        return result

    def format_comparison_table(self, result: PeerAnalysisResult) -> str:
        """
        Format peer comparison as ASCII table.

        Args:
            result: PeerAnalysisResult

        Returns:
            Formatted table string
        """
        table = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PEER COMPARISON - {result.target_ticker}                        
╚════════════════════════════════════════════════════════════════════════════╝

Valuation:  {result.valuation_verdict or 'N/A'}

Metric Comparison:
{'─' * 80}
{"Ticker":<10} {"Fwd P/E":<12} {"PEG":<12} {"Margin %":<12} {"D/E":<12} {"ROE %":<12}
{'─' * 80}
"""

        for peer in result.peers:
            table += (
                f"{peer.ticker:<10} "
                f"{peer.metrics.forward_pe or 'N/A':<12.2f} "
                f"{peer.metrics.peg_ratio or 'N/A':<12.2f} "
                f"{peer.metrics.profit_margin or 'N/A':<12.2f} "
                f"{peer.metrics.debt_to_equity or 'N/A':<12.2f} "
                f"{peer.metrics.roe or 'N/A':<12.2f}\n"
            )

        if result.avg_forward_pe:
            table += f"\n{'Average':<10} {result.avg_forward_pe:<12.2f} {result.avg_peg_ratio or 'N/A':<12.2f} {result.avg_profit_margin or 'N/A':<12.2f} {result.avg_debt_to_equity or 'N/A':<12.2f}\n"

        return table


if __name__ == "__main__":
    print("\n✅ Testing Peer Comparison Agent\n")

    scraper = YahooFinanceScraper()
    agent = PeerComparisonAgent(scraper)

    try:
        # Get target metrics
        target_data = scraper.scrape("TSLA")
        if target_data:
            result = agent.analyze(
                target_ticker="TSLA",
                target_metrics=target_data.get("metrics"),
                peer_tickers=target_data.get("peers"),
                num_peers=4,
            )

            if result:
                print(agent.format_comparison_table(result))
                print("\n✓ Peer comparison successful!")
            else:
                print("✗ Peer comparison failed")
        else:
            print("✗ Could not fetch target metrics")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        scraper.close()
