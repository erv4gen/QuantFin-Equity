import time , os ,re , ipdb
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup
import quandl
from time import mktime
import numpy as np


import ipdb

def quandl_stocks_host_price(symbol, date='2008-01-02', n=20):
    """
    ===---This function returns the Historical quotes of the selected ticket---===
    
    symbol is a string representing a stock symbol, e.g. 'AAPL'
 
    start_date and end_date are tuples of integers representing the year, month,
    and day
 
    end_date defaults to the current date when None
    """
    #ipdb.set_trace()
    print('Getting quots \nTicker: ',symbol,'\nDate: ',date)
    quandl.ApiConfig.api_key = open('c:\data\quandl\cred.txt','r').read()
    query_list = 'WIKI' + '/' + symbol
    def get_quote(date):
        responce = quandl.get(query_list, 
                returns='pandas', 
                start_date=date,
                end_date=date,
                collapse='daily',
                order='asc'
                )
        return responce
    
    for i in range(n):
        try:
            responce = get_quote(date)
        except:
            responce = np.array([])
        if responce.shape[0]==0:
            print('Wrong Day, Cheching Next')
            date = [int(x) for x in date.split('-')] 
            if date[2]<28:
                date[2] +=1
            else:
                date[2] -=2
            date = '-'.join([str(x) for x in date])
        else:
            print('Quote Loaded')
            break
            
    if responce.shape[0]==0:
        print('Reached Limit amount of tries')
        raise ValueError('Data not found for this day(weekend adj.)')
    else:
        return responce['Adj. Close'].item()

    
    
    
