#计算期数，以及判断我的期数的给的期数是否一致
import pandas as pd
import numpy as np
import time
import datetime
import re

one_month = 28

def f10(arr):
    #计算期数
    arr['my_period'] = np.nan
    arr['withhold_send_time'] = arr['withhold_send_time'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    arr = arr.sort_values(by=['withhold_send_time'])
    arr = arr.reset_index(drop=True)
    cur_period = 0
    start_day, start_index = arr.loc[arr.index[0], 'withhold_send_time'], arr.index[0]
    flag = False
    for j, i in enumerate(arr.index):
        cur_time = arr.loc[i, 'withhold_send_time']
        if flag:
            start_index = i
            start_day = cur_time
            flag = False
        if arr.loc[i, 'withhold_status'] == 'WITHHOLD_SUCCESS':
            flag = True
            if (cur_time - start_day).days > one_month:
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
                start_index = i
                start_day = cur_time
            cur_period += 1
            arr.loc[start_index:i+1, 'my_period'] = cur_period
        else:
            if (cur_time - start_day).days > one_month:
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
                start_index = i
                start_day = cur_time
            elif j==len(arr.index)-1:
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
    return arr

def f10_complicate(arr):
    #计算期数
    #复杂版，连续的成功会当成一期
    arr['my_period'] = np.nan
    arr['withhold_send_time'] = arr['withhold_send_time'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    arr = arr.sort_values(by=['withhold_send_time'])
    arr = arr.reset_index(drop=True)
    cur_period = 0
    start_day, start_index = arr.loc[arr.index[0], 'withhold_send_time'], arr.index[0]
    last_start_day = arr.loc[arr.index[0], 'withhold_send_time']
    flag = False
    for j, i in enumerate(arr.index):
        cur_time = arr.loc[i, 'withhold_send_time']
        if flag:
            last_start_day = start_day
            start_index = i
            start_day = cur_time
            flag = False
        if arr.loc[i, 'withhold_status'] == 'WITHHOLD_SUCCESS':
            flag = True
            # if start_day != last_start_day and (cur_time - last_start_day).days <= one_month:
            #     cur_period -= 1
            #     flag = False
            if arr.loc[arr.index[j-1], 'withhold_status']=='WITHHOLD_FAIL' and \
                            (cur_time - arr.loc[arr.index[j-1], 'withhold_send_time']).days > one_month:
                #处理【失败失败（1个月）成功】的情况
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
                last_start_day = start_day
                start_index = i
                start_day = cur_time
                flag = False
            else:
                cur_period += 1
                arr.loc[start_index:i+1, 'my_period'] = cur_period
        else:
            if (j!=0 and (cur_time - arr.loc[arr.index[j-1], 'withhold_send_time']).days>one_month/2 and arr.loc[arr.index[j-1], 'withhold_status']!='WITHHOLD_SUCCESS' )\
                    or (cur_time - start_day).days > one_month:
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
                last_start_day = start_day
                start_index = i
                start_day = cur_time
            elif j==len(arr.index)-1:
                cur_period += 1
                arr.loc[start_index:i, 'my_period'] = cur_period
    return arr

def f11(arr):
    #判断my_period和order_period的一致性
    arr = arr.reset_index(drop=True)
    for i in arr.index:
        arr.loc[i,'period_is_same'] = 1
        if i==0 or arr.loc[i,'my_period']!=arr.loc[i-1,'my_period']:
            if i != 0 and flag == False:
                arr.loc[start_index:i, 'period_is_same'] = 0
            start_index = i
            flag = True

        if i!=0 and arr.loc[i,'my_period']==arr.loc[i-1,'my_period']:
            if arr.loc[i, 'order_period'] != arr.loc[i-1, 'order_period']:
                flag = False
    if flag==False:
        arr.loc[start_index:i+1 , 'period_is_same'] = 0
    return arr

xlsx_File = pd.ExcelFile('all.xlsx')
all = xlsx_File.parse('Sheet1')

self = all[all.installment_repay_type=='SELF_REPAY']
self = self.drop(['installment_repay_type','total_times','memo'], axis=1)
self = self.dropna(how='any')
self = self.reset_index(drop=True)
self['order_period'] = self['order_period'].apply(lambda x: re.split('-',x)[-1])

my_period = self.groupby(['customer_user_id','customer_contract_no']).apply(f10)
my_period = my_period[['customer_user_id','customer_contract_no','my_period','order_period','withhold_send_time','withhold_status','order_amount']]
my_period = my_period.reset_index(drop=True)


period_is_same = my_period.groupby(['customer_user_id','customer_contract_no']).apply(f11)
period_is_same = period_is_same[['my_period','order_period','period_is_same','withhold_send_time','withhold_status','order_amount']]
period_is_same.to_excel('self_period.xlsx')

