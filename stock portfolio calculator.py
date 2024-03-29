import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#### inital parameters ####
invest = 10000
stocks = ['UPRO', 'TMF', 'BMY']
ratios = [0.4, 0.3, 0.3]
## date format: yyyy-mm-dd
start_date = '2018-10-05'
end_date = '2019-02-21'
## price type: 'High', 'Low', 'Open', 'Close'
price_type_buy = 'Close' 
price_type_sell = 'High'
price_type_all = 'High'

###################################################################################
#### calculate the max date range #####
stdates = []
eddates = []
for stname in stocks:
    stock_tmp = yf.Ticker(stname)
    hist_tmp = stock_tmp.history(period = 'max')
    stdates.append(hist_tmp.index[0])
    eddates.append(hist_tmp.index[-1])
std = str(max(stdates))[0:10]
edd = str(min(eddates))[0:10]

#### check the input ####
if len(stocks) != len(ratios):
    raise Exception('Number of stocks must be equal to the number of ratios')
if start_date < std or start_date > edd or end_date < std or end_date > edd:
    raise Exception('The start/end date you input is out of the maximum range of the date (%s to %s).' %(std, edd))
if sum(ratios) != 1:
    raise Exception('The sum of your ratios is not 100%')
    
#### to count the number of days
stock_tmp = yf.Ticker(stocks[0])
hist_tmp1 = stock_tmp.history(start = start_date, end = end_date)

#### a function to calculate final return and daily return for one stock ####
def final_cap(invest, stock_name, ratio, start_date, end_date, price_type_buy, price_type_sell):
    stock = yf.Ticker(stock_name)
    hist = stock.history(start = start_date, end = end_date)
    start_price = hist[price_type_buy][0]
    end_price = hist[price_type_sell][-1]
    all_price = hist[price_type_all]
    init_inv = invest*ratio
    share = init_inv/start_price
    cap_final = end_price*share
    cap_day = all_price*share
    return_one = cap_final - invest*ratio
    return cap_final, cap_day, share, return_one, init_inv

#### calculate final return and daily return for all stocks ####
capfs = []
shares = []
egls = []
init_invs = []
capds = np.zeros([len(stocks), len(hist_tmp1)])
for stname, rt, i in zip(stocks, ratios, range(len(stocks))):
    capf, capd, shr, egl, inv = final_cap(invest = invest, stock_name = stname, ratio = rt, start_date = start_date, \
                    end_date = end_date, price_type_buy = price_type_buy, price_type_sell = price_type_sell)
    capfs.append(capf)
    shares.append(round(shr, 2))
    egls.append(egl)
    init_invs.append(inv)
    capds[i] = capd
    
#### print the summary ####
ratiosp = [rt*100 for rt in ratios]
print('Investment Period: %s to %s' %(start_date, end_date))
print('Maximum Period: %s to %s' %(std, edd))

price_type = [[price_type_buy, price_type_sell, price_type_all]]
pricetp = pd.DataFrame(data = price_type, index = ['Price_Type'], columns = ['Buy', 'Sell', 'Daily'])
print(pricetp)

iinvest = init_invs+[sum(init_invs)]
iratios = ratiosp+[sum(ratios)*100]
fshares = shares+[sum(shares)]
fegls = egls+[sum(egls)]
fcapfs = capfs+[sum(capfs)]
fratios = np.round(fcapfs/sum(capfs), 3)*100
smry_tmp = np.array([iratios, fratios, fshares, iinvest, np.round(fegls, 2), np.round(fcapfs, 2)]).T
smry = pd.DataFrame(data = smry_tmp, index = stocks+['Total'], 
                    columns = ['Init_Prop(%)', 'Final_Prop(%)', 'Init_Shares', 'Init_Cap($)', 'Gain/Loss($)', 'Return($)'])
print(smry)



#### plot daily return ####
fig = go.Figure(data=go.Scatter(x=hist_tmp1.index, y=np.sum(capds, axis = 0), name = 'Daily Total '))
for i in range(len(stocks)):
    fig.add_trace(go.Scatter(x=hist_tmp1.index, y=capds[i], name = stocks[i]))
fig.add_shape(type = 'line', x0=start_date, y0=invest, x1=end_date,y1=invest, line=dict(
                color="LightSeaGreen", width=2, dash="dashdot"))
fig.update_layout(title='Total Daily Return', xaxis_title='Date', yaxis_title='Daily Return ($)')
fig.show()
