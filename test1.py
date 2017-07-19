import pandas as pd
import numpy as np
import time
import datetime

# xlsx_File = pd.ExcelFile('all.xlsx')
# all = xlsx_File.parse('Sheet1')    #40605
# a = all['withhold_send_time']
#
# for i in a.values:
#     if not isinstance(i, str):
#         print(i,type(i))

a = pd.Series([1,2,3], index=['a','b','c'])
print(type(a))
b = pd.DataFrame(a)
c = b.stack()

print(b)
print(c)