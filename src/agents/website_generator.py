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

        if isinstance(stock_info, dict):
            stock_name = stock_info.get("name", ticker)
            sector = stock_info.get("sector", "N/A")
        else:
            stock_name = stock_info.name if stock_info else ticker
            sector = stock_info.sector if stock_info else "N/A"

        if isinstance(metrics, dict):
            market_cap_val = f"${metrics.get('market_cap', 0):,.0f}" if metrics.get('market_cap') else 'N/A'
            pe_val = f"{metrics.get('pe_ratio', 0):.2f}" if metrics.get('pe_ratio') else 'N/A'
            roe_val = f"{metrics.get('roe', 0):.2f}%" if metrics.get('roe') else 'N/A'
            de_val = f"{metrics.get('debt_to_equity', 0):.2f}" if metrics.get('debt_to_equity') else 'N/A'
            cr_val = f"{metrics.get('current_ratio', 0):.2f}" if metrics.get('current_ratio') else 'N/A'
            pm_val = f"{metrics.get('profit_margin', 0):.2f}%" if metrics.get('profit_margin') else 'N/A'
            target_pe = metrics.get('pe_ratio', 0)
        else:
            market_cap_val = f"${metrics.market_cap:,.0f}" if metrics and metrics.market_cap else 'N/A'
            pe_val = f"{metrics.pe_ratio:.2f}" if metrics and metrics.pe_ratio else 'N/A'
            roe_val = f"{metrics.roe:.2f}%" if metrics and metrics.roe else 'N/A'
            de_val = f"{metrics.debt_to_equity:.2f}" if metrics and metrics.debt_to_equity else 'N/A'
            cr_val = f"{metrics.current_ratio:.2f}" if metrics and metrics.current_ratio else 'N/A'
            pm_val = f"{metrics.profit_margin:.2f}%" if metrics and metrics.profit_margin else 'N/A'
            target_pe = metrics.pe_ratio if metrics else 0

        # Prepare peer data for chart
        peer_names = []
        peer_pe = []
        if peer_analysis and peer_analysis.peers:
            for p in peer_analysis.peers:
                peer_names.append(p.ticker)
                if isinstance(p.metrics, dict):
                    peer_pe.append(p.metrics.get('pe_ratio', 0))
                else:
                    peer_pe.append(p.metrics.pe_ratio or 0)

        # Prepare macro data
        macro_sectors = []
        macro_impacts = []
        if macro_analysis and hasattr(macro_analysis, 'impacts'):
            for impact in macro_analysis.impacts:
                if isinstance(impact, dict):
                    macro_sectors.append(impact.get('event_type', 'Unknown'))
                    macro_impacts.append(impact.get('impact_score', 0))
                else:
                    macro_sectors.append(impact.event_type)
                    macro_impacts.append(impact.impact_score)

        # Week high/low
        if isinstance(stock_info, dict):
            week_high = f"${stock_info.get('fifty_two_week_high', 'N/A')}"
            week_low = f"${stock_info.get('fifty_two_week_low', 'N/A')}"
        else:
            week_high = f"${stock_info.fifty_two_week_high}" if stock_info and hasattr(stock_info, 'fifty_two_week_high') else 'N/A'
            week_low = f"${stock_info.fifty_two_week_low}" if stock_info and hasattr(stock_info, 'fifty_two_week_low') else 'N/A'

        analysis_date = datetime.now().strftime('%Y-%m-%d')
        analysis_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cache_hit_str = 'Yes' if result.cache_hit else 'No'
        exec_time = f"{result.execution_time_seconds:.1f}" if result.execution_time_seconds else "0.0"

        # Extract Investment Thesis data
        thesis = result.investment_thesis
        thesis_rating = thesis.rating if thesis else "N/A"
        thesis_conviction = thesis.conviction_level if thesis else "N/A"
        thesis_confidence = f"{thesis.confidence_score}%" if thesis and thesis.confidence_score else "N/A"
        thesis_horizon = thesis.time_horizon if thesis else "N/A"
        thesis_summary = thesis.thesis_summary if thesis else "No thesis available"
        thesis_strengths = thesis.key_strengths if thesis else []
        thesis_weaknesses = thesis.key_weaknesses if thesis else []
        thesis_catalysts = thesis.catalysts if thesis else []
        thesis_risks = thesis.risks if thesis else []

        # Extract Percentile Rankings data
        percentiles = {}
        percentile_labels = []
        percentile_values = []
        if peer_analysis and peer_analysis.percentile_ranking:
            for metric, percentile in peer_analysis.percentile_ranking.items():
                percentile_labels.append(metric)
                percentile_values.append(percentile)

        # Extract Financial Health data
        op_margin = f"{metrics.operating_margin:.2f}%" if metrics and metrics.operating_margin else 'N/A'
        roa_val = f"{metrics.roa:.2f}%" if metrics and metrics.roa else 'N/A'
        qr_val = f"{metrics.quick_ratio:.2f}" if metrics and metrics.quick_ratio else 'N/A'
        fcf_val = f"${metrics.free_cash_flow:,.0f}" if metrics and metrics.free_cash_flow else 'N/A'
        revenue_val = f"${metrics.revenue:,.0f}" if metrics and metrics.revenue else 'N/A'
        ni_val = f"${metrics.net_income:,.0f}" if metrics and metrics.net_income else 'N/A'

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
                    <div class="value">{analysis_date}</div>
                </div>
                <div class="info-card">
                    <label>Cache Hit</label>
                    <div class="value">{cache_hit_str}</div>
                </div>
                <div class="info-card">
                    <label>Execution Time</label>
                    <div class="value">{exec_time}s</div>
                </div>
            </div>
        </header>

        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('overview')">Overview</button>
            <button class="tab-btn" onclick="showTab('metrics')">Metrics</button>
            <button class="tab-btn" onclick="showTab('peers')">Peer Comparison</button>
            <button class="tab-btn" onclick="showTab('macro')">Macro Analysis</button>
            <button class="tab-btn" onclick="showTab('thesis')">Investment Thesis</button>
            <button class="tab-btn" onclick="showTab('percentiles')">Percentile Rankings</button>
            <button class="tab-btn" onclick="showTab('health')">Financial Health</button>
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

        <div id="thesis" class="tab-content">
            <h2 style="margin-bottom: 20px;">Investment Thesis</h2>
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">Rating</div>
                    <div class="metric-value" id="thesis-rating">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Conviction</div>
                    <div class="metric-value" id="thesis-conviction">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Confidence Score</div>
                    <div class="metric-value" id="thesis-confidence">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Time Horizon</div>
                    <div class="metric-value" id="thesis-horizon">N/A</div>
                </div>
            </div>
            <div class="verdict">
                <div class="verdict-title">Thesis Summary</div>
                <div class="verdict-text" id="thesis-summary">No thesis available</div>
            </div>
            <div style="margin-top: 20px;">
                <h3>Key Strengths</h3>
                <ul id="thesis-strengths" style="margin-left: 20px; margin-top: 10px; color: #cbd5e1;"></ul>
            </div>
            <div style="margin-top: 20px;">
                <h3>Key Weaknesses</h3>
                <ul id="thesis-weaknesses" style="margin-left: 20px; margin-top: 10px; color: #cbd5e1;"></ul>
            </div>
            <div style="margin-top: 20px;">
                <h3>Catalysts</h3>
                <ul id="thesis-catalysts" style="margin-left: 20px; margin-top: 10px; color: #cbd5e1;"></ul>
            </div>
            <div style="margin-top: 20px;">
                <h3>Risks</h3>
                <ul id="thesis-risks" style="margin-left: 20px; margin-top: 10px; color: #cbd5e1;"></ul>
            </div>
        </div>

        <div id="percentiles" class="tab-content">
            <h2 style="margin-bottom: 20px;">Percentile Rankings</h2>
            <div id="percentiles-chart" class="chart-container" style="height: 600px;"></div>
        </div>

        <div id="health" class="tab-content">
            <h2 style="margin-bottom: 20px;">Financial Health</h2>
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">Operating Margin</div>
                    <div class="metric-value" id="health-op-margin">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">ROA</div>
                    <div class="metric-value" id="health-roa">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Quick Ratio</div>
                    <div class="metric-value" id="health-quick-ratio">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Free Cash Flow</div>
                    <div class="metric-value" id="health-fcf">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Revenue</div>
                    <div class="metric-value" id="health-revenue">N/A</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Net Income</div>
                    <div class="metric-value" id="health-net-income">N/A</div>
                </div>
            </div>
        </div>

        <footer>
            <p>Stock Analysis Dashboard • Generated {analysis_datetime}</p>
        </footer>
    </div>

    <script>
        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}

        const peersData = {peer_names};
        const peersTable = document.getElementById('peers-table');
        peersData.forEach(ticker => {{
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #334155';
            row.innerHTML = `<td style="padding: 10px;">${{ticker}}</td><td style="padding: 10px; text-align: right; color: #38bdf8;">N/A</td>`;
            peersTable.appendChild(row);
        }});

        const metricsY = [{target_pe}, 0, 0, 0];
        Plotly.newPlot('metrics-chart', [{{'x': ['P/E', 'ROE', 'D/E', 'Current'], 'y': metricsY, 'type': 'bar', 'marker': {{'color': '#38bdf8'}}}}], {{'title': 'Financial Metrics', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});

        Plotly.newPlot('peers-chart', [{{'x': {peer_names}, 'y': {peer_pe}, 'type': 'bar', 'marker': {{'color': '#fbbf24'}}, 'name': 'Peers'}}, {{'x': ['{ticker}'], 'y': [{target_pe}], 'type': 'bar', 'marker': {{'color': '#10b981'}}, 'name': 'Target'}}], {{'title': 'P/E Comparison', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});

        Plotly.newPlot('macro-chart', [{{'x': {macro_sectors}, 'y': {macro_impacts}, 'type': 'bar', 'marker': {{'color': '#38bdf8'}}}}], {{'title': 'Macro Impact', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}}});

        // Investment Thesis data
        document.getElementById('thesis-rating').textContent = '{thesis_rating}';
        document.getElementById('thesis-conviction').textContent = '{thesis_conviction}';
        document.getElementById('thesis-confidence').textContent = '{thesis_confidence}';
        document.getElementById('thesis-horizon').textContent = '{thesis_horizon}';
        document.getElementById('thesis-summary').textContent = '{thesis_summary}';

        const thesisStrengths = {thesis_strengths_json};
        const strengthsList = document.getElementById('thesis-strengths');
        thesisStrengths.forEach(s => {{
            const li = document.createElement('li');
            li.textContent = s;
            strengthsList.appendChild(li);
        }});

        const thesisWeaknesses = {thesis_weaknesses_json};
        const weaknessesList = document.getElementById('thesis-weaknesses');
        thesisWeaknesses.forEach(w => {{
            const li = document.createElement('li');
            li.textContent = w;
            weaknessesList.appendChild(li);
        }});

        const thesisCatalysts = {thesis_catalysts_json};
        const catalystsList = document.getElementById('thesis-catalysts');
        thesisCatalysts.forEach(c => {{
            const li = document.createElement('li');
            li.textContent = c;
            catalystsList.appendChild(li);
        }});

        const thesisRisks = {thesis_risks_json};
        const risksList = document.getElementById('thesis-risks');
        thesisRisks.forEach(r => {{
            const li = document.createElement('li');
            li.textContent = r;
            risksList.appendChild(li);
        }});

        // Percentile Rankings chart
        const percentileLabels = {percentile_labels_json};
        const percentileValues = {percentile_values_json};
        Plotly.newPlot('percentiles-chart', [{{'y': percentileLabels, 'x': percentileValues, 'type': 'bar', 'orientation': 'h', 'marker': {{'color': '#8b5cf6'}}}}], {{'title': 'Percentile Rankings vs Peers', 'plot_bgcolor': '#0f172a', 'paper_bgcolor': '#1e293b', 'font': {{'color': '#e2e8f0'}}, 'xaxis': {{'title': 'Percentile (0-100)'}}}});

        // Financial Health data
        document.getElementById('health-op-margin').textContent = '{op_margin}';
        document.getElementById('health-roa').textContent = '{roa_val}';
        document.getElementById('health-quick-ratio').textContent = '{qr_val}';
        document.getElementById('health-fcf').textContent = '{fcf_val}';
        document.getElementById('health-revenue').textContent = '{revenue_val}';
        document.getElementById('health-net-income').textContent = '{ni_val}';
    </script>
</body>
</html>
""".format(ticker=ticker, stock_name=stock_name, sector=sector, market_cap_val=market_cap_val,
           pe_val=pe_val, week_high=week_high, week_low=week_low, roe_val=roe_val, de_val=de_val,
           cr_val=cr_val, pm_val=pm_val, target_pe=target_pe or 0,
           peer_names=json.dumps(peer_names), peer_pe=json.dumps(peer_pe),
           macro_sectors=json.dumps(macro_sectors), macro_impacts=json.dumps(macro_impacts),
           analysis_date=analysis_date, analysis_datetime=analysis_datetime, cache_hit_str=cache_hit_str, exec_time=exec_time,
           thesis_rating=thesis_rating, thesis_conviction=thesis_conviction, thesis_confidence=thesis_confidence,
           thesis_horizon=thesis_horizon, thesis_summary=thesis_summary,
           thesis_strengths_json=json.dumps(thesis_strengths), thesis_weaknesses_json=json.dumps(thesis_weaknesses),
           thesis_catalysts_json=json.dumps(thesis_catalysts), thesis_risks_json=json.dumps(thesis_risks),
           percentile_labels_json=json.dumps(percentile_labels), percentile_values_json=json.dumps(percentile_values),
           op_margin=op_margin, roa_val=roa_val, qr_val=qr_val, fcf_val=fcf_val, revenue_val=revenue_val, ni_val=ni_val)

        return html
