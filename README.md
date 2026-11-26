# momentum-backtest
Momentum Backtest: 12-1 Trend Rule on Four ETFs

I backtested a trend-following strategy on four ETFs (SPY, EWU, TLT, GLD) with transaction costs and out-of-sample validation, fixing parameters before testing. I logged my decisions and problems throughout, including a flawed first run.

Hypothesis

Assets that have risen over the past 12 months (excluding the latest month) tend to keep rising. Holding them when the trailing return is positive, and cash otherwise, should beat buy-and-hold on a risk-adjusted basis after transaction costs.

Settings (12-1 lookback, 2017-01-01 split, 10bp costs) were fixed before I looked at any results. This hypothesis was written down after my first run.

Data and universe
Assets: SPY (US equities), EWU (UK equities), TLT (long-dated US Treasuries), GLD (gold), all priced in USD.
Source: daily adjusted close prices from Yahoo Finance via yfinance, converted to month-end prices.
Period: results run from February 2006 to November 2026. The signal needs 12 months of history, so the first signal date is early 2006. The final month is incomplete.
I originally planned to use ISF.L for UK equities but replaced it with EWU because Yahoo's history for ISF.L was much shorter than the other assets. I made this change for data availability, not performance.
Method
Signal: return from 12 months ago to 1 month ago, measured at each month end. The latest month is skipped because very short-term moves tend to partly reverse, which can offset the previous 11 months and weaken the signal.
Positions: equal weight (25%) in each asset with a positive signal, the remainder in cash earning 0%. Rebalanced monthly.
Timing: the signal at the end of month t sets positions for month t+1. This avoids look-ahead bias, which is when a backtest uses information that wasn't available at the time of the trade. I do this with the shift(1) line in my code.
Costs: 10 basis points on every unit of turnover.
Benchmark: equal-weight buy-and-hold of the same four assets, rebalanced monthly.
Validation: 2006 to 2016 is in-sample and 2017 onwards is out-of-sample. The split separates designing a strategy from testing whether it works, which guards against overfitting. In this project I fixed my settings in advance rather than tuning them, so the split works as a consistency check across two periods (see "What I found").
Results

Net of costs. Annual return / volatility / Sharpe ratio / max drawdown.

Period	Strategy	Buy and hold
Full (2006-2026)	6.4% / 7.5% / 0.87 / -9.5%	7.7% / 10.1% / 0.78 / -25.4%
In-sample (2006-2016)	6.0% / 7.5% / 0.81 / -8.4%	6.3% / 9.9% / 0.67 / -25.4%
Out-of-sample (2017-2026)	6.9% / 7.6% / 0.93 / -9.5%	9.2% / 10.3% / 0.91 / -20.7%

Average monthly turnover: 11%. Costs reduced annual return by about 0.2 percentage points.

What I found

The strategy cut maximum drawdown to 9.5% from 25.4% over the full period, but earned a lower annual return than buy-and-hold in every period (for example 6.9% vs 9.2% out-of-sample). Its Sharpe ratio was higher in-sample (0.81 vs 0.67) and over the full period (0.87 vs 0.78), but out-of-sample the two were almost identical (0.93 vs 0.91), so I can't claim it adds value beyond lower drawdowns. The drawdown reduction held in both periods, but the Sharpe advantage did not. The in-sample outperformance probably relied heavily on one event, the 2008 crash, which I have not isolated.

This is also not a strict test against overfitting. I fixed the 12-1 setting before testing, so the split works as a consistency check across two periods rather than a true out-of-sample test. It would become one if I chose settings using 2006 to 2016 only, which is what the planned robustness checks would do.

Limitations
Cash earns 0% in this test, which understates the strategy, especially since 2022.
Much of the in-sample advantage probably comes from avoiding the 2008 crash, which is a single event.
The strategy holds less risk than buy-and-hold (lower volatility), so part of the improved Sharpe may just be de-risking. I have not compared against a volatility-matched benchmark.
Four assets, one parameter setting, and no statistical significance test.
Sharpe ratios ignore the risk-free rate.
Past results may not hold in future.
What went wrong and what I'd do next
First run: it included ISF.L for UK equities. This was a mistake, because Yahoo Finance had much less history for it than for the other assets, which pushed the first signal to 2010 and missed the 2008 crash. This taught me to check data coverage before trusting results.
Download error: TLT failed to download (database is locked), which I fixed by turning off multithreaded downloads.
Next steps: robustness checks across lookbacks and costs, a volatility-matched benchmark, interest on cash, and a larger universe of assets.
How to run
py -m pip install pandas numpy matplotlib yfinance
py backtest.py
Tools

I used an AI assistant to help debug the code and to explain concepts. I ran and tested it, logged the process, and wrote this write-up and my interpretation of the results