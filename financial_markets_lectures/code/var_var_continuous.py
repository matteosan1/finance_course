import numpy as np

from scipy.integrate import quad
from scipy.stats import t, norm
from typing import Tuple, Any

class RiskValuation:
  def __init__(self, dataframe: pd.DataFrame, y_col: str):
    self.df = dataframe
    self.y_col = y_col

  def VaR(self, confidence_level: float=0.95) -> Tuple[float, float]:
    var = -np.percentile(self.df[self.y_col], (1 - confidence_level) * 100)
    return var, confidence_level

  def parametric_VaR(self, distribution: Any, confidence_level: float=0.95) -> Tuple[float, float, Any]:
    fitted_params = distribution.fit(self.df[self.y_col])
    func = distribution(*fitted_params)
    alpha = 1.0 - confidence_level
    quantile = func.ppf(alpha)
    var = -quantile
    return var, confidence_level, func

  def ES(self, confidence_level: float=0.95):
    var, _ = self.VaR(confidence_level)
    tail = df[df[self.y_col] <= -var][self.y_col]
    expected_shortfall = -np.mean(tail)
    return expected_shortfall, confidence_level

  def parametric_ES(self, distribution: Any, confidence_level: float=0.95) -> Tuple[float, float, Any]:
    fitted_params = distribution.fit(df[self.y_col])
    func = distribution(*fitted_params)
    alpha = 1 - confidence_level
    param_es = -1/alpha * quad(func.ppf, 0, alpha)[0]
    return param_es, confidence_level, func


df = pd.read_csv("historical_data.csv")
df['P'] = data.multiply(0.2, axis='columns').sum(axis=1)

risk = RiskValuation(df, 'P')
var1, cl, _ = risk.parametric_VaR(norm)
es1, cl, _ = risk.parametric_ES(norm)
print ("Gaussian")
print (f"1d-{int(cl * 100)}% VaR: {var1:.4f}")
print (f"1d-{int(cl * 100)}% ES: {es1:.4f}")

var2, cl, _ = risk.parametric_VaR(t)
es2, cl, _ = risk.parametric_ES(t)
print ("t-student")
print (f"1d-{int(cl * 100)}% VaR: {var2:.4f}")
print (f"1d-{int(cl * 100)}% ES: {es2:.4f}")
