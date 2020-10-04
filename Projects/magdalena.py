from finmarkets import OvernightIndexSwap, InterestRateSwap
from finmarkets import DiscountCurve, generate_swap_dates, ForwardRateCurve
from dateutil.relativedelta import relativedelta
import project6_data

pillar_dates = [project6_data.today]

swaps = []
for quote in project6_data.ois_quotes:
    swap = OvernightIndexSwap(1,
                              generate_swap_dates(
                                  project6_data.today,
                                  quote['maturity']
                              ),
                              quote['rate']
    )
    swaps.append(swap)
    pillar_dates.append(swap.payment_dates[-1])
   
pillar_dates = sorted(pillar_dates)
n_df_vector = len(pillar_dates)
print (pillar_dates)

def objective_function(x):
    curve = DiscountCurve(
        project6_data.today,
        pillar_dates,
        x
    )
   
    sum_sq = 0.0

    for swap in swaps:
        sum_sq += swap.npv(curve) ** 2
    return sum_sq


from scipy.optimize import minimize

x0 = [1.0 for i in range(n_df_vector)]
bounds = [(0.0001, 100.0) for i in range(n_df_vector)]
bounds[0] = (1.0, 1.0)
result = minimize(objective_function, x0, bounds=bounds)

print (result)
print(objective_function(x0))
print(objective_function(result.x))

curve = DiscountCurve(project6_data.today, pillar_dates, result.x)


swaps = []
pillar_dates = []
for quote in project6_data.irs_quotes:
    swap = InterestRateSwap(
        project6_data.today,
        1,
        quote['rate'],
        project6_data.libor_tenor,
        quote['maturity']//12
    )
    swaps.append(swap)

    pillar_dates.append(project6_data.today + relativedelta(months=quote['maturity']))

pillar_dates = sorted(pillar_dates)
n_libor_vector = len(pillar_dates)
print (pillar_dates)

def objective_function(x):
    libor_curve = ForwardRateCurve(
        pillar_dates,
        x
    )

    sum_sq = 0.0

    for swap in swaps:
        sum_sq += swap.npv(curve, libor_curve) ** 2
    print (sum_sq)
    return sum_sq


from scipy.optimize import minimize

x0 = [0.01 for i in range(n_libor_vector)]
bounds = [(-100.0, 100.0) for i in range(n_libor_vector)]
bounds[0] = (project6_data.libor_fixing_value, project6_data.libor_fixing_value)

result = minimize(objective_function, x0, bounds=bounds)

print (result)
print(objective_function(x0))
print(objective_function(result.x))

#curve = ForwardRateCurve(pillar_dates, result.x)
