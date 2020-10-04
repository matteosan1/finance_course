#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 23:40:33 2019

@author: gioel
"""

from historical_data import stock1, stock2
from math import log, sqrt
from numpy import percentile

init_invest_stock1 = 100 * stock1[-1]
init_invest_stock2 = 50 * stock2[-1]

daily_ret_stock1 = []
 
for i in range(len(stock1)-1):
    day_var = (stock1[i + 1] / stock1[i])
    daily_ret_stock1.append(day_var)

daily_ret_stock2 = []

for k in range(len(stock2)-1):
    day_var2 = (stock2[k + 1] / stock2[k])
    daily_ret_stock2.append(day_var2)

port_ret = []
for j in range(len(daily_ret_stock1)):
    returns = init_invest_stock1 * daily_ret_stock1[j] + init_invest_stock2 * daily_ret_stock2[j]
    port_ret.append(returns - init_invest_stock1 - init_invest_stock2)

var = round(percentile(port_ret, 5),2)
print("Our portfolio's var is:",var)

five_days_var = round(var * sqrt(5), 2)
print("Our portfolio's five-days var is:",five_days_var)
