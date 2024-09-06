from finmarkets import generate_dates, SwapSide

class OvernightIndexSwap:
    def __init__(self, nominal, start_date, maturity, fixed_rate,
                 side=SwapSide.Receiver):
        self.nominal = nominal
        self.fixed_rate = fixed_rate
        self.payment_dates = generate_dates(start_date, maturity)
        self.side = side
      
    def npv_floating(self, dc):
        return self.nominal * (dc.df(self.payment_dates[0]) -
                               dc.df(self.payment_dates[-1]))
  
    def npv_fixed(self, dc):
        val = 0
        for i in range(1, len(self.payment_dates)):
            val += dc.df(self.payment_dates[i]) * \
                    (self.payment_dates[i] - self.payment_dates[i-1]).days/360 
        return self.nominal*self.fixed_rate*val
  
    def npv(self, dc):
        return self.side*(self.npv_floating(dc) - self.npv_fixed(dc))

    def fair_value_strike(self, dc):
        den = self.npv_fixed_leg(dc)/self.fixed_rate
        num = self.npv_floating_leg(dc)
        return num/den
