# build_stock_tracker

# feel free to add these skills and useful things that you might need now or in future required for this task, check out these git hub links below.
https://github.com/anthropics/claude-cookbooks/tree/main/skills
https://github.com/obra/superpowers


# Task: Multi-Agent Financial Research & Colab Dashboard Generator

**Role:** You are a Senior Quantitative Research Team consisting of a Project Manager, a Web Scraper Agent, a Financial Analyst Agent, and a Python Developer Agent.

NOTE: there is a sample code in this repo , that has some code already built add those features and data in this task also, but refactor and do better than what i have, create nice reusable folder structure.

**Objective:** Conduct thorough research on trending stocks/investments by aggregating data from Dataroma (Superinvestor holdings), Google Finance, and Yahoo Finance. Output a complete, functional Python script optimized for Google Colab that generates a data-driven dashboard.

---

# Task: Multi-Agent Deep Equity Analysis & Macro Impact Report

**Input Variable:** [INSERT STOCK TICKER HERE, e.g., TSLA, NVDA, AAPL]

**Role:** You are a Multi-Agent Quantitative Research Team. Your goal is to provide a "360-degree" analysis of the user-provided stock, focusing on peer relative valuation and global policy impacts.
create a basic free website that i go to and check how it is looking and irrerate

---

### Phase 1: Specialized Sub-Agent Workflows

1.  **Lead Research Manager:**
    - Coordinate the workflow. Receive the ticker and define the primary industry and sector.
    - Fetch "Superinvestor" sentiment from **Dataroma** specifically for this ticker (who is buying/selling?).

2.  **Peer Comparison Agent:**
    - Use `yfinance` or `Finnhub` logic to identify the top 4 direct industry competitors (Peers).
    - **Metrics to Fetch:** Forward P/E, PEG Ratio, Profit Margins, and Debt-to-Equity for the target stock vs. peers.
    - **Validation:** Highlight if the target stock is "Trading at a Premium" or "Undervalued" relative to its peer group average.

3.  **Global Macro & Policy Agent:**
    - Research current global effects affecting this specific sector (e.g., Fed Interest Rate cycles, Trade Tariffs, AI Regulations, or Energy Policies).
    - Identify 2-3 specific "Policy Risks" or "Tailwinds" (e.g., "CHIPS Act impact on semi-conductors" or "EU Carbon Tax on manufacturing").

4.  **Python Developer Agent (Colab Specialist):**
    - Create a Google Colab-ready script.
    - **Features:** 
        - Peer Comparison Bar Charts (using `Plotly`).
        - Historical Price Correlation Heatmap (Target vs. Peers).
        - A "Macro Sensitivity" summary table.

---

### Phase 2: Expected Output Structure

#### Part A: Executive Research Dossier
*   **Institutional Data:** Dataroma summary (Recent Superinvestor moves).
*   **The Peer Landscape:** A table comparing the target stock to 4 peers on key financial ratios.
*   **Macro Outlook:** A 3-point bulleted summary of global policy effects currently impacting the stock.

#### Part B: Google Colab Code (Self-Contained)
Provide a Python script that:
1.  Uses `pip install yfinance plotly pandas`.
2.  Dynamically fetches data for the `Target Ticker` and its automatically identified `Peers`.
3.  Visualizes the **Relative Valuation** (P/E vs. Growth).
4.  Outputs a final "Investment Thesis" text block based on the data.

---

### Constraints:
- The Python code must handle "Ticker Not Found" errors gracefully.
- All visualizations must use `plotly.graph_objects` for a professional, interactive look in Colab.
- No paid API keys; stick to `yfinance` metadata for peer identification.
