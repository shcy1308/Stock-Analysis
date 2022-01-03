import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt

## eps
ticker = 'ko'
stock = yf.Ticker(ticker)
earning_tmp1 = si.get_earnings_history(ticker)
earning_tmp2 = pd.DataFrame(earning_tmp1)
earning = earning_tmp2[earning_tmp2['startdatetimetype'] != 'TAS']

# actual earning
earn_act = earning.dropna()

# actual eps date
earntime = list(earn_act['startdatetime'].str[:10])

# price on actual earning date
price_aves = []
for i in range(len(earntime)):
  skprice = stock.history(start = dt.date.fromisoformat(earntime[i])-dt.timedelta(days = 30), end = earntime[i])
  price_ave = np.mean((skprice['Open']+skprice['Close'])/2)
  price_aves.append(price_ave)

# actual eps
eps_act = earn_act['epsactual']

# actual ttm eps
eps_ttms = [np.sum(eps_act[i:(i+4)]) for i in range(0, len(eps_act)-3)]

# pe ratios
pers = np.array(price_aves[0:-3])/np.array(eps_ttms)
pers

plt.plot(earntime, price_aves)
plt.plot(pers)
plt.xticks(rotation = 90)

plt.show()

summary = pd.DataFrame([earntime, price_aves, pers]).T
summary
