# coding=utf-8
# Token=728e54671e5284ce12bb098ea5d481b266570256d5430b53750093af

import tushare as ts

ts.set_token('728e54671e5284ce12bb098ea5d481b266570256d5430b53750093af')
pro=ts.pro_api()
#df=pro.query('daily',ts_code='000835.SZ',start_date='20170101',end_date='20180801')
df=ts.get_hist_data('000835')
print(df)
#df.to_csv('..\\..\\Quant\\stock\\Data\\NewDown\\000835.sz.csv')