"""
Data cleaning and normalization utilities.
Handles parsing, validation, and normalization of financial data.
"""

import re
from typing import Optional, Union


def normalize_ticker(ticker: str) -> str:
    """
    Normalize ticker to uppercase and strip whitespace.

    Args:
        ticker: Raw ticker string

    Returns:
        Normalized ticker (uppercase, stripped)
    """
    if not ticker:
        return ""
    return ticker.strip().upper()


def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker format.

    Args:
        ticker: Ticker to validate

    Returns:
        True if valid, False otherwise
    """
    if not ticker or len(ticker) == 0:
        return False

    # Allow letters, numbers, hyphens (e.g., BRK-B)
    if not re.match(r'^[A-Z0-9\-]{1,5}$', ticker.upper()):
        return False

    return True


def clean_numeric_value(value: Union[str, float, int, None]) -> Optional[float]:
    """
    Clean and convert numeric values from various formats.
    Handles: "1.2B", "500M", "1.5K", "50%", etc.

    Args:
        value: Value to clean (string with suffix or number)

    Returns:
        Cleaned float value or None if invalid
    """
    if value is None or value == "" or value == "N/A":
        return None

    try:
        # If already a number
        if isinstance(value, (int, float)):
            return float(value)

        # Convert to string and strip whitespace
        value_str = str(value).strip().upper()

        if not value_str or value_str == "N/A" or value_str == "-":
            return None

        # Handle percentage
        if value_str.endswith("%"):
            return float(value_str[:-1])

        # Handle currency (remove $)
        if value_str.startswith("$"):
            value_str = value_str[1:].strip()

        # Handle multipliers
        multipliers = {
            "T": 1e12,  # Trillion
            "B": 1e9,   # Billion
            "M": 1e6,   # Million
            "K": 1e3,   # Thousand
        }

        for suffix, multiplier in multipliers.items():
            if value_str.endswith(suffix):
                base_value = float(value_str[:-1])
                return base_value * multiplier

        # Try direct conversion
        return float(value_str)

    except (ValueError, TypeError, AttributeError):
        return None


def clean_percentage(value: Union[str, float, None]) -> Optional[float]:
    """
    Clean percentage values.

    Args:
        value: Percentage value (with or without % sign)

    Returns:
        Percentage as float (0-100) or None
    """
    if value is None or value == "" or value == "N/A":
        return None

    try:
        if isinstance(value, str):
            value_str = value.strip().upper()
            if value_str.endswith("%"):
                return float(value_str[:-1])
            return float(value_str)
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return None


def extract_range(value: str) -> Optional[tuple]:
    """
    Extract numeric range from string like "1.5 - 2.5".

    Args:
        value: Range string

    Returns:
        Tuple of (min, max) or None
    """
    if not value or not isinstance(value, str):
        return None

    try:
        parts = value.split("-")
        if len(parts) >= 2:
            min_val = clean_numeric_value(parts[0].strip())
            max_val = clean_numeric_value(parts[1].strip())
            if min_val is not None and max_val is not None:
                return (min_val, max_val)
    except Exception:
        pass

    return None


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """
    Sanitize string by removing extra whitespace.

    Args:
        value: String to sanitize

    Returns:
        Sanitized string or None
    """
    if not value:
        return None

    return " ".join(str(value).split())
