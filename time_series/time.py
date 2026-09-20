"""
Time Series + Statistics + Trading Quant — Hands-on Examples
==============================================================
Every topic from your roadmap, demonstrated with code on synthetic
OHLCV data (built to look like XAUUSD daily candles).

Run section by section (copy into a Jupyter notebook / VS Code
interactive window) or run the whole file top to bottom.
"""

import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)

# --------------------------------------------------------------------
# SETUP: synthetic daily OHLCV data (random walk, looks like gold price)
# --------------------------------------------------------------------
np.random.seed(42)
n_days = 500
dates = pd.date_range(start="2023-01-01", periods=n_days, freq="D")

returns = np.random.normal(loc=0.0003, scale=0.01, size=n_days)  # daily log-returns
close = 1900 * np.exp(np.cumsum(returns))  # start near 1900 (like XAUUSD)

df = pd.DataFrame({
    "date": dates,
    "close": close,
})
df["open"] = df["close"].shift(1).fillna(df["close"][0]) * (1 + np.random.normal(0, 0.001, n_days))
df["high"] = df[["open", "close"]].max(axis=1) * (1 + np.abs(np.random.normal(0, 0.002, n_days)))
df["low"] = df[["open", "close"]].min(axis=1) * (1 - np.abs(np.random.normal(0, 0.002, n_days)))
df["volume"] = np.random.randint(1000, 10000, n_days)

print("=" * 70)
print("SETUP: sample data")
print("=" * 70)
print(df.head())



# PART 1 — TIME SERIES


# ---- Phase A: Foundation ----------------------------------------------

# 2. Timestamp / DateTime
df["date"] = pd.to_datetime(df["date"])
print("\n[2] dtype after to_datetime:", df["date"].dtype)

# 3. Extract Year / Month / Day
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
print("\n[3] Year/Month/Day columns:\n", df[["date", "year", "month", "day"]].head(3))

# 4. Time-based indexing
ts = df.set_index("date")
print("\n[4] Slice Feb 2023 by date:\n", ts.loc["2023-02-01":"2023-02-05", "close"])

# 5. Resampling (D -> W -> M)
weekly = ts["close"].resample("W").mean()
monthly = ts["close"].resample("ME").mean()
print("\n[5] Weekly resample (first 3):\n", weekly.head(3))
print("[5] Monthly resample (first 3):\n", monthly.head(3))


# ---- Phase B: Analysis -------------------------------------------------

# 6. Percentage Change / Return
ts["pct_change"] = ts["close"].pct_change()
print("\n[6] Daily % change:\n", ts["pct_change"].head(5))

# 7. Rolling Window (generic — window of 20 days)
rolling_20 = ts["close"].rolling(window=20)
print("\n[7] Rolling(20) mean (first 3 valid):\n", rolling_20.mean().dropna().head(3))

# 8. Moving Average (SMA + EMA)
ts["sma_20"] = ts["close"].rolling(window=20).mean()
ts["ema_20"] = ts["close"].ewm(span=20, adjust=False).mean()
print("\n[8] SMA20 vs EMA20 (tail):\n", ts[["close", "sma_20", "ema_20"]].tail(3))

# 9. Lag / Shift
ts["close_lag1"] = ts["close"].shift(1)
print("\n[9] close vs close_lag1:\n", ts[["close", "close_lag1"]].head(3))

# 10. Cumulative Return
ts["cum_return"] = (1 + ts["pct_change"]).cumprod() - 1
print("\n[10] Cumulative return so far (last value):", round(ts["cum_return"].iloc[-1] * 100, 2), "%")

# 11. Trend (simple: is price above its own 50-day SMA?)
ts["sma_50"] = ts["close"].rolling(50).mean()
ts["trend"] = np.where(ts["close"] > ts["sma_50"], "uptrend", "downtrend")
print("\n[11] Trend label (tail):\n", ts[["close", "sma_50", "trend"]].tail(3))

# 12. Volatility (rolling std of returns, annualized)
ts["volatility_20d"] = ts["pct_change"].rolling(20).std()
ts["volatility_annualized"] = ts["volatility_20d"] * np.sqrt(252)
print("\n[12] 20d volatility (annualized, tail):\n", ts["volatility_annualized"].tail(3))


# ---- Phase C: Time Series for ML ---------------------------------------

# 13. Autocorrelation (basic) — is today's return related to yesterday's?
autocorr_lag1 = ts["pct_change"].autocorr(lag=1)
print("\n[13] Autocorrelation (lag 1) of returns:", round(autocorr_lag1, 4))

# 14. Stationarity (basic) — check with Augmented Dickey-Fuller if available,
#     else fallback to a simple rolling-mean/variance stability check.
try:
    from statsmodels.tsa.stattools import adfuller
    adf_result = adfuller(ts["close"].dropna())
    print("\n[14] ADF test on price -> p-value:", round(adf_result[1], 4),
          "(p > 0.05 usually means NOT stationary)")
    adf_result_returns = adfuller(ts["pct_change"].dropna())
    print("[14] ADF test on returns -> p-value:", round(adf_result_returns[1], 4),
          "(returns are usually stationary, price usually isn't)")
