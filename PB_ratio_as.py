import yfinance as yf
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/sp500.csv')

tickers = nq100
ratios = []
for sk in tickers['Symbol']:
  stock = yf.Ticker(sk)
  bs = stock.quarterly_balance_sheet
  ratio = stock.info['marketCap']/(bs.loc['Total Assets', :][0]-bs.loc['Total Liab', :][0])
  ratios.append(ratio)

mcr = pd.concat([tickers, pd.DataFrame(ratios)], axis = 1)
mcr.to_csv('C:/CShi/mcr.csv')
np.mean(ratios)

np.median(ratios)

len(ratios)
len(tickers['Symbol'][:20])
