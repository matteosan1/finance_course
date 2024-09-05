import numpy as np

from scipy.stats import expon, rv_continuous

class PoissonProcess(rv_continuous):
    def __init__(self, l):
        super().__init__()
        self.l = l

    def _cdf(self, x):
        x[x < 0] = 0
        return (1 - np.exp(-self.l*x))

    def _pdf(self, x):
        x[x < 0] = 0
        return self.l*np.exp(-self.l*x)

    def _ppf(self, x):
        return -np.log(1-x)/self.l

p = PoissonProcess(5)
t = p.rvs(size=500)

p1 = expon.fit(t)

xplot = np.linspace(0.01, 1.5, 100)
plt.hist(t, bins=20, density=True, color="xkcd:lightblue")
plt.plot(xplot, expon.pdf(xplot, *p1), color="xkcd:red")
plt.title("Inter-arrival time distribution")
plt.show()
