"""
Colab Script Generator - Creates self-contained Google Colab notebooks.
Generates Jupyter notebooks with all analysis and visualizations.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from src.utils.logger import setup_logger
from src.models.stock_data import AnalysisResult

logger = setup_logger(__name__)


class ColabGenerator:
    """Generates Google Colab-ready Python scripts with analysis."""

    def __init__(self):
        """Initialize Colab generator."""
        self.template_dir = Path(__file__).parent.parent.parent / "notebooks"

    def generate(
        self,
        analysis_result: AnalysisResult,
        output_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Generate Colab script from analysis results.

        Args:
            analysis_result: AnalysisResult object with all data
            output_dir: Directory to save script

        Returns:
            Path to generated script or None if failed
        """
        if not output_dir:
            output_dir = str(self.template_dir / "generated_scripts")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        ticker = analysis_result.target_ticker
        filename = f"analysis_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"
        filepath = output_path / filename

        logger.info(f"Generating Colab script for {ticker}")

        try:
            notebook = self._create_notebook(analysis_result)

            with open(filepath, "w") as f:
                json.dump(notebook, f, indent=2)

            logger.info(f"✓ Colab script generated: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error generating Colab script: {e}")
            return None

    def _create_notebook(self, result: AnalysisResult) -> Dict:
        """
        Create Jupyter notebook structure.

        Args:
            result: AnalysisResult

        Returns:
            Notebook dictionary
        """
        cells = []

        # Title cell
        cells.append(self._create_markdown_cell(f"# Stock Analysis: {result.target_ticker}"))

        # Setup cell
        cells.append(self._create_code_cell(
            """
# Install required libraries
!pip install pandas plotly yfinance beautifulsoup4 requests -q

import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("✅ Libraries installed successfully")
"""
        ))

        # Stock Info
        if result.stock_info:
            info_text = f"""
## {result.stock_info.name}
- **Sector:** {result.stock_info.sector}
- **Industry:** {result.stock_info.industry}
- **Website:** {result.stock_info.website}
"""
            cells.append(self._create_markdown_cell(info_text))

        # Fetch current data
        cells.append(self._create_markdown_cell("## Current Stock Metrics"))
        cells.append(self._create_code_cell(f"""
ticker = "{result.target_ticker}"
data = yf.Ticker(ticker)
info = data.info

# Display key metrics
metrics = {{
    'Current Price': f"${info.get('currentPrice', 'N/A'):,.2f}",
    'Market Cap': f"${info.get('marketCap', 'N/A'):,.0f}",
    'P/E Ratio': info.get('trailingPE', 'N/A'),
    'Forward P/E': info.get('forwardPE', 'N/A'),
    'Dividend Yield': f"{{info.get('dividendYield', 0)*100:.2f}}%",
    '52 Week High': f"${info.get('fiftyTwoWeekHigh', 'N/A'):,.2f}",
    '52 Week Low': f"${info.get('fiftyTwoWeekLow', 'N/A'):,.2f}",
}}

for key, value in metrics.items():
    print(f"{{key}}: {{value}}")
"""))

        # Historical chart
        cells.append(self._create_markdown_cell("## 1-Year Price Chart"))
        cells.append(self._create_code_cell(f"""
# Fetch historical data
hist = yf.download("{result.target_ticker}", period="1y", progress=False)

# Create interactive chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
fig.update_layout(
    title=f"{{ticker}} - 1 Year Price History",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    hovermode='x unified',
    template='plotly_white'
)
fig.show()
"""))

        # Peer comparison (if available)
        if result.peer_analysis and result.peer_analysis.peers:
            cells.append(self._create_markdown_cell("## Peer Comparison"))

            peer_tickers = [f'"{p.ticker}"' for p in result.peer_analysis.peers[:4]]
            cells.append(self._create_code_cell(f"""
# Fetch peer data
peers = [{', '.join(peer_tickers)}]
peer_data = {{}}

for peer in peers:
    peer_info = yf.Ticker(peer).info
    peer_data[peer] = {{
        'Forward P/E': peer_info.get('forwardPE'),
        'Profit Margin': peer_info.get('profitMargins'),
        'ROE': peer_info.get('returnOnEquity'),
    }}

# Create comparison dataframe
import pandas as pd
df_peers = pd.DataFrame(peer_data).T
print("\\n📊 Peer Comparison:")
print(df_peers.round(3))

# Visualize P/E comparison
if 'Forward P/E' in df_peers.columns:
    fig = go.Figure(data=[go.Bar(
        x=df_peers.index,
        y=df_peers['Forward P/E'],
        marker_color=['blue'] + ['gray']*len(peers)
    )])
    fig.update_layout(title='Forward P/E Ratio - Peer Comparison', yaxis_title='Forward P/E')
    fig.show()
"""))

        # Macro section
        if result.macro_analysis:
            macro_text = f"""
## Macro Outlook
**Overall Sentiment:** {result.macro_analysis.overall_sentiment}

### Tailwinds (Positive Factors):
{chr(10).join([f"- {t}" for t in result.macro_analysis.tailwinds[:3]])}

### Headwinds (Risk Factors):
{chr(10).join([f"- {h}" for h in result.macro_analysis.headwinds[:3]])}
"""
            cells.append(self._create_markdown_cell(macro_text))

        # Summary
        cells.append(self._create_markdown_cell("""
## Analysis Summary
This analysis provides a snapshot of the stock's:
- **Valuation:** Compared to industry peers
- **Fundamentals:** Key financial metrics
- **Macro Context:** Sector-specific policy impacts

---
**Generated by:** Build Stock Tracker  
**Analysis Date:** """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        return {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {
                    "name": "python",
                    "version": "3.10.0",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

    @staticmethod
    def _create_markdown_cell(content: str) -> Dict:
        """Create a markdown cell."""
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": content.split("\n"),
        }

    @staticmethod
    def _create_code_cell(code: str) -> Dict:
        """Create a code cell."""
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.split("\n"),
        }


if __name__ == "__main__":
    print("\n✅ Testing Colab Generator\n")

    from src.models.stock_data import (
        StockInfo,
        StockMetrics,
        MacroAnalysisResult,
        PeerAnalysisResult,
    )

    # Create sample analysis result
    result = AnalysisResult(
        target_ticker="AAPL",
        stock_info=StockInfo(
            ticker="AAPL",
            name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
        ),
        stock_metrics=StockMetrics(ticker="AAPL", price=175.50),
        macro_analysis=MacroAnalysisResult(
            target_ticker="AAPL",
            sector="Technology",
            overall_sentiment="Positive",
            tailwinds=["AI demand strong", "Margins improving"],
            headwinds=["Macro uncertainty", "Tariff risks"],
        ),
    )

    generator = ColabGenerator()
    script_path = generator.generate(result, output_dir="/tmp/colab_test")

    if script_path:
        print(f"✓ Script generated: {script_path}")
    else:
        print("✗ Generation failed")
