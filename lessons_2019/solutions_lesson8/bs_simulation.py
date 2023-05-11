import numpy as np
np.random.seed(1000)
import matplotlib.pyplot as plt
import csv
from finmarkets import put

def gen_paths(S0, r, sigmas, T, M, I):
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        for i in range(len(sigmas)):
            rand = np.random.standard_normal()
            paths[t, i] = paths[t - 1, i] * np.exp((r - 0.5 * sigmas[i] ** 2) * dt +
                                             sigmas[i] * np.sqrt(dt) * rand)
    return paths

S0 = 100                                    # initial stock price
K = [100]#[80, 90, 100, 110, 120]           # strike price
r = 0.01                                    # risk-free interest rate
sigmas = [s/100. for s in range(15, 55, 5) ]# volatility in market
T = [1] #0.25, 0.5, 0.75, 1, 2, 3]          # time in years
M = 365*max(T)                              # number of steps within each simulation
I = len(sigmas)                             # number of simulations


paths = gen_paths(S0, r, sigmas, max(T), M, I)

plt.ion()
plt.plot(paths)
plt.grid(True)
plt.xlabel('days')
plt.ylabel('$S^{i}_{t}$')
plt.show()
plt.savefig("underlyings.png")

with open("bs_training.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for sims in range(I):
        for i, S_t in enumerate(paths[:, sims]):
            for t in T:
                M = t * 365
                if i >= M:
                    continue
                for k in K:
                    put_price = put(S_t, k, r, sigmas[sims], t)
                    writer.writerow([sigmas[sims], k, t, S_t, put_price])


S0 = 100
K = 100
r = 0.01
sigmas = [0.25]
T = 1
M = 365*T
I = 1

paths = gen_paths(S0, r, sigmas, T, M, I)

with open("bs_testing.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i, S_t in enumerate(paths[:, 0]):
        put_price = put(S_t, K,  r, sigmas[0], T)
        writer.writerow([sigmas[0], K, T, S_t, put_price])


S0 = 100
K = 95
r = 0.01
sigmas = [0.20]
T = 3
M = 365*T
I = 1

paths = gen_paths(S0, r, sigmas, T, M, I)

with open("bs_testing_off.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i, S_t in enumerate(paths[:, 0]):
        put_price = put(S_t, K,  r, sigmas[0], T)
        writer.writerow([sigmas[0], K, T, S_t, put_price])
