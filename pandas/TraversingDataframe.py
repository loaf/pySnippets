#coding=utf-8

import pandas as pd


'''
f = open('../../Quant/stock/Data/SZ/000835.SZ.CSV')
df = pd.read_csv(f)

i=1
j=1
#按行遍历
for ix,row in df.iterrows():
   i=i+1
print(i)

#按列遍历
for ix,col in df.iteritems():
    j=j+1
print(j)

#对每列操作
for i in df.columns:
    print(df[i].max())

#对每行操作
for i in range(0,len(df)):
    print(df.iloc[i]['最高价(元)']/df.iloc[i]['开盘价(元)'])
'''

def _map(data, exp):
    for index, row in data.iterrows():   # 获取每行的index、row
        for col_name in data.columns:
            row[col_name] = exp(row[col_name]) # 把结果返回给data
    return data

def _1map(data, exp):
    _data = [[exp(row[col_name])               # 把结果转换成2级list
             for col_name in data.columns]
             for index, row in data.iterrows()
            ]
    return _data


if __name__ == "__main__":
    inp = [{'c1':10, 'c2':100}, {'c1':11,'c2':110}, {'c1':12,'c2':120}]
    df = pd.DataFrame(inp)

    temp = _map(df, lambda ele: ele+1 )
    print(temp)

    _temp = _1map(df, lambda ele: ele+1)
    res_data = pd.DataFrame(_temp)         # 对2级list转换成DataFrame
    print(res_data)
