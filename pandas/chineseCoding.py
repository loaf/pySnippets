#coding=utf-8

import pandas as pd

f=open('../../Quant/stock/Data/SZ/000835.SZ.CSV')
df=pd.read_csv(f,encoding="gbk")

print(df.head(3))
print(df.loc[0:3,[u"简称",u"开盘价(元)"]])

'''
一般CSV中如果有中文，一般是GBK格式，不是UTF8,所以直接用read_csv()会出现乱码，但在加上encoding=就可以了
而如果用中文列名，需要将utf-8，也转成gbk，用u在中文前即可，
但是python2和3不同，如果是3的话，不需要加encoding，也不需要在中文前加上u
'''