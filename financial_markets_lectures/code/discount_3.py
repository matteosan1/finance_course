import pandas as pd, matplotlib.pyplot as plt

from dates import GlobalConsts as gc, TimeInterval
from curves import DiscountCurve

df = pd.read_excel("discount_factors_2022-10-05.xlsx")

obs_date = gc.OBS_DATE
pillars = [obs_date + TimeInterval(i) for i in df['months']]
dc = DiscountCurve(pillars, df['dfs'])

df_date = obs_date + TimeInterval("195d")
df0 = dc.df(df_date)
print (f"discount factor at {df_date}: {df0:.4f}")

r0 = dc.get_zero_rate(df_date)
print (f"zero rate at {df_date}: {r0:.4f}")

plt.plot(pillars[:10], dc.discount_factors[:10], marker='o', markersize=10, 
         label="dfs")
plt.scatter(df_date, df0, marker='X', s=100, color='red', 
            label='interp. df')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()