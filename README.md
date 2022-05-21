# Financial-Computing
This is a project repository for financial computing course.


## title
Multi-stock portfolio analysis and forecasting

### Data preprocessing
data preparation.ipynb
By using the stock.csv file 
There is the way how to choose 3 stocks of total 14.

### Portfolio analysis
Analysis of portfolio.ipynb
Include correlation analysis of stocks, different weights to get profit, Monte Carlo simulation on Markowitz theory, Sharpe ratio and Deep learning to train a model which can get the optimal return and its corresponding weights.
The code of deep learning may run seconds.


### Time Series
TimeSeries.ipynb
You should do "pip install pandas_datareader" if you don't have this package.
Based on the weights which is calculated by Monte Carlo and Deep learning, predicting the cumulative return of each weight portfolio.

### Generalize our model
This is a project that you can get the cumulative return of each portfolio, you have 2 choices to generate the cumulative return image and get the corresponding weights.
Portfolio_monte.py
main.ipynb
Run in main.ipynb and can call the function in Portfolio_monte.py
When run main.ipynb:
you can choose : A: select random n stocks
                 B: give the stock list
If you choose A, you should input an integer then the code will give you random n stocks from tushare and get the cumulative return and corresponding weights.
But if the code choose a null stock, it will change the random stocks until there is no null stock.
And if you choose B, you should input all stocks you want to get a portfolio of them and push Enter to the end. Then it will be shown.
But if you input a stock which is not include in tushare or wrong stock code, it will be warning and you should choose again.
