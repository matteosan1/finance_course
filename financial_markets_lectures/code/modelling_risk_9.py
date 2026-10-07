import numpy as np

from scipy.stats import binom, norm, multivariate_normal

from finmarkets import Copula

np.random.seed(1)
n_assets = 10
PD = np.ones(shape=(n_assets,)) * 0.1
N = 1_000_000

rho = 0.99999
Sigma = np.full((n_assets, n_assets), rho)
np.fill_diagonal(Sigma, 1.0)

copula = Copula(n_assets, "gauss", {'corr':Sigma})
binoms = [binom(1, 0.1)]*n_assets
defaults = copula.sample_marginals(N, binoms)

print("Simulated defaults (first 5 scenarios):")
print(defaults[:5])

outcomes = np.sum(defaults, axis=1)
print("\nTotal defaults per simulation:")
print(outcomes[:5])

successes = outcomes >= 5
print("\nSimulation with >= 5 defaults:")
print(successes[:5].astype(int))

prob_correlata = np.mean(successes)
print(f"\nP(ndefs >=5|rho=1): {prob_correlata:.6f}")