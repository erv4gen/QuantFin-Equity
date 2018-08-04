
import numpy as np
import pandas as pd
import time



def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        rv = func(*args, **kwargs)
        after = time.time()
        print('elapsed', after - before)
        return rv
    return f


def get_data_sql(name='SNP500 Stocks - 50'):
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

    df = pd.read_sql(name,con=engine)
    return df

def get_data_local(con_man=True):
    if con_man:
        path = 'c:/data/res/res.csv'
        return pd.read_csv(path)
    else:
        path = 'c:/data/Datasets/stocksfundam-concated/res_man.csv'
        return pd.read_csv(path)