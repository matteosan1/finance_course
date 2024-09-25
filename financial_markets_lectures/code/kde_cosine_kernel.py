import matplotlib.pyplot as plt, numpy as np
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

pts = np.array([1,2,3,4,7,9])
y = np.zeros_like(pts)

X_plot = np.linspace(0, 10, 1000)

for i in [0.5, 0.7, 1, 1.5, 2]:
  kde = KernelDensity(kernel="cosine", bandwidth=i).fit(pts.reshape(-1, 1))
  log_dens = kde.score_samples(X_plot.reshape(-1, 1))
  plt.plot(X_plot, np.exp(log_dens), label=f"bw={i}")
plt.scatter(pts, y, color="xkcd:black")
plt.xlim(0, 10)
plt.ylim(-0.005, 0.3)
plt.legend()
plt.show()