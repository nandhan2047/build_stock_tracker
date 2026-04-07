"""
Dataroma scraper for superinvestor holdings and insider trading data.
Refactored from the original colab notebook code.
"""

import sys
sys.path.insert(0, '/home/claude/build_stock_tracker')

from typing import Optional, Tuple, Dict, List
from bs4 import BeautifulSoup

from config import DATAROMA_BASE_URL
from src.scrapers.base_scraper import BaseScraper, NoDataError
from src.utils.logger import setup_logger
from src.utils.data_cleaning import clean_numeric_value, normalize_ticker

logger = setup_logger(__name__)


class DataromaScraper(BaseScraper):
    """Scraper for Dataroma superinvestor holdings data."""

    def scrape(self, ticker: str) -> Optional[Dict]:
        """
        Scrape superinvestor holdings and insider trading data.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with superinvestor and insider data
        """
        ticker = normalize_ticker(ticker)
        logger.info(f"Scraping Dataroma for {ticker}")

        try:
            super_investor_data, insider_trades_data = self._scrape_stock_page(ticker)

            return {
                "ticker": ticker,
                "superinvestor_holdings": super_investor_data,
                "insider_trades": insider_trades_data,
            }

        except Exception as e:
            logger.error(f"Error scraping Dataroma for {ticker}: {e}")
            return None

    def _scrape_stock_page(self, ticker: str) -> Tuple[Optional[List[Dict]], Optional[List[Dict]]]:
        """
        Scrape Dataroma stock page for both superinvestor holdings and insider trades.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Tuple of (superinvestor_data, insider_trades_data)
        """
        url = f"{DATAROMA_BASE_URL}?sym={ticker}"

        response = self._fetch_page(url)
        if not response:
            logger.warning(f"Failed to fetch Dataroma page for {ticker}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract superinvestor holdings (table id="grid")
        super_investor_data = self._extract_superinvestor_table(soup, ticker)

        # Extract insider trades (table id="ins_sum")
        insider_trades_data = self._extract_insider_trades_table(soup, ticker)

        return super_investor_data, insider_trades_data

    @staticmethod
    def _extract_superinvestor_table(soup: BeautifulSoup, ticker: str) -> Optional[List[Dict]]:
        """
        Extract superinvestor holdings from table with id='grid'.

        Args:
            soup: BeautifulSoup object of page
            ticker: Stock ticker

        Returns:
            List of dictionaries with superinvestor data
        """
        try:
            table = soup.find("table", id="grid")
            if not table:
                logger.debug(f"No superinvestor table found for {ticker}")
                return None

            logger.info(f"Found superinvestor table for {ticker}")

            # Extract headers
            header_row = table.find("thead").find("tr") if table.find("thead") else None
            if not header_row:
                return None

            columns = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]

            # Remove empty first column if present
            if columns and columns[0] == "":
                columns = columns[1:]

            # Extract data rows
            data = []
            tbody = table.find("tbody")
            if not tbody:
                return None

            for row in tbody.find_all("tr"):
                cells = [td.get_text(strip=True) for td in row.find_all("td")]

                # Remove sorting icon if present
                if cells and cells[0] == "≡":
                    cells = cells[1:]

                # Match column count
                if cells and len(cells) == len(columns):
                    row_dict = dict(zip(columns, cells))

                    # Clean numeric values
                    for key in ["% of portfolio", "Shares", "Value"]:
                        if key in row_dict:
                            row_dict[key] = clean_numeric_value(row_dict[key])

                    row_dict["Ticker"] = ticker
                    data.append(row_dict)

            return data if data else None

        except Exception as e:
            logger.warning(f"Error extracting superinvestor table for {ticker}: {e}")
            return None

    @staticmethod
    def _extract_insider_trades_table(soup: BeautifulSoup, ticker: str) -> Optional[List[Dict]]:
        """
        Extract insider trading summary from table with id='ins_sum'.

        Args:
            soup: BeautifulSoup object of page
            ticker: Stock ticker

        Returns:
            List of dictionaries with insider trade data
        """
        try:
            table = soup.find("table", id="ins_sum")
            if not table:
                logger.debug(f"No insider trades table found for {ticker}")
                return None

            logger.info(f"Found insider trades table for {ticker}")

            # Find the second thead (first is label, second is headers)
            theads = table.find_all("thead")
            if len(theads) < 2:
                return None

            header_row = theads[1].find("tr")
            if not header_row:
                return None

            columns = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]

            # Extract data rows
            data = []
            tbody = table.find("tbody")
            if not tbody:
                return None

            for row in tbody.find_all("tr"):
                cells = [td.get_text(strip=True) for td in row.find_all("td")]

                if cells and len(cells) == len(columns):
                    row_dict = dict(zip(columns, cells))

                    # Rename first column to 'Transaction Type' if needed
                    if "" in row_dict:
                        row_dict["Transaction Type"] = row_dict.pop("")

                    # Clean numeric values
                    if "Total" in row_dict:
                        row_dict["Total"] = clean_numeric_value(row_dict["Total"])

                    row_dict["Ticker"] = ticker
                    data.append(row_dict)

            return data if data else None

        except Exception as e:
            logger.warning(f"Error extracting insider trades table for {ticker}: {e}")
            return None

    def get_superinvestor_sentiment(self, ticker: str) -> Optional[Dict]:
        """
        Get sentiment analysis of superinvestor moves.

        Args:
            ticker: Stock ticker

        Returns:
            Dictionary with sentiment metrics
        """
        try:
            _, insider_data = self._scrape_stock_page(ticker)

            if not insider_data:
                return None

            # Analyze insider trading data
            total_buys = sum(1 for item in insider_data if "Buy" in item.get("Transaction Type", ""))
            total_sells = sum(1 for item in insider_data if "Sell" in item.get("Transaction Type", ""))

            sentiment = "Neutral"
            if total_buys > total_sells:
                sentiment = "Positive (More Buys)"
            elif total_sells > total_buys:
                sentiment = "Negative (More Sells)"

            return {
                "ticker": ticker,
                "total_buys": total_buys,
                "total_sells": total_sells,
                "sentiment": sentiment,
                "buy_sell_ratio": total_buys / total_sells if total_sells > 0 else float("inf"),
            }

        except Exception as e:
            logger.warning(f"Error analyzing superinvestor sentiment for {ticker}: {e}")
            return None

    def get_top_holders(self, ticker: str, limit: int = 10) -> Optional[List[Dict]]:
        """
        Get top superinvestor holders sorted by value.

        Args:
            ticker: Stock ticker
            limit: Maximum number of holders to return

        Returns:
            List of top holders
        """
        try:
            super_data, _ = self._scrape_stock_page(ticker)

            if not super_data:
                return None

            # Sort by Value (descending)
            sorted_data = sorted(
                super_data,
                key=lambda x: x.get("Value") or 0,
                reverse=True,
            )

            return sorted_data[:limit]

        except Exception as e:
            logger.warning(f"Error getting top holders for {ticker}: {e}")
            return None


if __name__ == "__main__":
    # Test the scraper
    scraper = DataromaScraper()

    print("\n✅ Testing Dataroma Scraper\n")

    # Test single stock
    try:
        result = scraper.scrape("AAPL")
        if result:
            print(f"✓ AAPL superinvestor holdings: {len(result['superinvestor_holdings'] or [])} entries")
            print(f"✓ AAPL insider trades: {len(result['insider_trades'] or [])} entries")

            # Test sentiment
            sentiment = scraper.get_superinvestor_sentiment("AAPL")
            if sentiment:
                print(f"✓ AAPL sentiment: {sentiment['sentiment']}")

            # Test top holders
            top_holders = scraper.get_top_holders("AAPL", limit=5)
            if top_holders:
                print(f"✓ AAPL top 5 holders: {[h.get('Investor') for h in top_holders]}")
        else:
            print("✗ Failed to scrape AAPL")
    except Exception as e:
        print(f"✗ Error: {e}")

    scraper.close()
