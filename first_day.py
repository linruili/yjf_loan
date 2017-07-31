#计算每期的开始日

import pandas as pd
import datetime
import numpy as np
from collections import defaultdict

def f13(arr):
    #合同中每期开始日判断
    days = defaultdict(int)
    for j,i in enumerate(arr.index):
        if j==0 or arr.loc[i,'my_period'] != arr.loc[arr.index[j-1],'my_period']:
            day = arr.loc[i,'withhold_send_time'].day
            days[day] += 1
    days = sorted(days.items(), key=lambda item:item[1], reverse=True)
    if days[0][1] >= 2 and days[0][0]==arr.loc[arr.index[0], 'first_repay_day']:
        arr['first_day'] = days[0][0]
    elif days[0][1] < 2 and arr.loc[arr.index[0], 'first_repay_day']==arr.loc[arr.index[0],'withhold_send_time'].day:
        arr['first_day'] = arr.loc[arr.index[0], 'first_repay_day']
    else:
        arr['first_day'] = -1
    return arr

xlsx_File = pd.ExcelFile('self_period.xlsx')
period_is_same = xlsx_File.parse('Sheet1')
xlsx_File = pd.ExcelFile('tmp_src_ns_installment.xlsx')
installment = xlsx_File.parse('Sheet1')
installment = installment[['contract_no','first_repay_date']]
installment['first_repay_date'] = installment['first_repay_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
installment['first_repay_day'] = installment['first_repay_date'].apply(lambda x: x.day)
installment = installment.drop(['first_repay_date'], axis=1)

period_is_same = period_is_same.drop(['Unnamed: 2'], axis=1)
period_is_same = period_is_same.fillna(method='ffill')

period_is_same = pd.merge(period_is_same, installment, left_on='customer_contract_no', right_on='contract_no')
period_is_same = period_is_same.drop(['contract_no'], axis=1)

self_days = period_is_same.groupby(['customer_user_id','customer_contract_no']).apply(f13)
self_days = self_days[['customer_user_id','customer_contract_no','first_day']]
self_days = self_days.drop_duplicates()
self_days = self_days.reset_index(drop=True)


self_days.to_excel('self_days.xlsx', index=False)
