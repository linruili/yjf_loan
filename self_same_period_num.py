#判断每个合同，总共多少期，期数判断相同的多少期
import pandas as pd
import numpy as np
import datetime


def f12(arr):
    total_period = 0
    same_period_num = 0
    for j,i in enumerate(arr.index):
        if j==0:
            total_period += 1
            if arr.loc[i, 'period_is_same']==1:
                same_period_num += 1
        elif arr.loc[i,'my_period'] != arr.loc[arr.index[j-1],'my_period']:
            total_period += 1
            if arr.loc[i, 'period_is_same']==1:
                same_period_num += 1
    arr['total_period'] = total_period
    arr['same_period_num'] = same_period_num
    return arr

xlsx_File = pd.ExcelFile('self_period.xlsx')
period_is_same = xlsx_File.parse('Sheet1')

period_is_same = period_is_same.drop(['Unnamed: 2'], axis=1)
period_is_same = period_is_same.fillna(method='ffill')

same_period_num = period_is_same.groupby(['customer_user_id','customer_contract_no']).apply(f12)
same_period_num = same_period_num[['customer_user_id','customer_contract_no','total_period','same_period_num']]
same_period_num = same_period_num.drop_duplicates()
same_period_num = same_period_num.reset_index(drop=True)

same_period_num.to_excel('self_same_period_num.xlsx', index=False)
print(same_period_num['total_period'].sum())
print(same_period_num['same_period_num'].sum())
print(same_period_num['same_period_num'].sum()/same_period_num['total_period'].sum())