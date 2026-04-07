"""
Colab utility functions - Display website in Colab.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import os
from typing import Optional


def open_website_in_colab(website_path: str) -> Optional[str]:
    """
    Read HTML website file for display in Colab.

    Args:
        website_path: Path to the HTML file

    Returns:
        HTML content as string
    """
    website_path = Path(website_path)

    if not website_path.exists():
        print(f"❌ Website file not found: {website_path}")
        return None

    try:
        with open(website_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading website: {e}")
        return None


def display_website_link(website_path: str) -> None:
    """
    Print website file path and usage instructions.

    Args:
        website_path: Path to the HTML file
    """
    website_path = Path(website_path)

    if not website_path.exists():
        print(f"❌ Website file not found: {website_path}")
        return

    print(f"\n{'='*80}")
    print(f"📊 WEBSITE GENERATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"\n✓ File: {website_path.absolute()}")
    print(f"\n🎯 To view in Colab, run next cell:")
    print(f"   from src.utils.colab_utils import open_website_in_colab")
    print(f"   from IPython.display import HTML")
    print(f"   html = open_website_in_colab('{website_path}')")
    print(f"   display(HTML(html))")
    print(f"\n📥 Or download the HTML file to open locally")
    print(f"\n{'='*80}\n")

