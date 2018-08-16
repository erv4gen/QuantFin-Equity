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
            snp500 =  plot_df[['SNPDate', 'SNPValue']]
            if plot_df['Absolute_Stock_Perfomance_Flag'][-1]>0:
                color = 'g'
            else:
                color = 'r'
            plot_df['Absolute_Stock_Perfomance'].plot(label=ticker,color=color)
            ax = plt.gca()
            if legend:
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        line_df = pd.Series([0]*plot_df.shape[0])
        
        line_df.plot(color='grey')
        xmin, xmax = ax.get_xlim()
        ax2 = ax.twinx()
        
        #import pdb
        #pdb.set_trace()
        line2 = ax2.plot(snp500['SNPDate'],
                         snp500['SNPValue'],
                     '-o',
                    color ='b',
                         linewidth=5)
        ax.axhline(linewidth=2, color="w") 
        ax2.axhline(linewidth=2, color="w")
        
        for item in ax.xaxis.get_ticklabels():
            item.set_rotation(70)
        #ax2.set_ylim([-10,2000])
        plt.ylabel('Absolute_Stock_Perfomance')
        plt.xlabel('Time')
    except:
        pass