def GetStats(gathers = None,path='', limit = None):
    '''
    This function Return Finance multiplicators from all snp500 stocks
    input : gathers = ['var1', 'var2','var3', ...] ; limit = for test only ; path = path to dataset 
    ouptut : Pandas dataframe with columns ['Date','Unix Time', ' Ticket','var1', 'var2','var3',..]
    
    '''
    if not gathers:
        print("input gathers as a list")
        return None
    #INIT Data##################
    columns = ['Date',
                'UNIX',
                'Ticker']
    columns.extend(gathers)
    
    print(*gathers,sep=',')
    stock_files = path+ '_KeyStats'
    stock_list = [x[0] for x in os.walk(stock_files)]
    df = pd.DataFrame(columns=columns)
    
    #print(stacks_list)
    amount_of_files = len(stock_list[1:])
    if limit:
        print("Limit set to:", limit)
    else:
        print("Will Crowl All dataset")
    counter = -1
    
    ##################
    
    #Go through Each Ticker (folder)
    for each_dir in tqdm(stock_list[1:]):
        counter +=1
        if limit==counter:
            break
        ticker = each_dir.split('\\')[-1]
        print('Start working with: ',ticker)
        each_file = os.listdir(each_dir)
        
        if len(each_file)>0:
            #Get all historic data 
            for file in each_file:
                
                date_stamp = datetime.strptime(file,'%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_path_file = each_dir +'\\'+file
                with open(full_path_file,'r') as f:
                    source =f.read()
                soup = BeautifulSoup(source, 'html.parser')
                data = []
                rows = soup.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    data.extend([cell.text for cell in cols])
                try:
                    values = {}

                    for gather in gathers:
                        try:
                            def match(x, gather):
                                try:
                                    if re.match('^%s' % gather, x).group() is not None:
                                        return True
                                    else:
                                        return False
                                except:
                                    #if 'DE Ratio' not in gather and gather in x:
                                        #ipdb.set_trace()
                                    return False
                            element = [x for x in data if match(x,gather)][0]
                            value = data[data.index(element)+1]
                            if '%' in value:
                                value = float(value.strip('%')) / 100.
                            else:
                                value = float(value)
                            values[gather] = value
                        except Exception as e: 
                            values[gather] = -99999.0
                    
                    #Get stock price for spesific date
                    new_row = {**{'Date':date_stamp,
                                    'UNIX':unix_time,
                                    'Ticker':ticker,
                                   },**values}
                    df = df.append(new_row,ignore_index=True)
                except Exception as e:
                    print(e)
    return df





def get_stock_perfomance(symbol=None,date_range=None,snppath=r'c:\data\Datasets\intraQuarter\YAHOO-INDEX_GSPC.csv',delta = 31556926):
    '''Return the historic stock price of selected ticker
    input: symbol = 'ABC' ; date_range = pd.Series of dates in UNIX format
    if input date is weekend will return closest workday.
    
    output: pd.Dataframe of stock prices and SNP500 index perfomance.
    
    '''
    df = pd.DataFrame(columns=[
                               'Ticker',
                                'UNIX',
                              'SNPDate',
                              'SNPValue',
                              'StockPrice',
                               'Absolute_SNP500_Perfomance',
                               'YtY_Stock_Price_Value_Change',
                               'YtY_SNP500_Value_Change',
                                'Absolute_Stock_Perfomance',
                               'Absolute_Stock_Perfomance_Flag',
                                'YtY_Stock_Perfomance',
                               'YtY_Stock_Perfomance_Flag',
                                'Stock_Future_Value',
                                'SNP500_Future_Value',
                                'Stock_Future_Pefomance',
                                'SNP500_Future_Perfomance',
                                'Alpha',
                                'Investable_Flag'        
     
                              ])
    starting_stock_value = False
    starting_sp_500_value = False
    i = 0
    snp500 = pd.read_csv(snppath, index_col=0)

    print("Getting Stock Price Data...")
        
    for unix_time in tqdm(date_range):
            
        try:
            print('Getting Original Date')
            unix_time_current = unix_time
            while datetime.fromtimestamp(unix_time_current).weekday() > 4:
                print('Pointing Current Date is - ',datetime.fromtimestamp(unix_time_current).weekday(),'(Day of the week)\nChecking Next Day')
                #ipdb.set_trace()
                unix_time_current += 86400
            snp500_data_current = datetime.fromtimestamp(unix_time_current).strftime('%Y-%m-%d')
            row = snp500[snp500.index==snp500_data_current]
            snp500_value_current = float(row['Adj Close'])
            stock_price_current = quandl_stocks_host_price(symbol=symbol,date=snp500_data_current)
            
            
            unix_time_future = unix_time_current + delta            
            
            try:
                if unix_time_future > (time.time()-86400):
                    raise Exception('Cannot see the future')
                while datetime.fromtimestamp(unix_time_future).weekday() > 4:
                    print('Pointing Future Date is - ',datetime.fromtimestamp(unix_time_future).weekday(),'(Day of the week)\nChecking Next Day')
                    #ipdb.set_trace()
                    unix_time_future -= 86400
                snp500_data_future = datetime.fromtimestamp(unix_time_future).strftime('%Y-%m-%d')
                row = snp500[snp500.index==snp500_data_future]
                snp500_value_future = float(row['Adj Close'])
                stock_price_future = quandl_stocks_host_price(symbol=symbol,date=snp500_data_future)
            except Exception as e:
                print(e)
                snp500_value_future = -1
                stock_price_future = -1

            
        except:
            print('Cannot Get data from Quandl. Skipping this one')
            snp500_value_future = -1
            stock_price_future = -1
            snp500_value_current = -1
            stock_price_current = -1
        
        
        if not starting_stock_value and not starting_sp_500_value:
            stock_change_abs = 0
            snp500_change_abs = 0
            
            yty_pr_change = 0
            yty_snp_change = 0
            abs_stock_perf_flag = 0
            yty_perf_flag = 0
            
            starting_sp_500_value = snp500_value_current
            starting_stock_value = stock_price_current
            
        else:
            stock_change_abs = 100*(stock_price_current -starting_stock_value) / starting_stock_value #absolute stock change 
            snp500_change_abs = 100*(snp500_value_current - starting_sp_500_value) / starting_sp_500_value # absoulte snp500 change
            
            yty_pr_change = 100*(stock_price_current -df.loc[i-1,'StockPrice']) / df.loc[i-1,'StockPrice'] #'YtY Stock Price Value Change'
            yty_snp_change = 100*(snp500_value_current -df.loc[i-1,'SNPValue']) / df.loc[i-1,'SNPValue'] #'YtY SNP500 Value Change'
        
        #'Absolute Difference - abs price perfomance minus abs snp500 perfomance'
        abs_difference_in_perfomance_pr_vs_snp = stock_change_abs-snp500_change_abs
        #'YearToYear Difference - yty price % change minus yty snp500 % change
        YtYDifference_in_perfomance_pr_vs_snp = yty_pr_change - yty_snp_change
        
        abs_stock_perf_flag =  int(np.where( (stock_change_abs-snp500_change_abs)>0,1,0 ))#'Absolute Stock Perfomance Comparing to SNP500 Index Flag - 1 if outperfom snp500 ; 0 is underperform',
        yty_perf_flag =  int(np.where( (yty_pr_change -yty_snp_change) >0 , 1,0 )) #'YtY Stock Perfomance Flag - 1 if outperfom snp500 ; 0 is underperform'
        
        #Current_to_future_stock_change = (
        
        stock_change_abs_funure  = (stock_price_future - stock_price_current) / stock_price_current
        snp500_change_abs_future = (snp500_value_future - snp500_value_current) / snp500_value_current
        alpha = stock_change_abs_funure - snp500_change_abs_future
        investable = np.where((stock_change_abs_funure - snp500_change_abs_future) >0,1,0) #1 - outperform, 0 - ounderperform
        df = df.append({'Ticker': symbol,
                        'UNIX': unix_time,
                      'SNPDate' :snp500_data_current,
                      'SNPValue' : snp500_value_current,
                      'StockPrice' : stock_price_current,
                       'Absolute_Stock_Perfomance' :stock_change_abs ,
                       'Absolute_SNP500_Perfomance' : snp500_change_abs,
                       'YtY_Stock_Price_Value_Change' : yty_pr_change,
                       'YtY_SNP500_Value_Change': yty_snp_change,
                        'Absolute_Stock_Perfomance': abs_difference_in_perfomance_pr_vs_snp,
                       'Absolute_Stock_Perfomance_Flag': abs_stock_perf_flag,
                         'YtY_Stock_Perfomance': YtYDifference_in_perfomance_pr_vs_snp,
                       'YtY_Stock_Perfomance_Flag' : yty_perf_flag,
                        'Stock_Future_Value': stock_price_future,
                        'SNP500_Future_Value': snp500_value_future,
                        'Stock_Future_Pefomance': stock_change_abs_funure,
                       'SNP500_Future_Perfomance': snp500_change_abs_future,
                       'Alpha': alpha,
                       'Investable_Flag':investable},
                       ignore_index=True)
        i+=1
    save = r"c:\data\finml\PriceVsSNP500_"+str(symbol)+".csv"
    print('Will save to file: ',save)
    df.to_csv(save,index=False)
    return df





