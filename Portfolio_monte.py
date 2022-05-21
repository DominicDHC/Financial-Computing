#!/usr/bin/env python
# coding: utf-8

# In[4]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


# In[5]:


import tushare as ts
TOKEN = "e371c4002c53bc022bb788d62cbd234d74d28eb1a1c8f20f008a46e1"
ts.set_token(TOKEN)
pro = ts.pro_api()
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data = data.dropna().reset_index()


# In[3]:

def cumulative_returns_plot(StockReturns,name_list):
    for name in name_list:
        CumulativeReturns = ((1+StockReturns[name]).cumprod()-1)
        CumulativeReturns.plot(label=name)
    plt.legend()
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.show()


# In[7]:

def get_mcw(stock_list):
    stocks = []
    for stock in stock_list:
        if (stock in data['ts_code'].values) == False:
            print("Wrong stock code!")
            return get_w()
        st = pro.daily(ts_code=stock, start_date="20010101", 
                            end_date="20211030",fields=["ts_code","trade_date", "close"])
        st.index = pd.to_datetime(st['trade_date'], format = "%Y/%m/%d")
        st = st[["close"]]
        st.rename(columns={'close':stock},inplace=True)
        stocks.append(st)
    StockPrices = pd.concat([stocks[i] for i in range(len(stocks))],axis='columns',names=['trade_date']).dropna()
    if StockPrices.empty == True:
        print("These stocks have not common trade data in tushare, select random stocks again.")
        return w_for_rand(len(stocks))
    StockReturns = StockPrices.pct_change().dropna()
    stock_return = StockReturns.copy()
    
    cov_mat = stock_return.cov()
    cov_mat_annual = cov_mat * 252

    # Sets the number of simulations
    number = 10000
    # Set an empty numpy array to store the weight, yield and standard deviation obtained from each simulation
    random_p = np.empty((number, len(stock_list)+2))
    # Set the seed of random number to make the result repeatable
    np.random.seed(5)
 
    for i in range(number):
   
        random5=np.random.random(len(stock_list))
        random_weight=random5/np.sum(random5)
 
        #Calculate the average annual rate of return
        mean_return=stock_return.mul(random_weight,axis=1).sum(axis=1).mean()
        annual_return=(1+mean_return)**252-1
 
        #Calculate the annualized standard deviation, which is also called volatility
        random_volatility=np.sqrt(np.dot(random_weight.T,np.dot(cov_mat_annual,random_weight)))
 
    #Store the weight generated above, the calculated yield and standard deviation into the array random_ P medium
        random_p[i][:len(stock_list)]=random_weight
        random_p[i][len(stock_list)]=annual_return
        random_p[i][len(stock_list)+1]=random_volatility

    RandomPortfolios=pd.DataFrame(random_p)
    RandomPortfolios.columns=[s +'_weight' for s in stock_list]+['Returns','Volatility']
    # Set the risk-free return rate to 0
    risk_free = 0
    # Calculate the sharp ratio for each asset
    RandomPortfolios['Sharpe'] = (RandomPortfolios.Returns - risk_free) / RandomPortfolios.Volatility
    max_index = RandomPortfolios.Sharpe.idxmax()
    numstocks=len(stock_list)
    MSR_weights = np.array(RandomPortfolios.iloc[max_index, 0:numstocks])

    StockReturns['Portfolio_MSR'] = stock_return.mul(MSR_weights, axis=1).sum(axis=1)
    print("----------------------------------------------------")
    print("The best weight for portfolio is: ",MSR_weights)
    print("----------------------------------------------------")
    print("The cumulative return of portfolio:")
    cumulative_returns_plot(StockReturns,['Portfolio_MSR'])
    return 
    
    
def w_for_rand(n):
    stock_list = data['ts_code'][np.random.randint(0,len(data.index)-1,n)].values
    print("----------------------------------------------------")
    print("The stock portfolio is: ",stock_list)
    get_mcw(stock_list)
    return 

# In[ ]:

def get_w():
    print("----------------------------------------------------")
    way = input("Choose your way:\nA: select random n stocks\nB: give the stock list\n")
    if way == "A":
        print("----------------------------------------------------")
        n = int(input("How many stocks do you want to buy?(input an integer)"))
        w_for_rand(n)
        return
    if way == "B":
        stock_list = []
        print("----------------------------------------------------")
        print('Which stocks do you want to buy(put stock code one by one end with nothing):\n')
        for stock in iter(input, ''):
            if stock == '':
                break
            else:
                stock_list.append(stock)
        get_mcw(stock_list)
        return
    else:
        print("----------------------------------------------------")
        print("Wrong value!")
        get_w()
    return

















