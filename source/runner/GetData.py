from Functions import General ,PlotFunctions , DataAcquisition
import time , os
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup
import quandl
from time import mktime
import datetime
import mysql.connector
from ipdb import set_trace

import numpy as np

path = 'c:/data/Datasets/stocksfundam/'
limit  = int(input("what the size(amount of tickers)?"))
stock_list = [f for f in os.listdir(path)]  
i = 0
df_list = []
for stock in stock_list:
    ticker = stock.split('_')[0]
    df = pd.read_csv(path+stock)
    df['Ticker'] = ticker
    df['UNIX'] = df['Quarter end'].apply(lambda s:time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple()) )
    ticker_price_df = DataAcquisition.get_stock_perfomance(symbol=ticker,date_range=df['UNIX'])
    res_df = pd.merge(df,ticker_price_df,on=['UNIX','Ticker'],how='inner')
    df_list.append(res_df)
    if i>limit:
        break
    else:
        i+=1
        continue
    

res_df = pd.concat(df_list, ignore_index=True)


res_df['Date'] = pd.to_datetime(res_df['Quarter end'])
res_df.Absolute_Stock_Perfomance = res_df.Absolute_Stock_Perfomance.astype(float)
res_path = r'c:\data\Datasets\agg'+str(limit)+'.csv'

res_df.to_csv(res_path,index=False)

try:     
    from sqlalchemy import create_engine , event
    cred = {x.split(':')[0]: x.split(':')[1] for x in open(r'c:\data\sqlcred\mysql.txt','r').read().splitlines()}

    user = cred['user']
    passw =cred['pass']
    host = cred['server']
    db =  cred['db']
    constr= 'mysql+mysqlconnector://{USER}:{PASS}@{HOST}/{DB}'.format(USER=user,
                                                                    PASS=passw,
                                                                    HOST=host,
                                                                    DB=db)


    engine = create_engine(constr)
    @event.listens_for(engine, 'before_cursor_execute')
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemanby):
        if executemany:
            cursor.fast_executemany = True

   #clean columns name 
    print("Star Export To MySQL Server")
    res_df.columns = [x.replace('(','').replace(')','') for x in res_df.columns]
    name = 'SNP500 Stocks stuructured'
    res_df.to_sql(name=name,con=engine,if_exists='replace')
    print("Export has finished successfully")
except:
    print('cannot conect to SQL')