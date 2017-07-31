#计算满足以下条件的用户个数：每个合同都是可判断的
import pandas as pd
import numpy as np
import datetime

overdue_day=5

def f5(arr):
    #如果有超过overdue_day的连续失败次数，则逾期；否则，每期最后成功的为正样本;其余为nan
    arr['contract_isOverdue'] = np.nan
    arr['withhold_send_time'] = arr['withhold_send_time'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    arr = arr.sort_values(by=['withhold_send_time'])
    flag = False
    start_day = arr.loc[arr.index[0],'withhold_send_time']
    for j in range(len(arr.index)):
        i = arr.index[j]
        if arr.loc[i,'withhold_status'] == 'WITHHOLD_SUCCESS':
            flag = False
            if i!=arr.index[0] and arr.loc[arr.index[j-1], 'withhold_send_time']=='WITHHOLD_FAIL':
                if (arr.loc[i,'withhold_send_time']-arr.loc[arr.index[j-1], 'withhold_send_time']).days > 10:
                    return arr
        else:
            cur_time = arr.loc[i,'withhold_send_time']
            if not flag:
                start_day = cur_time
            if (cur_time - start_day).days > overdue_day:
                arr['contract_isOverdue'] = 1
                return arr
    if arr.contract_isOverdue.isnull().any() and arr.loc[i,'withhold_status']=='WITHHOLD_SUCCESS':
        arr['contract_isOverdue'] = 0
    return arr

def f6(arr):
    a = arr.value_counts()
    if len(arr.value_counts())==0:
        return 0
    return len(arr)==a[0]

xlsx_File = pd.ExcelFile('test.xlsx')
all = xlsx_File.parse('Sheet1')


all = all.drop(['installment_repay_type','order_period','total_times','order_amount','memo'], axis=1)
all = all.dropna(how='any')
all = all.reset_index(drop=True)


contract_isOverdue = all.groupby('customer_contract_no').apply(f5)
contract_isOverdue = contract_isOverdue[['customer_user_id', 'customer_contract_no','contract_isOverdue']]
#contract_isOverdue.columns=[customer_user_id  customer_contract_no  contract_isOverdue]
contract_isOverdue = contract_isOverdue.drop_duplicates().reset_index(drop=True)
useful_id = contract_isOverdue.groupby('customer_user_id')['contract_isOverdue'].agg(f6)
useful_id = pd.DataFrame({useful_id.index.name:useful_id.index, 'is_useful':useful_id.data}, index=range(len(useful_id)))
print(useful_id['is_useful'].value_counts())