except ImportError:
    print("\n[14] statsmodels not installed — quick manual check instead:")
    first_half_std = ts["close"].iloc[:n_days // 2].std()
    second_half_std = ts["close"].iloc[n_days // 2:].std()
    print("     std(first half):", round(first_half_std, 2), "| std(second half):", round(second_half_std, 2))
    print("     Big difference => likely non-stationary (raw price series usually is).")

# 15. Time-based Train/Test Split (NEVER random split for time series)
split_point = int(n_days * 0.8)
train = ts.iloc[:split_point]
test = ts.iloc[split_point:]
print("\n[15] Train range:", train.index.min().date(), "->", train.index.max().date())
print("     Test range:", test.index.min().date(), "->", test.index.max().date())

# 16. Forecasting concept — naive baseline forecast (tomorrow = today)
ts["naive_forecast"] = ts["close"].shift(1)
naive_mae = (ts["close"] - ts["naive_forecast"]).abs().mean()
print("\n[16] Naive forecast MAE (baseline every model should beat):", round(naive_mae, 2))

# 17. Data Leakage example — WRONG vs RIGHT way to scale/feature-engineer
wrong_mean = ts["close"].mean()  # uses full dataset including future -> LEAKAGE
right_mean_train_only = train["close"].mean()  # only past data -> CORRECT
print("\n[17] Leakage demo — mean using ALL data (wrong):", round(wrong_mean, 2))
print("     Mean using TRAIN only (correct):", round(right_mean_train_only, 2))
print("     Any feature/scaler must be fit on train only, then applied to test.")


# ======================================================================
# PART 2 — STATISTICS
# ======================================================================

prices = ts["close"]
rets = ts["pct_change"].dropna()

# 1. Mean
print("\n[Stat 1] Mean price:", round(prices.mean(), 2))

# 2. Median
print("[Stat 2] Median price:", round(prices.median(), 2))

# 3. Percentile
print("[Stat 3] 90th percentile price:", round(prices.quantile(0.90), 2))

# 4. Variance
print("[Stat 4] Variance of returns:", round(rets.var(), 6))

# 5. Standard Deviation
print("[Stat 5] Std dev of returns:", round(rets.std(), 6))

# 6. Distribution (basic) — skew and kurtosis tell the shape
print("[Stat 6] Skew:", round(rets.skew(), 3), "| Kurtosis:", round(rets.kurt(), 3))

# 7. Outlier detection (basic z-score method)
z_scores = (rets - rets.mean()) / rets.std()
outliers = rets[z_scores.abs() > 3]
print("[Stat 7] Number of outlier days (|z| > 3):", len(outliers))

# ---- Relationship ----

btc_like = 30000 * np.exp(np.cumsum(np.random.normal(0.0006, 0.02, n_days)))
df2 = pd.DataFrame({"gold": prices.values, "btc": btc_like}, index=prices.index)
gold_ret = df2["gold"].pct_change().dropna()
btc_ret = df2["btc"].pct_change().dropna()

# 8. Covariance
print("\n[Stat 8] Covariance (gold vs btc returns):", round(gold_ret.cov(btc_ret), 8))

# 9. Correlation
print("[Stat 9] Correlation (gold vs btc returns):", round(gold_ret.corr(btc_ret), 4))

# 10. Correlation vs Causation — just a reminder printed, no test for this
print("[Stat 10] Correlation != Causation: two assets moving together doesn't mean one causes the other")
print("          (both could be driven by a third factor, e.g. USD strength / macro conditions)")

# ---- Trading Quant ----

# 11. Return (simple)
total_return_pct = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
print("\n[Quant 11] Total simple return over period:", round(total_return_pct, 2), "%")

# 12. Log Return (basic)
log_returns = np.log(prices / prices.shift(1)).dropna()
print("[Quant 12] Mean daily log return:", round(log_returns.mean(), 6))

# 13. Volatility (annualized, from log returns — standard in quant finance)
annual_vol = log_returns.std() * np.sqrt(252)
print("[Quant 13] Annualized volatility:", round(annual_vol * 100, 2), "%")

# 14. Risk / Reward (example single trade)
entry, stop_loss, take_profit = 1950, 1935, 1995
risk = entry - stop_loss
reward = take_profit - entry
print("[Quant 14] Risk/Reward ratio:", round(reward / risk, 2))

# 15. Drawdown
cum_returns = (1 + ts["pct_change"].fillna(0)).cumprod()
running_max = cum_returns.cummax()
drawdown = (cum_returns - running_max) / running_max
print("[Quant 15] Max drawdown:", round(drawdown.min() * 100, 2), "%")

# 16. Win Rate (simulate 50 trades)
np.random.seed(1)
trade_results = np.random.choice([1, -1], size=50, p=[0.55, 0.45])  # 1=win, -1=loss
win_rate = (trade_results == 1).mean()
print("[Quant 16] Win rate (simulated 50 trades):", round(win_rate * 100, 1), "%")

# 17. Expectancy — needs avg win size and avg loss size
avg_win = 1.5   # e.g. avg win = 1.5R
avg_loss = 1.0  # e.g. avg loss = 1R
expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
print("[Quant 17] Expectancy per trade:", round(expectancy, 3), "R")

# 18. Sharpe Ratio (basic, assuming 0% risk-free rate)
sharpe = (log_returns.mean() / log_returns.std()) * np.sqrt(252)
print("[Quant 18] Annualized Sharpe ratio:", round(sharpe, 2))

# 19. Z-Score (basic) — how far is today's price from its own recent mean?
recent_mean = prices.rolling(20).mean().iloc[-1]
recent_std = prices.rolling(20).std().iloc[-1]
current_z = (prices.iloc[-1] - recent_mean) / recent_std
print("[Quant 19] Current price Z-score (vs last 20d):", round(current_z, 2))

# 20. Probability (basic) — probability of a positive-return day, empirically
prob_up_day = (rets > 0).mean()
print("[Quant 20] Empirical probability of an up-day:", round(prob_up_day * 100, 1), "%")

print("\n" + "=" * 70)
print("Done. Every number above is a *concept demo* — swap the synthetic")
print("`close` series for real XAUUSD/BTC OHLCV data and everything runs the same.")
print("=" * 70)