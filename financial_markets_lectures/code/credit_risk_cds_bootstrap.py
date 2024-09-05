import pandas as pd, numpy as np

from scipy.optimize import minimize
from finmarkets import TimeInterval

obs_date = date.today()
dc = pd.read_excel("discount_factors_2022-10-05.xlsx")
mq = pd.read_excel("cds_quotes.xlsx")

dates = [obs_date + TimeInterval(i) for i in dc['maturities']]
discount_curve = DiscountCurve(obs_date, dates, dc['dfs'])

cdswaps = []
pillar_dates = []
for i in range(len(mq)):
  cds = CreditDefaultSwap(1e6, start_date,
                          mq.loc[i, 'maturities'], mq.loc[i, 'quotes'])
  cdswaps.append(cds)
  pillar_dates.append(cds.payment_dates[-1])

def objective_function(ndps, obs_date, pillar_dates, discount_curve):
  credit_curve = CreditCurve(obs_date, pillar_dates, ndps)
  sum_sq = 0
  for cds in cdswaps:
      sum_sq += cds.npv(discount_curve, credit_curve)**2
  return sum_sq

ndp_guess = [1 for _ in range(len(cdswaps))]
bounds = [(0.01, 1) for _ in range(len(cdswaps))]

r = minimize(objective_function, ndp_guess, bounds=bounds,
             args=(obs_date, pillar_dates, discount_curve))
print (r)
