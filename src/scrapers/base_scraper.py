"""
Base scraper class and common scraping utilities.
Provides abstract base and helper functions for all scrapers.
"""

import requests
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import REQUEST_TIMEOUT, REQUEST_DELAY_SECONDS, REQUEST_RETRY_COUNT, USER_AGENT
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, timeout: int = REQUEST_TIMEOUT, delay: float = REQUEST_DELAY_SECONDS):
        self.timeout = timeout
        self.delay = delay
        self.session = self._create_session()
        self.last_request_time = 0

    def _create_session(self) -> requests.Session:
        """Create a requests session with proper headers."""
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        return session

    def _respectful_delay(self):
        """Add delay to respect server rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    def _fetch_page(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Fetch a page with retry logic and error handling.

        Args:
            url: URL to fetch
            params: Query parameters
            **kwargs: Additional arguments for requests.get()

        Returns:
            Response object or None if failed
        """
        for attempt in range(REQUEST_RETRY_COUNT):
            try:
                self._respectful_delay()
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    allow_redirects=True,
                    **kwargs
                )
                response.raise_for_status()
                return response

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{REQUEST_RETRY_COUNT} for {url}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}/{REQUEST_RETRY_COUNT} for {url}")
            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP error {e.response.status_code} on attempt {attempt + 1}/{REQUEST_RETRY_COUNT}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                return None

            if attempt < REQUEST_RETRY_COUNT - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        logger.error(f"Failed to fetch {url} after {REQUEST_RETRY_COUNT} attempts")
        return None

    @abstractmethod
    def scrape(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """Main scraping method. Must be implemented by subclasses."""
        pass

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ScraperError(Exception):
    """Custom exception for scraper errors."""
    pass


class TickerNotFoundError(ScraperError):
    """Exception raised when ticker is not found."""
    pass


class NoDataError(ScraperError):
    """Exception raised when no data can be scraped."""
    pass


def handle_consent_page(response: requests.Response, session: requests.Session) -> Optional[requests.Response]:
    """
    Handle Yahoo Finance consent page.

    Args:
        response: Initial response that may be a consent page
        session: Requests session with cookies

    Returns:
        Response after handling consent, or None if failed
    """
    from bs4 import BeautifulSoup

    if "consent" not in response.url.lower():
        return response

    logger.info("Detected consent page, attempting to bypass...")

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        consent_form = soup.find("form", {"action": True, "method": "post"})

        if not consent_form:
            logger.warning("Could not find consent form")
            return None

        form_data = {}
        for input_tag in consent_form.find_all("input", {"type": "hidden"}):
            name = input_tag.get("name")
            value = input_tag.get("value")
            if name and value:
                form_data[name] = value

        post_url = consent_form.get("action")
        if not post_url.startswith("http"):
            from urllib.parse import urljoin
            post_url = urljoin(response.url, post_url)

        form_data["agree"] = "agree"
        form_data[".submit"] = "agree"

        logger.info(f"Submitting consent form to {post_url}")
        consent_response = session.post(post_url, data=form_data, timeout=10)
        consent_response.raise_for_status()
        time.sleep(3)

        return consent_response

    except Exception as e:
        logger.error(f"Error handling consent page: {e}")
        return None


if __name__ == "__main__":
    logger.info("Base scraper module loaded successfully")
