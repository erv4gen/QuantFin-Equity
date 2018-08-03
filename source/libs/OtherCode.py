'''@timer
def Key_stats2(gather = 'Total Debt/Equity (mrq)',path=''):
    stock_files = path+ '_KeyStats'
    stock_list = [x[0] for x in os.walk(stock_files)]
    #print(stacks_list)
    for each_dir in stock_list[1:]:
        ticker = each_dir.split()
        each_file = os.listdir(each_dir)
        if len(each_file)>0:
            for file in each_file:
                date_stamp = datetime.strptime(file,'%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_path_file = each_dir +'\\'+file
                with open(full_path_file,'r') as f:
                    source =f.read()
                try:
                    value = source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                except IndexError:
                    print("error")

print(value)'''

