import pandas as pd
import numpy as np
import datetime

overdue_day=5

def f1(arr):
    #日期最大最小值相差超过overdue_day的，返回1
    arr = arr.apply(lambda x:datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    days = (arr.max() - arr.min()).days
    if days>overdue_day:
        return 1
    else:
        return 0

def f2(arr):
    #若合同中有订单逾期，返回1
    if sum(arr['isOverdue']) >= 1:
        return 1
    else:
        return 0

xlsx_File = pd.ExcelFile('all.xlsx')
all = xlsx_File.parse('Sheet1')    #40605

auto = all[all.installment_repay_type=='AUTO']
auto = auto.drop(['installment_repay_type', 'total_times','order_period','order_amount'], axis=1)
auto = auto.dropna(how='any')


contract_num = auto.groupby('customer_user_id')['customer_contract_no'].count()
#convert Series to DataFrame.  columns=[contract_num ,customer_user_id]
contract_num = pd.DataFrame({contract_num.index.name:contract_num.index, 'contract_num':contract_num.data}, index=range(len(contract_num)))



overdue = auto['withhold_send_time'].groupby(auto['order_no']).agg(f1)
#convert Series to DataFrame.  columns=[order_no ,order_isOverdue]
overdue = pd.DataFrame({overdue.index.name:overdue.index, 'order_isOverdue':overdue.data}, index=range(len(overdue)))

tmp = auto.loc[:,['customer_contract_no','order_no']]
contract_overdue = pd.merge(tmp, overdue)
contract_overdue = contract_overdue.groupby('customer_contract_no')['order_isOverdue'].sum()
#columns=[contract_isOverdue, customer_contract_no]
contract_overdue = pd.DataFrame({contract_overdue.index.name:contract_overdue.index,'contract_isOverdue':contract_overdue.data}, \
                                index=range(len(contract_overdue)))


#auto_result1.columns=[customer_user_id,  customer_contract_no,  contract_isOverdue]
tmp = auto.loc[:,['customer_user_id','customer_contract_no']]
auto_result1 = pd.merge(tmp, contract_overdue)
auto_result1 = auto_result1.drop_duplicates()
auto_result1 = auto_result1.reset_index(drop=True)
auto_result1.loc[auto_result1['contract_isOverdue']>0, 'contract_isOverdue'] = 1
print(auto_result1)
auto_result1.to_excel('auto_result1.xlsx', index=False)

#auto_result2.columns=['customer_user_id', 'contract_num', 'contract_overdue_num']
contract_overdue_num = auto_result1.groupby('customer_user_id')['contract_isOverdue'].sum()
contract_overdue_num = pd.DataFrame({contract_overdue_num.index.name:contract_overdue_num.index,\
                                     'contract_overdue_num':contract_overdue_num.data}, index=range(len(contract_overdue_num)))
auto_result2 = pd.merge(contract_num, contract_overdue_num)
auto_result2 = auto_result2[['customer_user_id', 'contract_num', 'contract_overdue_num']]
print(auto_result2)
auto_result2.to_excel('auto_result2.xlsx', index=False)



