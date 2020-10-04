#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:24:34 2019

@author: gioel
"""
from datetime import date
from finmarkets import ForwardRateCurve
from math import exp


notional = 100000

libor_curve = ForwardRateCurve(
   pillar_dates = [
        date(2019, 11, 23),
        date(2020, 11, 23),
        date(2021, 11, 23),
        date(2022, 11, 23),
        date(2023, 11, 23),
        date(2024, 11, 23),
        date(2025, 11, 23),
        date(2026, 11, 23),
        date(2027, 11, 23),
        date(2028, 11, 23),
        date(2029, 11, 23),
        date(2030, 11, 23),
        date(2031, 11, 23),
        date(2034, 11, 23),
        date(2039, 11, 23),
        date(2044, 11, 23),
        date(2049, 11, 23),
        date(2059, 11, 23),
        date(2069, 11, 23),
        date(2079, 11, 23)
    ],
   pillar_rates = [
        0.01,
        0.010025,
        0.0101,
        0.010225,
        0.0104,
        0.010625,
        0.0109,
        0.011225,
        0.0116,
        0.012025,
        0.0125,
        0.013025,
        0.0136,
        0.014225,
        0.0149,
        0.015625,
        0.0164,
        0.017225,
        0.0181,
        0.019025
    ]
)

coupon_rates = [0.010025,0.0101, 0.010225,0.0104]

j = 0
i = 2020
while i < 2024:
    a = libor_curve.forward_rate(date(i, 7, 23))
    coupon_rates.insert(j, a)
    j += 2
    i += 1

coupons = []

for k in range(0, len(coupon_rates)):
    b = round(notional * coupon_rates[k])
    coupons.append(b)
    


    
