#%%
import sys
sys.path.append('c:/pjt/QuantFin-Equity/source/libs/')
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score
from matplotlib import pyplot , style
style.use('dark_background')
import seaborn as sns


def get_features(features=['P/B ratio',
                          'ROE'],dropna=True, local=True, con_man=True):
    import General
    from sklearn.preprocessing import StandardScaler

    sscaller = StandardScaler()

    if local:
        df = General.get_data_local(con_man=con_man)
    else:
        df = General.get_data_sql()
    if dropna:
        df.replace({-99999.00:None},inplace=True)
        df = df.replace('None',np.nan).dropna(axis=0)
        df.dropna(how='any',inplace=True)
    

    y = np.array(df['Absolute_Stock_Perfomance_Flag'])
    Z = np.array(df['Alpha'])
    df = df[features]
    df = df.astype(float)
    X = np.array(df.values)
    
    X = sscaller.fit_transform(X)
    return X, y , Z



X,y, Z = get_features()

'''First Run - Simple rules'''
###############
#%%
from sklearn.dummy import DummyClassifier
strategy = ['stratified','most_frequent','uniform']

for start in strategy:
    dummyc = DummyClassifier(strategy=start)
    dummyc.fit(X,y)
    print(start,': Dummy Score:',round(dummyc.score(X,y),2))

#%%
from sklearn.model_selection  import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm , cross_validation

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,y, test_size=0.4)
#clf = LogisticRegression()

clf = svm.SVC()
#clf = LogisticRegression()
clf.fit(X_train,Y_train)


clf.fit(X,y)
print('SVM Score:\n')
clf.score(X_test,Y_test)
