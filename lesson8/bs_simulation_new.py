import numpy as np
import matplotlib.pyplot as plt
import csv
from finmarkets import call

R = np.arange(0.01, 0.1, 0.001)
S_k = np.arange(0.5, 1.5, 0.05)
sigmas = np.arange(0.15, 0.55, 0.0005)
T = [0.25, .5, 0.75, 1, 2, 3]
    
with open("bs_training.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for r in R:
        for s in S_k:
            for sigma in sigmas:
                for t in T:
                    call_price = call(s, r, sigma, t)
                    writer.writerow([s, r, sigma, t, call_price])

with open("bs_testing.csv", mode='w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for r in R:
        for s in S_k:
            for sigma in sigmas:
                for t in T:
                    call_price = call(s, r, sigma, t)
                    writer.writerow([s, r, sigma, t, call_price])

