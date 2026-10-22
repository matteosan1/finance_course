import numpy as np

from short_rate import VasicekModel
  
r0 = 0.02
a = 0.3        
b = 0.1        
sigma = 0.03   
T = 1.0        
dt = 0.001     
N = 10000

model = VasicekModel(a=a, b=b, sigma=sigma)
exact_price = model.P(r0, T)

r_paths = model.simulate_r(r0=r0, N=N, T=T, dt=dt, seed=42)
integral_r = np.sum(r_paths[:, :-1], axis=1) * dt
discount_factors = np.exp(-integral_r)

mc_price = np.mean(discount_factors)
mc_error = np.std(discount_factors) / np.sqrt(N)

print(f"Exact Vasicek Price: {exact_price:.4f}")
print(f"MC Price: {mc_price:.4f} +- {mc_error:.4f}")