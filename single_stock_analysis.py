import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

######################## financial analysis ####################
stock = yf.Ticker("adbe")
unit = 'year'

if unit == 'quart':
  fin = stock.quarterly_financials
  bs = stock.quarterly_balance_sheet
elif unit == 'year':
  fin = stock.financials
  bs = stock.balance_sheet

if(fin.shape[0] == 0):
    print('Invalid Ticker')
else:
    ## gross
    rev_total = fin.loc['Total Revenue', :]
    rev_cost = fin.loc['Cost Of Revenue', :]
    gross_pchg = [round((rev_total[i]-rev_total[i+1])/rev_total[i+1], 3) for i in range(len(rev_total)-1)]+[0]
    gross_pchg = pd.DataFrame(gross_pchg)
    gross_pchg.index = rev_total.index
  
    ## gross marging
    gmargin = (rev_total-rev_cost)/rev_total
    gmargin_pchg = [round((gmargin[i]-gmargin[i+1])/gmargin[i+1], 3) for i in range(len(gmargin)-1)]+[0]
    gmargin_pchg = pd.DataFrame(gmargin_pchg)
    gmargin_pchg.index = gmargin.index
    
    gross_smry = pd.concat([rev_total, gross_pchg, gmargin, gmargin_pchg], axis = 1)
    gross_smry.columns = ['Gross', 'G_PCHG', 'G_Margin', 'GM_PCHG']
    
    ## PB ratio 
    pb_ratio = stock.info['marketCap']/bs.loc['Net Tangible Assets', :][0]

    ## Ratio of totoal liab and total asset
    lia_ast = bs.loc['Total Liab', :]/bs.loc['Total Assets', :]

    ## Ratio of current totoal liab and current total asset
    lia_ast_cur = bs.loc['Total Current Liabilities', :]/bs.loc['Total Current Assets', :]
    
    ## cash/liab
    cash_lia_cur = bs.loc['Cash', :]/bs.loc['Total Current Liabilities', :]
    cash_lia = bs.loc['Cash', :]/bs.loc['Total Liab', :]
    
    ## (cash+short_term_invest)/laib
    if 'Short Term Investments' in bs.index:
        cain_lia_cur = (bs.loc['Cash', :] + bs.loc['Short Term Investments',:])/bs.loc['Total Current Liabilities', :]
        cain_lia = (bs.loc['Cash', :] + bs.loc['Short Term Investments',:])/bs.loc['Total Liab', :]
    else:
        cain_lia_cur = cash_lia_cur
        cain_lia = cash_lia 
    
    dfasset = [lia_ast_cur, lia_ast, cash_lia_cur, cash_lia, cain_lia_cur, cain_lia]
    asset_smry = pd.DataFrame(dfasset).T
    asset_smry.columns = ['Cur_L/A', 'Tot_L/A', 'Cur_C/L', 'Tot_C/L', 'Cur_CI/L', 'Tot_CI/L']
    
    print(gross_smry)
    print(round(pb_ratio, 3))
    print(round(asset_smry, 3))
    print(stock.info['pegRatio'])
  
################ basic info #####################
variables = ['revenueGrowth', 'targetLowPrice', 'targetMedianPrice', \
'targetHighPrice', 'forwardPE', 'priceToBook', 'pegRatio', 'beta', \
'recommendationKey']

skinfo = stock.info
info = list(map(skinfo.get, variables))
basic_info = pd.DataFrame(info)
basic_info.index = variables
basic_info

############### price range ####################
ticker = 'adbe'

stdate = '2017-01-01'
#eddate = '2019-06-30'
eddate = dt.datetime.today()

stock = yf.Ticker(ticker)
skhist = stock.history(start = stdate, end = eddate)
skhigh = skhist['High']
sklow = skhist['Low']
skclose = skhist['Close']
dates = skhist.index

time = np.array((dates - dates[0])/np.timedelta64(1, 'D')).reshape(-1, 1)

reg_high = LinearRegression().fit(time, skhigh)
pred_high = reg_high.predict(time)

reg_low = LinearRegression().fit(time, sklow)
pred_low = reg_low.predict(time)

plt.plot(time, pred_high)
plt.plot(time, pred_low)
plt.plot(time, skclose)
plt.legend(['High', 'Low', 'Close'])
plt.show()

##################### historical PE ratio #####################
## eps
ticker = 'adbe'
stock = yf.Ticker(ticker)
earning_tmp1 = si.get_earnings_history(ticker)
earning_tmp2 = pd.DataFrame(earning_tmp1)
earning = earning_tmp2[earning_tmp2['startdatetimetype'] != 'TAS']

# actual earning
earn_act = earning.dropna()

# actual eps date
earntime = list(earn_act['startdatetime'].str[:10])

# price on actual earning date
price_cls = []
for i in range(len(earntime)):
  skprice = stock.history(start = dt.date.fromisoformat(earntime[i])-dt.timedelta(days = 30), end = earntime[i])
  price_cl = np.mean(skprice['Close'])
  price_cls.append(price_cl)

# actual eps
eps_act = earn_act['epsactual']

# actual ttm eps
eps_ttms = [np.sum(eps_act[i:(i+4)]) for i in range(0, len(eps_act)-3)]

# pe ratios
pers = np.array(price_aves[0:-3])/np.array(eps_ttms)
pers

plt.plot(earntime, price_cls)
plt.plot(pers)
plt.xticks(rotation = 90)
plt.legend(['Price', 'PER'])
plt.show()

summary = pd.DataFrame([earntime, price_cls, pers]).T
summary
