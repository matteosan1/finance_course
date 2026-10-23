import pandas as pd, statsmodels.api as sm

from typing import Union, List

class CAPMModel:
  def __init__(self, dataframe: pd.DataFrame):
    self.df = dataframe
    self.model = None
    self.predicted = None
    self.var = {}

  def fit(self, y_col: str, x_col: Union[str, List[str]], 
          verbose: bool=False):
    X = sm.add_constant(self.df[x_col])
    self.model = sm.OLS(self.df[y_col], X).fit()
    if verbose:
      print (self.model.summary())
    self.predicted = self.model.predict(X)

  def risk_decomposition(self, y_col: str, x_col: Union[str, List[str]],
                         verbose: bool=False):
    if self.model is None:
      raise ValueError("You need to fit a model first.")
    alpha, beta = self.model.params
    self.var['total'] = self.df[y_col].var()
    self.var['systematic'] = (beta**2) * self.df[x_col].var()
    self.var['idiosyncratic'] = self.model.resid.var()
    if verbose:
      print(f"Total Variance: {self.var['total']:.6f}")
      print(f"Systematic:     {self.var['systematic']:.6f}")
      print(f"Idiosyncratic:  {self.var['idiosyncratic']:.6f}")

returns = pd.read_csv("capm.csv")
capm = CAPMModel(returns)
capm.fit('ret_GE', 'ret_SP500', verbose=True)