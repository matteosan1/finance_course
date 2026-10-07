from scipy.optimize import newton
from typing import List, Dict, Union

from curves import DiscountCurve
from ird import OvernightIndexSwap

class Bootstrapper:
  def __init__(self, objects: List[OvernightIndexSwap]):    
    self.objects = objects
    self.pillars = []

  def objective_function(self, x, i, x_prev, curve, kwargs) -> float:
    c = curve(self.pillars, x_prev + [x])
    return self.objects[i].npv(c, **kwargs)

  def run(self, curve_cls: type[DiscountCurve], 
          guess: float=1.0, kwargs: Dict={}) -> DiscountCurve:
    x = []
    last_guess = guess

    for i, obj in enumerate(self.objects):
      self.pillars.append(obj.fix_dates[-1])        
      res = newton(self.objective_function, last_guess, 
        args=(i, x, curve_cls, kwargs))
      x.append(res)
      last_guess = res
    return curve_cls(self.pillars, x)

bootstrap = Bootstrap(oiss)
dfs = bootstrap.run(obj_df)
    
discount_curve = DiscountCurve(pillars, dfs)
