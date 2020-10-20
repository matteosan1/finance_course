from datetime import date
from dateutil.relativedelta import relativedelta

def generate_swap_dates(starting_date, maturity_months):
    dates = []
    for i in range(0, maturity_months, 12):
        dates.append(starting_date + relativedelta(months=i))
    dates.append(starting_date + relativedelta(months=maturity_months))
    return dates