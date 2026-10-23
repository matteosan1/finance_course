import matplotlib.pyplot as plt, numpy as np

from scipy.stats import multivariate_normal, t, norm

from copulas import Copula

mean = np.array([bmw.mean(), sie.mean()])
cov = df[['BMW.DE', 'SIE.DE']].cov().values
bmw_std, sie_std = bmw.std(), sie.std()
rv_norm = multivariate_normal(mean, cov)
x, y = np.mgrid[-0.15:0.15:0.001, -0.15:0.15:0.001]
pos = np.dstack((x, y))
z = rv_norm.pdf(pos)

l2 = rv_norm.pdf(mean + [2 * bmw_std, 2 * sie_std])
l5 = rv_norm.pdf(mean + [5 * bmw_std, 5 * sie_std])

N = len(df) # the number of samples matches the historical series length (12 y)

bmw_gauss_fit = norm.fit(bmw)
sie_gauss_fit = norm.fit(sie)
bmw_gauss_f = norm(*bmw_gauss_fit)
sie_gauss_f = norm(*sie_gauss_fit)

corr = df[['BMW.DE', 'SIE.DE']].corr(method="spearman")
gauss_copula_1 = Copula(n=2, typ="gauss", params={"corr": corr})
gauss_copula_1.rvs(size=N)
vals_norm_1 = gauss_copula_1.rvs_marginals(distributions=[bmw_gauss_f, sie_gauss_f])

bmw_t_fit = t.fit(bmw, fdf=5)
sie_t_fit = t.fit(sie, fdf=5)
bmw_t_f = t(*bmw_t_fit)
sie_t_f = t(*sie_t_fit)

gauss_copula_2 = Copula(n=2, typ="gauss", params={"corr": corr})
gauss_copula_2.rvs(size=N)
vals_norm_2 = gauss_copula_2.rvs_marginals(distributions=[bmw_t_f, sie_t_f])

t_copula = Copula(n=2, typ="t", params={"corr": corr})
t_copula.rvs(size=N)
vals_t = t_copula.rvs_marginals(distributions=[bmw_t_f, sie_t_f])

datasets = [vals_norm_1, vals_norm_2, vals_t, np.column_stack((bmw, sie))]
counts = []
for data in datasets:
    pdf_vals = rv_norm.pdf(data)
    counts.append(np.sum(pdf_vals < l5))
labels = ["Gauss Fit, Gauss Copula", "t Fit, Gauss Copula", 
          "t Fit, t Copula", "Historical Data"]
colors = ["xkcd:blue", "xkcd:red", "xkcd:emerald green", "black"]

fig, ax = plt.subplots(figsize=(9, 7))
for i in range(len(datasets)):
  ax.scatter(datasets[i][:, 0], datasets[i][:, 1], s=10, color=colors[i],
             alpha=0.5, label=f"{labels[i]} ({counts[i]})")

CS = ax.contour(x, y, z, [l5, l2], cmap="Pastel2")
CS.levels = [rf"{v}$\sigma$" for v in [5, 2]]
ax.clabel(CS, CS.levels, inline=True, fontsize=10)
ax.set_xlabel("BMW")
ax.set_ylabel("Siemens")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left")
plt.show()
