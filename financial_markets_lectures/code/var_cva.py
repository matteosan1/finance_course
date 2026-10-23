import numpy as np

from short_rate import VasicekModel
from distributions import PoissonProcess

np.random.seed(42)

R = 0.4
LGD = 1 - R
r0 = 0.03
a, b, sigma = 0.3, 0.05, 0.03
T = 1
N = 10000
dt = 1/365
_lambda = 0.05

vasicek = VasicekModel(a, b, sigma)
risk_free_price = vasicek.P(r0, T)
print (f"Bond price without adjustment: {risk_free_price:.4f}")

paths = vasicek.simulate_r(r0, N, T, dt)
expected_exposure = np.zeros(len(time_grid))
for idx, t in enumerate(time_grid):
  tau_residual = T - t
    
  if tau_residual <= 0:
    expected_exposure[idx] = 1.0
    continue
        
  r_t = paths[:, idx]
  bond_prices = vasicek.P(r_t, tau_residual)
  expected_exposure[idx] = np.mean(bond_prices)
  
pp = PoissonProcess(_lambda)
CVA = 0
for j in range(0, 365):
  CVA += LGD*np.max(expected_exposure[j], 0)* \
    (pp.survival_prob((j-1)/365)-pp.survival_prob(j/365))

print (f"CVA: {CVA:.3f}")
print (f"Price: {risk_free_price-CVA:.4f}")
print (f"CVA/Rf-Price: {CVA/risk_free_price:.3f}")
