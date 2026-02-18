🚀 Live App:
https://ma-strategy-backtester-j7qmj33hfprtrbvftgm988.streamlit.app/

# MA-Strategy-Backtester

Moving Average Crossover Backtesting System for NSE stocks using Python.  
This project tests, evaluates, and optimizes a trend-following strategy using historical market data.

---

## Objective

- Implement a moving average crossover trading strategy  
- Backtest performance on NSE stocks  
- Evaluate risk metrics (Sharpe, drawdown, returns)  
- Compare with buy-and-hold  
- Run portfolio-level analysis  
- Optimize MA parameter combinations  

---

## Features

- Historical data download using Yahoo Finance  
- Short & long moving averages  
- Trading signal generation  
- Strategy backtesting with transaction costs  
- Performance metrics calculation:
  - Sharpe Ratio
  - Max Drawdown
  - Total Returns
  - Market Returns
- Portfolio backtesting (multiple stocks)  
- Parameter optimization (MA combinations)  
- Visualization of:
  - Price + MAs
  - Strategy vs Market equity curve  
- CSV export for analysis

- 📈 Interactive Streamlit dashboard
- 📊 Moving average crossover strategy
- ⚙️ Adjustable MA parameters
- 📉 Risk metrics: Sharpe ratio, drawdown, returns
- 🧠 Strategy vs buy-and-hold comparison
- 🔍 Portfolio and optimization support
- 🌐 Live deployed web application


---

## Tech Stack

- Python  
- pandas  
- numpy  
- matplotlib  
- yfinance  

---

## Strategy Logic

1. Calculate short and long moving averages  
2. Generate signals:
   - Buy → Short MA > Long MA  
   - Sell → Short MA < Long MA  
3. Apply transaction cost on signal change  
4. Compute:
   - Strategy returns  
   - Market returns  
5. Evaluate performance metrics  






