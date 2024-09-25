import matplotlib.pyplot as plt, numpy as np
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

# Plot the progression of histograms to kernels
np.random.seed(1)
N = 2000
X = np.concatenate(
    (np.random.normal(0, 1, int(0.3 * N)), np.random.normal(5, 1, int(0.7 * N)))
)[:, np.newaxis]
X_plot = np.linspace(-5, 10, 1000)[:, np.newaxis]
bins = np.linspace(-5, 10, 30)

fig, ax = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
ax[0].hist(X[:, 0], bins=bins, histtype="bar", edgecolor="xkcd:brown", 
           fc="xkcd:orange", density=True)
ax[0].set_title("Histogram")
ax[0].set_xlim(-4, 9)
ax[0].set_ylim(0, 0.3)
ax[0].set_ylabel("Normalized Density")

# Gaussian KDE
kde = KernelDensity(kernel="gaussian", bandwidth=0.3).fit(X)
log_dens = kde.score_samples(X_plot)
ax[1].fill(X_plot[:, 0], np.exp(log_dens), color="xkcd:blue", 
           fc="xkcd:lightblue")
ax[1].set_title("Gaussian Kernel Density")
ax[1].set_xlim(-4, 9)
ax[1].set_ylim(0, 0.3)
plt.show()