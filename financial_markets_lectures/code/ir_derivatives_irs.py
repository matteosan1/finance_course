from datetime import date
from typing import Union

from dates import GlobalConsts as gc, TimeInterval, yearFraction
from curves import DiscountCurve, TermStructure

class InterestRateSwap:
  """
  A class to represent interest rate swaps

  Attributes:
  -----------
  nominal: float
    nominal of the swap
  start_date: datetime.date
    starting date of the contract
  maturity: str
    maturity of the swap.
  fixed_rate: float
    rate of the fixed leg of the swap
  frequency_float: str
    tenor of the float leg
  frequency_fix: str
    tenor of the fixed leg. default value is 1 year
  side: Side
    define the Payer or Receiver nature of the swap, default Receiver
  """    
  def __init__(self, nominal: float, start_date: date, 
               maturity: Union[str, TimeInterval], fixed_rate: float, 
               frequency_float: str, frequency_fix: str="1y", 
               side: str="Receiver", day_count_convention: str="ACT360"):      
    self.nominal = nominal
    self.start_date = start_date
    self.maturity = maturity if isinstance(maturity, TimeInterval) \
      else TimeInterval(maturity)
    self.side = 1 if side == "Receiver" else -1
    self.day_count_convention = day_count_convention        
    self.fixed_rate = fixed_rate
    self.fix_dates = self.maturity.generate_schedule(start_date, frequency_fix)
    self.float_dates = self.maturity.generate_schedule(start_date, frequency_float)

  def annuity(self, dc: DiscountCurve) -> float:
    """
    Computes the fixed leg annuity

    Params:
    -------
    dc: DiscountCurve
      discount curve object used for the annuity
    """
    a = 0
    for i in range(1, len(self.fix_dates)):
      if gc.OBS_DATE > self.fix_dates[i]:
        continue
      tau = yearFraction(self.fix_dates[i-1], self.fix_dates[i], 
                         self.day_count_convention)
      a += tau*dc.df(self.fix_dates[i])
    return a

  def swap_rate(self, dc: DiscountCurve, fc: TermStructure) -> float:
    """
    Compute the swap rate of the IRS

    Params:
    -------
    dc: DiscountCurve
      discount curve object used for swap rate calculation
    fc: TermStructure
      forward curve object used for swap rate calculation
    """
    num = 0
    for j in range(1, len(self.float_dates)):
      if gc.OBS_DATE > self.float_dates[j]:
        continue
      L = fc.forward_rate(self.float_dates[j-1], self.float_dates[j])
      tau = yearFraction(self.float_dates[j-1], self.float_dates[j], 
                         self.day_count_convention)
      D = dc.df(self.float_dates[j])
      num += L * tau * D
    return num/self.annuity(dc)

  def npv(self, dc: DiscountCurve, fc: TermStructure) -> float:
    """
    Computes the NPV of the swap

    Params:
    -------
    dc: DiscountCurve
      discount curve to be used in the calculation
    fc: TermStructure
      forward curve          
    """
    S = self.swap_rate(dc, fc)
    A = self.annuity(dc)
    return self.side*self.nominal*(self.fixed_rate - S)*A
