import numpy as np

from scipy.stats import rv_continuous

class PiecewisePoissonProcess(rv_continuous):
    def __init__(self, lambdas, times):
        super().__init__(a=0.0)
        self.lambdas = np.array(lambdas)
        self.times = np.array(times)

    def _cumulative_intensity(self, x):
        x = np.atleast_1d(x)
        cum_int = np.zeros_like(x, dtype=float)
        
        for i, val in enumerate(x):
            if val <= 0:
                continue
            
            total = 0.0
            prev_t = 0.0
            for lam, t in zip(self.lambdas, self.times):
                if val <= t:
                    total += lam * (val - prev_t)
                    prev_t = val
                    break
                total += lam * (t - prev_t)
                prev_t = t
            
            if val > prev_t:
                total += self.lambdas[-1] * (val - prev_t)
            
            cum_int[i] = total
        return cum_int

    def _hazard_rate(self, x):
        x = np.atleast_1d(x)
        conditions = [x <= t for t in self.times]
        return np.piecewise(x, conditions, list(self.lambdas) \
               + [self.lambdas[-1]])

    def _cdf(self, x):
        return 1 - np.exp(-self.cumulative_intensity_vectorized(x))

    def _pdf(self, x):
        return self._hazard_rate(x) \
               * np.exp(-self.cumulative_intensity_vectorized(x))

    def cumulative_intensity_vectorized(self, x):
        if np.isscalar(x):
            return self._cumulative_intensity([x])[0]
        return self._cumulative_intensity(x)

    def survival_prob(self, x):
        return 1 - self._cdf(x)