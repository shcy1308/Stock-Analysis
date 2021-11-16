import yfinance as yf
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from pytickersymbols import PyTickerSymbols

#stock_data = PyTickerSymbols()
#us_stocks = stock_data.get_stocks_by_index('S&P 500')
#pd.DataFrame(list(us_stocks))

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/sp500.csv')

######### start and end time
stdate = '2021-11-01'
eddate = date.today()

######### price increase
def high_inc(tickers, stdate, eddate, headn):
  incrs = []
  for sk in tickers['Symbol']:
      stock = yf.Ticker(sk)
      skhist = stock.history(start = stdate, end = eddate)
      incr = (skhist['Low'][-1] - skhist["High"][0])/skhist["High"][0]
      incrs.append(incr)
  pincrs = pd.concat([tickers, pd.DataFrame(incrs)], axis = 1)
  pincrs = pincrs.rename(columns = {0: 'Inc'})
  princs_sort = pincrs.sort_values(by = 'Inc', ascending = False)
  
  return princs_sort.head(headn)

### highy increased stocks in sp500
sp500_incs = high_inc(tickers = sp500, stdate = stdate, eddate = eddate, headn = 600)
sp500_incs
sp500_incs.to_csv("C:/CShi/sp500_incs.csv")

### highy increased stocks in nasdaq100
nq100_incs = high_inc(tickers = nq100, stdate = stdate, eddate = eddate, headn = 600)
nq100_incs
nq100_incs.to_csv("C:/CShi/nq100_incs.csv")

allhighincs = pd.concat([sp500_incs, nq100_incs], axis = 0)
allhighincs_sort = allhighincs.sort_values(by = 'Inc', ascending = False)
allhighincs_sort
allhighincs_sort.to_csv("C:/CShi/all_incs.csv")
