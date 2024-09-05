from finmarkets import SwapSide

class InterestRateSwap:
    def __init__(self, nominal, start_date, maturity,
                 fixed_rate, frequency_float, frequency_fix="1y", 
                 side=SwapSide.Receiver):
        self.nominal = nominal
        self.fixed_rate = fixed_rate
        self.fix_dates = generate_dates(start_date, maturity, frequency_fix)
        self.float_dates = generate_dates(start_date, maturity, frequency_float)
        self.side = side

    def annuity(self, dc, current_date=None):
        if current_date is None:
            current_date = self.fix_dates[0]

        a = 0
        for i in range(1, len(self.fix_dates)):
            if current_date > self.fix_dates[i]:
                continue
            tau = (self.fix_dates[i]-self.fix_dates[i-1]).days/360
            a += tau*dc.df(self.fix_dates[i])
        return a

    def npv(self, dc, fc, current_date=None):
        S = self.swap_rate(dc, fc)
        A = self.annuity(dc, current_date)
        return self.side*self.nominal*(self.fixed_rate - S)*A

    def swap_rate(self, dc, fc):
        num = 0
        for j in range(1, len(self.float_dates)):
            F = fc.forward_rate(self.float_dates[j], self.float_dates[j-1])
            tau = (self.float_dates[j] - self.float_dates[j-1]).days / 360
            D = dc.df(self.float_dates[j])
            num += F * tau * D
        return num/self.annuity(dc)
