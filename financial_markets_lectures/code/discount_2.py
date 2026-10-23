import pandas as pd, matplotlib.pyplot as plt

from dates import GlobalConsts as gc, TimeInterval
from curves import DiscountCurve

df = pd.read_excel("discount_factors_2022-10-05.xlsx")

pillars = [gc.OBS_DATE + TimeInterval(i) for i in df['months']]
dc = DiscountCurve(pillars, df['dfs'])

df_date = gc.OBS_DATE + TimeInterval("195d")
df0 = dc.df(df_date)
r0 = dc.get_zero_rate(df_date)
print (f"discount factor at {df_date}: {df0:.4f}")
print (f"zero rate at {df_date}: {r0:.4f}")
