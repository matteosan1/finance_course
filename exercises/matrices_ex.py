import numpy as np
p = [[1, 0], [0, 1]]
q = [[1, 2], [3, 4]]
print("original matrices:")
print(p)
print(q)

print("Result of the matrix multiplication:")
print(np.dot(p, q))




import numpy as np
m = np.array([[3, -2],[1, 0]])
print("Original matrix:")
print(m)
w, v = np.linalg.eig(m)
print("Matrix eigenvalues", w)
print("Matrix eigenvectors", v)





import numpy as np
m = np.array([[1,2],[3,4]])
print("Original matrix:")
print(m)
result = np.linalg.inv(m)
print("Inverse of the matrix:")
print(result)







import numpy as np

def nested_loops():
    successes = 0
    factor = 1001
    for i1 in range(100, 1000):
        for i2 in range(100, 1000):
            for i3 in range(100, 1000):
                for i4 in range(100, 1000):
                    M = np.array([[i1, i2], [i3, i4]])
                    M2 = np.dot(M, M)
                    if np.array_equal(M2, factor*M):
                        successes += 1
                        print (M)
                        print (M2)
                        print ()
                        if successes == 2:
                            return

nested_loops()





import numpy as np
a = np.array([[4, 12, -16], [12, 37, -53], [-16, -53, 98]])
print("Original array:")
print(a)
L = np.linalg.cholesky(a)
print("Lower−triangular L in the Cholesky decomposition of the said array:")
print(L)











