from datetime import date
from typing import Union

from global_consts import GlobalConst as gc
from dates import TimeInterval, yearFraction
from curves import DiscountCurve, TermStructure

class InterestRateSwap:
  def __init__(self, nominal: float, start_date: date, maturity: Union[str, TimeInterval], fixed_rate: float, 
               frequency_float: str, frequency_fix: str="1y", side: str="Receiver", day_count_convention: str="ACT360"):      
    self.nominal = nominal
    self.start_date = start_date
    self.maturity = maturity if isinstance(maturity, TimeInterval) \\
      else TimeInterval(maturity)
    self.side = 1 if side == "Receiver" else -1
    self.day_count_convention = day_count_convention        
    self.fixed_rate = fixed_rate
    self.fix_dates = self.maturity.generate_schedule(start_date, frequency_fix)
    self.float_dates = self.maturity.generate_schedule(start_date, frequency_float)

  def annuity(self, dc: DiscountCurve) -> float:
    a = 0
    for i in range(1, len(self.fix_dates)):
      if gc.OBS_DATE > self.fix_dates[i]:
        continue
      tau = yearFraction(self.fix_dates[i-1], self.fix_dates[i], self.day_count_convention)
      a += tau*dc.df(self.fix_dates[i])
    return a

  def swap_rate(self, dc: DiscountCurve, fc: TermStructure) -> float:
    num = 0
    for j in range(1, len(self.float_dates)):
      if gc.OBS_DATE > self.float_dates[j]:
        continue
      F = fc.forward_rate(self.float_dates[j-1], self.float_dates[j])
      tau = yearFraction(self.float_dates[j-1], self.float_dates[j], self.day_count_convention)
      D = dc.df(self.float_dates[j])
      num += F * tau * D
    return num/self.annuity(dc)

  def npv(self, dc: DiscountCurve, fc: TermStructure) -> float:
    S = self.swap_rate(dc, fc)
    A = self.annuity(dc)
    return self.side*self.nominal*(self.fixed_rate - S)*A
    
    