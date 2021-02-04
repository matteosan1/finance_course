#This file is designed to contain the code for running Monte Carlo simulations in generating zero-coupon bond price and the yield curve

import math
import random
from array import array

face = 1 #change this later


def r_generator (a,b,r0,sigma,num_its): #Creates an array of r_t (discrete)
	i = 0
	r = [r0]
	for i in range(num_its): #goes from i = 0 to (numb_its - 1)
		brownian = random.normalvariate(0, 1) #Brownian motion variable
		r_new = r[i] + a*(b-r[i]) + sigma*brownian #calculates each r_t
		r.append(r_new)
	return r



def monte_carlo_ZCB (a,b,sigma,r0,dt,t0,tf,numb_sims,face):
	#Returns a matrix that is [numb_sims]by[numb_iterations]
	number_iterations = int((tf-t0)/dt) #number of iterations per simulation
	i = 0 #delete?
	ZCB_price = []
	tau = tf-t0
	for i in range(numb_sims): #iterates through the simulations
		ZCB_one_round = [] #initializes disposable array 
		r_one_round = r_generator(a,b,r0,sigma,number_iterations) #calculates the r_t
		#
		B = (1-math.exp(-a*tau))/a #calculates B (equation 18b)
		A = float(face*math.exp((B-tau)*(b-(sigma**2)/(2*(a**2)))-((sigma**2)*(B**2))/(4*a)))  #calculates equation 18a
		for j in range(number_iterations): #iterates through time
			ZCB_one_round.append(A*math.exp(-B*r_one_round[j]))
		ZCB_price.append(ZCB_one_round) #MAKE SURE THIS APPENDS THE VALUES TO A NEW LIST IN THIS ARRAY
	return ZCB_price
	
def yield_curve (maturities,a,b,sigma,r0,dt,t0,tf,numb_sims): #calculates the yield curve
	#maturities is an array of the times-to-maturity
	yield_sims = [] 
	#Will hold numb_sims of yield
	yield_time_sim = [] 
	#Will hold [time_iterations]by[numb_sims]
	yield_all = [] 
	#Will be final [len(maturities)]by[time_iterations]by[numb_sims]
	for j in range(len(maturities)): #iterates through each maturity term
		ZCB_prices = monte_carlo_ZCB(a,b,sigma,r0,dt,t0,tf,numb_sims,face) 
		time_iterations = int((tf-t0)/dt)
		for i in range(time_iterations):
			for k in range(numb_sims):
				yield_sims.append(-1*math.log(ZCB_prices[k][i])/maturities[j])
			#This calculates and appends the yield at simulation k with maturity j, at time i (I hope)
			yield_time_sim.append(yield_sims)
		yield_all.append(yield_time_sim)
	return yield_all
	
maturities = [1,2,3]
yc = yield_curve(maturities,.1,0,.1,0,.05,0,1,1)

from matplotlib import pyplot as plt
import numpy as np

for i in range(3):
    for y in yc[i]:
        #print (yc[0][0])
        plt.plot(y)
plt.show()

