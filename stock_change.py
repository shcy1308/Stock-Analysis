import yfinance as yf
import pandas as pd
from datetime import date
import numpy as np

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/Stock-Analysis/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/Stock-Analysis/sp500.csv')

######### start and end time
stdate = '2017-01-01'
eddate = '2019-12-31'

######### price increase
def inc_pcnt(tickers, stdate, eddate):
  incrs = []
  for sk in tickers['Symbol']:
      stock = yf.Ticker(sk)
      skhist = stock.history(start = stdate, end = eddate)
      skhist = skhist.dropna()
      if skhist.shape[0] != 0:
        incr = (skhist['Low'][-1] - skhist["High"][0])/skhist["High"][0]
      else:
        incr = None
      incrs.append(incr)
      
  pincrs = pd.concat([tickers, pd.DataFrame(incrs)], axis = 1)
  pincrs = pincrs.rename(columns = {0: 'Inc'})
  princs_sort = pincrs.sort_values(by = 'Inc', ascending = False)
  
  return princs_sort

### highy increased stocks in sp500
sp500_incs = inc_pcnt(tickers = sp500, stdate = stdate, eddate = eddate)
sp500_incs
sp500_incs.to_csv("C:/CShi/sp500_incs.csv")

### highy increased stocks in nasdaq100
nq100_incs = inc_pcnt(tickers = nq100, stdate = stdate, eddate = eddate)
nq100_incs
nq100_incs.to_csv("C:/CShi/nq100_incs.csv")

allhighincs = pd.concat([sp500_incs, nq100_incs], axis = 0)
allhighincs_sort = allhighincs.sort_values(by = 'Inc', ascending = False)
allhighincs_sort
allhighincs_sort.to_csv("C:/CShi/all_incs.csv")

########################## VOO and QQQ #############################
indeces = pd.DataFrame(['voo', 'qqq'])
indeces.columns = ['Symbol']
inc_pcnt(tickers = indeces, stdate = stdate, eddate = eddate)

