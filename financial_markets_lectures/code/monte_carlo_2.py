import matplotlib.pyplot as plt

from numpy.random import randint
from scipy.stats import norm

n = 50000
unif = randint(1, 7, n)
gauss = norm.rvs(size=n)

plt.hist(unif, 6, range=[0.5, 6.5], color="xkcd:lightblue",
         edgecolor="xkcd:blue")
plt.title(r"Uniform distribution from $\tt{randint}$")
plt.show()

plt.hist(gauss, 100, range=[-4, 4], color="xkcd:lightblue",
         edgecolor="xkcd:blue")
plt.title(r"Example of Gaussian distribution from $\tt{scipy}$")
plt.show()


