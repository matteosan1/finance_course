import math, numpy

from scipy.stats import norm, binom
from scipy.integrate import quad

from datetime import date
from dateutil.relativedelta import relativedelta

from math import exp, log, sqrt
from scipy.stats import norm
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np

def d1(S, K, sigma, r, deltaT):
	return 1/(sigma*np.sqrt(deltaT))*(np.log(S/K)+(r+np.power(sigma, 2)/2)*deltaT)
	
def d2(S, K, sigma, r, deltaT):
	return d1(S, K, sigma, r, deltaT) - sigma*np.sqrt(deltaT)
	
def call(S, K, sigma, r, deltaT):
	return norm.cdf(d1(S, K, sigma, r, deltaT))*S - K*norm.cdf(d2(S, K, sigma, r, deltaT))*np.exp(-r*deltaT)
	
def put(S, K, sigma, r, deltaT):
	return K*norm.cdf(-d2(S, K, sigma, r, deltaT))*np.exp(-r*deltaT) - norm.cdf(-d1(S, K, sigma, r, deltaT))*S

def d1_m(M, sigma, r, deltaT):
	return 1/(sigma*sqrt(deltaT))*(log(M)+(r+sigma**2/2)*deltaT)
	
def d2_m(M, sigma, r, deltaT):
	return d1_m(M, sigma, r, deltaT) - sigma*sqrt(deltaT)
	
def call_m(M, sigma, r, deltaT):
	return norm.cdf(d1_m(M, sigma, r, deltaT))*M - norm.cdf(d2_m(M, sigma, r, deltaT))*exp(-r*deltaT)
	
def put_m(M, sigma, r, deltaT):
	return norm.cdf(-d2_m(M, sigma, r, deltaT))*exp(-r*deltaT) - norm.cdf(-d1_m(M, sigma, r, deltaT))*M

def generate_dates(start_date, maturity_months):
  dates = []
  for i in range(0, maturity_months, 12):
    dates.append(start_date + relativedelta(months=i))
  dates.append(start_date + relativedelta(months=maturity_months))
  return dates


class DiscountCurve:
    """
    DiscountCurve: class that manage discount curves.

    Attributes:
    -----------
    today: datetime.date
        Observation date
    pillar_dates: list of datetime.date
        List of pillars of the discount curve.
    discount_factors: list of float
        List of the actual discount factors.
    """
    def __init__(self, today, pillar_dates, discount_factors):
        self.today = today
        self.pillar_dates = pillar_dates
        self.discount_factors = discount_factors
        
    def df(self, d):
        """
        df: method to get interpolated discoutn factor at `d`.

        Params:
        -------
        d: datetime.date
            The actual date at which we would like the interpolated discount factor.
        """
        log_discount_factors = \
            [math.log(discount_factor)
             for discount_factor in self.discount_factors]
        pillar_days = [(pillar_date - self.today).days
                       for pillar_date in self.pillar_dates]
        d_days = (d - self.today).days
        interpolated_log_discount_factor = \
            numpy.interp(d_days, pillar_days, log_discount_factors)
        return math.exp(interpolated_log_discount_factor)
    
    def forward_rate(self, d1, d2):
        """
        forward_rate: computes the forward rate referred to the period d2-d1.

        Params:
        -------
        d1: datetime.date
        d2: datetime.date
        """
        return (self.df(d1) / self.df(d2) - 1.0) * \
            (365.0 / ((d2 - d1).days))
    
class ForwardRateCurve(object):
    """
    ForwardRateCurve: container for a forward rate curve.

    Attributes:
    -----------
    pillar_dates: list of datetime.date
        List of pillars of the forward rate curve.
    pillar_rates: list of rates
        List of rates of the forward curve.
    """
    def __init__(self, pillar_dates, pillar_rates):
        self.today = pillar_dates[0]
        self.pillar_dates = pillar_dates
        self.pillar_rates = pillar_rates
        
        self.pillar_days = [
            (pillar_date - self.today).days
            for pillar_date in self.pillar_dates
        ]

    def forward_rate(self, d):
        """
        forward_rate: compute the forward rate at time d by interpolation.
        
        Params:
        -------
        d: datetime.date
            The date for the interpolation.
        """
        d_days = (d - self.today).days
        return numpy.interp(d_days, self.pillar_days, self.pillar_rates)

