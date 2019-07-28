# encoding:UTF-8
from math import log, e, sqrt, pi,exp
from scipy import stats
import pandas as pd
import tushare as ts


class BinaryModel():
    '''
    定义CCR模型（二叉树模型的一种 ：

    '''
    def __init__(self, S, X, r, q, T, sigma, N, opt_type='call'):
        self.S = S
        self.X = X
        self.r = r
        self.q = q
        self.T = T
        self.sigma = sigma
        self.N = N
        self.opt_type = opt_type
        self.dt = self.T/self.N  ##步长
        self.u = exp(self.sigma * sqrt(self.dt)) #上涨系数
        self.d = 1/self.u   #下跌系数
        self.prob = (exp((self.r - self.q) * self.dt) - self.d) / (self.u - self.d)
        self.opt_spot = dict()  #存储期权spot_price, 加快迭代速度

    def __maturity_price(self, n, nu):
        print 'test'



    def factorial_loop(sell, n):
        '''
        N的阶乘
        :param n:
        :return: 结果
        '''
        result = 1
        for i in range(n):
            result *= i + 1
        return result

    def factorial_recurison(self, n):
        if n ==1:
            return n
        else:
            return n * self.factorial_recurison(n-1)



if __name__ == '__main__':
    binaryModel = BinaryModel()
    print binaryModel.factorial_recurison(4)