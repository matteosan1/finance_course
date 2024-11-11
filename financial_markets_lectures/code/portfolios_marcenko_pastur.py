import numpy as np
import matplotlib.pyplot as plt

def marcenko_pastur_filter(cov_matrix, T):
    eigvals, eigvecs = np.linalg.eigh(cov_matrix)
    eigvals = np.real(eigvals)
    
    N = cov_matrix.shape[0]
    q = T / N
    sigma2 = np.mean(eigvals)
    lambda_plus = sigma2 * (1 + np.sqrt(1 / q))**2
    
    filtered_eigvals = np.where(eigvals > lambda_plus, eigvals, 0)
    cov_matrix_filtered = (eigvecs * filtered_eigvals) @ eigvecs.T
    
    return cov_matrix_filtered

np.random.seed(0)
N = 100
T = 300
data = np.random.normal(size=(T, N))
cov_matrix_empirical = np.cov(data, rowvar=False)
cov_matrix_denoised = marcenko_pastur_filter(cov_matrix_empirical, T)

eigvals_original = np.linalg.eigvalsh(cov_matrix_empirical)
eigvals_denoised = np.linalg.eigvalsh(cov_matrix_denoised)

plt.figure(figsize=(10, 5))
plt.plot(eigvals_original, label="Real noisy", color="red")
plt.plot(eigvals_denoised, label="Marcenko-Pastur", color="blue")
plt.yscale("log")
plt.xlabel("Eigenvalue Index")
plt.ylabel("Eigenvalue value")
plt.legend()
plt.show()
   
