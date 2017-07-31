
import pandas as pd
import numpy as np
import datetime

xlsx_File = pd.ExcelFile('self_same_period_num.xlsx')
self_same_period_num = xlsx_File.parse('Sheet1')

xlsx_File = pd.ExcelFile('self_days.xlsx')
self_days = xlsx_File.parse('Sheet1')

print(self_same_period_num['total_period'].value_counts())
# print(len(self_days) - self_days['first_day'].value_counts().iloc[0])
print(self_days['first_day'].value_counts())
