import numpy as np

class CIRModel:
    def __init__(self, k, theta, sigma):
        self.k = k
        self.theta = theta
        self.sigma = sigma
        self.gamma = np.sqrt(self.k**2 + 2*self.sigma**2)

    def r(self, r0, T, steps=100):
        r = np.zeros(shape=(steps,))
        r[0] = r0
        for i in range(1, steps):
            r[i] = r[i-1] + self.k*(self.theta - r[i-1])*dt \
                   + self.sigma*np.random.normal()*np.sqrt(dt*r[i-1])
        return r

    def _B(self, T):
        c = np.exp(self.gamma*T) - 1
        return 2*c/((self.gamma + self.k)*c + 2*self.gamma)

    def _A(self, T):
        c = np.exp(self.gamma*T) - 1
        num = 2*self.gamma*np.exp((self.k+self.gamma)*T/2)
        den = (self.gamma + self.k)*c + 2*self.gamma
        return np.power(num/den, 2*self.k*self.theta/self.sigma**2)

    def ZCB(self, r0, t, T):
        return self._A(T)*np.exp(-r0*self._B(T))
