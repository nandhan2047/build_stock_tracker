"""
Financial calculations module.
Provides utility classes for financial ratio calculations and peer analysis.
"""

from typing import List, Optional
import statistics


class FinancialCalculator:
    """Performs financial ratio calculations."""

    @staticmethod
    def calculate_pe_ratio(price: float, earnings_per_share: float) -> Optional[float]:
        """Calculate P/E ratio."""
        if earnings_per_share is None or earnings_per_share == 0:
            return None
        return price / earnings_per_share

    @staticmethod
    def calculate_forward_pe(price: float, forward_eps: float) -> Optional[float]:
        """Calculate forward P/E ratio."""
        if forward_eps is None or forward_eps == 0:
            return None
        return price / forward_eps

    @staticmethod
    def calculate_peg_ratio(pe_ratio: float, growth_rate: float) -> Optional[float]:
        """
        Calculate PEG ratio.
        PEG = P/E Ratio / Expected Annual Earnings Growth Rate (%)
        """
        if pe_ratio is None or growth_rate is None or growth_rate == 0:
            return None
        return pe_ratio / growth_rate

    @staticmethod
    def calculate_debt_to_equity(total_debt: float, equity: float) -> Optional[float]:
        """Calculate debt-to-equity ratio."""
        if equity is None or equity == 0:
            return None
        return total_debt / equity

    @staticmethod
    def calculate_current_ratio(current_assets: float, current_liabilities: float) -> Optional[float]:
        """Calculate current ratio (liquidity)."""
        if current_liabilities is None or current_liabilities == 0:
            return None
        return current_assets / current_liabilities

    @staticmethod
    def calculate_quick_ratio(
        current_assets: float,
        inventory: float,
        current_liabilities: float
    ) -> Optional[float]:
        """Calculate quick ratio (acid-test ratio)."""
        if current_liabilities is None or current_liabilities == 0:
            return None
        quick_assets = current_assets - (inventory or 0)
        return quick_assets / current_liabilities

    @staticmethod
    def calculate_roe(net_income: float, shareholders_equity: float) -> Optional[float]:
        """Calculate Return on Equity (ROE)."""
        if shareholders_equity is None or shareholders_equity == 0:
            return None
        return (net_income / shareholders_equity) * 100

    @staticmethod
    def calculate_roa(net_income: float, total_assets: float) -> Optional[float]:
        """Calculate Return on Assets (ROA)."""
        if total_assets is None or total_assets == 0:
            return None
        return (net_income / total_assets) * 100

    @staticmethod
    def calculate_profit_margin(net_income: float, revenue: float) -> Optional[float]:
        """Calculate profit margin."""
        if revenue is None or revenue == 0:
            return None
        return (net_income / revenue) * 100

    @staticmethod
    def calculate_operating_margin(operating_income: float, revenue: float) -> Optional[float]:
        """Calculate operating margin."""
        if revenue is None or revenue == 0:
            return None
        return (operating_income / revenue) * 100

    @staticmethod
    def calculate_free_cash_flow(operating_cash_flow: float, capex: float) -> Optional[float]:
        """Calculate free cash flow."""
        if operating_cash_flow is None:
            return None
        capex = capex or 0
        return operating_cash_flow - capex

    @staticmethod
    def calculate_fcf_yield(free_cash_flow: float, market_cap: float) -> Optional[float]:
        """Calculate free cash flow yield."""
        if market_cap is None or market_cap == 0:
            return None
        return (free_cash_flow / market_cap) * 100


