from dateutil.relativedelta import relativedelta

def TimeInterval(interval):
  tag = interval[-1].lower()
  value = int(interval[:-1])
  if tag == "d":
    return relativedelta(days=value)
  elif tag == "m":
    return relativedelta(months=value)
  elif tag == "y":
    return relativedelta(years=value)
