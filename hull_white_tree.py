import numpy as np
import math

#dR = theta - a*R)*dt + sigma * np.sqrt(dt)
#dRs = -a*Rs*dt = sigma*np.sqrt(dt)

#t = i*deltat
#Rs = j*deltaR

def prob(a, j, deltat, type=0):
    if type == 0:
        pu = 1/6 + 1/2*(a**2*j**2*deltat**2 - a*j*deltat)
        pm = 2/3 - a**2*j**2*deltat**2
        pd = 1/6 + 1/2*(a**2*j**2*deltat**2 + a*j*deltat)
    elif type == 1:
        pu = 1/6 + 1/2*(a**2*j**2*deltat**2 + a*j*deltat)
        pm = -1/3 - a**2*j**2*deltat**2 - 2*a*j*deltat
        pd = 7/6 + 1/2*(a**2*j**2*deltat**2 + 3*a*j*deltat)
    elif type == -1:
        pd = 1/6 + 1/2*(a**2*j**2*deltat**2 - a*j*deltat)
        pm = -1/3 - a**2*j**2*deltat**2 + 2*a*j*deltat
        pu = 7/6 + 1/2*(a**2*j**2*deltat**2 - 3*a*j*deltat)

    return pu, pm, pd

sigma = 0.01
a = 0.1
deltat = 1
deltaR = sigma*np.sqrt(3*deltat)
print (deltaR)
jmax = math.ceil(0.184/a)
print (jmax)
