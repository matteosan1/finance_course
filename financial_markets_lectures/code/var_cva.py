import pandas as pd, numpy as np

from datetime import date
from dateutil.relativedelta import relativedelta
from finmarkets import DiscountCurve, TimeInterval, CreditCurve, TermStructure

today = date.today()
df = pd.read_excel("discount_factors_2022-10-05.xlsx")
pillars = [today + TimeInterval(i) for i in df['months']]
dc = DiscountCurve(today, pillars, df['dfs'])

pillar_dates = [today + relativedelta(years=i) for i in range(1, 11)]
S = [0.9, 0.8, 0.7, 0.6, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
cc = CreditCurve(today, pillar_dates, S)

notional = 1000000
swap = InterestRateSwap(notional, today, "10y", 0.035, "6m")
end_date =  today + TimeInterval("10y")

euribor_data = pd.read_excel('euribor_curve.xlsx', sheet_name='EURIBOR6M')
dates = [today + TimeInterval(i) for i in euribor_data['maturities']]
fc = TermStructure(today, dates, euribor_data.loc[:, 'rates']*0.01)

R = 0.4
cva = 0
EEs = []
d = today
while d < end_date:
  EE = max(0, swap.npv(dc, fc, d))*dc.df(d)
  EEs.append(EE)
  cva += (1-R)*EE*(cc.ndp(d)-cc.ndp(d+relativedelta(days=1)))
  d += relativedelta(days=1)

print (f"CVA: {cva:.2f}")
print (f"CVA as fraction of notional: {cva/notional:.2f}")
