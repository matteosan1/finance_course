import numpy as np
import matplotlib.pyplot as plt

true_value = 1/130
experiments = 300
simulations = 1000
r = []
for e in range(experiments):
    seed(e*experiments)
    r.append(draw_sim(simulations))

print (f"mu_true: {true_value:.6f}")
print (f"mu: {np.mean(r):.6f} +- {np.std(r)/np.sqrt(experiments):.6f}")