import numpy as np

from datetime import date

from finmarkets import DiscountCurve

n_cds = 10
rho = 0.3
corr = np.ones(shape=(n_cds, n_cds))*rho
np.fill_diagonal(cov, 1)

obs_date = gc.OBS_DATE
pillar_dates = [obs_date + TimeInterval(f"{i}y") for i in range(6)]
dfs = [1/(1+0.05)**i for i in range(6)]
dc = DiscountCurve(pillar_dates, dfs)

basket = BasketDefaultSwaps(1, n_cds, obs_date, "2y", 0.01, "3m")
basket.credit_curve([0.01]*10, corr, 3, pillar_dates, "gauss", {'corr':corr}, seed=1)                  
print (basket.npv(dc))