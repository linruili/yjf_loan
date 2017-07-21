import pandas as pd
import numpy as np
import datetime

overdue_day=5

def f3(arr):
    #以30天为一期划分，如果某期日期最大最小值相差超过overdue_day的，返回1
    arr = arr.apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    arr = arr.sort_values()
    start_day = arr.min()
    for cur_time in arr:
        if (cur_time-start_day).days > 20 :
            start_day = cur_time
        if (cur_time-start_day).days > overdue_day:
            return 1
    return 0


xlsx_File = pd.ExcelFile('all.xlsx')
all = xlsx_File.parse('Sheet1')    #40605

self = all[all.installment_repay_type=='SELF_REPAY']
self = self.drop(['installment_repay_type', 'total_times','order_period','order_amount'], axis=1)
self = self.dropna(how='any')


contract_num = self.groupby('customer_user_id')['customer_contract_no'].count()
#convert Series to DataFrame.  columns=[contract_num ,customer_user_id]
contract_num = pd.DataFrame({contract_num.index.name:contract_num.index, 'contract_num':contract_num.data}, index=range(len(contract_num)))



#overdue = self.loc[:,['withhold_send_time', 'withhold_status']].groupby(self['customer_contract_no']).agg(f3)
#columns=[contract_isOverdue, customer_contract_no]
contract_overdue = self['withhold_send_time'].groupby(self['customer_contract_no']).agg(f3)
contract_overdue = pd.DataFrame({contract_overdue.index.name:contract_overdue.index, \
                                 'contract_isOverdue':contract_overdue.data}, index=range(len(contract_overdue)))

tmp = self.loc[:,['customer_user_id','customer_contract_no']]
contract_overdue_num = pd.merge(tmp, contract_overdue)
contract_overdue_num = contract_overdue_num.groupby('customer_user_id')['contract_isOverdue'].sum()
#contract_overdue_num.columns=['customer_user_id', 'contract_overdue_num']
contract_overdue_num = pd.DataFrame({contract_overdue_num.index.name:contract_overdue_num.index,\
                                     'contract_overdue_num':contract_overdue_num.data}, index=range(len(contract_overdue_num)))

#self_result2.columns=['customer_user_id', 'contract_num', 'contract_overdue_num']
self_result2 = pd.merge(contract_num, contract_overdue_num)
self_result2 = self_result2[['customer_user_id', 'contract_num', 'contract_overdue_num']]
self_result2.to_excel('self_result2.xlsx', index=False)