import numpy as np

class CIRModel:
  def __init__(self, a, b, sigma):
    self.a = a
    self.b = b
    self.sigma = sigma

  def _gamma(self):
    return np.sqrt(self.a**2 + 2 * self.sigma**2)

  def _B(self, tau):
    gamma = self._gamma()
    numer = 2.0 * (np.exp(gamma * tau) - 1.0)
    denom = (gamma + self.a) * (np.exp(gamma * tau) - 1.0) + 2.0 * gamma
    return numer / denom

  def _A(self, tau):
    gamma = self._gamma()
    numer = 2.0 * gamma * np.exp((self.a + gamma) * tau / 2.0)
    denom = (gamma + self.a) * (np.exp(gamma * tau) - 1.0) + 2.0 * gamma
    power = (2.0 * self.a * self.b) / (self.sigma**2)
    return (numer / denom) ** power

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

    sqrt_dt = np.sqrt(dt)
    for i in range(1, num_points):
      r_prev = np.maximum(r[:, i - 1], 0.0)
      drift = self.a * (self.b - r_prev) * dt
      diffusion = self.sigma * np.sqrt(r_prev) * sqrt_dt * Z[:, i - 1]
      r[:, i] = r[:, i - 1] + drift + diffusion
        
    return r
