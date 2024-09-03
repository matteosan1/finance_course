import numpy as np

from datetime import date
from dateutil.relativedelta import relativedelta

from finmarkets import DiscountCurve, CreditCurve, PoissonProcess

n_cds = 10
rho = 0.3
cov = np.ones(shape=(n_cds, n_cds))*rho
np.fill_diagonal(cov, 1)
copula = GaussianCopula(n_cds, cov)

poisson = PoissonProcess(l=0.01)

obs_date = date.today()
pillar_dates = [obs_date + relativedelta(years=i) for i in range(6)]
dfs = [1/(1+0.05)**i for i in range(6)]
dc = DiscountCurve(obs_date, pillar_dates, dfs)

np.random.seed(1)
basket = BasketDefaultSwaps(1, n_cds, obs_date, "2y", 0.01, "3m")
basket.credit_curve(n_defaults=3, copula_func=copula, default_prob=poisson,
                    obs_date=obs_date, pillars=pillar_dates)
print (basket.npv(dc))