import random
from array import array
import numpy as np

class ShortModel:
    def __init__(self, k, theta, sigma):
                self.k = k
                self.theta = theta
                self.sigma = sigma
                
class VasicekModel(ShortModel):
        def r_generator(self, r0, T, N):
                np.random.seed(777)
                r = [r0]
                dt = T/float(N)
                for _ in range(N): 
                        r_new = r[-1] + self.k*(self.theta - r[-1])*dt + self.sigma*np.random.normal()
                        r.append(r_new)
                return r

        def ZCB(self, tau, r0=0):
                B = (1-np.exp(-self.k*tau))/self.k
                A = np.exp((self.theta-(self.sigma**2)/(2*(self.k**2))) *
                           (B-tau) - (self.sigma**2)/(4*self.k)*(B**2))
                return A * np.exp(-r0*B)

        
        #	number_iterations = int((tf-t0)/dt) #number of iterations per simulation
        #	i = 0 #delete?
        #	ZCB_price = []
        #	tau = tf-t0
        #	for i in range(numb_sims): #iterates through the simulations
        #		ZCB_one_round = [] #initializes disposable array 
        #		r_one_round = r_generator(a,b,r0,sigma,number_iterations) #calculates the r_t
        #		#
        #		B = (1-math.exp(-a*tau))/a #calculates B (equation 18b)
        #		A = float(face*math.exp((B-tau)*(b-(sigma**2)/(2*(a**2)))-((sigma**2)*(B**2))/(4*a)))  #calculates equation 18a
        #		for j in range(number_iterations): #iterates through time
        #			ZCB_one_round.append(A*math.exp(-B*r_one_round[j]))
        #		ZCB_price.append(ZCB_one_round) #MAKE SURE THIS APPENDS THE VALUES TO A NEW LIST IN THIS ARRAY
        #	return ZCB_price


class CIR(ShortModel):
        def r_generator(self, r0, T, N):
                np.random.seed(777)
                r = [r0]
                dt = T/float(N)
                for _ in range(N):
                        r_new = r[-1] + self.k*(self.theta-r[-1])*dt + \
                                self.sigma*np.sqrt(r[-1])*np.random.normal()
                        r.append(r_new)
                return r

#
#
#	
#def yield_curve (maturities,a,b,sigma,r0,dt,t0,tf,numb_sims): #calculates the yield curve
#	#maturities is an array of the times-to-maturity
#	yield_sims = [] 
#	#Will hold numb_sims of yield
#	yield_time_sim = [] 
#	#Will hold [time_iterations]by[numb_sims]
#	yield_all = [] 
#	#Will be final [len(maturities)]by[time_iterations]by[numb_sims]
#	for j in range(len(maturities)): #iterates through each maturity term
#		ZCB_prices = monte_carlo_ZCB(a,b,sigma,r0,dt,t0,tf,numb_sims,face) 
#		time_iterations = int((tf-t0)/dt)
#		for i in range(time_iterations):
#			for k in range(numb_sims):
#				yield_sims.append(-1*math.log(ZCB_prices[k][i])/maturities[j])
#			#This calculates and appends the yield at simulation k with maturity j, at time i (I hope)
#			yield_time_sim.append(yield_sims)
#		yield_all.append(yield_time_sim)
#	return yield_all
#	
#maturities = [1,2,3]
#yc = yield_curve(maturities,.1,0,.1,0,.05,0,1,1)

#v = CIR(0.20, 0.01, 0.012)
#r = v.r_generator(0.01875, 10, 200)

v = VasicekModel(0.02, 0.5, 0.02)
zcbs = [v.ZCB(t, 0.015) for t in np.r_[0.0:25.5:0.5]]

from matplotlib import pyplot as plt

plt.plot(zcbs)
plt.show()


