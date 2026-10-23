import pandas as pd

from dates import GlobalConsts as gc, TimeInterval
from finmarkets import DiscountCurve, OvernightIndexSwap

ois = OvernightIndexSwap(1e6, gc.OBS_DATE, "3y", 0.025)

df = pd.read_excel("discount_factors_2022-10-05.xlsx")
pillars = [gc.OBS_DATE + TimeInterval(i) for i in df['months']]
curve = DiscountCurve(pillars, df['dfs'])

print (f"OIS NPV: {ois.npv(curve):,.2f} EUR")