class OvernightIndexSwap:
    """
    OvernightIndexSwap: a class to valuate Overnight Index Swaps

    Attributes:
    -----------
    notional: float
        Notional of the swap.
    payment_dates: list of datetime.date
        List of payment dates of the swap.
    fixed_rate: float
        Rate of the fixed leg of the swap.
    """
    def __init__(self, notional, payment_dates, fixed_rate):
        self.notional = notional
        self.payment_dates = payment_dates
        self.fixed_rate = fixed_rate
        
    def npv_floating_leg(self, discount_curve):
        """
        npv_floating_leg: computes the floating leg npv.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        return self.notional * (discount_curve.df(self.payment_dates[0]) -
                                discount_curve.df(self.payment_dates[-1]))

    def npv_fixed_leg(self, discount_curve):
        """
        npv_fixed_leg: computes the fixed leg npv.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        npv = 0
        for i in range(1, len(self.payment_dates)):
            start_date = self.payment_dates[i-1]
            end_date = self.payment_dates[i]
            tau = (end_date - start_date).days / 360
            df = discount_curve.df(end_date)
            npv = npv + df * tau
        return self.notional * self.fixed_rate * npv
    
    def npv(self, discount_curve):
        """
        npv: computes the total npv of the swap.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        float_npv = self.npv_floating_leg(discount_curve)
        fixed_npv = self.npv_fixed_leg(discount_curve)
        return float_npv - fixed_npv

    def fair_value_strike(self, discount_curve):
        """
        fair_value_strike: compute the fair value strike of the OIS.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for npv calculation.
        """
        den = self.npv_fixed_leg(discount_curve)/self.fixed_rate
        num = self.npv_floating_leg(discount_curve)
        return num/den
    
class InterestRateSwap:
    """
    InterestRateSwap: a class to valuate Interest Rate Swaps

    Attributes:
    -----------
    start_date: datetime.date
        Starting date of the contract.
    notional: float
        Notional of the swap.
    fixed_rate: float
        Rate of the fixed leg of the swap.
    tenor_months: int
        Tenor of the contract in months.
    maturity_years: int
        Maturity of the swap in years.
    """    
    def __init__(self, start_date, notional, 
                 fixed_rate, tenor_months, 
                 maturity_years):
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.fixed_leg_dates = \
            generate_swap_dates(start_date, 12 * maturity_years)
        self.floating_leg_dates = \
            generate_swap_dates(start_date, 12 * maturity_years,
                                tenor_months)
        
    def annuity(self, discount_curve):
        """
        annuity: compute the annuity.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for the annuity.
        """
        a = 0
        for i in range(1, len(self.fixed_leg_dates)):
            a += discount_curve.df(self.fixed_leg_dates[i])
        return a

    def swap_rate(self, discount_curve, libor_curve):
        """
        swap_rate: compute the swap rate of the IRS.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for swap rate calculation.
        libor_curve: ForwardRateCurve
            Libor curve object used for swap rate calculation.
        """
        s = 0
        for j in range(1, len(self.floating_leg_dates)):
            F = libor_curve.forward_rate(self.floating_leg_dates[j-1])
            tau = (self.floating_leg_dates[j] - \
                   self.floating_leg_dates[j-1]).days / 360
            P = discount_curve.df(self.floating_leg_dates[j])
            s += F * tau * P
        return s / self.annuity(discount_curve)
        
    def npv(self, discount_curve, libor_curve):
        """
        npv: compute the npv of the IRS.

        Params:
        -------
        discount_curve: DiscountCurve
            Discount curve object used for swap rate calculation.
        libor_curve: ForwardRateCurve
            Libor curve object used for swap rate calculation.
        """
        S = self.swap_rate(discount_curve, libor_curve)
        A = self.annuity(discount_curve)
        return self.notional * (S - self.fixed_rate) * A

class InterestRateSwaption:
    """
    InterestRateSwaption: class to manage swaptions.

    Attributes:
    -----------
    exercise_date: datetime.date
        The exercise date of the swaptions.
    irs: InterestRateSwap
        The IRS underlying the swaptions.
    """
    def __init__(self, exercise_date, irs):
        self.exercise_date = exercise_date
        self.irs = irs
        
    def npv_bs(self, discount_curve, libor_curve, sigma):
        """
        npv_bs: estimate the swaption NPV using Black-Scholes formula.
        
        Params:
        -------
        discount_curve: DiscountCurve
            The curve to discount the npv.
        libor_curve: ForwardRateCurve
            The libor curve to compute the swap rate.
        simga: float
            The volatility of the swap rate.
        """
        A = self.irs.annuity(discount_curve)
        S = self.irs.swap_rate(discount_curve, libor_curve)
        T = (self.exercise_date - discount_curve.today).days / 365
        d1 = (math.log(S/self.irs.fixed_rate) + 0.5 * sigma**2 * T) / (sigma * T**0.5)
        d2 = d1 - (sigma * T**0.5)
        npv = self.irs.notional * A * (S * scipy.stats.norm.cdf(d1) -
                                       self.irs.fixed_rate * scipy.stats.norm.cdf(d2))
        return npv
    
    def npv_mc(self, discount_curve, libor_curve, sigma, n_scenarios=10000):
        """
        npv_bs: estimate the swaption NPV with Monte Carlo Simulation.
        
        Params:
        -------
        discount_curve: DiscountCurve
            The curve to discount the npv.
        libor_curve: ForwardRateCurve
            The libor curve to compute the swap rate.
        simga: float
            The volatility of the swap rate.
        n_scenarios: int
            Number of Monte Carlo experiment to simulate.
        """
        A = self.irs.annuity(discount_curve)
        S = self.irs.swap_rate(discount_curve, libor_curve)
        T = (self.exercise_date - discount_curve.today).days / 365
        discounted_payoffs = []
        for i_scenario in range(n_scenarios):
            S_simulated = S * math.exp(-0.5 * sigma * sigma * T +
                                       sigma * math.sqrt(T) * numpy.random.normal())
            swap_npv = self.irs.notional * (S_simulated - self.irs.fixed_rate) * A
            discounted_payoffs.append(max(0, swap_npv))
        npv_mc = numpy.mean(discounted_payoffs)
        npv_error = 2.56 * numpy.std(discounted_payoffs) / math.sqrt(n_scenarios)
        return npv_mc, npv_error

class CreditCurve(object):
    """
    CreditCurve: a class to manage credit curves.

    Attributes:
    -----------
    pillar_date: list of datetime.date
        List of dates that forms the pillars of the curve.
    ndps: list of floats
        List of non-default probabilities.
    """    
    def __init__(self, pillar_dates, ndps):
        self.pillar_dates = pillar_dates
        
        self.pillar_days = [
            (pd - pillar_dates[0]).days
            for pd in pillar_dates
        ]
        
        self.ndps = ndps
        
    def ndp(self, value_date):
        """
        npd: method to interpolate non-default probability at arbitrary dates.

        Params:
        -------
        value_date: datatime.date
            The date of the interpolation.
        """
        value_days = (value_date - self.pillar_dates[0]).days
        return numpy.interp(value_days,
                            self.pillar_days,
                            self.ndps)
    
    def hazard(self, value_date):
        """
        hazard: compute the annualized hazard rate.

        Params:
        -------
        value_date: datetime.date
            The date at which the hazard rate is computed.
        """
        ndp_1 = self.ndp(value_date)
        ndp_2 = self.ndp(value_date + relativedelta(days=1))
        delta_t = 1.0 / 365.0
        h = -1.0 / ndp_1 * (ndp_2 - ndp_1) / delta_t
        return h
    
class CreditDefaultSwap:
    """
    CreditDefaultSwap: a class to valuate Credit Default Swaps

    Attributes:
    -----------
    notional: float
        Notional of the swap.
    start_date: datetime.date
        Starting date of the contract.
    fixed_spread: float
        The spread associated to the premium leg.
    maturity: int
        Maturity of the swap in years.
    tenor: int
        Tenor of the premium leg in months, default is 3.
    recovery: float
        Recovery parameter in case of default, default value is 40%
    """    
    def __init__(self, notional, start_date, fixed_spread, 
                 maturity, tenor=3, recovery=0.4):
        self.notional = notional
        self.payment_dates = generate_swap_dates(start_date, maturity*12, tenor)
        self.fixed_spread = fixed_spread
        self.recovery = recovery
    
    def npv_premium_leg(self, discount_curve, credit_curve):
        """
        npv_premium_leg: valuate the premium leg.

        Params:
        -------
        discount_curve: DiscountCurve 
            The curve to discount the NPV.
        credit_curve: CreditCurve
            The curve to extract the default probabilities.
        """
        npv = 0
        for i in range(1, len(self.payment_dates)):
            npv += (
                discount_curve.df(self.payment_dates[i]) *
                credit_curve.ndp(self.payment_dates[i])
            )
        return npv * self.notional * self.fixed_spread
    
    def npv_default_leg(self, discount_curve, credit_curve):
        """
        npv_ default_leg: valuate the default leg.

        Params:
        -------
        discount_curve: DiscountCurve 
            The curve to discount the NPV.
        credit_curve: CreditCurve
            The curve to extract the default probabilities.
        """
        npv = 0
        d = self.payment_dates[0]
        while d <= self.payment_dates[-1]:
            npv += discount_curve.df(d) * (
                credit_curve.ndp(d) -
                credit_curve.ndp(d + relativedelta(days=1))
            )
            d += relativedelta(days=1)
        return npv * self.notional * (1 - self.recovery)
    
    def npv(self, discount_curve, credit_curve):
        """
        npv: valuate the CDS.

        Params:
        -------
        discount_curve: DiscountCurve 
            The curve to discount the NPV.
        credit_curve: CreditCurve
            The curve to extract the default probabilities.
        """
        return self.npv_default_leg(discount_curve, credit_curve) - \
               self.npv_premium_leg(discount_curve, credit_curve)

    def breakevenRate(self, discount_curve, credit_curve):
        num = self.npv_default_leg(discount_curve, credit_curve)
        den = self.npv_premium_leg(discount_curve, credit_curve)/self.fixed_spread
        return num/den

class BasketDefaultSwaps:
    def __init__(self, notional,  names, rho, start_date, 
                 spread, maturity, tenor=3, recovery=0.4):
        self.names = names
        self.rho = rho
        self.cds = CreditDefaultSwap(notional, start_date, spread, 
                                     maturity, tenor, recovery)

    def one_factor_model(self, M, f, Q_dates, Q, dc, j):
        P = norm.cdf((norm.ppf(Q) - numpy.sqrt(self.rho)*M)/numpy.sqrt(1-self.rho))
        b = binom(self.names, P)
        S = 1 - (1 - b.cdf(j-1))
        cc = CreditCurve(Q_dates, S)
        return f(dc, cc)*norm.pdf(M)
            
    def breakeven(self, Q_dates, Q, dc, ndefaults):
        s = quad(self.one_factor_model, -numpy.inf, numpy.inf, 
                 args=(self.cds.breakevenRate, Q_dates, Q, dc, ndefaults))
        return s[0]
    
    def npv(self, Q_dates, Q, dc, ndefaults):
        s = quad(self.one_factor_model, -np.inf, np.inf, 
                 args=(self.cds.npv, Q_dates, Q, dc, ndefaults))
        return s[0]        
             
import bs4
import requests

def obtain_parse_wiki_snp500(): 
  response = requests.get( "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies" ) 
  soup = bs4.BeautifulSoup(response.text)
 
  # This selects the first table, using CSS Selector syntax and then ignores the header row ([1:]) 
  symbolslist = soup.select('table')[0].select('tr')[1:]
 
  # Obtain the symbol information for each row in the S&P500 constituent table 
  symbols = [] 
  for i, symbol in enumerate(symbolslist): 
    tds = symbol.select('td')
    symbols.append((tds[0].select('a')[0].text,
                    tds[1].select('a')[0].text,
                    tds[3].text)) 
 
  return symbols