class PeerAnalyzer:
    """Analyzes peer comparison metrics."""

    @staticmethod
    def calculate_average_metric(values: List[Optional[float]]) -> Optional[float]:
        """
        Calculate average of a list of metric values, ignoring None values.

        Args:
            values: List of metric values

        Returns:
            Average value or None if no valid values
        """
        if not values:
            return None

        # Filter out None and invalid values
        valid_values = [v for v in values if v is not None and isinstance(v, (int, float))]

        if not valid_values:
            return None

        return statistics.mean(valid_values)

    @staticmethod
    def calculate_peer_percentile(target_value: float, peer_values: List[float]) -> int:
        """
        Calculate what percentile the target value falls in among peers.

        Args:
            target_value: The target company's metric value
            peer_values: List of peer metric values

        Returns:
            Percentile rank (0-100)
        """
        if not peer_values or target_value is None:
            return 50  # Default to 50th percentile

        # Filter valid values
        valid_peers = [v for v in peer_values if v is not None and isinstance(v, (int, float))]

        if not valid_peers:
            return 50

        # Count how many peers have lower value
        lower_count = sum(1 for v in valid_peers if v < target_value)

        # Calculate percentile
        percentile = (lower_count / len(valid_peers)) * 100

        return int(percentile)

    @staticmethod
    def calculate_valuation_verdict(
        target_pe: float,
        avg_peer_pe: float,
        premium_threshold: float = 0.15
    ) -> str:
        """
        Determine if stock is overvalued, fairly valued, or undervalued vs peers.

        Args:
            target_pe: Target company's P/E ratio
            avg_peer_pe: Average peer P/E ratio
            premium_threshold: Threshold for premium classification (default 15%)

        Returns:
            Verdict string: "Premium", "Fair Value", or "Undervalued"
        """
        if target_pe is None or avg_peer_pe is None or avg_peer_pe == 0:
            return "N/A"

        # Calculate ratio difference
        ratio_diff = (target_pe - avg_peer_pe) / avg_peer_pe

        if ratio_diff > premium_threshold:
            return "Premium"
        elif ratio_diff < -premium_threshold:
            return "Undervalued"
        else:
            return "Fair Value"

    @staticmethod
    def calculate_similarity_score(
        target_metrics: dict,
        peer_metrics: dict,
        key_metrics: Optional[List[str]] = None
    ) -> float:
        """
        Calculate how similar a peer is to the target based on key metrics.

        Args:
            target_metrics: Target company's metrics dict
            peer_metrics: Peer company's metrics dict
            key_metrics: List of metric keys to compare

        Returns:
            Similarity score (0-1, higher is more similar)
        """
        if key_metrics is None:
            key_metrics = ["forward_pe", "profit_margin", "roe", "debt_to_equity"]

        similarity_scores = []

        for metric in key_metrics:
            target_val = target_metrics.get(metric)
            peer_val = peer_metrics.get(metric)

            if target_val is None or peer_val is None:
                continue

            # Calculate difference ratio
            if target_val == 0:
                diff_ratio = abs(peer_val) if peer_val != 0 else 1
            else:
                diff_ratio = abs(peer_val - target_val) / abs(target_val)

            # Convert to similarity (lower diff = higher similarity)
            similarity = max(0, 1 - diff_ratio)
            similarity_scores.append(similarity)

        if not similarity_scores:
            return 0.5  # Default neutral score

        return round(statistics.mean(similarity_scores), 3)

    @staticmethod
    def identify_peer_characteristics(peer_metrics: dict) -> dict:
        """
        Identify key characteristics of a peer company.

        Args:
            peer_metrics: Peer company's metrics dict

        Returns:
            Dictionary with characteristics
        """
        characteristics = {
            "profitable": False,
            "efficient": False,
            "leveraged": False,
            "liquid": False,
        }

        # Check profitability
        if peer_metrics.get("profit_margin") and peer_metrics["profit_margin"] > 5:
            characteristics["profitable"] = True

        # Check efficiency (ROE)
        if peer_metrics.get("roe") and peer_metrics["roe"] > 15:
            characteristics["efficient"] = True

        # Check leverage
        if peer_metrics.get("debt_to_equity") and peer_metrics["debt_to_equity"] > 1:
            characteristics["leveraged"] = True

        # Check liquidity
        if peer_metrics.get("current_ratio") and peer_metrics["current_ratio"] > 1.5:
            characteristics["liquid"] = True

        return characteristics


if __name__ == "__main__":
    # Test FinancialCalculator
    print("Testing FinancialCalculator...")
    calc = FinancialCalculator()

    pe = calc.calculate_pe_ratio(100, 5)
    print(f"P/E Ratio: {pe}")  # Should be 20

    peg = calc.calculate_peg_ratio(20, 10)
    print(f"PEG Ratio: {peg}")  # Should be 2.0

    roe = calc.calculate_roe(1000000, 5000000)
    print(f"ROE: {roe:.2f}%")  # Should be 20%

    # Test PeerAnalyzer
    print("\nTesting PeerAnalyzer...")
    analyzer = PeerAnalyzer()

    avg = analyzer.calculate_average_metric([20, 25, 30, 22])
    print(f"Average Metric: {avg:.2f}")  # Should be ~24.25

    percentile = analyzer.calculate_peer_percentile(25, [20, 25, 30, 22])
    print(f"Percentile: {percentile}%")  # Should be 50

    verdict = analyzer.calculate_valuation_verdict(26, 25, 0.15)
    print(f"Valuation Verdict: {verdict}")  # Should be "Fair Value"

    similarity = analyzer.calculate_similarity_score(
        {"forward_pe": 20, "roe": 15},
        {"forward_pe": 22, "roe": 14}
    )
    print(f"Similarity Score: {similarity}")

    print("\n✅ All tests passed!")
