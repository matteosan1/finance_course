from datetime import date
from typing import Union

from finmarkets import TimeInterval, yearFraction, DiscountCurve
       
class OvernightIndexSwap:
  def __init__(self, nominal: float, start_date: date, 
               maturity: Union[str, TimeInterval], fixed_rate: float, 
               frequency_fix: str="1y", side: str="Receiver", 
               day_count_convention: str="ACT365"):      
    self.nominal = nominal
    self.start_date = start_date
    self.maturity = maturity if isinstance(maturity, TimeInterval) \\
      else TimeInterval(maturity)
    self.side = 1 if side == "Receiver" else -1
    self.day_count_convention = day_count_convention        
    self.fixed_rate = fixed_rate
    self.fix_dates = self.maturity.generate_schedule(start_date, frequency_fix)        
   
  def _npv_floating(self, dc: DiscountCurve) -> float:
    return self.nominal * (dc.df(self.fix_dates[0]) - dc.df(self.fix_dates[-1]))
  
  def _npv_fixed(self, dc: DiscountCurve) -> float:
    val = 0
    for i in range(1, len(self.fix_dates)):
      if gc.OBS_DATE > self.fix_dates[i]:
        continue
      tau = yearFraction(self.fix_dates[i-1], self.fix_dates[i], 
                         self.day_count_convention)
      val += dc.df(self.fix_dates[i]) * tau
    return self.nominal*self.fixed_rate*val
          
  def npv(self, dc: DiscountCurve) -> float: # type: ignore
    return self.side*(self._npv_floating(dc) - self._npv_fixed(dc))