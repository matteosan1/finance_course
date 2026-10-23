import pandas as pd

from dates import GlobalConsts as gc, TimeInterval
from curves import DiscountCurve
from ird import OvernightIndexSwap

df = pd.read_excel("ois_2024_10_14.xlsx", index_col="maturities")

oiss = []
for i in range(len(df)):
  maturity = df.index[i]
  quote = df['quotes'][maturity]*0.01
  oiss.append(OvernightIndexSwap(1, gc.OBS_DATE, maturity, quote))

