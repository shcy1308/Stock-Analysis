import yfinance as yf
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/sp500.csv')

tickers = sp500
pegratios = []

for sk in tickers['Symbol']:
  stock = yf.Ticker(sk)
  pegr = stock.info['pegRatio']
  pegratios.append(pegr)

pegrs = pd.concat([tickers, pd.DataFrame(pegratios)], axis = 1)
pegrs.to_csv('C:/CShi/pegrs.csv')
