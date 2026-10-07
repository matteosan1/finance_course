from datetime import date
from typing import Union

from finmarkets import GlobalConst as gc
from finmarkets import TimeInterval, yearFraction, DiscountCurve, CreditCurve

class CreditDefaultSwap:
  def __init__(self, nominal: float, start_date: date, maturity: Union[str, TimeInterval], spread: float, 
               frequency: str="3m", recovery: float=0.4, side="Buyer", day_count_convention: str="ACT360"):
    self.nominal = nominal
    self.start_date = start_date
    self.maturity = TimeInterval(maturity) if isinstance(maturity, str) else maturity
    self.recovery = recovery
    self.side = 1 if side == "Buyer" else -1
    self.day_count_convention = day_count_convention
    self.spread = spread
    self.recovery = recovery
    self.fix_dates = self.maturity.generate_schedule(start_date, frequency)

  def npv_premium_leg(self, cc: CreditCurve, dc: DiscountCurve) -> float:
    npv = 0
    for i in range(1, len(self.fix_dates)):
      if self.fix_dates[i] < gc.OBS_DATE:
        continue
      tau = YearFraction(self.fix_dates[i-1], self.fix_dates[i], self.day_count_convention)
      npv += dc.df(self.fix_dates[i]) * cc.ndp(self.fix_dates[i]) * tau
    return self.spread * npv * self.nominal
   
  def npv_default_leg(self, cc: CreditCurve, dc: DiscountCurve) -> float:
    npv = 0
    d = max(self.fix_dates[0], gc.OBS_DATE)
    while d < self.fix_dates[-1]:
      npv += dc.df(d) * (cc.ndp(d) - cc.ndp(d + TimeInterval("1d")))
      d += TimeInterval("1d")
    return npv * self.nominal * (1 - self.recovery)

  def npv(self, cc: CreditCurve, dc: DiscountCurve) -> float:
    return self.side*(self.npv_default_leg(cc, dc) - self.npv_premium_leg(cc, dc))

  def breakeven_rate(self, cc: CreditCurve, dc: DiscountCurve) -> float:
    num = self.npv_default_leg(cc, dc)
    den = self.npv_premium_leg(cc, dc)/self.spread
    return num/den

