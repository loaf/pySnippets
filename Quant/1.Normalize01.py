# coding=utf-8
# 归一化原始数据，从文本文件，将数据处理后，存入数据库

import os
import pandas as pd

dataPath='../../Quant/stock/Data/Test'
ProcessedPath='../../Quant/stock/Data/Nop' #归一化后的目录


anyPreData2D=[] #记录任意一点的前5天数据形成的2维数组

def getDataFrame(fileName):
    f=open(fileName)
    df=pd.read_csv(f,usecols=[0,1,2,4,5,6,7,12,13,20,21]) #0代码 1简称 2日期 4开盘 5最高 6 最低 7收盘 12均价 13 换手率 20市盈 21市净
    return  df

def clearData(data):
    #清洗数据
    data=data.dropna() #删除数据中有NaN的
    data = data.drop_duplicates() #删除重复的行
    data.sort_values(by=['日期']) #以日期排序
    data = data.reset_index(drop=True) #重编索引号
    return data



if __name__ == "__main__":
    for f in os.listdir(dataPath):
        NormalizeDF=[]
        fi = os.path.join(dataPath, f)

        if os.path.isdir(fi) or os.path.splitext(f)[1] != ".CSV":
            continue

        if os.path.exists(os.path.join(ProcessedPath, f)):
            continue

        df = getDataFrame(fi)
        df = clearData(df)
        #df.to_csv('../../temp1.csv', index=True, header=True)

        for i in range(0, len(df)):
            NormalizeList=[df.iloc[i]['代码']]
            NormalizeList.append(df.iloc[i]['简称'])
            NormalizeList.append(df.iloc[i]['日期'])
            NormalizeList.append((df.iloc[i]['最高价(元)'] - df.iloc[i]['开盘价(元)']) / df.iloc[i]['开盘价(元)'])
            NormalizeList.append((df.iloc[i]['最低价(元)'] - df.iloc[i]['开盘价(元)']) / df.iloc[i]['开盘价(元)'])
            NormalizeList.append((df.iloc[i]['收盘价(元)'] - df.iloc[i]['开盘价(元)']) / df.iloc[i]['开盘价(元)'])
            NormalizeList.append(df.iloc[i]['均价(元)'])
            NormalizeList.append(df.iloc[i]['换手率(%)'])
            NormalizeList.append(df.iloc[i]['市盈率'])
            NormalizeList.append(df.iloc[i]['市净率'])

            NormalizeDF.append(NormalizeList)


        dfAny = pd.DataFrame(NormalizeDF)
        dfAny.to_csv(os.path.join(ProcessedPath, f), index=False, header=True)


