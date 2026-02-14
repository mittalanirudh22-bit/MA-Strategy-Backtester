# MA-Strategy-Backtester
Moving average crossover backtest on NSE stock using Python

## Objective
Test a simple MA crossover trading strategy using Python.

## Data
Stock: INFY (NSE)
Source: yfinance
Period: 2024–2026

## Strategy Logic
- Buy when MA20 > MA50
- Sell when MA20 < MA50

## Metrics
Sharpe Ratio: 0.79  
Max Drawdown: -16.8%  
Strategy Return: 34%  
Market Return: 10%  

## Result
Strategy outperformed buy-and-hold with moderate risk.

## Tools Used
Python, pandas, numpy, matplotlib, yfinance
