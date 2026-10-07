import numpy as np

class VasicekModel:
  def __init__(self, a, b, sigma):
    self.a = a
    self.b = b
    self.sigma = sigma

  def r(self, r0, N, T, dt, Z=None):
    num_steps = int(np.round(T / dt))
    num_points = num_steps + 1

    r = np.zeros(shape=(N, num_points))
    r[:, 0] = r0

    if Z is None:
      Z = np.random.normal(size=(N, num_steps))

    for i in range(1, num_points):
      r[:, i] = r[:, i - 1] + self.a * (self.b - r[:, i - 1]) * dt \\
                + self.sigma * np.sqrt(dt) * Z[:, i - 1]
    return r

  def discount_factors(self, r_path, dt):
    N, num_points = r_path.shape
    dfs = np.zeros((N, num_points))
    dfs[:, 0] = 1.0
    integrated_r = np.cumsum(r_path[:, :-1], axis=1) * dt
    dfs[:, 1:] = np.exp(-integrated_r)
    return dfs

  def B(self, delta_t):
    return (1 - np.exp(-self.a * delta_t)) / self.a

  def A(self, delta_t):
    term1 = (self.b - self.sigma**2 / (2 * self.a**2)) * (self.B(delta_t) - delta_t)
    term2 = (self.sigma**2 * self.B(delta_t) ** 2) / (4 * self.a)
    return np.exp(term1 - term2)

  def spot_rates(self, r_path, dt):
    N, num_points = r_path.shape
    spot_rates = np.zeros((N, num_points))
    spot_rates[:, 0] = r_path[:, 0]
    running_sum_r = np.cumsum(r_path[:, :-1], axis=1)
    steps = np.arange(1, num_points)
    spot_rates[:, 1:] = running_sum_r / steps
    return spot_rates

  def ZCB(self, r_t, delta_t):    
    if np.isscalar(delta_t) and delta_t == 0:
      return np.ones_like(r_t) if isinstance(r_t, np.ndarray) else 1.0

    price = self.A(delta_t) * np.exp(-self.B(delta_t) * r_t)
    return np.where(delta_t == 0, 1.0, price)

  def yield_rate(self, r_t, delta_t):
    if np.isscalar(delta_t) and delta_t == 0:
      return r_t if isinstance(r_t, np.ndarray) else float(r_t)

    price = self.bond_price(r_t, delta_t)
    return -np.log(price) / delta_t

  def ZBO(self, r, K, t, T, S, option_type=OptionType.Call):
      sigma_p = self.sigma*np.sqrt((1-np.exp(-2*self.k*(T-t)))/(2*self.k))*\
                self.B(T, S)
      h = 1/sigma_p*np.log((self.ZCB(r, t, S))/(self.ZCB(r, t, T)*K))+sigma_p/2
      arg1 = option_type*h
      arg2 = option_type*(h-sigma_p)
      return option_type*(self.ZCB(r, t, S)*norm.cdf(arg1)-\
             K*self.ZCB(r, t, T)*norm.cdf(arg2))
