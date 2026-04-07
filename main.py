"""
Main Streamlit application for Build Stock Tracker.
Interactive web dashboard for stock analysis.
"""

import sys
from pathlib import Path

# Add project root to path (works in Colab & local)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

from src.agents.research_manager import ResearchManager
from src.models.stock_data import AnalysisConfig
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Build Stock Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CUSTOM STYLING ====================
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .positive {
        color: #00d084;
    }
    .negative {
        color: #ff2b2b;
    }
    .neutral {
        color: #808080;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== SESSION STATE ====================
if "research_manager" not in st.session_state:
    st.session_state.research_manager = ResearchManager(use_cache=True)

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "ticker_input" not in st.session_state:
    st.session_state.ticker_input = "AAPL"


# ==================== HELPER FUNCTIONS ====================
def format_large_number(num):
    """Format large numbers for display."""
    if num is None:
        return "N/A"
    if abs(num) >= 1e12:
        return f"${num / 1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"${num / 1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"${num / 1e6:.2f}M"
    else:
        return f"${num:,.2f}"


def create_peer_comparison_chart(result):
    """Create peer comparison chart."""
    if not result.peer_analysis or not result.peer_analysis.peers:
        return None

    peers = result.peer_analysis.peers
    tickers = [p.ticker for p in peers]
    forward_pes = [p.metrics.forward_pe or 0 for p in peers]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=tickers,
            y=forward_pes,
            marker_color=["#0066cc" if p.ticker == result.target_ticker else "#cccccc" for p in peers],
            text=[f"{pe:.1f}" for pe in forward_pes],
            textposition="auto",
        )
    )

    fig.update_layout(
        title="Forward P/E Ratio Comparison",
        xaxis_title="Ticker",
        yaxis_title="Forward P/E",
        template="plotly_white",
        height=400,
    )

    return fig


def create_metrics_table(result):
    """Create metrics comparison table."""
    if not result.peer_analysis or not result.peer_analysis.peers:
        return None

    data = {
        "Ticker": [result.target_ticker] + [p.ticker for p in result.peer_analysis.peers],
        "Forward P/E": [result.stock_metrics.forward_pe if result.stock_metrics else None]
        + [p.metrics.forward_pe for p in result.peer_analysis.peers],
        "Profit Margin %": [result.stock_metrics.profit_margin if result.stock_metrics else None]
        + [p.metrics.profit_margin for p in result.peer_analysis.peers],
        "ROE %": [result.stock_metrics.roe if result.stock_metrics else None]
        + [p.metrics.roe for p in result.peer_analysis.peers],
        "D/E Ratio": [result.stock_metrics.debt_to_equity if result.stock_metrics else None]
        + [p.metrics.debt_to_equity for p in result.peer_analysis.peers],
    }

    return pd.DataFrame(data).round(2)


# ==================== HEADER ====================
st.markdown("# 📈 Build Stock Tracker")
st.markdown(
    "**Multi-Agent Financial Research & Dashboard Generator** | Peer Analysis | Macro Impacts | Colab Scripts"
)

st.divider()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    ticker = st.text_input(
        "Enter Stock Ticker",
        value=st.session_state.ticker_input,
        placeholder="e.g., AAPL, TSLA, MSFT",
        key="ticker_input",
    ).upper()

    col1, col2 = st.columns(2)
    with col1:
        include_peer = st.checkbox("Peer Analysis", value=True)
    with col2:
        include_macro = st.checkbox("Macro Analysis", value=True)

    st.markdown("---")
    st.markdown("## 📊 About")
    st.markdown(
        """
        This tool provides comprehensive stock analysis:
        - **Stock Metrics:** P/E, margins, ROE, debt ratios
        - **Peer Comparison:** Valuation vs competitors
        - **Macro Analysis:** Policy impacts & sector trends
        - **Colab Scripts:** Self-contained analysis notebooks

        [GitHub](https://github.com/nandhan2047/build_stock_tracker)
        """
    )

    st.markdown("---")
    st.markdown("### Cache Status")
    if st.button("🔄 Clear Cache", use_container_width=True):
        st.session_state.research_manager.cache_manager.clear_all()
        st.success("✅ Cache cleared!")

