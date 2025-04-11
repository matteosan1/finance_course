import numpy as np

from scipy.interpolate import interp1d

t = [1, 2, 4]
p = [0.9607894391523232, 0.9139311852712282, 0.8187307530779818]
f = [np.log(x) for x in p]

inter = interp1d(t, f)	
print (f"{np.exp(inter(1.5)):.3f}")