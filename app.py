import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Quant Backtesting Dashboard", layout="wide")

st.title("📈 Algorithmic Trading Backtesting Dashboard")


def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.dropna(inplace=True)
    return data


def add_indicators(data, short_window=20, long_window=50):
    data["Returns"] = data["Close"].pct_change()
    data["MA_short"] = data["Close"].rolling(short_window).mean()
    data["MA_long"] = data["Close"].rolling(long_window).mean()
    data.dropna(inplace=True)
    return data


def generate_signals(data):
    data["Signal"] = 0
    data.loc[data["MA_short"] > data["MA_long"], "Signal"] = 1
    data.loc[data["MA_short"] < data["MA_long"], "Signal"] = -1
    return data


def backtest_strategy(data):
    data["Strategy Returns"] = data["Signal"].shift(1) * data["Returns"]
    data.dropna(inplace=True)

    data["Cumulative Market"] = (1 + data["Returns"]).cumprod()
    data["Cumulative Strategy"] = (1 + data["Strategy Returns"]).cumprod()

    return data


def performance_metrics(data):
    std = data["Strategy Returns"].std()

    if std == 0 or np.isnan(std):
        sharpe = 0
    else:
        sharpe = (data["Strategy Returns"].mean() / std) * (252 ** 0.5)

    cum = data["Cumulative Strategy"]
    peak = cum.cummax()
    drawdown = (cum - peak) / peak

    return {
        "Sharpe": sharpe,
        "Max Drawdown": drawdown.min(),
        "Total Returns": cum.iloc[-1] - 1,
        "Market Returns": data["Cumulative Market"].iloc[-1] - 1
    }


st.subheader("Select Stock")

option = st.radio("Choose input method:", ["Dropdown", "Custom ticker"])

if option == "Dropdown":
    ticker = st.selectbox(
        "Select Stock",
        ["ADANIPOWER.NS", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
    )
else:
    ticker = st.text_input("Enter custom ticker (example: GODIGIT.NS)", "ADANIPOWER.NS")

short_ma = st.slider("Short MA", 10, 100, 20)
long_ma = st.slider("Long MA", 50, 200, 50)

if st.button("Run Backtest"):

    data = load_data(ticker, "2023-01-01", "2026-02-16")
    data = add_indicators(data, short_ma, long_ma)
    data = generate_signals(data)
    data = backtest_strategy(data)

    metrics = performance_metrics(data)


    st.subheader("📊 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sharpe Ratio", round(metrics["Sharpe"], 2))
    col2.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
    col3.metric("Strategy Returns", f"{metrics['Total Returns']:.2%}")
    col4.metric("Market Returns", f"{metrics['Market Returns']:.2%}")

  
    st.subheader("Price & Moving Averages")

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(data["Close"], label="Price")
    ax.plot(data["MA_short"], label="Short MA")
    ax.plot(data["MA_long"], label="Long MA")
    ax.legend()
    st.pyplot(fig)

  
    st.subheader("Strategy vs Market Performance")

    fig2, ax2 = plt.subplots(figsize=(12,6))
    ax2.plot(data["Cumulative Strategy"], label="Strategy")
    ax2.plot(data["Cumulative Market"], label="Market")
    ax2.legend()
    st.pyplot(fig2)

