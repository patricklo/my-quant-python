# encoding:UTF-8
from math import log,e,sqrt,pi
from scipy import stats
import pandas as pd

class BSMModel():
    def get_option_price(self, S, X,r,q,sigma,T,opt_type='call'):
        d1 = (log(S / X) + (r - q + sigma**2/2) * T) / (sigma * sqrt(T))
        d2 = d1  - sigma*sqrt(T)
        N1,N2 = stats.norm.cdf([float(d1),float(d2)])
        call = S*e ** (-q * T) - X * e ** (-r * T) * N2
        if opt_type=='call':
            return call
        else:
            put = call + X * e ** (-r * T) - S
            return put

if __name__ == '__main__':
    bsmModel = BSMModel()
    print bsmModel.get_option_price(float(2.47),float(2.25),0.05,0.0,0.325,float(24.0/365.0))