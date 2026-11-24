# momentum-backtest
Momentum Backtest project
Momentum Backtest: 12-1 Trend Rule on Four ETFs

[One or two sentences in your own words: what you tested and what you found.]

Hypothesis

Assets that have risen over the past 12 months (excluding the latest month) tend to keep rising. Holding them when the trailing return is positive, and cash otherwise, should beat buy-and-hold on a risk-adjusted basis after transaction costs.

Settings (12-1 lookback, 2017-01-01 split, 10bp costs) were fixed before I looked at any results. This hypothesis was written down after my first run.

Data and universe
Assets: SPY (US equities), EWU (UK equities), TLT (long-dated US Treasuries), GLD (gold), all priced in USD.
Source: daily adjusted close prices from Yahoo Finance via yfinance, converted to month-end prices.
Period: results run from February 2006 to November 2026. The signal needs 12 months of history, so the first signal date is early 2006.
I originally planned to use ISF.L for UK equities but replaced it with EWU because Yahoo's history for ISF.L was too short. I made this change for data availability, not performance.
Method
Signal: return from 12 months ago to 1 month ago, measured at each month end. [Explain in your own words why the latest month is skipped.]
Positions: equal weight (25%) in each asset with a positive signal, the remainder in cash earning 0%. Rebalanced monthly.
Timing: the signal at the end of month t sets positions for month t+1. [Explain in your own words what look-ahead bias is and why this matters.]
Costs: 10 basis points on every unit of turnover.
Benchmark: equal-weight buy-and-hold of the same four assets, rebalanced monthly.
Validation: 2006 to 2016 is in-sample. 2017 onwards is out-of-sample. [Explain in your own words why the split exists.]
Results

Net of costs. Annual return / volatility / Sharpe ratio / max drawdown.

Period	Strategy	Buy and hold
Full (2006-2026)	6.4% / 7.5% / 0.87 / -9.5%	7.7% / 10.1% / 0.78 / -25.4%
In-sample (2006-2016)	6.0% / 7.5% / 0.81 / -8.4%	6.3% / 9.9% / 0.67 / -25.4%
Out-of-sample (2017-2026)	6.9% / 7.6% / 0.93 / -9.5%	9.2% / 10.3% / 0.91 / -20.7%

Average monthly turnover: 11%. Costs reduced annual return by about 0.2 percentage points.

Equity curve

What I found

[Write 3 to 5 sentences in your own words. Cover: (1) did the strategy beat buy-and-hold on Sharpe, and in which periods; (2) what happened to drawdowns and returns, and why you think that is; (3) whether the out-of-sample result confirms the in-sample result.]

Limitations
Cash earns 0% in this test, which understates the strategy, especially since 2022.
Much of the in-sample advantage probably comes from avoiding the 2008 crash, which is a single event.
The strategy holds less risk than buy-and-hold (lower volatility), so part of the improved Sharpe may just be de-risking. I have not compared against a volatility-matched benchmark.
Four assets, one parameter setting, and no statistical significance test.
Sharpe ratios ignore the risk-free rate.
Past results may not hold in future.
What went wrong and what I'd do next
First run: [Describe in your own words that the first run used ISF.L by mistake, started in 2010, missed 2008 and gave a different answer. What did that teach you about sensitivity to the test period?]
Download error: TLT failed to download (database is locked), which I fixed by downloading tickers one at a time.
Next steps: robustness checks across lookbacks and costs, a volatility-matched benchmark, interest on cash, and a larger universe of assets.
How to run
py -m pip install pandas numpy matplotlib yfinance
py backtest.py
Tools

[Edit to match what is true, for example: "I used an AI assistant to help write and debug the code. The design decisions, testing, logging and interpretation are my own."]