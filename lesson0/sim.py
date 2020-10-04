import numpy as np
np.random.seed(10)
import matplotlib.pyplot as plt
import csv

def gen_paths(S0, r, T, M):
    dt = 1
    paths = np.zeros((M + 1), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * 0.2 ** 2) * dt +
                                         0.2 * np.sqrt(dt) * rand)
    return paths

S0 = 100                                    # initial stock price
r = 0.01                                    # risk-free interest rate
M = 365*2                                   # number of steps within each simulation

paths = gen_paths(S0, r, 1, M)

for p in paths:
    print (p)
#plt.ion()
plt.plot(paths)
plt.grid(True)
plt.xlabel('days')
plt.ylabel('$S^{i}_{t}$')
plt.show()
#plt.savefig("underlyings.png")
