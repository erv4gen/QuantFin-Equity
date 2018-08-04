#%%
import sys
sys.path.append('c:/pjt/QuantFin-Equity/source/libs/')
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from matplotlib import pyplot , style
style.use('dark_background')
import seaborn as sns
import General ,PlotFunctions , DataAcquisition
%matplotlib inline



#%%
df = get_data_local()
df.columns
df = df[df > -100.]
df = df[df.Absolute_Stock_Perfomance<200]
vdf = df[['Alpha',
       'Assets',
        'Liabilities',
         'Dividend per share',
        'ROE',
       'YtY_Stock_Price_Value_Change',
        'P/E ratio',
       'Absolute_Stock_Perfomance',
        'P/B ratio',
       'YtY_Stock_Perfomance',
        'Dividend payout ratio',
        'Free cash flow per share',
        'Absolute_Stock_Perfomance_Flag']]
        

vdf = vdf.replace('None',np.nan).dropna(axis=0)
vdf = vdf.astype(float)
vdf.dtypes

#%%
PlotFunctions.plot_df(vdf,figsize=(10,15))
sns.jointplot(vdf['ROE'],vdf['Absolute_Stock_Perfomance'],alpha=0.4,size=17)
pd.plotting.scatter_matrix(vdf,figsize=(45,40),c='blue')
ax= vdf[['Absolute_Stock_Perfomance','YtY_Stock_Price_Value_Change']].plot.box(figsize=(20,20))

