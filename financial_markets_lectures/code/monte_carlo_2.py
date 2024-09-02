import matplotlib.pyplot as plt

from numpy.random import randint

dist = randint(0, 5, size=10000)

plt.hist(dist, 6, range=[-0.5, 5.5])
plt.title("Uniform distribution from randint")
plt.show()
