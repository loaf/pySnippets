# coding=utf-8
import pandas as pd

rTP=1.0 #Take Profit止盈为100%，相当于翻了一倍
rSL=0.1 #Stop loss止损 10%
PreDay=5 #前置天数
ValidSegment=[[]] #记录有效的段，由一个3元数组组成，一个是入口的ID，一个是出口的ID，一个是段的跨度n
PreData2D=[[]] #记录前5天的数据形成的2维数组
PreDataList=[] #前5天的数列


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
    curPrice = data.iloc[i]['收盘价(元)']
    j=ix+1
    while j<len(data):
        if (data.iloc[j]['收盘价(元)']-curPrice)/curPrice < -rSL:
            j=-1
            break

        if (data.iloc[j]['收盘价(元)']-curPrice)/curPrice > rTP:
            j=searchOutPoint(data,j)
            break
        j=j+1

    if j==len(data)-1: #如果直到最后一行，既不满足有效高度，又没有止损，可认为是无效的数据
        j=-1

    return j

def searchOutPoint(data,ix): #从当前点按动态止赢的方法查找有效的出市点
    j=ix
    while j<len(data)-1:
        avg = (data.iloc[j - 1]['收盘价(元)'] + data.iloc[j - 2]['收盘价(元)'] + data.iloc[j - 3]['收盘价(元)'] +
               data.iloc[j - 4]['收盘价(元)'] + data.iloc[j - 5]['收盘价(元)']) / 5
        if data.iloc[ix]['收盘价(元)']<=avg:
            break
        j=j+1
    return j

def SaveInOutPoint(InPoint,OutPoint):  #将入市点，出市点和间隔交易日记录下来
    ...
    return True

def SaveToInPointDatabase(): #将入市点前PreDay天的数据保存到待分析的材料库，可以根据上面的outTime和intervalDay为这些数据打上带权重的标签
    ...
    return True

def SaveToOutPointDatabase(): #将出市点前PreDay天的数据保存到待分析的材料库，分析出市的的前置规律，不过，因为规则已确定，有没有必要另说
    ...
    return True

if __name__ == "__main__":
    df=getDataFrame('../../Quant/stock/Data/SZ/000835.SZ.CSV')
    df=clearData(df)
    df.to_csv('../../temp1.csv',index=True,header=True)

    for i in range(5, len(df)):
        curTime=df.iloc[i]['日期']
        curPrice=df.iloc[i]['收盘价(元)']

        outIX=searchInPoint(df,i)

        if  outIX > 0:
            ValidSegment.append([i, outIX, outIX-i])

    for i in range(1,len(ValidSegment)): #第0行是空值

        IXinpoint=ValidSegment[i][0]
        IXoutpoint=ValidSegment[i][1]
        MaxHighRate=(df.iloc[IXoutpoint]['收盘价(元)']-df.iloc[IXinpoint]['收盘价(元)'])/df.iloc[IXinpoint]['收盘价(元)']

        PreDataList=['IN']
        PreDataList.append(df.iloc[IXinpoint]['代码'])
        PreDataList.append(df.iloc[IXinpoint]['日期'])
        for j in list(range(5,0,-1)):
            PreDataList.append(df.iloc[IXinpoint - j]['开盘价(元)'])
            PreDataList.append(df.iloc[IXinpoint - j]['最高价(元)'])
            PreDataList.append(df.iloc[IXinpoint - j]['最低价(元)'])
            PreDataList.append(df.iloc[IXinpoint - j]['收盘价(元)'])
            PreDataList.append(df.iloc[IXinpoint - j]['均价(元)'])
            PreDataList.append(df.iloc[IXinpoint - j]['换手率(%)'])
        PreDataList.append(ValidSegment[i][2])
        PreDataList.append(MaxHighRate)

        PreData2D.append(PreDataList)
        #print(PreDataList)

        #SaveInOutPoint(inPoint,outPoint)
        #SaveToInPointDatabase()#将入市点前n天的数据放到一个列表中，相当于用6*5个参数表示前5天的一个形态，然后加上一个间隔天数，一个最终幅度，用来标签权重
        #SaveToOutPointDatabase() #将出市点前5天的数据到表一个列表中

    #print(df.iloc[i]['最高价(元)'] / df.iloc[i]['开盘价(元)'])
   # ValidSegment[0]=[2,3,4]
    #ValidSegment.append([1,2,3])
    dfV=pd.DataFrame(ValidSegment)
    dfV.to_csv('../../temp2.csv',index=True,header=True)
    dfV2=pd.DataFrame(PreData2D)
    dfV2.to_csv('../../temp3.csv',index=True,header=True)
    #print(dfv)
    #print(len(ValidSegment))
    #print(ValidSegment[])
   # print(df.head())

'''

for item=1 to maxItem
    enterTime = 当日日期
    enterPrice = 当日收盘价

    for loop=item+1 to maxItem

        if (curPrice-bp)/bp<rSL  //先达到止损位了,不再寻找，这个enterTime不成立    
            break

        if (curPrice-bp)/bp>rTP //先达到止赢位，可以认为这个开始点是一个有效线段
            OutTime=searchOutPoint() //从这个止赢位进入寻找最佳出点的子程序，寻找方法是，从这个价格开始，实现均线动态止盈

    SaveToLineDatabase(enterTime,outTime,intervalDay) //将入市点，出市点和间隔交易日记录下来
    SaveToEnterPointDatabase() //将入市点前PreDay天的数据保存到待分析的材料库，可以根据上面的outTime和intervalDay为这些数据打上带权重的标签
    SaveToOutPointDatabase() //将出市点前PreDay天的数据保存到待分析的材料库，分析出市的的前置规律，不过，因为规则已确定，有没有必要另说
    item=item+1


'''