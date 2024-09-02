import matplotlib.pyplot as plt

from numpy.random import normal

gauss = normal(size=50000)

plt.hist(gauss, 100, range=[-4, 4])
plt.title("Example of Gaussian distribution from numpy")
plt.show()