# ==================== MAIN CONTENT ====================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Analyze Stock", use_container_width=True, type="primary"):
        if not ticker:
            st.error("❌ Please enter a ticker symbol")
        else:
            with st.spinner(f"🔍 Analyzing {ticker}..."):
                try:
                    config = AnalysisConfig(
                        ticker=ticker,
                        num_peers=4,
                        include_peer_analysis=include_peer,
                        include_macro_analysis=include_macro,
                        include_colab_generation=False,
                    )

                    result = st.session_state.research_manager.analyze(ticker, config)

                    if result:
                        st.session_state.analysis_result = result
                        st.success(f"✅ Analysis complete for {ticker}!")
                    else:
                        st.error(f"❌ Failed to analyze {ticker}. Please check the ticker symbol.")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    logger.error(f"Analysis error: {e}", exc_info=True)

with col2:
    if st.button("📥 Load Sample (AAPL)", use_container_width=True):
        with st.spinner("Loading sample analysis..."):
            try:
                config = AnalysisConfig(ticker="AAPL", include_colab_generation=False)
                result = st.session_state.research_manager.analyze("AAPL", config)
                if result:
                    st.session_state.analysis_result = result
                    st.success("✅ Sample analysis loaded!")
            except Exception as e:
                st.error(f"❌ Error loading sample: {str(e)}")

with col3:
    if st.button("ℹ️ How to Use", use_container_width=True):
        st.info(
            """
            **Quick Start:**
            1. Enter a stock ticker (e.g., AAPL)
            2. Select analysis options
            3. Click "Analyze Stock"
            4. Review results and insights

            **Features:**
            - Real-time stock data
            - Peer comparison analysis
            - Macro policy impacts
            - Interactive visualizations
            """
        )

st.divider()

