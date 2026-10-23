import pandas as pd, numpy as np

from dates import GlobalConsts as gc, TimeInterval
from curves import DiscountCurve, CreditCurve
from credit import CreditDefaultSwap
from bootstrap import Bootstrapper

dc = pd.read_excel("discount_factors_2022-10-05.xlsx")
mq = pd.read_excel("cds_quotes.xlsx")

dates = [gc.OBS_DATE + TimeInterval(i) for i in dc['maturities']]
discount_curve = DiscountCurve(dates, dc['dfs'])

cdswaps = []
for i in range(len(mq)):
  cds = CreditDefaultSwap(1e6, gc.OBS_DATE,
                          mq.loc[i, 'maturities'], mq.loc[i, 'quotes'])
  cdswaps.append(cds)

bootstrap = Bootstrap(cdswaps)
credit_curve = bootstrap.run(CreditCurve, args=(discount_curve,))
