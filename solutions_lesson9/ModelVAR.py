#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:31:00 2019

@author: gioel
"""
from math import sqrt
from scipy.stats import norm

fca = 500000
apple = 750000

fca_vol = 0.025
apple_vol = 0.007

corr = 0.4

variance = (fca * fca_vol)**2 + (apple * apple_vol)**2 + 2 * corr * (fca * fca_vol) * (apple * apple_vol)
std_dev = sqrt(variance)

var = round(abs(norm.ppf(0.025) * std_dev), 2)
ten_days_var = round(var * sqrt(10),2)

print('The var of the portfolio is:',var)
print('The ten-days var of the portfolio is:',ten_days_var)
