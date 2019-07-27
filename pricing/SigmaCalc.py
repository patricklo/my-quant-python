# encoding:UTF-8
from math import log,e,sqrt,pi
from scipy import stats
import pandas as pd
import tushare as ts
from BSMModel import *

class SigmaCalc():
    def calcSigma(sell):
        etf_return = ts.get_k_data('510050','2017-11-01').set_index('date').close.pct_change().dropna()
        sigma = etf_return.rolling(60).std()[-1] * sqrt(252)
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

