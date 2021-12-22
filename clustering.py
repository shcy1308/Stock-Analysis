import yfinance as yf
import numpy as np
from sklearn.cluster import KMeans
from datetime import date
import pandas as pd

########## read nasdaq 100 tickers
nq100 = pd.read_csv('C:/CShi/nasdaq100.csv')

########## read sp500 tickers
sp500 = pd.read_csv('C:/CShi/sp500.csv')

tickers = sp500

stdate = '2021-11-01'
eddate = date.today()

drs = None
for st in tickers['Symbol']:
  stock = yf.Ticker(st)
  price = stock.history(start = stdate, end = eddate)
  dr = (price['Close'] - price['Open'])/price['Open']
  drs = pd.concat([drs, dr], axis = 1)

dfdr = drs.T

kmeans = KMeans(n_clusters = 50, random_state = 0).fit(dfdr.iloc[:,:13])
labels = pd.DataFrame(kmeans.labels_)
stclst = pd.concat([tickers, labels], axis = 1)
stclst.to_csv('C:/CShi/stclst.csv')
