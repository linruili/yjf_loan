import pandas as pd
import numpy as np
import time
import datetime
import re



xlsx_File = pd.ExcelFile('all.xlsx')
all = xlsx_File.parse('Sheet1')

all = all[all.order_amount.apply(int) > 50]
all = all.reset_index(drop=True)


test = all.loc[:1000,:]

all.to_excel('all.xlsx', index=False)
test.to_excel('test.xlsx', index=False)