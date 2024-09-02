from numpy.random import uniform, seed
from numpy import sqrt, power

def simulation(trials):
  r = 1
  in_circle = 0
  for _ in range(trials):
      x1 = -r + uniform()*2*r
      x2 = -r + uniform()*2*r
      distance = sqrt(x1**2 + x2**2)
      if distance <= r:
          in_circle += 1
  return in_circle 
  
def simulation_v2(trials):
    r = 1
    x1 = uniform(-r, r, trials)
    x2 = uniform(-r, r, trials)
    distances = sqrt(power(x1, 2) + power(x2, 2))
    return (distance <= r).sum()
	
seed(2)
trials = 10000
in_circle = simulation(trials)
print (f"Approx. pi: {in_circle/trials*4}")