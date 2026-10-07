import pandas as pd, statsmodels.api as sm

from typing import Union, List

class CAPMModel:
  def __init__(self, dataframe: pd.DataFrame):
    self.df = dataframe
    self.model = None
    self.predicted = None

  def fit(self, y_col: str, x_col: Union[str, List[str]]):
    X = sm.add_constant(self.df[x_col])
    self.model = sm.OLS(self.df[y_col], X).fit()
    print (self.model.summary())
    self.predicted = self.model.predict(X)

  def risk_decomposition(self, y_col: str, x_col: str):
    if self.model is None:
      raise ValueError("You need to fit a model first.")
    alpha, beta = self.model.params
    ddof = 1
    n = len(self.df[y_col])
    total_var = float(np.var(self.df[y_col], ddof=ddof))
    systematic_var = float((beta**2) * np.var(self.df[x_col], ddof=ddof))
    idiosyncratic_var = float(np.var(self.model.resid, ddof=ddof))
    print(f"Total Variance: {total_var:.6f}")
    print(f"Systematic:     {systematic_var:.6f}")
    print(f"Idiosyncratic:  {idiosyncratic_var:.6f}")

returns = pd.read_csv("capm.csv")
capm = CAPMModel(returns)
capm.fit('ret_GE', 'ret_SP500')