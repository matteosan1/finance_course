from datetime import date, datetime
from typing import Union

def yearFraction(start_date: Union[str, date], end_date: Union[str, date], 
                 day_count_convention: str = "ACT365") -> float:
  start_date = datetime.strptime(start_date, "%Y-%m-%d").date() \\
    if isinstance(start_date, str) else start_date
  end_date = datetime.strptime(end_date, "%Y-%m-%d").date() \\
    if isinstance(end_date, str) else end_date
  days = (end_date - start_date).days
  if day_count_convention == "ACT365":
      return days / 365
  elif day_count_convention == "ACT360":
      return days / 360
  else:
      raise ValueError(f"Convenzione non supportata: {day_count_convention}")
