# coding=utf-8
import pandas as pd
# import os
import time

rTP=1.0 # Take Profit止盈为100%，相当于翻了一倍
rSL=0.1 # Stop loss止损 10%
PreDay=5 #前置天数

anyPreData2D=[] #记录任意一点的前5天数据形成的2维数组


def getDataFrame(fileName):
    f=open(fileName)
    df=pd.read_csv(f,usecols=[0,2,4,5,6,7,12,13])
    return  df

def clearData(data):
    #清洗数据
    data=data.dropna() #删除数据中有NaN的
    data = data.drop_duplicates() #删除重复的行
    data.sort_values(by=['日期']) #以日期排序
    data = data.reset_index(drop=True) #重编索引号
    return data

def searchInPoint(data,ix):  #验证此点是否有效的入市点，如果是，找出有效的出市点并记录
    #curTime = data.iloc[i]['日期']
    rn=-1
    curPrice = data.iloc[i]['收盘价(元)']
    j=ix+1
    while j<len(data):
        if (data.iloc[j]['收盘价(元)']-curPrice)/curPrice < -rSL:
            break

        if (data.iloc[j]['收盘价(元)']-curPrice)/curPrice >= rTP:
            rn=searchOutPoint(data,j)
            break

        j=j+1

    return rn

def searchOutPoint(data,ix): #从当前点按动态止赢的方法查找有效的出市点
    j=ix
    while j<len(data)-1:
        avg = (data.iloc[j - 1]['收盘价(元)'] + data.iloc[j - 2]['收盘价(元)'] + data.iloc[j - 3]['收盘价(元)'] +
               data.iloc[j - 4]['收盘价(元)'] + data.iloc[j - 5]['收盘价(元)']) / 5
        if data.iloc[ix]['收盘价(元)']<=avg:
            break
        j=j+1
    return j


def savePre_N_data(data,ix): #将当前点前5天的数据保存下来
    PreDataList=['Any']
    PreDataList.append(data.iloc[ix]['代码'])
    PreDataList.append(data.iloc[ix]['日期'])
    PreDataList.append(ix)
    PreDataList.append(0)
    for i in list(range(PreDay,0,-1)):
        PreDataList.append(data.iloc[ix - i]['开盘价(元)'])
        PreDataList.append(data.iloc[ix - i]['最高价(元)'])
        PreDataList.append(data.iloc[ix - i]['最低价(元)'])
        PreDataList.append(data.iloc[ix - i]['收盘价(元)'])
        PreDataList.append(data.iloc[ix - i]['均价(元)'])
        PreDataList.append(data.iloc[ix - i]['换手率(%)'])
    PreDataList.append(0)
    PreDataList.append(0)
    return PreDataList


if __name__ == "__main__":

    print('Begin:',time.strftime('%X',time.localtime(time.time())))

    df=getDataFrame('../../Quant/stock/Data/SZ/000835.SZ.CSV')
    df=clearData(df)
    df.to_csv('../../temp1.csv',index=True,header=True)

    outPreDataList=[]

    for i in range(PreDay, len(df)):
        curTime=df.iloc[i]['日期']
        curPrice=df.iloc[i]['收盘价(元)']

        outIX=searchInPoint(df,i)

        preDatalist=savePre_N_data(df,i)

        if outIX > 0:
            preDatalist[0]='IN'
            preDatalist[4]=outIX
            preDatalist[PreDay*6+5]=outIX-i
            preDatalist[PreDay*6+6]=(df.iloc[outIX]['收盘价(元)']-df.iloc[i]['收盘价(元)'])/df.iloc[i]['收盘价(元)']

        anyPreData2D.append(preDatalist)
    '''
    print('Begin update OutData:', time.strftime('%X', time.localtime(time.time())))

    outPreDataList=list(set(outPreDataList))#删除重复值
    for j in outPreDataList:
        anyPreData2D[outPreDataList[outPreDataList.index(j)]-5][0]='OUT'
    '''
    dfAny=pd.DataFrame(anyPreData2D)
    dfAny.to_csv('../../tempAny.csv', index=True, header=False)

    print('Over:', time.strftime('%X', time.localtime(time.time())))
