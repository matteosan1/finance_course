from datetime import date
from dateutil.relativedelta import relativedelta
import ois_data
import finmarkets
import numpy as np

from historical_data import stock1, stock2
assert len(stock1) == len(stock2), 'The 2 stocks have not the same n° of observations'

returns_stock_1 = []
returns_stock_2 = []

i=0
while i < len(stock1)-1:
    # perchè -1 ?
    #returns_stock_1.append(stock1[i+1] / stock1[i] - 1)
    #returns_stock_2.append(stock2[i+1] / stock2[i] - 1)
    returns_stock_1.append(stock1[i+1] / stock1[i])
    returns_stock_2.append(stock2[i+1] / stock2[i])
    i+=1

PTF_n_stocks_A = 100
PTF_n_stocks_B = 50
#PTF_tot_stocks = PTF_n_stocks_A + PTF_n_stocks_B
#PTF_weight_A = PTF_n_stocks_A / PTF_tot_stocks
#PTF_weight_B = PTF_n_stocks_B / PTF_tot_stocks

# a questo punto devi trovare la distribuzione delle variazioni a 1 giorno del valore del portafoglio
returns_PTF = []
PTF_today = PTF_n_stocks_A * stock1[-1] + PTF_n_stocks_B * stock2[-1]
i=0
while i < len(returns_stock_1):
    #weighted_return = PTF_weight_A * returns_stock_1[i] + PTF_weight_B * returns_stock_2[i]
    PTF_tomorrow = PTF_n_stocks_A * stock1[-1] * returns_stock_1[i] + PTF_n_stocks_B * stock2[-1] * returns_stock_2[i]
    #returns_PTF.append(weighted_return)
    returns_PTF.append(PTF_tomorrow - PTF_today)
    i+=1
'''
print ('returns_PTF: ', returns_PTF)
RETURNS_PTF = np.array(returns_PTF)
print ('RETURNS_PTF: ', RETURNS_PTF)
np.sort(RETURNS_PTF)
print ('RETURNS_PTF SORTED: ', RETURNS_PTF)
'''
#returns_PTF.sort(reverse=True)

percentile = np.percentile(returns_PTF,5)

N_days = 5
N_day_VAR = percentile * (N_days**(0.5))
#print('(1) 5 days VAR: ', round(percentile, 4) ,"%")
print('5 days VAR: ', round(N_day_VAR, 4) ,"%")

########### EX 2 ###########
position_1 = 500000
position_2 = 750000
sigma_1 = 0.025
sigma_2 = 0.007
correlation = 0.4

n_days = 10
# VAR1 e VAR2 non conviene moltiplicarli per 2
#VAR_1 = position_1*2*sigma_1
#VAR_2 = position_2*2*sigma_2
VAR_1 = position_1*sigma_1
VAR_2 = position_2*sigma_2

# questa formula non è corretta
#VAR_PTF = (VAR_1**2 + VAR_2**2 - VAR_1*VAR_2*correlation)**0.5 * n_days**0.5
VAR_PTF = (VAR_1**2 + VAR_2**2 + 2 * VAR_1 * VAR_2 * correlation) #**0.5  * n_days**0.5
#print('(2) VAR_PTF (FCA, Apple): ', round(VAR_PTF,2), "EUR")

# VAR_PTF non è il VaR, ma la varianza della gaussiana che rappresenta la distribuzione
#  delle variazioni del valore del portafoglio
# per ottenere il 10-day 97.5% VaR devi calcolare
# il 2.5 percentile della gaussiana normale N(0,1) con media nulla e sigma 1
# determinare il corrispondente percentile della tua gaussiana N(0, VAR_PTF) con la relazione Z = (X-mu)/sigma
# moltiplicare per sqrt(n_days)
# VaR = X * sqrt(n_days) = Z * sigma * sqrt(n_days)

from scipy.stats import norm

Z = norm.ppf(0.025)
mu = 0
sigma = np.sqrt(VAR_PTF)

VaR = Z * sigma * np.sqrt(n_days)

print ("10-days 97.5% VaR  {:.2f}".format(VaR))


########### EX 3 ###########
from curve_data import discount_curve, libor_curve

from math import exp
N = 100000
maturity = 4
# il coupon nell'esercizio non è fisso, ma è indicizzato con il LIBOR del file curve_data
#fixed_coupon = 0.06
price = 0

coupon_dates = [x * 6 for x in range(1, maturity*2+1)]
today = date.today()
for tau in coupon_dates:
    date_x = today + relativedelta(months=tau)
    discount_rate = discount_curve.df(date_x)
    coupon = libor_curve.forward_rate(date_x)
    #print('discount_rate: ', discount_rate)
    # il prezzo è sbagliato, devi moltiplicare per il discount factor
    #price += N * fixed_coupon / discount_rate
    price += N * coupon * discount_rate

date_x = today + relativedelta(months=coupon_dates[-1])
discount_rate = discount_curve.df(date_x)
# il prezzo è sbagliato, devi moltiplicare per il discount factor
price += N * discount_rate
print ("Bond price is: {:.2f} EUR".format(price))


