import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style



def plot_df(df,figsize=(15,10)):
    plt.figure(figsize=figsize)
    plt.title("The 'Absolute Difference' Perfomance")
    try:
        for ticker in df.Ticker.unique():
            plot_df = df[df['Ticker']==ticker]
            plot_df = plot_df.set_index(['Date'])
            if plot_df['Absolute_Stock_Perfomance_Flag'][-1]>0:
                color = 'g'
            else:
                color = 'r'

            plot_df['Absolute_Stock_Perfomance'].plot(label=ticker,color=color)
            ax = plt.gca()
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.ylabel('Absolute Difference')
    except:
        pass