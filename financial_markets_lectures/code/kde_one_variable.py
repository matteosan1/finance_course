import matplotlib.pyplot as plt, numpy as np
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

pts = np.array([1,2,3,4,7,9])
y = np.zeros_like(pts)

X_plot = np.linspace(0, 10, 1000)

kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(pts.reshape(-1, 1))
log_dens = kde.score_samples(X_plot.reshape(-1, 1))

plt.plot(X_plot, np.exp(log_dens), color="xkcd:blue")
plt.fill_between(X_plot, -0.005, np.exp(log_dens), color="xkcd:blue", alpha=0.1)
for p in pts:
  plt.plot(X_plot, norm(p, 1).pdf(X_plot)*0.15)
plt.scatter(pts, y, color="xkcd:black")
plt.xlim(0, 10)
plt.ylim(-0.005, 0.2)
plt.show()