from finmarkets import DiscountCurve, CreditCurve
from datetime import date
from dateutil.relativedelta import relativedelta

pillar_dates = []
df = []
obs_date = date.today()
start_date = obs_date
for i in range(1, 2):
    pillar_dates.append(obs_date + relativedelta(years=i))
    df.append(1 / (1 + 0.05) ** i)
dc = DiscountCurve(obs_date, pillar_dates, df)
cc = CreditCurve(obs_date, 
                 [obs_date + relativedelta(years=i) for i in range(1, 5)],
                 [0.99, 0.97, 0.95, 0.93])
tranches = [[0.0, 0.03], [0.03, 0.06], [0.06, 0.09], [0.09, 1.0]]
spreads = [0.15, 0.07, 0.03, 0.01]
cdo = CollDebtObligation(100e6, 125, tranches, 0.3, cc,
                         start_date, spreads, "1y", "12m")
          
for i in range(len(tranches)):
    print (f"Tranche {i} ({tranches[i]}): {cdo.fair_value(i, dc):.5f}")