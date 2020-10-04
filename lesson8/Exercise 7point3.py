#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:28:23 2019

@author: gioel
"""
from finmarkets import CreditDefaultSwap, DiscountCurve, CreditCurve, generate_swap_dates
from curve_data import discount_curve, pricing_date, credit_curve

cds_to_price = [
{'nominal': 5000000, 'maturity': 18, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 30, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 42, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 72, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 108, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 132, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 160, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 184, 'spread': 0.02},
{'nominal': 5000000, 'maturity': 210, 'spread': 0.02}
]

from finmarkets import  OvernightIndexSwap
import cds_data
from bootstrapping_cc import pillar_dates, result


my_cds_npvs = []
for quote in cds_to_price:
    cds = CreditDefaultSwap(quote["nominal"],
                            pricing_date,
                            quote["maturity"] // 12, # divido per 12 perchè voglio la maturity in anni
                            quote["spread"])
    my_cds_npvs.append(cds.npv(discount_curve, credit_curve))

print (my_cds_npvs)
#print(cds.premium_leg_npv(discount_curve, credit_curve))
#print(cds.default_leg_npv(discount_curve, credit_curve))
#print(cds.npv(discount_curve, credit_curve))
