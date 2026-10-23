import numpy as np

from dates import GlobalConsts as gc, TimeInterval
from curves_v3 import DiscountCurve
from distributions import PoissonProcess
from copulas import Copula
from credit import BasketDefaultSwaps

n_cds = 10
poisson_process = []
for i in range(n_cds):
  poisson_process.append(PoissonProcess(0.01))

rho = 0.3
corr = np.ones(shape=(n_cds, n_cds))*rho
np.fill_diagonal(corr, 1)
copula = Copula(n=n_cds, typ="gauss", params={'corr':corr})

pillar_dates = [gc.OBS_DATE + TimeInterval(f"{i}y") for i in range(6)]
dfs = [1/(1+0.05)**i for i in range(6)]
dc = DiscountCurve(pillar_dates, dfs)

basket = BasketDefaultSwaps(poisson_process, 3, 1, gc.OBS_DATE, "2y", 0.01, "3m")
basket.credit_curve(copula)
print (f"NPV: {basket.npv(dc):.4f}")