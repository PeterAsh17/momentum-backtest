# Project Log

## 2026-11-10
- Done: set up GitHub, Git, Python and VS Code. Ran the first 12-1 momentum backtest on SPY, EWU, TLT and GLD.
- Problems: TLT download failed ("database is locked") and ISF.L had too little history.
- Decisions: replaced ISF.L with EWU for data availability. This was decided before seeing any results. Set the split date at 2017-01-01 and the lookback at 12 months in advance.
- Next: write the README hypothesis, read the results tables, plan the out-of-sample test.