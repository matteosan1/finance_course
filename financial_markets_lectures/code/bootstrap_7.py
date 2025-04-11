import pandas as pd, numpy as np

from finmarkets import generate_dates, DiscountCurve, TimeInterval
from datetime import date

mq = pd.read_excel('ois_2022_09_30.xlsx', index_col='maturities')

pillar_dates = []
swaps = []
for i in range(len(mq)):
    maturity = mq.index[i]
    swap = OvernightIndexSwap(1e5, start_date,
                              maturity,
                              0.01 * mq['quotes'][maturity])
    swaps.append(swap)
    pillar_dates.append(swap.payment_dates[-1])
pillar_dates = sorted(pillar_dates)

def objective_function(dfs, obs_date, pillars, swaps):
    dfs = np.concatenate(([1], dfs))
    curve = DiscountCurve(obs_date, pillars, dfs)
    sum_sq = 0.0
    for swap in swaps:
        sum_sq += swap.npv(curve)**2
    return sum_sq

x0 = [1.0 for i in range(len(swaps))]
bounds = [(0.01, 10.0) for i in range(len(swaps))]

result = minimize(objective_function, x0, bounds=bounds,
                  args=(obs_date, pillar_dates, swaps))
print (result)


