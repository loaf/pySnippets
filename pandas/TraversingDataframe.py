#coding=utf-8

import pandas as pd

f=open('../../Quant/stock/Data/SZ/000835.SZ.CSV')
df=pd.read_csv(f)

for i in d

disftance_list=[]
for i in range(0,len(df)):
    disftance_list.append(df.iloc[i]['最高价(元)']/df.iloc[i]['开盘价(元)'])
