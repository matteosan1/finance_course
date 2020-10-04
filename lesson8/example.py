from numpy.random import randn, seed

class Line:
    def __init__(self, m, q):
        self.m = m#params[0]
        self.q = q#params[1]

    def error_squared(self, xs, ys):
        sum = 0
        for i, x in enumerate(xs):
            sum += (ys[i] - self.m*x - self.q)**2

        return sum

    def plot(self, r):
        points = []
        for x in r:
            points.append(self.m*x + self.q)

        return points

def generate_points(m, q, sigma=10):
    seed(1)
    points = []
    for i in range(100):
        points.append(m*i + q + randn()*sigma)

    return points

from matplotlib import pyplot as plt

xs = range(100)
points = generate_points(1.5, 10.0)
params = []

def obj_function(x):
    line = Line(x[0], x[1])
    sum = line.error_squared(xs, points)
    params.append((line.m, line.q))
    return sum

from scipy.optimize import minimize

x_guess = [0, 0]
bounds = [(-3, 3), (-10, 10)]
result = minimize(obj_function, x_guess, bounds=bounds)

plt.scatter(range(100), points, s=10)
line = Line(result.x[0], result.x[1])
plt.plot(xs, line.plot(xs), color=(1, 0, 0))
plt.show()
