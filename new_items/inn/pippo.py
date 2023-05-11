import numpy as np

x = np.arange(1,2, 0.1)
x = [44909.00,
     44895.00,
     44939.00,
     44957.00,
     44971.00,
     44985.00,
     44999.00,
     45016.00,
     45030.00,
     45044.00,
     45058.00,
     45091.00,
     45121.00,
     45152.00,
     45183.00,
     45212.00,
     45244.00]
y = [0.91,
     0.98,
     1.24,
     1.50,
     1.53,
     1.62,
     1.41,
     1.92,
     1.83,
     2.08,
     2.00,
     1.93,
     2.10,
     2.39,
     2.40,
     2.43,
     2.58]
#y = 1*np.power(x, 3) + 0.5 * np.power(x, 2) - x + 0.2
#print (y)
X = []
for i in x:
    temp = [1, i, i**2, i**3]
    X.append(temp)

X = np.array(X)
ap = np.linalg.inv(X.T.dot(X)).dot(X.T)
print (ap[0], y[0])
m1 = ap[0]*y[0]
print (m1)

a = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
print (a)
#print (x, y)
