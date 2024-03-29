import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import sdeint 

#### get the stock price data ####
today = date.today()
stdate = '2020-04-01'
eddate = today
voo = yf.Ticker("ARKK")
phist = voo.history(start = stdate, end = eddate)
popen = phist['Open']
pclose = phist['Close']
dr = pclose - popen
drp = dr/popen

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_title('% of Daily Return')
ax2.set_title('Daily Return')
ax1.hist(drp[:(len(drp)-1)])
ax2.hist(dr[:(len(drp)-1)])
plt.show()

#### model with sde ####
nyear = 2
mus = [np.log(pclose[i]/pclose[i-1]) for i in range(1, len(pclose))]
mu = np.mean(mus)*252
sigma = np.sqrt(np.var(mus)*252)
tspan = np.arange(0, nyear, nyear/(nyear*252))
x0 = pclose[0]

def f(x, t):
    return mu*x

def g(x, t):
    return sigma*x

relast = np.array([])
for i in range(100):
    result = sdeint.itoint(f, g, x0, tspan)
    relast = np.concatenate((relast, result[-1]), axis = None)
    plt.plot(result, color='blue')
plt.show()

#### predict the gain ####
rho = 2
pcurrent = pclose[-1]
print('current price:', np.round(pcurrent, decimals=2))
print('investment years:', nyear)
print('Prob to gain >', str(round((rho-1)*100))+'%:',  np.mean(relast > rho*pcurrent))
