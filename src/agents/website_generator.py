"""
HTML Website Generator - Creates interactive stock analysis website.
Generates standalone HTML with Plotly charts, works in Colab.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import json
from datetime import datetime
from typing import Optional
import base64

from src.utils.logger import setup_logger
from src.models.stock_data import AnalysisResult

logger = setup_logger(__name__)


class HTMLWebsiteGenerator:
    """Generates interactive HTML website from analysis results."""

    def __init__(self):
        """Initialize website generator."""
        self.output_dir = Path(__file__).parent.parent.parent / "websites"

    def generate(self, analysis_result: AnalysisResult, output_dir: Optional[str] = None) -> Optional[str]:
        """
        Generate HTML website from analysis results.

        Args:
            analysis_result: AnalysisResult object
            output_dir: Directory to save website

        Returns:
            Path to generated HTML file
        """
        if not output_dir:
            output_dir = str(self.output_dir)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        ticker = analysis_result.target_ticker
        filename = f"analysis_{ticker}.html"
        filepath = output_path / filename

        logger.info(f"Generating website for {ticker}")

        try:
            html_content = self._create_html(analysis_result)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"✓ Website generated: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error generating website: {e}")
            return None

    def _create_html(self, result: AnalysisResult) -> str:
        """Create HTML content with all analysis data."""
        ticker = result.target_ticker
        stock_info = result.stock_info
        metrics = result.stock_metrics
        peer_analysis = result.peer_analysis
        macro_analysis = result.macro_analysis

        stock_name = stock_info.name if stock_info else ticker
        sector = stock_info.sector if stock_info else "N/A"

        # Prepare peer data for chart
        peer_names = [p.ticker for p in peer_analysis.peers] if peer_analysis and peer_analysis.peers else []
        peer_pe = [p.pe_ratio for p in peer_analysis.peers if p.pe_ratio] if peer_analysis and peer_analysis.peers else []
        target_pe = metrics.pe_ratio if metrics else 0

        # Prepare macro data
        macro_sectors = []
        macro_impacts = []
        macro_sentiments = []
        if macro_analysis:
            for impact in macro_analysis.sector_impacts:
                macro_sectors.append(impact.sector)
                macro_impacts.append(impact.impact_score)
                macro_sentiments.append(impact.sentiment)

        market_cap_val = f"${metrics.market_cap:,.0f}" if metrics and metrics.market_cap else 'N/A'
        pe_val = f"{metrics.pe_ratio:.2f}" if metrics and metrics.pe_ratio else 'N/A'
        week_high = f"${stock_info.fifty_two_week_high}" if stock_info else 'N/A'
        week_low = f"${stock_info.fifty_two_week_low}" if stock_info else 'N/A'
        roe_val = f"{metrics.roe:.2f}%" if metrics and metrics.roe else 'N/A'
        de_val = f"{metrics.debt_to_equity:.2f}" if metrics and metrics.debt_to_equity else 'N/A'
        cr_val = f"{metrics.current_ratio:.2f}" if metrics and metrics.current_ratio else 'N/A'
        pm_val = f"{metrics.profit_margin:.2f}%" if metrics and metrics.profit_margin else 'N/A'

        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Analysis - {ticker}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #e2e8f0; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #334155; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; color: #38bdf8; }}
        .header-info {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }}
        .info-card {{ background: #1e293b; padding: 15px; border-radius: 8px; border-left: 3px solid #38bdf8; }}
        .info-card label {{ font-size: 0.85em; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; }}
        .info-card .value {{ font-size: 1.3em; font-weight: bold; color: #fbbf24; margin-top: 5px; }}
        .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .tab-btn {{ background: #1e293b; border: 2px solid #334155; color: #e2e8f0; padding: 10px 20px; cursor: pointer; border-radius: 6px; transition: all 0.3s; }}
        .tab-btn.active {{ background: #38bdf8; border-color: #38bdf8; color: #0f172a; }}
        .tab-btn:hover {{ border-color: #38bdf8; }}
        .tab-content {{ background: #1e293b; padding: 30px; border-radius: 10px; border: 1px solid #334155; display: none; }}
        .tab-content.active {{ display: block; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; }}
        .metric-label {{ font-size: 0.9em; color: #94a3b8; text-transform: uppercase; }}
        .metric-value {{ font-size: 1.8em; font-weight: bold; color: #38bdf8; margin-top: 8px; }}
        .chart-container {{ background: #0f172a; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #334155; }}
        .verdict {{ background: #1e293b; padding: 20px; border-radius: 8px; border-left: 4px solid #38bdf8; margin: 20px 0; }}
        .verdict-title {{ font-size: 1.2em; font-weight: bold; color: #38bdf8; }}
        .verdict-text {{ margin-top: 10px; color: #cbd5e1; }}
        footer {{ text-align: center; margin-top: 50px; padding: 20px; color: #64748b; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 {ticker} - Stock Analysis</h1>
            <p style="color: #94a3b8; margin-top: 5px;">{stock_name}</p>
            <div class="header-info">
                <div class="info-card">
                    <label>Sector</label>
                    <div class="value">{sector}</div>
                </div>
                <div class="info-card">
                    <label>Analysis Date</label>
                    <div class="value">{datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
                <div class="info-card">
                    <label>Cache Hit</label>
                    <div class="value">{('Yes' if result.cache_hit else 'No')}</div>
                </div>
                <div class="info-card">
                    <label>Execution Time</label>
                    <div class="value">{result.execution_time_seconds:.1f}s</div>
                </div>
            </div>
        </header>

        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('overview')">📊 Overview</button>
            <button class="tab-btn" onclick="showTab('metrics')">📈 Metrics</button>
            <button class="tab-btn" onclick="showTab('peers')">👥 Peer Comparison</button>
            <button class="tab-btn" onclick="showTab('macro')">🌍 Macro Analysis</button>
        </div>

        <div id="overview" class="tab-content active">
            <h2 style="margin-bottom: 20px;">Stock Overview</h2>
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">Market Cap</div>
                    <div class="metric-value">{market_cap_val}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">P/E Ratio</div>
                    <div class="metric-value">{pe_val}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">52 Week High</div>
                    <div class="metric-value">{week_high}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">52 Week Low</div>
                    <div class="metric-value">{week_low}</div>
                </div>
            </div>
        </div>

        <div id="metrics" class="tab-content">
            <h2 style="margin-bottom: 20px;">Financial Metrics</h2>
            <div id="metrics-chart" class="chart-container" style="height: 500px;"></div>
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">ROE</div>
                    <div class="metric-value">{roe_val}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Debt to Equity</div>
                    <div class="metric-value">{de_val}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Current Ratio</div>
                    <div class="metric-value">{cr_val}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Profit Margin</div>
                    <div class="metric-value">{pm_val}</div>
                </div>
            </div>
        </div>

        <div id="peers" class="tab-content">
            <h2 style="margin-bottom: 20px;">Peer Comparison</h2>
            <div id="peers-chart" class="chart-container" style="height: 500px;"></div>
            <div style="margin-top: 20px;">
                <h3>Competitive Position</h3>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr style="background: #0f172a; border-bottom: 2px solid #334155;">
                            <th style="padding: 10px; text-align: left;">Company</th>
                            <th style="padding: 10px; text-align: right;">P/E Ratio</th>
                        </tr>
                    </thead>
                    <tbody id="peers-table">
                    </tbody>
                </table>
            </div>
        </div>

        <div id="macro" class="tab-content">
            <h2 style="margin-bottom: 20px;">Macro Analysis</h2>
            <div id="macro-chart" class="chart-container" style="height: 500px;"></div>
        </div>

        <footer>
            <p>Stock Analysis Dashboard • Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>

    <script>
        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}

        const peersData = {json.dumps(peer_names)};
        const peersTable = document.getElementById('peers-table');
        peersData.forEach(ticker => {{
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #334155';
            row.innerHTML = `<td style="padding: 10px;">${{ticker}}</td><td style="padding: 10px; text-align: right; color: #38bdf8;">N/A</td>`;
            peersTable.appendChild(row);
        }});

        Plotly.newPlot('metrics-chart', [{{'x': ['P/E', 'ROE', 'D/E', 'Current'], 'y': [{target_pe}, {roe_val or 0}, {de_val or 0}, {cr_val or 0}], 'type': 'bar', 'marker': {{'color': '#38bdf8'}}}}], {{'title': 'Financial Metrics', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});

        Plotly.newPlot('peers-chart', [{{'x': {json.dumps(peer_names)}, 'y': {json.dumps(peer_pe)}, 'type': 'bar', 'marker': {{'color': '#fbbf24'}}, 'name': 'Peers'}}, {{'x': ['{ticker}'], 'y': [{target_pe}], 'type': 'bar', 'marker': {{'color': '#10b981'}}, 'name': 'Target'}}], {{'title': 'P/E Comparison', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});

        Plotly.newPlot('macro-chart', [{{'x': {json.dumps(macro_sectors)}, 'y': {json.dumps(macro_impacts)}, 'type': 'bar', 'marker': {{'color': '#38bdf8'}}}}], {{'title': 'Macro Impact', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});
    </script>
</body>
</html>
""".format(ticker=ticker, stock_name=stock_name, sector=sector, market_cap_val=market_cap_val,
           pe_val=pe_val, week_high=week_high, week_low=week_low, roe_val=roe_val, de_val=de_val,
           cr_val=cr_val, pm_val=pm_val, target_pe=target_pe,
           peer_names=json.dumps(peer_names), peer_pe=json.dumps(peer_pe),
           macro_sectors=json.dumps(macro_sectors), macro_impacts=json.dumps(macro_impacts))
