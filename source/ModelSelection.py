#%%
import sys
sys.path.append('c:/pjt/QuantFin-Equity/source/libs/')
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score
from matplotlib import pyplot , style
style.use('dark_background')
import seaborn as sns
import statistics

def get_features(features=['P/B ratio',
                          'ROE'],dropna=True, local=True, con_man=True):
    import DataAcquisition
    from sklearn.preprocessing import StandardScaler

    sscaller = StandardScaler()

    if local:
        df = DataAcquisition.get_data_local(con_man=con_man)
    else:
        df = DataAcquisition.get_data_sql()
    if dropna:
        df = df.replace('None',np.nan).replace(-99999.00,np.nan).replace(-1,np.nan).dropna(axis=0)
        df.dropna(how='any',inplace=True)
    

    y = np.array(df['Absolute_Stock_Perfomance_Flag'])
    Z = df[['Stock_Future_Pefomance','SNP500_Future_Perfomance']]
    df = df[features]
    df = pd.concat([df,Z],axis=1)
    df = df.astype(float)
    X = np.array(df.values)
    
    X = sscaller.fit_transform(X)
    return X, y


def get_dummy(X,y):
    from sklearn.dummy import DummyClassifier
    strategy = ['stratified','most_frequent','uniform']

    for start in strategy:
        dummyc = DummyClassifier(strategy=start)
        dummyc.fit(X,y)
        print(start,': Dummy Score:',round(dummyc.score(X,y),2))


def run_backtest(y,y_p,Z):
    invest_amount = 1000
    stock_return = []
    index_return = []
    for i in range(Z.shape[0]):
        if y_p[i]==1:
            inv_return = invest_amount + (invest_amount*Z[i,0])
            stock_return.append(inv_return)
        else:
            inv_return = invest_amount + (invest_amount*Z[i,1])
            index_return.append(inv_return)

    return [{'Mean Stock Retun': statistics.mean(stock_return),
            'Sum Stock Return' : sum(stock_return)},
            {'Mean SnP Return ': statistics.mean(index_return),
            'Sum SnP Return' :  sum(index_return)} ]

    


X , y = get_features()
#'''First Run - Simple rules'''
###############


######RUN CODE###
from sklearn.model_selection  import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm , cross_validation

get_dummy(X,y)
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,y, test_size=0.4)
#clf = LogisticRegression()
X_train = X_train[:,:-2]
Z_train = X_train[:,-2:]

X_test = X_test[:,:-2]
Z_test = X_test[:,-2:]

#%%
clf = svm.SVC()
#clf = LogisticRegression()
clf.fit(X_train,Y_train)


clf.fit(X_train,Y_train)
print('SVM Score:\n',round(clf.score(X_test,Y_test),2))
y_predict = clf.predict(X_test)

print('Run Backtest:')
run_backtest(Y_test,y_predict,Z_test)