"""
12-1 momentum backtest on a small ETF universe.

Hypothesis (write this in your README BEFORE looking at results):
Assets with a positive trailing 12-month return (skipping the most recent
month) keep outperforming over the next month. Holding them when the signal is
positive, and cash otherwise, should beat buy-and-hold on a risk-adjusted
basis after transaction costs.

Run with:  python backtest.py   (or  py backtest.py  on Windows)
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Settings (decide these up front; do not tune them on the out-of-sample period)
# ----------------------------------------------------------------------------
TICKERS = ["SPY", "EWU", "TLT", "GLD"]  # US equities, UK equities (USD), bonds, gold
START = "2005-01-01"
SPLIT_DATE = "2017-01-01"  # before = in-sample, after = out-of-sample
LOOKBACK = 12              # months
SKIP = 1                   # skip the most recent month (the "12-1" convention)
COST_BPS = 10              # cost per unit of turnover, in basis points


# ----------------------------------------------------------------------------
# Step 3: data
# ----------------------------------------------------------------------------
def load_monthly_prices():
    prices = yf.download(TICKERS, start=START, auto_adjust=True, progress=False, threads=False)["Close"]
    prices = prices[TICKERS].ffill()  # UK and US holidays differ, so fill gaps
    empty = [t for t in TICKERS if prices[t].isna().all()]
    if empty:
        raise SystemExit(f"No data downloaded for {empty}. Run it again, or clear the yfinance cache.")
    # Check the data before trusting it
    print("Data range:", prices.index[0].date(), "to", prices.index[-1].date())
    print("Missing values per ticker:\n", prices.isna().sum(), "\n")
    # Month-end prices. If "ME" raises an error: pip install --upgrade pandas
    return prices.resample("ME").last()


# ----------------------------------------------------------------------------
# Step 4: signal
# ----------------------------------------------------------------------------
def momentum_signal(monthly_prices, lookback=LOOKBACK, skip=SKIP):
    """Return from `lookback` months ago to `skip` months ago, known at month end."""
    return monthly_prices.shift(skip) / monthly_prices.shift(lookback) - 1


# ----------------------------------------------------------------------------
# Step 5: returns with costs
# ----------------------------------------------------------------------------
def run_strategy(monthly_prices):
    rets = monthly_prices.pct_change()
    signal = momentum_signal(monthly_prices).dropna()

    # Equal weight in each asset with a positive signal, remainder in cash (0%).
    # shift(1) is CRUCIAL: the signal at the end of month t is used to hold
    # positions DURING month t+1. Remove it and you get look-ahead bias.
    weights = (signal > 0).astype(float).div(len(TICKERS)).shift(1)

    valid = weights.dropna().index
    rets, weights = rets.loc[valid], weights.loc[valid]

    turnover = weights.diff().abs().sum(axis=1)
    turnover.iloc[0] = weights.iloc[0].abs().sum()  # cost of the initial purchase
    costs = turnover * COST_BPS / 10_000

    gross = (weights * rets).sum(axis=1)
    net = gross - costs
    benchmark = rets.mean(axis=1)  # equal weight, rebalanced monthly, always invested
    return pd.DataFrame(
        {"Strategy (net)": net, "Strategy (gross)": gross, "Buy and hold": benchmark}
    ), turnover


# ----------------------------------------------------------------------------
# Step 6: measure properly
# ----------------------------------------------------------------------------
def metrics(r):
    equity = (1 + r).cumprod()
    years = len(r) / 12
    ann_ret = equity.iloc[-1] ** (1 / years) - 1
    ann_vol = r.std() * np.sqrt(12)
    sharpe = (r.mean() * 12) / ann_vol  # risk-free rate ignored for simplicity
    max_dd = (equity / equity.cummax() - 1).min()
    return pd.Series(
        {
            "Annual return": ann_ret,
            "Annual volatility": ann_vol,
            "Sharpe": sharpe,
            "Max drawdown": max_dd,
        }
    )


def report(results, turnover):
    periods = {
        "FULL PERIOD": results,
        "IN-SAMPLE (before split)": results.loc[:SPLIT_DATE],
        "OUT-OF-SAMPLE (after split)": results.loc[SPLIT_DATE:],
    }
    for name, df in periods.items():
        table = df.apply(metrics).T.round(3)
        print(f"=== {name}: {df.index[0].date()} to {df.index[-1].date()} ===")
        print(table, "\n")
    print(f"Average monthly turnover: {turnover.mean():.2f} "
          f"(1.0 = replacing the whole portfolio)")


def plot(results):
    equity = (1 + results).cumprod()
    ax = equity.plot(figsize=(10, 5), title="Growth of 1 unit")
    ax.axvline(pd.Timestamp(SPLIT_DATE), color="grey", linestyle="--")
    ax.text(pd.Timestamp(SPLIT_DATE), ax.get_ylim()[1] * 0.95, " out-of-sample", color="grey")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig("equity_curve.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    monthly = load_monthly_prices()
    results, turnover = run_strategy(monthly)
    report(results, turnover)
    plot(results)
