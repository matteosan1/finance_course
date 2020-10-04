#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 23:41:48 2019

@author: gioel
"""
from finmarkets import DiscountCurve, generate_swap_dates, OvernightIndexSwap
import cds_data

pillar_dates = [cds_data.pricing_date]
swaps = [] 
for quote in cds_data.quotes:
    swap = OvernightIndexSwap(1e6,generate_swap_dates(cds_data.pricing_date,quote['maturity']),0.01 * quote['spread'])
    swaps.append(swap)
    pillar_dates.append(swap.payment_dates[-1])
pillar_dates = sorted(pillar_dates)
n_df_vector = len(pillar_dates)


def objective_function(x):
    curve = DiscountCurve(cds_data.pricing_date,pillar_dates,x)
    sum_sq = 0.0
    for swap in swaps:
        sum_sq += swap.npv(curve) ** 2
    return sum_sq

from scipy.optimize import minimize

x0 = [1.0 for i in range(n_df_vector)]
bounds = [(0.01, 1.0) for i in range(n_df_vector)]
bounds[0] = (1.0, 1.0)
result = minimize(objective_function, x0, bounds=bounds)
print(result)

curve = DiscountCurve(cds_data.pricing_date, pillar_dates, result.x)

list(result.x)
print(pillar_dates)
