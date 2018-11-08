#coding=utf-8

import pandas as pd
import numpy as np

f=open('../../Quant/stock/dele/1.CSV')
df=pd.read_csv(f)

df=df.dropna() #删除数据中有NaN的
df = df.drop_duplicates() #删除重复的行
df.sort_values(by=['date']) #以日期排序
df = df.reset_index(drop=True) #重编索引号


print(df)
print(np.argmax(df.values,axis=0))
print(np.argmin(df.values,axis=0))
