import pandas as pd, numpy as np

from finmarkets import DiscountCurve, TimeInterval, CreditCurve, TermStructure
from finmarkets import VasicekModel, PoissonProcess

np.random.seed(42)

R = 0.4
LGD = 1 - R
r0 = 0.03
a, b, sigma = 0.3, 0.05, 0.03
T = 1
N = 10000
dt = 1/365
_lambda = 0.05

vasicek = VasicekModel(a, b, sigma)
paths = vasicek.r(r0, N, T, dt)
ZCB = vasicek.ZCB(paths, T)
risk_free_price = np.mean(ZCB[:, 0])

print (f"Bond price without adjustment: {risk_free_price:.4f}")

pp = PoissonProcess(_lambda)

t_prev = np.arange(0, 365) / 365.0
t_curr = np.arange(1, 366) / 365.0

default_probs = pp.survival_prob(t_prev) - pp.survival_prob(t_curr)
cva_sims = LGD*(ZCB[:, 1:] @ default_probs)
cva_mean = np.mean(cva_sims)

print(f"CVA medio: {cva_mean:.3f}")
print(f"Price: {risk_free_price - cva_mean:.4f}")
print(f"CVA/Rf-Price: {cva_mean / risk_free_price:.3f}")
