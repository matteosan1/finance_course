from datetime import date
from dateutil.relativedelta import relativedelta

from finmarkets import TimeInterval

def generate_dates(start_date, end_date, frequency="1y"):
    if isinstance(end_date, str):
        end_date = start_date + TimeInterval(end_date)
    d = start_date
    dates = [start_date]
    while True:
        d += TimeInterval(frequency)
        if d < end_date:
            dates.append(d)
        else:
            dates.append(end_date)
            break
    return dates
    
print (generate_dates(date.today(), "25M"))