import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# -------------------- DATA LOADING --------------------
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.dropna(inplace=True)
    data.index = pd.to_datetime(data.index)
    return data


# -------------------- INDICATORS --------------------
def add_indicators(data, short_window=20, long_window=50):
    data["Returns"] = data["Close"].pct_change()
    data["MA_short"] = data["Close"].rolling(short_window).mean()
    data["MA_long"] = data["Close"].rolling(long_window).mean()
    data["Volatility"] = data["Returns"].rolling(20).std()
    return data


# -------------------- SIGNAL GENERATION --------------------
def generate_signals(data):
    data["Signal"] = 0
    data.loc[data["MA_short"] > data["MA_long"], "Signal"] = 1
    data.loc[data["MA_short"] < data["MA_long"], "Signal"] = -1
    return data


# -------------------- BACKTEST --------------------
def backtest_strategy(data, cost=0.005):
    data["Strategy Returns"] = data["Signal"].shift(1) * data["Returns"]

    trades = data["Signal"].diff().abs()
    data["Strategy Returns"] -= trades * cost

    data["Cumulative Market"] = (1 + data["Returns"]).cumprod()
    data["Cumulative Strategy"] = (1 + data["Strategy Returns"]).cumprod()

    return data


# -------------------- PERFORMANCE METRICS --------------------
def performance_metrics(data):
    std = data["Strategy Returns"].std()

    if std == 0 or np.isnan(std):
      sharpe = 0
    else:
      sharpe = (data["Strategy Returns"].mean() / std) * (252 ** 0.5)

    cum = data["Cumulative Strategy"]
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    max_drawdown = drawdown.min()

    total_returns = data["Cumulative Strategy"].iloc[-1] - 1
    market_returns = data["Cumulative Market"].iloc[-1] - 1

    metrics = {
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown,
        "Total Returns": total_returns,
        "Market Returns": market_returns
    }

    return metrics


# -------------------- OPTIMIZATION --------------------
def optimize_strategy(data):
    results = []

    for short in [20, 50, 100]:
        for long in [50, 100, 200]:

            df = data.copy()
            df = add_indicators(df, short, long)
            df = generate_signals(df)
            df = backtest_strategy(df)

            sharpe = (df["Strategy Returns"].mean() /
                      df["Strategy Returns"].std()) * (252 ** 0.5)

            results.append([short, long, sharpe])

    results_df = pd.DataFrame(
        results,
        columns=["Short MA", "Long MA", "Sharpe"]
    )

    return results_df.sort_values(by="Sharpe", ascending=False)


# -------------------- PLOTTING --------------------
def plot_results(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data["Close"], label="Price")
    plt.plot(data["MA_short"], label="MA Short")
    plt.plot(data["MA_long"], label="MA Long")
    plt.legend()
    plt.title(f"{ticker} Prices vs Moving Averages")
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(data["Cumulative Strategy"], label="MA Strategy")
    plt.plot(data["Cumulative Market"], label="Buy and Hold")
    plt.legend()
    plt.title(f"{ticker} Strategy vs Market")
    plt.show()


# -------------------- SINGLE STOCK RUN --------------------
def run_single_stock(ticker):
    data = load_data(ticker, "2024-01-01", "2026-02-16")
    data = add_indicators(data)
    data = generate_signals(data)
    data = backtest_strategy(data)

    metrics = performance_metrics(data)

    print(f"\nPerformance for {ticker}")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    plot_results(data, ticker)

    data.to_csv(f"{ticker}_result.csv")
    return data


# -------------------- MULTI STOCK PORTFOLIO --------------------
def run_multiple_stocks(tickers):
    portfolio_results = []

    for ticker in tickers:
        data = load_data(ticker, "2024-01-01", "2026-02-16")
        data = add_indicators(data)
        data = generate_signals(data)
        data = backtest_strategy(data)

        metrics = performance_metrics(data)
        metrics["Ticker"] = ticker

        portfolio_results.append(metrics)

    return pd.DataFrame(portfolio_results)


# -------------------- MAIN EXECUTION --------------------
if __name__ == "__main__":

    # Single stock analysis
    run_single_stock("ADANIPOWER.NS")

    # Portfolio analysis
    tickers = ["INFY.NS", "RELIANCE.NS", "TCS.NS","ACC.NS","ATGL.NS","BANKBARODA.NS","CESC.NS","CONCOR.NS"]
    portfolio_df = run_multiple_stocks(tickers)

    print("\nPortfolio Analysis")
    print(portfolio_df)

    portfolio_df.to_csv("portfolio_performance.csv")

    # Optimization
    base_data = load_data("ADANIPOWER.NS", "2024-01-01", "2026-02-16")
    optimization_results = optimize_strategy(base_data)

    print("\nOptimization Results")
    print(optimization_results)

    optimization_results.to_csv("optimization_results.csv")
