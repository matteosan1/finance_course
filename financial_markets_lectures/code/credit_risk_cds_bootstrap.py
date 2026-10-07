import pandas as pd, numpy as np

from finmarkets import GlobalConst as gc
from finmarkets import TimeInterval, DiscountCurve, CreditDefaultSwap
from finmarkets import CreditCurve, Bootstrap

obs_date = start_date = gc.OBS_DATE
dc = pd.read_excel("discount_factors_2022-10-05.xlsx")
mq = pd.read_excel("cds_quotes.xlsx")

dates = [obs_date + TimeInterval(i) for i in dc['maturities']]
discount_curve = DiscountCurve(dates, dc['dfs'])

cdswaps = []
for i in range(len(mq)):
  cds = CreditDefaultSwap(1e6, start_date,
                          mq.loc[i, 'maturities'], mq.loc[i, 'quotes'])
  cdswaps.append(cds)

bootstrap = Bootstrap(cdswaps)
credit_curve = bootstrap.run(CreditCurve, args=(discount_curve,))
