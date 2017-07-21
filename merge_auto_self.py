import pandas as pd
import numpy as np
import datetime


xlsx_File = pd.ExcelFile('auto_result2.xlsx')
auto_result2 = xlsx_File.parse('Sheet1')
xlsx_File = pd.ExcelFile('self_result2.xlsx')
self_result2 = xlsx_File.parse('Sheet1')

tmp = pd.merge(auto_result2, self_result2, on='customer_user_id', how='outer')
tmp = tmp.fillna(0)
tmp['contract_num'] = tmp['contract_num_x'] + tmp['contract_num_y']
tmp['contract_overdue_num'] = tmp['contract_overdue_num_x'] + tmp['contract_overdue_num_y']
#merged_result.columns=[customer_user_id  contract_num  contract_overdue_num  isCredible]
merged_result = tmp.drop(['contract_overdue_num_x', 'contract_overdue_num_y', 'contract_num_x', 'contract_num_y'], axis=1)

merged_result.loc[merged_result.contract_num>30, 'isCredible'] = 1
merged_result.loc[(merged_result.contract_overdue_num>1) | \
                  ((merged_result.contract_overdue_num==1) & (merged_result.contract_num<100)), 'isCredible'] = 0

print(merged_result['isCredible'].value_counts())

merged_result.to_excel('merged_result.xlsx', index=False)
