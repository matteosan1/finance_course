import numpy as np

from scipy.stats import rv_continuous

class PoissonProcess(rv_continuous):
  def __init__(self, lambdas, times=None, name="PoissonProcess"):
    super().__init__(a=0.0, name=name)
        
    if np.isscalar(lambdas):
      self.lambdas = np.array([float(lambdas)])
      self.times = np.array([])
    else:
      self.lambdas = np.array(lambdas, dtype=float)
      self.times = np.array(times, dtype=float) if times is not None else np.array([])

    if len(self.lambdas) != len(self.times) + 1:
      raise ValueError(f"lambdas must have len(times) + 1, got "
        "{len(self.lambdas)} and {len(self.times)} times.")

      self._T = np.concatenate(([0.0], self.times))  # T_0 = 0
      if len(self.times) > 0:
        delta_T = np.diff(self._T)
        cum_at_knots = np.cumsum(self.lambdas[:-1] * delta_T)
        self._C = np.concatenate(([0.0], cum_at_knots))
      else:
        self._C = np.array([0.0])

  def _cumulative_intensity(self, x):
    x_clean = np.maximum(0.0, np.asarray(x))

    if len(self.times) == 0:
      return self.lambdas[0] * x_clean

    idx = np.searchsorted(self._T, x_clean, side="right") - 1
    idx = np.clip(idx, 0, len(self.lambdas) - 1)
    return self._C[idx] + self.lambdas[idx] * (x_clean - self._T[idx])

  def _hazard_rate(self, x):
    x_clean = np.maximum(0.0, np.asarray(x))

    if len(self.times) == 0:
      return np.full_like(x_clean, self.lambdas[0])

    idx = np.searchsorted(self._T, x_clean, side="right") - 1
    idx = np.clip(idx, 0, len(self.lambdas) - 1)
    return self.lambdas[idx]

  def _cdf(self, x):
    return 1.0 - np.exp(-self._cumulative_intensity(x))

  def _pdf(self, x):
    return self._hazard_rate(x) * np.exp(-self._cumulative_intensity(x))

  def _ppf(self, q):
    q_clean = np.asarray(q)
    H = -np.log(1.0 - q_clean)  # Intensita cumulata target

    if len(self.times) == 0:
      return H / self.lambdas[0]

    idx = np.searchsorted(self._C, H, side="right") - 1
    idx = np.clip(idx, 0, len(self.lambdas) - 1)
    return self._T[idx] + (H - self._C[idx]) / self.lambdas[idx]

  def survival_prob(self, x):
    return np.exp(-self._cumulative_intensity(x))

p = PoissonProcess(5)
t = p.rvs(size=500)

p1 = expon.fit(t)

xplot = np.linspace(0.01, 1.5, 100)
plt.hist(t, bins=20, density=True, color="xkcd:lightblue")
plt.plot(xplot, expon.pdf(xplot, *p1), color="xkcd:red")
plt.title("Inter-arrival time distribution")
plt.show()
