from datetime import date
from typing import Union

from dates import GlobalConsts as gc, TimeInterval, yearFraction
from curves import DiscountCurve

class OvernightIndexSwap:
  """
  A class to represent O/N swaps

  Attributes:
  -----------
  notional: float
    notional of the swap
  start_date: datetime.date
    start date of the contract
  maturity: str
    maturity of the swap.
  fixed_rate: float
    rate of the fixed leg of the swap
  side: Side
    Payer or Receiver type, default Receiver
  """
  def __init__(self, nominal: float, start_date: date, 
               maturity: Union[str, TimeInterval], fixed_rate: float, 
               frequency_fix: str="1y", side: str="Receiver", 
               day_count_convention: str="ACT360"):      
    self.nominal = nominal
    self.start_date = start_date
    self.maturity = maturity if isinstance(maturity, TimeInterval) \
      else TimeInterval(maturity)
    self.side = 1 if side == "Receiver" else -1
    self.day_count_convention = day_count_convention        
    self.fixed_rate = fixed_rate
    self.fix_dates = self.maturity.generate_schedule(start_date, frequency_fix)        

  def _npv_floating(self, dc: DiscountCurve) -> float:
    """
    Compute the floating leg NPV
    
    Params:
    -------
    dc: DiscountCurve
      discount curve to be used in the calculation
    """
    return self.nominal * (dc.df(self.fix_dates[0]) - dc.df(self.fix_dates[-1]))
  
  def _npv_fixed(self, dc: DiscountCurve) -> float:
    """
    Computes the fixed leg NPV
    
    Params:
    -------
    dc: DiscountCurve
      discount curve to be used in the calculation
    """
    val = 0
    for i in range(1, len(self.fix_dates)):
      if gc.OBS_DATE > self.fix_dates[i]:
        continue
      tau = yearFraction(self.fix_dates[i-1], self.fix_dates[i], 
                         self.day_count_convention)
      val += dc.df(self.fix_dates[i]) * tau
    return self.nominal*self.fixed_rate*val
  
  def npv(self, dc: DiscountCurve) -> float: # type: ignore
    """
    Computes the contract NPV seen from the point of view of the 
    receiver of the floating leg.
    
    Params:
    -------
    dc: DiscountCurve
      discount curve to be used in the calculation
    """
    return self.side*(self._npv_floating(dc) - self._npv_fixed(dc))
