from scipy.optimize import newton
from finmarkets import DiscountCurve

class Bootstrap:
    def __init__(self, obs_date, objects):
        self.obs_date = obs_date
        self.objects = objects

    def run(self, obj_func, guess=1.0, args=()):
        x = []    
        for i in range(len(self.objects)):
            res = newton(obj_func, guess, 
                         args=(i, x, self.objects, self.obs_date, *args))
            x.append(res)
        return x


def obj_df(df, i, dfs, objs, obs_date, *args):
    pillars = [obs_date] + [objs[j].payment_dates[-1] for j in range(i+1)]
    dc = DiscountCurve(obs_date, pillars, [1] + dfs + [df])
    return objs[i].npv(dc)

bootstrap = Bootstrap(obs_date, oiss)
dfs = bootstrap.run(obj_df)
    
discount_curve = DiscountCurve(obs_date, pillars, dfs)
