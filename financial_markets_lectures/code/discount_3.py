import pandas as pd, matplotlib.pyplot as plt

from datetime import date
from finmarkets import TimeInterval, DiscountCurve

df = pd.read_excel("discount_factors.xlsx")

obs_date = date.today()
pillars = [today + TimeInterval(i) for i in df['months']]

dc = DiscountCurve(obs_date, pillars, df['dfs'])
df_date = obs_date + TimeInterval("195d") # about 6.5 months
df0 = dc.df(df_date)

print (f"discount factor at {df_date}: {df0:.4f}")

plt.plot(pillars[:10], dfs[:10], marker='o', markersize=10, 
         label="dfs")
plt.scatter(df_date, df0, marker='X', s=100, color='red', 
            label='interp. df')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()