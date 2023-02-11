import numpy as np
import math

#dR = theta - a*R)*dt + sigma * np.sqrt(dt)
#dRs = -a*Rs*dt = sigma*np.sqrt(dt)

#t = i*deltat
#Rs = j*deltaR

sigma = 0.01
a = 0.1
deltat = 1
deltaR = sigma*np.sqrt(3*deltat)
jmax = math.ceil(0.184/a/deltat)
jmin = -jmax

class Node:
    def __init__(self, i, j, type=0):
        self.label = (i, j)
        self.R = 0
        self.type = None


def setNode(n, a, deltat):
    if n.label[1] <= jmin:
        n = Node
        
    for k in range(3):
        
    def 
        if type == 0:
            self.up = (i+1, j+1)
            self.down = (i+1, j-1)
            self.mid = (i+1, j)
        elif type == 1:
            self.up = (i+1, j+2)
            self.down = (i+1, j)
            self.mid = (i+1, j+1)
        elif type == -1:
            self.up = (i+1, j)
            self.down = (i+1, j-2)
            self.mid = (i+1, j-1)

    def prob(self, a, j, deltat):
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


            
i = 0
j = 0
n = Node(i, j, 0)
        
