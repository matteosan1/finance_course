from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from typing import List, Union

class TimeInterval:
  def __init__(self, code: str):
    code = code.upper().strip()
    val_str, unit = code[:-1], code[-1]
    if not val_str.isdigit() or unit not in {"D", "W", "M", "Y"}:
        raise ValueError(f"Invalid TimeInterval format: '{code}'."
          "Please use something like '1D', '3M', '1Y'.")
    self.value, self.unit = int(val_str), unit
    
  def __add__(self, start_date: Union[str, date]) -> date:
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date() \\ 
      if isinstance(start_date, str) else start_date
    if self.unit == 'D':
        return start_date + relativedelta(days=self.value)
    elif self.unit == 'W':
        return start_date + relativedelta(weeks=self.value)
    elif self.unit == 'M':
        return start_date + relativedelta(months=self.value)
    elif self.unit == 'Y':
        return start_date + relativedelta(years=self.value)
    raise ValueError("Invalid unit encountered.")

  __radd__ = __add__
  
  def generate_schedule(self, start_date: Union[str, date], 
                        frequency: Union[str, 'TimeInterval']) -> list[date]:
    """
    Generates a list of intermediate payment dates starting from start_date 
    up to the maturity date defined by this TimeInterval.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date() \\
      if isinstance(start_date, str) else start_date
    if isinstance(frequency, str):
      frequency = TimeInterval(frequency)
      
    end_date = self + start_date          
    schedule = [start_date]
    current_date = start_date #+ frequency

    while True:
      current_date += frequency
      if current_date < end_date:
        schedule.append(current_date)
      else:
        schedule.append(end_date)
        break
    return schedule
        