# ==================== RESULTS DISPLAY ====================
if st.session_state.analysis_result:
    result = st.session_state.analysis_result

    # COMPANY INFO
    st.markdown(f"## 🏢 {result.target_ticker}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Company",
            result.stock_info.name if result.stock_info else "N/A",
        )

    with col2:
        st.metric(
            "Sector",
            result.stock_info.sector if result.stock_info else "N/A",
        )

    with col3:
        st.metric(
            "Industry",
            result.stock_info.industry if result.stock_info else "N/A",
        )

    with col4:
        st.metric(
            "Analysis Time",
            f"{result.execution_time_seconds:.2f}s" if result.execution_time_seconds else "N/A",
        )

    st.divider()

    # KEY METRICS
    st.markdown("### 💰 Key Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    if result.stock_metrics:
        with col1:
            st.metric("Current Price", f"${result.stock_metrics.price:.2f}" if result.stock_metrics.price else "N/A")

        with col2:
            st.metric("Market Cap", format_large_number(result.stock_metrics.market_cap))

        with col3:
            st.metric(
                "P/E Ratio",
                f"{result.stock_metrics.pe_ratio:.2f}" if result.stock_metrics.pe_ratio else "N/A",
            )

        with col4:
            st.metric(
                "Forward P/E",
                f"{result.stock_metrics.forward_pe:.2f}" if result.stock_metrics.forward_pe else "N/A",
            )

        with col5:
            st.metric(
                "PEG Ratio",
                f"{result.stock_metrics.peg_ratio:.2f}" if result.stock_metrics.peg_ratio else "N/A",
            )

    # TABS FOR DIFFERENT SECTIONS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Peer Analysis", "🌍 Macro Analysis", "📈 Financials", "📥 Download"])

    # TAB 1: PEER ANALYSIS
    with tab1:
        if result.peer_analysis:
            st.markdown("### Peer Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Valuation",
                    result.peer_analysis.valuation_verdict or "N/A",
                )

            with col2:
                st.metric(
                    "Peers Analyzed",
                    len(result.peer_analysis.peers) if result.peer_analysis.peers else 0,
                )

            # Peer metrics table
            metrics_df = create_metrics_table(result)
            if metrics_df is not None:
                st.markdown("**Metrics Comparison Table**")
                st.dataframe(metrics_df, use_container_width=True)

            # Peer chart
            chart = create_peer_comparison_chart(result)
            if chart:
                st.plotly_chart(chart, use_container_width=True)

            # Percentile rankings
            if result.peer_analysis.percentile_ranking:
                st.markdown("**Percentile Rankings**")
                ranking_data = {
                    "Metric": list(result.peer_analysis.percentile_ranking.keys()),
                    "Percentile": list(result.peer_analysis.percentile_ranking.values()),
                }
                st.dataframe(pd.DataFrame(ranking_data), use_container_width=True)
        else:
            st.info("No peer analysis available")

    # TAB 2: MACRO ANALYSIS
    with tab2:
        if result.macro_analysis:
            st.markdown("### Macro & Policy Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Overall Sentiment",
                    result.macro_analysis.overall_sentiment or "N/A",
                )

            with col2:
                macro_score = result.macro_analysis.macro_score
                st.metric(
                    "Macro Score",
                    f"{macro_score:+.1f}/10" if macro_score else "N/A",
                )

            st.markdown("#### 📈 Tailwinds (Positive Factors)")
            for i, tailwind in enumerate(result.macro_analysis.tailwinds, 1):
                st.success(f"{i}. {tailwind}")

            st.markdown("#### 📉 Headwinds (Risk Factors)")
            for i, headwind in enumerate(result.macro_analysis.headwinds, 1):
                st.error(f"{i}. {headwind}")
        else:
            st.info("No macro analysis available")

    # TAB 3: FINANCIALS
    with tab3:
        if result.stock_metrics:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Profitability**")
                fin_data = {
                    "Metric": ["Profit Margin", "Operating Margin", "ROE", "ROA"],
                    "Value": [
                        f"{result.stock_metrics.profit_margin:.2f}%" if result.stock_metrics.profit_margin else "N/A",
                        f"{result.stock_metrics.operating_margin:.2f}%" if result.stock_metrics.operating_margin else "N/A",
                        f"{result.stock_metrics.roe:.2f}%" if result.stock_metrics.roe else "N/A",
                        f"{result.stock_metrics.roa:.2f}%" if result.stock_metrics.roa else "N/A",
                    ],
                }
                st.dataframe(pd.DataFrame(fin_data), use_container_width=True)

            with col2:
                st.markdown("**Strength & Liquidity**")
                strength_data = {
                    "Metric": ["Current Ratio", "Quick Ratio", "Debt-to-Equity", "Free Cash Flow"],
                    "Value": [
                        f"{result.stock_metrics.current_ratio:.2f}" if result.stock_metrics.current_ratio else "N/A",
                        f"{result.stock_metrics.quick_ratio:.2f}" if result.stock_metrics.quick_ratio else "N/A",
                        f"{result.stock_metrics.debt_to_equity:.2f}" if result.stock_metrics.debt_to_equity else "N/A",
                        format_large_number(result.stock_metrics.free_cash_flow),
                    ],
                }
                st.dataframe(pd.DataFrame(strength_data), use_container_width=True)
        else:
            st.info("No financial data available")

    # TAB 4: DOWNLOAD
    with tab4:
        st.markdown("### Download Analysis")

        # Download as JSON
        json_data = result.to_json()
        st.download_button(
            label="📥 Download Analysis (JSON)",
            data=json_data,
            file_name=f"analysis_{result.target_ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )

        # Download as CSV (metrics only)
        if result.peer_analysis:
            metrics_df = create_metrics_table(result)
            if metrics_df is not None:
                csv_data = metrics_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Peer Comparison (CSV)",
                    data=csv_data,
                    file_name=f"peers_{result.target_ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                )

        st.markdown("---")
        st.info("💡 **Tip:** Use the JSON download for comprehensive analysis data or share with others.")

    st.divider()

    # FOOTER
    st.markdown(
        f"""
    ---
    **Analysis Generated:** {result.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}  
    **Cache Hit:** {'Yes ✅' if result.cache_hit else 'No (Fresh Data)'}  
    **Execution Time:** {result.execution_time_seconds:.2f} seconds
    """
    )

else:
    # WELCOME MESSAGE
    st.markdown(
        """
    ## Welcome to Build Stock Tracker! 👋

    ### Get started:
    1. **Enter a stock ticker** in the sidebar (e.g., AAPL, TSLA, MSFT)
    2. **Configure analysis options** (peer analysis, macro analysis)
    3. **Click "Analyze Stock"** to run the full analysis
    4. **Review the results** with interactive charts and insights

    ### What you'll get:
    - ✅ **Stock Metrics:** Current price, P/E ratio, margins, ROE, debt ratios
    - ✅ **Peer Comparison:** See how your stock stacks up vs competitors
    - ✅ **Macro Analysis:** Understand policy impacts on your sector
    - ✅ **Interactive Charts:** Explore data with Plotly visualizations
    - ✅ **Download Options:** Export analysis as JSON or CSV

    ### Try the sample:
    Click "Load Sample (AAPL)" to see a complete analysis!

    ---
    """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Features", "8+")
    with col2:
        st.metric("Data Sources", "3")
    with col3:
        st.metric("Cache Enabled", "✅")
