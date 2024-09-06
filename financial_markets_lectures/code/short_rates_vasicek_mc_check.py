import numpy as np

from finmarkets.short_rates.vasicek import VasicekModel
  
r0 = 0.03
v = VasicekModel(0.3, 0.10, 0.03)
np.random.seed(1)
n = 1000
T = 1
steps = 100
dt = 1/steps

rs = np.zeros(shape=(n,))
for i in range(n):
    r = v.r(r0, T, steps)
    rs[i] = np.exp(-np.sum(r)*dt)

print (f"Exact Vasicek Price: {v.ZCB(r0, 0, T):.4f}")
print (f"MC Price: {np.mean(rs):.4f} +- {np.std(rs)/np.sqrt(n):.4f}")
