# encoding:UTF-8
from math import log, e, sqrt, pi,exp
from scipy import stats
import pandas as pd
import tushare as ts
import pandas_datareader.data as web
from datetime import datetime

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
        self.dt = float(self.T/self.N)  ##步长
        self.u = float(exp(self.sigma * sqrt(self.dt))) #上涨系数
        self.d = 1.0/self.u   #下跌系数
        self.prob = (exp((self.r - self.q) * self.dt) - self.d) / float(self.u - self.d)
        self.opt_spot = dict()  #存储期权spot_price, 加快迭代速度

    def __maturity_price(self, n, nu):
        '''
        计算到期时，n步中有nu步上涨的情况下，标的基础资产价格
        :param n:
        :param nu: n步中上涨的步数
        :return:

        S * u^nu * d^(n-nu) -> S * u^(2 * nu -n)
        '''
        return self.S * (self.u ** (2 * nu -n))


    def __binomial_pricing(self, n, nu):
        '''
        使用递归法计算二叉树节点上期权的价值
        :param n: 二叉树步数 -> 树的深度
        :param nu: nu步是上涨的
        :return:
        '''
        # 如果(n,nu)组合已经计算过，则直接从dict中提取计算结果，否则执行下面的计算过程
        if (n, nu) in self.opt_spot:
            return self.opt_spot[(n, nu)]

        # compute the exercise profit
        stockPrice = self.__maturity_price(n,nu)
        if self.opt_type == 'c':
            exercise_profit = max(0, stockPrice - self.X)
        else:
            exercise_profit = max(0, self.X - stockPrice)

        # Base case
        if n == self.N:
            return exercise_profit

        #recusive case: compute the binomial value
        discount_factor = exp(-self.r * self.dt)
        V_exp = self.prob * self.__binomial_pricing(n+1, nu+1) \
                + (1 - self.prob) * self.__binomial_pricing(n+1, nu)
        binomial = discount_factor * V_exp

        #计算美式期权的价值
        opt_america = max(binomial, exercise_profit)
        self.opt_spot[(n,nu)] = opt_america
        return opt_america

    def pricing(self):
        return self.__binomial_pricing(0,0)

    def run(self):
        '''
        模型应用
        :return:
        '''


if __name__ == '__main__':
    T = 15.0/365.0
    N = 100.0
    S = 2.4
    r = 0.0246
    q = 0.0
    X = 2.45
    sigma = 0.2744
    opt_type = 'p'
    binaryModel = BinaryModel(S, X, r, q, T, sigma, N, opt_type)
    #print binaryModel.pricing()
    #print binaryModel.factorial_recurison(4)

    start = datetime(2017,1,1)
    ###https://blog.csdn.net/Smile_Smilling/article/details/79934900
    appl = web.DataReader("AAPL", "yahoo", start)
    appl['rtn'] = appl['Close'].pct_change()
    appl['Volatility'] = appl['rtn'].rolling(100).std() * sqrt(252)

    sigma = appl['Volatility'].iloc[-1]
    T = 34/365
    N = 100
    S = 170.84
    r = 0.0236
    q = 0.0165
    X = 170

    binaryModel2 = BinaryModel(S, X, r, q, T, sigma, N, opt_type)
    print(binaryModel2.pricing())
    #gs = web.DataReader("GS", "iex-last")
    #print gs