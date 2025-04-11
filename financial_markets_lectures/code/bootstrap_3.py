import pandas as pd

from datetime import date
from finmarkets import DiscountCurve, TimeInterval, OvernightIndexSwap

obs_date = start_date = date.today()
ois = OvernightIndexSwap(1e6, start_date, "3y", 0.025)

df = pd.read_excel("discount_factors_2022-10-05.xlsx")
pillars = [obs_date + TimeInterval(i) for i in df['months']]
curve = DiscountCurve(obs_date, pillars, df['dfs'])

print (f"OIS NPV: {ois.npv(curve):,.2f} EUR")