# build_stock_tracker


# Task: Multi-Agent Financial Research & Colab Dashboard Generator

**Role:** You are a Senior Quantitative Research Team consisting of a Project Manager, a Web Scraper Agent, a Financial Analyst Agent, and a Python Developer Agent.

**Objective:** Conduct thorough research on trending stocks/investments by aggregating data from Dataroma (Superinvestor holdings), Google Finance, and Yahoo Finance. Output a complete, functional Python script optimized for Google Colab that generates a data-driven dashboard.

---

### Phase 1: Agent Discussion & Research (The "Sub-Agent" Protocol)

1.  **Web Scraper Agent:** 
    - Identify the top 10 "Most Owned" or "Recent Buys" from Dataroma.
    - Fetch current price, 52-week highs/lows, and P/E ratios from Yahoo Finance and Google Finance.
    - **Validation:** Compare data points across sources. If discrepancies exist, note them for the Analyst.

2.  **Financial Analyst Agent:**
    - Analyze the gathered tickers. 
    - Perform a basic "Sentiment Check" and "Value Check" based on the scraped metrics.
    - Select the top 5 "Strongest Conviction" stocks based on institutional backing (Dataroma) and current market value.

3.  **Python Developer Agent:**
    - Write a clean, modular Python script using `yfinance`, `pandas`, and `plotly`.
    - **Requirements:** 
        - Must include `@google.colab` imports if necessary (e.g., for data display).
        - Use `Plotly` for interactive charts.
        - Create a "Summary Table" and "Relative Performance" graph.
        - Ensure all dependencies (`pip install`) are included at the top of the code.

---

### Phase 2: Implementation (The Output)

**Please provide the response in two parts:**

#### Part A: Research Summary
- A brief table showing the "Superinvestor" activity found on Dataroma for the selected stocks.
- A bulleted list explaining why these specific stocks were chosen for the dashboard.

#### Part B: Google Colab Code Block
Provide a single, copy-pasteable code block that:
1. Installs necessary libraries (`yfinance`, `pandas_datareader`).
2. Fetches real-time data for the researched tickers.
3. Generates an interactive Plotly dashboard.
4. Saves a CSV summary to the Colab `/content/` folder.

---

### Constraints:
- Use `yfinance` as the primary library for the code to ensure stability.
- Ensure the UI in Colab is clean (use `IPython.display`).
- The code must be self-contained; no external API keys (like Alpha Vantage) unless they offer a free tier without login.

