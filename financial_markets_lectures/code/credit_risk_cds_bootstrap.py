import pandas as pd, numpy as np

from datetime import date

from finmarkets import TimeInterval, DiscountCurve, CreditDefaultSwap
from finmarkets import CreditCurve, Bootstrap

obs_date = start_date = date.today()
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

def obj_cc(ndp, i, ndps, objs, obs_date, discount_curve):
    pillars = [obs_date] + [objs[j].payment_dates[-1] for j in range(i+1)]
    credit_curve = CreditCurve (obs_date, pillars, [1] + ndps + [ndp])
    return objs[i].npv(discount_curve, credit_curve)

bootstrap = Bootstrap(obs_date, cdswaps)
ndps = bootstrap.run(obj_cc, args=(discount_curve,))

credit_curve = CreditCurve(obs_date, pillar_dates, ndps)