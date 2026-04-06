"""
Data models for the stock tracker application.
Uses Pydantic for type validation and serialization.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
import json


class StockInfo(BaseModel):
    """Basic stock information."""

    ticker: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company name")
    sector: Optional[str] = Field(None, description="Industry sector")
    industry: Optional[str] = Field(None, description="Specific industry")
    country: Optional[str] = Field(None, description="Country of headquarters")
    website: Optional[str] = Field(None, description="Company website")
    employees: Optional[int] = Field(None, description="Number of employees")
    description: Optional[str] = Field(None, description="Company description")

    class Config:
        arbitrary_types_allowed = True


class StockMetrics(BaseModel):
    """Financial metrics and ratios for a stock."""

    ticker: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity %
    roa: Optional[float] = None  # Return on Assets %
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    total_assets: Optional[float] = None
    total_debt: Optional[float] = None
    shareholders_equity: Optional[float] = None
    earnings_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_growth: Optional[float] = None  # %

    class Config:
        arbitrary_types_allowed = True


class PeerMetrics(BaseModel):
    """Metrics for a peer stock in comparison."""

    ticker: str
    name: Optional[str] = None
    metrics: StockMetrics
    similarity_score: Optional[float] = None  # 0-1, how similar to target


class PeerAnalysisResult(BaseModel):
    """Result of peer comparison analysis."""

    target_ticker: str
    peers: List[PeerMetrics] = Field(default_factory=list)
    avg_pe_ratio: Optional[float] = None
    avg_forward_pe: Optional[float] = None
    avg_peg_ratio: Optional[float] = None
    avg_profit_margin: Optional[float] = None
    avg_debt_to_equity: Optional[float] = None
    valuation_verdict: Optional[str] = None  # "Premium", "Fair Value", "Undervalued"
    percentile_ranking: Optional[Dict[str, int]] = None  # metric -> percentile (0-100)

    class Config:
        arbitrary_types_allowed = True


class MacroImpact(BaseModel):
    """Macro policy impact on a stock/sector."""

    event_type: str  # e.g., "interest_rate_increase", "tariff", "regulation"
    description: str
    impact_direction: str = Field(..., description="Positive, Negative, or Neutral")
    impact_score: float = Field(..., ge=-10, le=10, description="Impact score from -10 to +10")
    sector_exposure: float = Field(..., ge=0, le=1, description="Sector sensitivity (0-1)")
    date_identified: datetime = Field(default_factory=datetime.now)
    source: Optional[str] = None


class MacroAnalysisResult(BaseModel):
    """Result of macro analysis."""

    target_ticker: str
    sector: Optional[str] = None
    impacts: List[MacroImpact] = Field(default_factory=list)
    overall_sentiment: Optional[str] = None  # "Positive", "Negative", "Neutral", "Mixed"
    tailwinds: List[str] = Field(default_factory=list, description="Policy tailwinds (max 3)")
    headwinds: List[str] = Field(default_factory=list, description="Policy risks (max 3)")
    macro_score: Optional[float] = Field(
        None, ge=-10, le=10, description="Overall macro outlook score"
    )


class InvestmentThesis(BaseModel):
    """Investment thesis combining all analysis."""

    target_ticker: str
    price_target: Optional[float] = None
    rating: Optional[str] = None  # "Buy", "Hold", "Sell"
    conviction_level: Optional[str] = None  # "High", "Medium", "Low"
    key_strengths: List[str] = Field(default_factory=list)
    key_weaknesses: List[str] = Field(default_factory=list)
    catalysts: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    thesis_summary: Optional[str] = None
    time_horizon: Optional[str] = None  # "6 months", "1 year", "2+ years"
    confidence_score: Optional[float] = Field(None, ge=0, le=100)


class AnalysisResult(BaseModel):
    """Complete analysis result for a stock."""

    target_ticker: str
    analysis_date: datetime = Field(default_factory=datetime.now)
    stock_info: Optional[StockInfo] = None
    stock_metrics: Optional[StockMetrics] = None
    peer_analysis: Optional[PeerAnalysisResult] = None
    macro_analysis: Optional[MacroAnalysisResult] = None
    investment_thesis: Optional[InvestmentThesis] = None
    colab_script_path: Optional[str] = None
    cache_hit: bool = Field(default=False, description="Whether this was loaded from cache")
    execution_time_seconds: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True

    def to_json(self, indent: int = 2) -> str:
        """Convert to pretty JSON."""
        return self.model_dump_json(indent=indent)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()


class SuperinvestorHolding(BaseModel):
    """Superinvestor holding data from Dataroma."""

    investor_name: str
    ticker: str
    shares: Optional[float] = None
    value: Optional[float] = None
    portfolio_percentage: Optional[float] = None
    recent_change: Optional[str] = None  # "Increased", "Decreased", "New"
    holding_date: Optional[datetime] = None


class InsiderTransaction(BaseModel):
    """Insider trading transaction data."""

    ticker: str
    insider_name: Optional[str] = None
    position: Optional[str] = None
    transaction_type: str  # "Buy", "Sell", "Exercise", "Grant"
    shares: Optional[float] = None
    price_per_share: Optional[float] = None
    transaction_date: Optional[datetime] = None
    value: Optional[float] = None


class ShareholderData(BaseModel):
    """Shareholder/institutional investor data."""

    ticker: str
    holder_name: str
    holder_type: Optional[str] = None  # "Institution", "Insider", "Fund"
    shares: Optional[float] = None
    portfolio_percentage: Optional[float] = None
    value: Optional[float] = None
    change_percentage: Optional[float] = None


class CacheEntry(BaseModel):
    """Cache entry metadata."""

    key: str
    data: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    hit_count: int = 0
    is_expired: bool = False

    def check_expiry(self) -> bool:
        """Check if cache entry has expired."""
        if datetime.now() > self.expires_at:
            self.is_expired = True
            return True
        return False


class ScraperConfig(BaseModel):
    """Configuration for scraper execution."""

    timeout: int = 10
    retry_count: int = 3
    delay_seconds: float = 2
    use_cache: bool = True
    cache_expiry_days: int = 7
    headers: Optional[Dict[str, str]] = None


class AnalysisConfig(BaseModel):
    """Configuration for analysis execution."""

    ticker: str
    num_peers: int = 4
    include_peer_analysis: bool = True
    include_macro_analysis: bool = True
    include_colab_generation: bool = True
    use_cache: bool = True
    verbose: bool = False


# Example usage and validation
if __name__ == "__main__":
    # Test StockInfo
    stock = StockInfo(
        ticker="AAPL",
        name="Apple Inc.",
        sector="Technology",
        industry="Consumer Electronics",
    )
    print("StockInfo:")
    print(stock.model_dump_json(indent=2))

    # Test StockMetrics
    metrics = StockMetrics(
        ticker="AAPL",
        price=175.50,
        market_cap=2.8e12,
        pe_ratio=28.5,
        forward_pe=26.2,
        peg_ratio=2.1,
    )
    print("\nStockMetrics:")
    print(metrics.model_dump_json(indent=2))

    # Test MacroImpact
    impact = MacroImpact(
        event_type="interest_rate_increase",
        description="Federal Reserve raises rates by 25bp",
        impact_direction="Negative",
        impact_score=-3.5,
        sector_exposure=0.95,
        source="Federal Reserve",
    )
    print("\nMacroImpact:")
    print(impact.model_dump_json(indent=2))

    # Test AnalysisResult
    result = AnalysisResult(
        target_ticker="AAPL",
        stock_info=stock,
        stock_metrics=metrics,
        execution_time_seconds=15.3,
    )
    print("\nAnalysisResult:")
    print(result.model_dump_json(indent=2))
