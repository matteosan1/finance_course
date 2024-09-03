import pandas as pd

from finmarkets.ml.pca import PCAWrapper

df = pd.read_csv("DGS_2017_2018.csv", index_col="date")

pca = PCAWrapper(df, normalize=False)
pca.fit()

explained_var = pca.explained_var()
cum_explained_var = np.cumsum(explained_var)

cps = pca.components()
