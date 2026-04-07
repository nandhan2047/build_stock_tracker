"""
Yahoo Finance scraper for stock metrics, financials, and peer identification.
Refactored from the original colab notebook code.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import re
from typing import Optional, List, Dict, Tuple
from bs4 import BeautifulSoup
import yfinance as yf

from config import YAHOO_FINANCE_BASE_URL
from src.scrapers.base_scraper import BaseScraper, ScraperError, TickerNotFoundError
from src.utils.logger import setup_logger
from src.utils.data_cleaning import clean_numeric_value, validate_ticker, normalize_ticker
from src.models.stock_data import StockInfo, StockMetrics

logger = setup_logger(__name__)


class YahooFinanceScraper(BaseScraper):
    """Scraper for Yahoo Finance data."""

    def scrape(self, ticker: str) -> Optional[Dict]:
        """
        Scrape multiple data sources for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with all scraped data
        """
        ticker = normalize_ticker(ticker)

        if not validate_ticker(ticker):
            raise TickerNotFoundError(f"Invalid ticker format: {ticker}")

        logger.info(f"Starting scrape for {ticker}")

        try:
            # Try to fetch basic info to validate ticker exists
            info = self.get_stock_info(ticker)
            if not info:
                raise TickerNotFoundError(f"Ticker {ticker} not found on Yahoo Finance")

            metrics = self.get_stock_metrics(ticker)
            peers = self.identify_peers(ticker)

            return {
                "info": info,
                "metrics": metrics,
                "peers": peers,
                "ticker": ticker,
            }

        except Exception as e:
            logger.error(f"Error scraping {ticker}: {e}")
            raise

    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Get basic stock information using yfinance.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with stock info
        """
        try:
            ticker = normalize_ticker(ticker)
            logger.info(f"Fetching stock info for {ticker}")

            # Use yfinance for basic info
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if not info or "shortName" not in info:
                return None

            stock_info = {
                "ticker": ticker,
                "name": info.get("shortName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "country": info.get("country", ""),
                "website": info.get("website", ""),
                "employees": info.get("fullTimeEmployees"),
                "description": info.get("longBusinessSummary", ""),
            }

            return stock_info

        except Exception as e:
            logger.warning(f"Error fetching stock info for {ticker}: {e}")
            return None

    def get_stock_metrics(self, ticker: str) -> Optional[Dict]:
        """
        Get financial metrics for a stock using yfinance.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with financial metrics
        """
        try:
            ticker = normalize_ticker(ticker)
            logger.info(f"Fetching metrics for {ticker}")

            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            # Extract metrics
            metrics = {
                "ticker": ticker,
                "price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "profit_margin": info.get("profitMargins"),
                "operating_margin": info.get("operatingMargins"),
                "roe": info.get("returnOnEquity"),
                "roa": info.get("returnOnAssets"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "quick_ratio": info.get("quickRatio"),
                "free_cash_flow": info.get("freeCashflow"),
                "revenue": info.get("totalRevenue"),
                "net_income": info.get("netIncomeToCommon"),
                "total_assets": info.get("totalAssets"),
                "total_debt": info.get("totalDebt"),
                "shareholders_equity": info.get("totalStockholderEquity"),
                "earnings_per_share": info.get("trailingEps"),
                "dividend_yield": info.get("dividendYield"),
                "earnings_growth": info.get("earningsGrowth"),
            }

            return metrics

        except Exception as e:
            logger.warning(f"Error fetching metrics for {ticker}: {e}")
            return None

    def identify_peers(self, ticker: str, num_peers: int = 4) -> Optional[List[str]]:
        """
        Identify peer companies for a given ticker.

        Uses yfinance and basic sector/industry matching.

        Args:
            ticker: Stock ticker symbol
            num_peers: Number of peers to identify

        Returns:
            List of peer ticker symbols
        """
        try:
            ticker = normalize_ticker(ticker)
            logger.info(f"Identifying {num_peers} peers for {ticker}")

            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            # Get sector and industry
            sector = info.get("sector", "")
            industry = info.get("industry", "")

            if not sector:
                logger.warning(f"No sector found for {ticker}")
                return None

            # Try to use yfinance's peer list if available
            if hasattr(yf_ticker, "info") and "companyOfficers" in yf_ticker.info:
                # This is a fallback - yfinance doesn't provide peers directly
                # We'll use a hardcoded list of common peers by sector
                peers = self._get_peers_by_sector(sector, industry, ticker, num_peers)
            else:
                peers = self._get_peers_by_sector(sector, industry, ticker, num_peers)

            return peers if peers else None

        except Exception as e:
            logger.warning(f"Error identifying peers for {ticker}: {e}")
            return None

    @staticmethod
    def _get_peers_by_sector(sector: str, industry: str, target_ticker: str, num_peers: int = 4) -> Optional[List[str]]:
        """
        Get peers based on sector and industry classification.

        This is a simplified approach. In Phase 2, we can use ML embeddings.

        Args:
            sector: Stock sector
            industry: Stock industry
            target_ticker: Target ticker (to exclude from results)
            num_peers: Number of peers to return

        Returns:
            List of peer tickers
        """
        # Hardcoded peer mapping by sector/industry
        # In production, this would be more sophisticated
        peer_mapping = {
            "Technology": {
                "Software": ["MSFT", "ADBE", "CRM", "INTU", "SNPS"],
                "IT Services": ["ACCENTURE", "COGNIZANT", "IBM", "INFY"],
                "Semiconductors": ["NVDA", "AMD", "INTEL", "QCOM", "ASML"],
                "Consumer Electronics": ["AAPL", "MSFT", "SONY", "SAMSUNG"],
            },
            "Healthcare": {
                "Pharmaceuticals": ["PFE", "JNJ", "LLY", "MRK", "ABBV"],
                "Biotech": ["AMGN", "BIIB", "GILD", "CELG"],
                "Medical Devices": ["MDT", "ABT", "ISRG", "SYK"],
            },
            "Financials": {
                "Banks": ["JPM", "BAC", "WFC", "GS", "MS"],
                "Insurance": ["BRK-B", "AIG", "PRU", "MET"],
                "Financial Services": ["BLK", "SCHW", "CME", "ICE"],
            },
            "Energy": {
                "Oil & Gas": ["XOM", "CVX", "COP", "SLB", "EOG"],
                "Utilities": ["DUK", "SO", "NEE", "D", "AEP"],
            },
            "Consumer": {
                "Retail": ["AMZN", "WMT", "HD", "LOW", "TGT"],
                "Consumer Goods": ["PG", "KO", "PEP", "NSRGY", "NKE"],
            },
            "Industrials": {
                "Aerospace & Defense": ["BA", "RTX", "LMT", "GE", "HII"],
                "Machinery": ["CAT", "CMI", "DOW", "PCAR", "AME"],
            },
            "Materials": {
                "Chemicals": ["DD", "APD", "ECL", "LYB", "WRK"],
                "Metals & Mining": ["FCX", "NEM", "SCCO", "AA"],
            },
        }

        try:
            # Find peers in the mapping
            if sector in peer_mapping:
                sector_peers = peer_mapping[sector]

                if industry in sector_peers:
                    candidates = sector_peers[industry]
                else:
                    # Use all companies in sector if industry not found
                    candidates = []
                    for industry_list in sector_peers.values():
                        candidates.extend(industry_list)
            else:
                # No peers found for this sector
                return None

            # Remove target ticker and return requested number
            candidates = [t for t in candidates if t != target_ticker]
            return candidates[:num_peers] if candidates else None

        except Exception as e:
            logger.warning(f"Error in peer mapping: {e}")
            return None

    def get_historical_data(self, ticker: str, period: str = "1y") -> Optional[Dict]:
        """
        Get historical price data for correlation analysis.

        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., '1y', '6mo', '3mo')

        Returns:
            Dictionary with historical data
        """
        try:
            ticker = normalize_ticker(ticker)
            logger.info(f"Fetching historical data for {ticker}")

            yf_ticker = yf.Ticker(ticker)
            hist = yf_ticker.history(period=period)

            if hist.empty:
                return None

            return {
                "ticker": ticker,
                "data": hist.to_dict(),
                "period": period,
            }

        except Exception as e:
            logger.warning(f"Error fetching historical data for {ticker}: {e}")
            return None

    def get_multiple_tickers_data(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Get data for multiple tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary with data for each ticker
        """
        results = {}

        for ticker in tickers:
            try:
                data = self.scrape(ticker)
                results[ticker] = data
            except Exception as e:
                logger.warning(f"Failed to scrape {ticker}: {e}")
                results[ticker] = None

        return results


if __name__ == "__main__":
    # Test the scraper
    scraper = YahooFinanceScraper()

    print("\n✅ Testing Yahoo Finance Scraper\n")

    # Test single stock
    try:
        result = scraper.scrape("AAPL")
        print(f"✓ AAPL info: {result['info']}")
        print(f"✓ AAPL metrics: {result['metrics']}")
        print(f"✓ AAPL peers: {result['peers']}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test peer identification
    try:
        peers = scraper.identify_peers("TSLA")
        print(f"\n✓ TSLA peers: {peers}")
    except Exception as e:
        print(f"✗ Error: {e}")

    scraper.close()
