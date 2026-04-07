"""
Macro Analyst Agent - Researches policy and macro impacts on stocks.
Analyzes global macro factors affecting the target sector.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from typing import Optional, List, Dict
from datetime import datetime
from config import MACRO_SECTOR_SENSITIVITY

from src.utils.logger import setup_logger
from src.models.stock_data import MacroAnalysisResult, MacroImpact

logger = setup_logger(__name__)


class MacroAnalyst:
    """
    Macro Analyst Agent.

    Responsibilities:
    1. Research sector-specific macro impacts
    2. Identify current policy risks and tailwinds
    3. Analyze interest rate sensitivity
    4. Research tariffs and trade impacts
    5. Assess regulatory impacts
    6. Produce macro sentiment analysis
    """

    def __init__(self):
        """Initialize macro analyst."""
        self.impacts_database = self._load_impacts_database()

    def analyze(self, target_ticker: str, sector: Optional[str]) -> Optional[MacroAnalysisResult]:
        """
        Analyze macro impacts for a stock.

        Args:
            target_ticker: Stock ticker
            sector: Stock sector

        Returns:
            MacroAnalysisResult with policy impacts
        """
        logger.info(f"🌍 Analyzing macro impacts for {target_ticker} ({sector})")

        if not sector:
            logger.warning(f"No sector provided for {target_ticker}")
            # Try to infer sector from ticker or provide generic analysis
            sector = "Technology"  # Default for demo

        result = MacroAnalysisResult(target_ticker=target_ticker, sector=sector)

        # Identify impacts relevant to this sector
        impacts = self._identify_sector_impacts(sector)
        result.impacts = impacts

        # Determine tailwinds and headwinds
        tailwinds, headwinds = self._categorize_impacts(impacts)
        result.tailwinds = tailwinds[:3]  # Limit to 3
        result.headwinds = headwinds[:3]

        # Calculate overall sentiment
        result.overall_sentiment = self._calculate_sentiment(impacts)

        # Calculate macro score
        result.macro_score = self._calculate_macro_score(impacts)

        logger.info(f"✓ Macro analysis completed: {result.overall_sentiment}")

        return result

    def _load_impacts_database(self) -> Dict[str, List[MacroImpact]]:
        """
        Load or create a database of current macro impacts.

        In Phase 2, this will be replaced with real-time scraping.

        Returns:
            Dictionary of impacts by category
        """
        # Phase 1: Hardcoded impacts (updated manually)
        # Phase 2: Will integrate FRED API, Mirofish, Trading Economics

        impacts_db = {
            "interest_rates": [
                MacroImpact(
                    event_type="interest_rate_environment",
                    description="Fed Funds Rate remains elevated at 5.25-5.50% (as of April 2024)",
                    impact_direction="Negative",
                    impact_score=-3.0,
                    sector_exposure=0.85,
                    source="Federal Reserve",
                ),
                MacroImpact(
                    event_type="rate_outlook",
                    description="Market expects potential rate cuts in late 2024 if inflation continues moderating",
                    impact_direction="Positive",
                    impact_score=2.5,
                    sector_exposure=0.85,
                    source="CME FedWatch",
                ),
            ],
            "inflation": [
                MacroImpact(
                    event_type="inflation_trend",
                    description="PCE inflation at 2.7% YoY, approaching Fed 2% target",
                    impact_direction="Positive",
                    impact_score=2.0,
                    sector_exposure=0.70,
                    source="Bureau of Labor Statistics",
                ),
            ],
            "trade": [
                MacroImpact(
                    event_type="trade_tariffs",
                    description="Potential 10-20% tariffs on Chinese imports proposed",
                    impact_direction="Negative",
                    impact_score=-4.0,
                    sector_exposure=0.90,
                    source="Trade News",
                ),
                MacroImpact(
                    event_type="trade_war_risk",
                    description="US-China trade tensions elevated; tech sector particularly exposed",
                    impact_direction="Negative",
                    impact_score=-3.5,
                    sector_exposure=0.95,
                    source="Trade Analysis",
                ),
            ],
            "technology": [
                MacroImpact(
                    event_type="ai_regulation",
                    description="EU AI Act in effect; US considering AI regulation framework",
                    impact_direction="Negative",
                    impact_score=-2.5,
                    sector_exposure=1.0,
                    source="Regulatory News",
                ),
                MacroImpact(
                    event_type="semiconductor_demand",
                    description="Strong AI demand driving semiconductor demand; CHIPS Act support",
                    impact_direction="Positive",
                    impact_score=3.5,
                    sector_exposure=0.95,
                    source="Industry Analysis",
                ),
            ],
            "healthcare": [
                MacroImpact(
                    event_type="drug_pricing",
                    description="HHS proposing new drug price negotiation authority",
                    impact_direction="Negative",
                    impact_score=-2.0,
                    sector_exposure=0.85,
                    source="CMS Announcements",
                ),
            ],
            "energy": [
                MacroImpact(
                    event_type="energy_transition",
                    description="IRA incentives driving renewable energy investment",
                    impact_direction="Positive",
                    impact_score=3.0,
                    sector_exposure=0.90,
                    source="Energy Policy",
                ),
                MacroImpact(
                    event_type="oil_prices",
                    description="Oil prices stable around $80-85/barrel",
                    impact_direction="Neutral",
                    impact_score=0.0,
                    sector_exposure=1.0,
                    source="Commodity Markets",
                ),
            ],
        }

        return impacts_db

    def _identify_sector_impacts(self, sector: str) -> List[MacroImpact]:
        """
        Identify relevant impacts for a specific sector.

        Args:
            sector: Stock sector

        Returns:
            List of relevant MacroImpact objects
        """
        relevant_impacts = []

        # Get sector sensitivity weights
        sector_sensitivity = MACRO_SECTOR_SENSITIVITY.get(sector, {})

        if not sector_sensitivity:
            logger.warning(f"No sensitivity mapping for sector: {sector}")
            # Return generic impacts
            for impacts_list in self.impacts_database.values():
                relevant_impacts.extend(impacts_list)
            return relevant_impacts

        # Add relevant impacts based on sector
        impacts_to_include = []

        # Always include interest rate and inflation
        impacts_to_include.extend(self.impacts_database.get("interest_rates", []))
        impacts_to_include.extend(self.impacts_database.get("inflation", []))

        # Add sector-specific impacts
        if sector_sensitivity.get("tariffs", 0) > 0.5:
            impacts_to_include.extend(self.impacts_database.get("trade", []))

        if sector_sensitivity.get("regulations", 0) > 0.5:
            if sector == "Technology":
                impacts_to_include.extend(self.impacts_database.get("technology", []))
            elif sector == "Healthcare":
                impacts_to_include.extend(self.impacts_database.get("healthcare", []))

        if sector == "Energy":
            impacts_to_include.extend(self.impacts_database.get("energy", []))

        # Adjust impact scores based on sector sensitivity
        for impact in impacts_to_include:
            # Get sensitivity for this impact type
            sensitivity_key = impact.event_type.split("_")[0]  # e.g., "interest" from "interest_rate_environment"
            sensitivity = sector_sensitivity.get(sensitivity_key, 0.5)

            # Scale impact score by sensitivity
            impact.impact_score = impact.impact_score * sensitivity
            impact.sector_exposure = sensitivity

        relevant_impacts.extend(impacts_to_include)

        return relevant_impacts

    def _categorize_impacts(self, impacts: List[MacroImpact]) -> tuple:
        """
        Categorize impacts into tailwinds and headwinds.

        Args:
            impacts: List of macro impacts

        Returns:
            Tuple of (tailwinds_list, headwinds_list)
        """
        tailwinds = []
        headwinds = []

        for impact in impacts:
            if impact.impact_direction == "Positive":
                tailwinds.append(impact.description)
            elif impact.impact_direction == "Negative":
                headwinds.append(impact.description)

        # Sort by impact score magnitude
        tailwinds.sort()
        headwinds.sort()

        return tailwinds, headwinds

    def _calculate_sentiment(self, impacts: List[MacroImpact]) -> str:
        """
        Calculate overall macro sentiment.

        Args:
            impacts: List of impacts

        Returns:
            Sentiment string ("Positive", "Negative", "Neutral", "Mixed")
        """
        if not impacts:
            return "Neutral"

        avg_impact = sum(i.impact_score for i in impacts) / len(impacts)

        if avg_impact > 1.0:
            return "Positive"
        elif avg_impact < -1.0:
            return "Negative"
        elif abs(avg_impact) < 0.5:
            return "Neutral"
        else:
            return "Mixed"

    def _calculate_macro_score(self, impacts: List[MacroImpact]) -> float:
        """
        Calculate overall macro score (-10 to +10).

        Args:
            impacts: List of impacts

        Returns:
            Macro score
        """
        if not impacts:
            return 0.0

        total_score = sum(i.impact_score * (i.sector_exposure or 0.5) for i in impacts)
        avg_score = total_score / len(impacts)

        # Clamp to -10 to +10
        return max(-10, min(10, avg_score))

    def format_macro_report(self, result: MacroAnalysisResult) -> str:
        """
        Format macro analysis as readable report.

        Args:
            result: MacroAnalysisResult

        Returns:
            Formatted report string
        """
        report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    MACRO IMPACT ANALYSIS - {result.target_ticker}                    
╚════════════════════════════════════════════════════════════════════════════╝

Sector:             {result.sector}
Overall Sentiment:  {result.overall_sentiment}
Macro Score:        {result.macro_score:+.1f}/10

📈 TAILWINDS (Policy Tailwinds)
{'─' * 80}
"""
        for i, tailwind in enumerate(result.tailwinds, 1):
            report += f"{i}. {tailwind}\n"

        report += f"""
📉 HEADWINDS (Policy Risks)
{'─' * 80}
"""
        for i, headwind in enumerate(result.headwinds, 1):
            report += f"{i}. {headwind}\n"

        report += f"""
⚠️  KEY IMPACTS
{'─' * 80}
"""
        for impact in result.impacts[:5]:  # Show top 5
            direction_emoji = "📈" if impact.impact_direction == "Positive" else "📉"
            report += f"{direction_emoji} {impact.description}\n"
            report += f"   Impact: {impact.impact_score:+.1f} | Exposure: {impact.sector_exposure:.0%}\n\n"

        return report


if __name__ == "__main__":
    print("\n✅ Testing Macro Analyst\n")

    analyst = MacroAnalyst()

    try:
        # Test analysis for different sectors
        for sector in ["Technology", "Energy", "Healthcare", "Financials"]:
            result = analyst.analyze("TEST", sector=sector)
            if result:
                print(analyst.format_macro_report(result))
                print("\n" + "=" * 80 + "\n")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
