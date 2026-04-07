"""
Local-Only Mode - Run analysis with ZERO external API calls
All data is sample/mock data - completely offline and private
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

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
            MacroImpact(
                factor="Interest Rates",
                sensitivity=0.8,
                direction="Negative",
                explanation="Higher rates reduce consumer spending"
            ),
            MacroImpact(
                factor="AI Adoption",
                sensitivity=0.9,
                direction="Positive",
                explanation="AI demand driving hardware sales"
            ),
            MacroImpact(
                factor="Tariffs",
                sensitivity=0.7,
                direction="Negative",
                explanation="China tariffs affect imports"
            ),
        ]
    )

    result.analysis_date = datetime.now()
    result.execution_time_seconds = 0.05
    result.cache_hit = False

    return result


def demo_report():
    """Generate and display sample report"""
    from src.agents.research_manager import ResearchManager

    result = get_sample_analysis("AAPL")
    manager = ResearchManager(use_cache=False)

    return manager.generate_report(result)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔒 LOCAL-ONLY MODE - ZERO EXTERNAL API CALLS")
    print("💾 Running with sample data only")
    print("🔐 100% Privacy - All data stays on your machine")
    print("="*80 + "\n")

    print(demo_report())

    print("\n" + "="*80)
    print("✅ Analysis Complete - NO DATA LEFT YOUR MACHINE")
    print("="*80 + "\n")
