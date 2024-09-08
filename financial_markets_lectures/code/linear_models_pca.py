import pandas as pd, numpy as np

class PCAWrapper:
  def __init__(self, X, normalize=True):
    if not isinstance(X, pd.DataFrame):
      raise ValueError("X must be a pandas DataFrame.")
    self.X = X
    self.n_features = X.shape[1]
    self.index = X.index
    self.X_std = (X - np.mean(X, axis=0))
    if normalize:
      self.X_std /= np.std(self.X_std, axis=0)

  def fit(self):
    cov_mat = np.cov(self.X_std.T)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    max_abs_idx = np.argmax(np.abs(eig_vecs), axis=0)
    signs = np.sign(eig_vecs[max_abs_idx, range(eig_vecs.shape[0])])
    eig_vecs = eig_vecs*signs[np.newaxis,:]
    eig_vecs = eig_vecs.T

    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[i,:]) for i in range(len(eig_vals))]
    eig_pairs.sort(key=lambda x: x[0], reverse=True)
    self.eig_vals_sorted = np.array([x[0] for x in eig_pairs])
    self.eig_vecs_sorted = np.array([x[1] for x in eig_pairs])

  def to_df_pc(self, data, is_loading=False):
    cols = ['PC' + str(i) for i in np.arange(1, data.shape[1] + 1)]
    idx = self.X.columns if is_loading else self.index
    return pd.DataFrame(data, columns=cols, index=idx)

  def components(self, n_pc=None):
    n_pc = self.X.shape[1] if n_pc is None else n_pc
    cps = self.eig_vecs_sorted[:n_pc, :]
    cps = self.to_df_pc(cps.T, is_loading=True)
    return cps

  def explained_var(self):
    return self.eig_vals_sorted/np.sum(self.eig_vals_sorted)

  def transform(self, n_pc=None):
    n_pc = self.X.shape[1] if n_pc is None else n_pc
    return self.X_std.dot(self.components(n_pc))

  def project(self, n_pc=None):
    n_pc = self.X.shape[1] if n_pc is None else n_pc
    return self.transform().iloc[:, 0:n_pc].dot(self.components().T.iloc[0:n_pc, :])

  def residuals(self, n_pc=None):
    residuals = self.X - self.project(n_pc)
    return residuals
