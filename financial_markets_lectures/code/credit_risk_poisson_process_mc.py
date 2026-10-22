import matplotlib.pyplot as plt

from scipy.stats import expon

from distributions import PoissonProcess

p = PoissonProcess(5)
t = p.rvs(size=500)

p1 = expon.fit(t)

xplot = np.linspace(0.01, 1.5, 100)
plt.hist(t, bins=20, density=True, color="xkcd:lightblue")
plt.plot(xplot, expon.pdf(xplot, *p1), color="xkcd:red")
plt.title("Inter-arrival time distribution")
plt.show()
