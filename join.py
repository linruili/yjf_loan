import pandas as pd
import numpy as np

xlsx_File = pd.ExcelFile('tmp_src_ns_order_info.xlsx')
src_ns_order_info = xlsx_File.parse('Sheet1')    #40605
xlsx_File = pd.ExcelFile('tmp_src_ns_order_info_withhold_history.xlsx')
src_ns_order_info_withhold_history = xlsx_File.parse('Sheet1')     #86223
xlsx_File = pd.ExcelFile('tmp_src_ns_installment.xlsx')
src_ns_installment = xlsx_File.parse('Sheet1')    #40605

all = pd.merge(src_ns_order_info, src_ns_order_info_withhold_history)
all1 = pd.merge(all, src_ns_installment, left_on='customer_contract_no', right_on='contract_no')
all2 = all1.loc[:,['customer_user_id', 'customer_contract_no','installment_repay_type', 'total_times',\
                   'order_no','order_period', 'order_amount', 'withhold_send_time', 'withhold_status']]

all3 = all2.sort_values(by=['customer_user_id', 'customer_contract_no', 'order_no', 'withhold_send_time'])
all4 = all3[(all3.withhold_status != 'INIT')&(all3.withhold_status != 'WITHHOLD_CANCEL')&(all3.withhold_status != 'CALC')]

all4.to_excel('all.xlsx', index=False)