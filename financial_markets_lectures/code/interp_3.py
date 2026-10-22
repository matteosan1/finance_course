from scipy.optimize import minimize

def obj_func(x):
    return -x[0]*x[1]

x0 = [1, 1]
bounds = [(0.01, 100) for _ in range(len(x0))]
budget = 700
side_cost = 10
up_cost = 2
down_cost = 7

def cons(x, budget, up_cost, down_cost, side_cost):
    return budget - 2*x[0]*side_cost - x[1]*(up_cost + down_cost)

constraints = {'type':'eq', 'fun':cons,
               'args':(budget, up_cost, down_cost, side_cost)}

r = minimize(obj_func, x0, bounds=bounds, constraints=constraints)
print (r)