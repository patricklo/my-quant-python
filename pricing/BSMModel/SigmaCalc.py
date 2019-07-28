# encoding:UTF-8
from math import log,e,sqrt,pi
from scipy import stats
import pandas as pd
import tushare as ts
from pricing.BSMModel.BSMModel import *

class SigmaCalc():
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

    def calcSigma(sell):
        etf_return = ts.get_k_data('510050','2017-11-01').set_index('date').close.pct_change().dropna()
        sigma = etf_return.rolling(60).std()[-1] * sqrt(252)
        return sigma
    '''
    4.2使用牛顿法计算隐含波动率
使用BSM模型计算期权价格时，
	• opt = BSM(S,X,r,q,σ,T)
如果将S,X,r,T的值固定，则可以将期权价格看做是σ (sigma)的函数：
	• opt=f(σ)
	• 则已知期权价格opt的情况下，求解σ相当于是求g(σ)=f(σ)−opt=0
	这个方程的解 则为->隐含波动率
	• 使用牛顿法求解g(σ)=0需要知道g^′ (σ),而g^′ (σ)=f^′ (σ)  
	g^′ (σ)即g(σ)的导数=f^′ (σ)    (opt 常数的导数是0)
	• f^′ (σ)是期权价格对波动率的一阶导数，即Vega:
	  Vega=e^(−qt)  S_0  N^′ (d_1 )  √T
	其中：
	N^′ (X)=1/(√2π) e^(−(x^2/2))
	d_1=(ln⁡((e^(−qt) S_0)/x)+(r+σ^2/2)T)/(σ√T)

    '''
    def vega(self, S, X, r, q, sigma, T):
        '''
        定义函数计算期权的vega
        :param S:
        :param X:
        :param r:
        :param q:
        :param sigma:
        :param T:
        :return: 返回期权的vega值
        '''
        d1 = (log(e ** (-q*T) * S / X) + (r + sigma ** 2/2) * T) / (sigma * sqrt(T))
        N_dash = e ** (-d1 ** 2 /2) /sqrt(2 * pi)
        return S * N_dash * sqrt(T)

    def get_implied_vol(self, S, X, r, q, T, V_mkt, opt_type='call'):
        '''

        :param S:
        :param X:
        :param r:
        :param q:
        :param T:
        :param V_mkt:
        :param opt_type:
        :return:
        '''

        sigma = 0.5
        error = 10 **(-6)
        for i in range(100):
            V = self.get_option_price(S, X, r, q, sigma, T, opt_type)
            if abs(V - V_mkt) < error:
                return sigma
            sigma = sigma - (V - V_mkt)/self.vega(S, X, r, q, sigma, T)
            print (i, sigma)
        return sigma
if __name__ == '__main__':
    sigmaCalc = SigmaCalc()
    '''
    T: 看期权到期时间给的是普通日期 还是工作日，如是普通日期，则/365；如果是工作日，则/252
    '''
    print sigmaCalc.calcSigma()
    S = 2.4
    '''
    sigma  - standard deviation 波动率, 使用的是历史波动率
    其实应该使用未来波动率，但原因在于一是不得知，二是近期历史的波动率确实能反应未来的波动率，所以使用近期历史数据
    
    隐含波动率 - 
    BSM模型中的波动比率，是对未来波动率的预期值，当使用历史波动率时，隐含的假设就是历史波动率会延续到未来。
    
    利用模型波动率的含义，理论上可以通过期权的市场价格反推波动率。
    此时求得的波动率可以理解为市场对波动率的预期，也就是隐含波动率。
    
    *** 平价期权与波动率基本呈线性关系，因此计算隐含波动率时一般使用平价期权的数据
    
    但在现实操作中，难以直接求得波动率的解析解，一般使用数据方法来计算，比如牛顿法
    
    
    牛顿法特点：
    1.牛顿法的收敛速度非常快，利用很少的计算就可以实现比较好的精度
    2.使用牛顿法作为优化算法的情况下，并不能保证找到全局最优
    3.牛顿法需要随机产生一个初始计算位置，对于非单调问题，初始位置的选择会对结果产生非常大的影响
    4.计算过程会用到原函数的导数，对于导数不可知或计算困难的情况就难以使用牛顿法
    
    
    使用牛顿法计算隐含波动率
    
    '''
    sigma = 0.21020789878854265  #这是历史波动率
    bottom_strike = 2.2 #行权价格
    r = 0.0246  #无风险收益率，可以使用一年期国债收益率，数据可以从中国债券信息网查询 ：https://www.chinabond.com.cn/d2s/cbData.html
    q = 0
    T = float(15/365.0)
    opt_price = []
    bsmModel = BSMModel()
    for i in range(16):
        strike = bottom_strike + i * 0.05  # 行权价格，每次加0.05
        call = bsmModel.get_option_price(S, strike, r, q, sigma, T)
        put = bsmModel.get_option_price(S, strike, r, q,sigma, T, opt_type='put')
        opt_price.append([strike, call.round(6), put])
    df = pd.DataFrame(opt_price, columns=['strike','call','put'])

    print df
    print sigmaCalc.vega(2.4,2.45,0.0246,0.0, 0.27, 16.0/365.0)
    V_mkt = 0.0871 ##市场上观察到的期权价格
    print sigmaCalc.get_implied_vol(2.41, 2.4, 0.024839, 0.0, 43.0/365,V_mkt,'call')

