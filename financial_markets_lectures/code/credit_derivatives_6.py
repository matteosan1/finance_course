import numpy as np

from finmarkets import DiscountCurve
from datetime import date
from dateutil.relativedelta import relativedelta

n_cds = 10
l = 0.06
rho = 0.3

obs_date_date = date.today()
start_date = obs_date
pillar_dates = [obs_date + relativedelta(years=i) for i in range(6)]
dfs = [1/(1+0.05)**i for i in range(1, 6)]
dc = DiscountCurve(obs_date, pillar_dates, dfs)
Q = [1-np.exp(-(l*t)) for t in range(1, 6)]

basket = BasketDefaultSwapsOneFactor(1, n_cds, rho, obs_date, 0.01, "2y")
print(basket.npv(pillar_dates, Q, dc, 3))
