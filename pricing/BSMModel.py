# encoding:UTF-8
from math import log,e,sqrt,pi
from scipy import stats
import pandas as pd

class BSMModel():
    def get_option_price(self, S, X,r,q,sigma,T,opt_type='call'):
        '''
        根据BSM模型计算期权价格
        :param S: 标的资产当前价格
        :param X: 或者K，指期权行权价格
        :param r: 无风险收益率
        :param q: 基础资产分红收益率  - 一般假设没有分红
        :param sigma: 标的资产的年化波动率
        :param T: 以年计算的期权到期时间   - 时间应该年化，即 到期时间天数/365
        :param opt_type: 'call' 或 'put'
        :return: 返回期权价格
        '''
        d1 = (log(S / X) + (r - q + sigma**2/2) * T) / (sigma * sqrt(T))
        d2 = d1  - sigma*sqrt(T)
        N1,N2 = stats.norm.cdf([d1,d2])
        call = S* (e ** (-q * T)) * N1- X * (e ** (-r * T)) * N2
        if opt_type=='call':
            return call
        else:
            put = call + X * e ** (-r * T) - S
            return put

if __name__ == '__main__':
    bsmModel = BSMModel()
    '''
    T: 看期权到期时间给的是普通日期 还是工作日，如是普通日期，则/365；如果是工作日，则/252
    '''
    print bsmModel.get_option_price(float(2.47),float(2.25),0.05,0.0,0.325,float(24.0/365.0),'call')