import yfinance as yf
import pandas as pd
import numpy as np

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/Stock-Analysis/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/Stock-Analysis/sp500.csv')

variables = ['revenueGrowth', 'targetLowPrice', 'targetMedianPrice', 'targetHighPrice', 'forwardPE', 'priceToBook', 'pegRatio', 'beta', 'recommendationKey']

tickers = sp500

infos = []
for sk in tickers['Symbol']:
  stock = yf.Ticker(sk)
  skinfo = stock.info
  info = list(map(skinfo.get, variables))
  infos.append(info)
  
basic_infos = pd.DataFrame(infos)
basic_infos.columns = variables
stock_infos = pd.concat([tickers, basic_infos], axis = 1)
stock_infos.to_csv('C:/CShi/stock_infos.csv')

