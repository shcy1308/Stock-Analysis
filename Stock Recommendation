import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

today = date.today()
stdate = '2020-01-01'
rec_since = '2020-01-01'
eddate = today
stock = yf.Ticker('TMO')
sthist = stock.history(start = stdate, end = eddate)
rec = stock.recommendations
rec1 = rec[rec.index > rec_since]
rec_type = ['Buy', 'Overweight', 'Outperform', 'Market Perform', 'Long-Term Buy', 'Market Outperform', 'Positive', 'Strong Buy']
if type(rec1) != type(None):
    tab = pd.crosstab(index = rec1['To Grade'], columns = 'Count')
    ptab = tab/tab.sum()
    ptab.columns = ['Pctg']
    tab1 = pd.merge(tab, ptab, left_index = True, right_index = True)
    ###### find recommendation ######
    cond = [(rt in rec_type) for rt in list(tab.index)]
    recp = np.sum(cond*ptab['Pctg'])
    print('% recommendation = ', np.round(recp, 4))
    print(tab1)
else:
    print('No Recommendation')
