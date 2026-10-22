import numpy as np

class VasicekModel:
  def __init__(self, a, b, sigma):
    self.a = a
    self.b = b
    self.sigma = sigma

  def _B(self, tau):
    return (1.0 - np.exp(-self.a * tau)) / self.a

  def _A(self, tau):
    B_val = self._B(tau)
    term1 = (self.b - (self.sigma**2) / (2 * self.a**2)) * (B_val - tau)
    term2 = (self.sigma**2 * B_val**2) / (4 * self.a)
    return np.exp(term1 - term2)

  def P(self, r, tau):
    if np.isscalar(tau) and tau == 0:
      return 1.0

    A_val = self._A(tau)
    B_val = self._B(tau)
    return A_val * np.exp(-B_val * r)

  def R(self, r, tau):
    if np.isscalar(tau):
      if tau == 0:
        return r
      P_val = self.P(r, tau)
      return -np.log(P_val) / tau
    else:
      tau_safe = np.where(tau == 0, 1e-10, tau)
      P_val = self.P(r, tau_safe)
      return -np.log(P_val) / tau_safe

  def simulate_r(self, r0, N, T, dt, Z=None, seed=1):
    np.random.seed(seed)
    num_steps = int(np.round(T / dt))
    num_points = num_steps + 1

    r = np.zeros(shape=(N, num_points))
    r[:, 0] = r0

    if Z is None:
        Z = np.random.normal(size=(N, num_steps))

    for i in range(1, num_points):
        r[:, i] = r[:, i - 1] + self.a * (self.b - r[:, i - 1]) * dt \
                + self.sigma * np.sqrt(dt) * Z[:, i - 1]
    return r
