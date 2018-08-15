import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style



def plot_df(df=None,figsize=(15,10), legend=True, lim=None):
    plt.figure(figsize=figsize)
    plt.title("The 'Absolute Difference' Perfomance")
    try:
        for ticker in df.Ticker.unique():
            plot_df = df[df['Ticker']==ticker]
            if plot_df['Absolute_Stock_Perfomance'].max() > lim:
                continue
            plot_df = plot_df.set_index(['Date'])
            if plot_df['Absolute_Stock_Perfomance_Flag'][-1]>0:
                color = 'g'
            else:
                color = 'r'

            plot_df['Absolute_Stock_Perfomance'].plot(label=ticker,color=color)
            ax = plt.gca()
            if legend:
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        line_df = pd.Series([0]*df[df['Ticker']=='AAPL'].shape[0]*1.8)
        line_df.plot(color='w')
        plt.ylabel('Absolute_Stock_Perfomance')
        plt.xlabel('Time')
    except:
        pass