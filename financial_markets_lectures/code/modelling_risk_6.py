import numpy as np

from finmarkets import GaussianCopula

def default_sim(P_marginal, cov, samples = 100000):
  successes = 0.
  g = GaussianCopula(3, cov)
  copula_sample = g.sample(samples)
  print (f"3D copula distribution (first two samples only)\n{copula_sample[:2]}")
  for v in copula_sample:
    if all(v <= P_marginal):
        successes += 1      
  print (f"Measured P_def: {successes/samples}")

Pdef = 0.1
cov = np.array([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])
print ("Uncorrelated defaults")
default_sim(Pdef, cov)

cov = np.array([[1, 0.9999999, 0.9999999],
                [0.9999999, 1, 0.9999999],
                [0.9999999, 0.9999999, 1]])
print ("\nCorrelated defaults")
default_sim(Pdef, cov)
