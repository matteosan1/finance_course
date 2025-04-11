import pandas as pd

from datetime import date
from finmarkets import OvernightIndexSwap, TimeInterval


df = pd.read_excel("ois_2024_10_14.xlsx", index_col="maturities")

obs_date = date.today()
oiss = []
pillars = []
for i in range(len(df)):
  maturity = df.index[i]
  quote = df['quotes'][maturity]*0.01
  oiss.append(OvernightIndexSwap(1, obs_date, maturity, quote))

for i in range(len(df)):
  maturity = df.index[i]
  pillars.append(obs_date + TimeInterval(maturity))
