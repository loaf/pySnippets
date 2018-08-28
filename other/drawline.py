# coding=utf-8

import pymssql
import matplotlib.pyplot as plt
#import random

#randNum=random.randint(1,6080738)
def toColor(x):
    if x==1:
        return 'b'
    elif x==2:
        return 'g'
    elif x==3:
        return 'r'
    elif x==4:
        return 'y'
    elif x==5:
        return 'c'
    elif x==6:
        return 'k'
    elif x==7:
        return 'm'
    elif x==8:
        return 'b'
    elif x==9:
        return 'g'
    else:
        return 'k'
try:
    conn=pymssql.connect(host='192.168.11.198',user='sa',password='123456',database='P8')
    with conn:
        cur=conn.cursor()
        query='select groupid,scaleid,type3id,v1x,v1y,v2x,v2y,v3x,v3y from p8_fordraw where groupid=cast(floor(RAND()*3421064) as int)'

        i=0
        while i< 1000:
            i+=1
            cur.execute(query)
            resultset=cur.fetchall()

            #col_names=[cn[0] for cn in cur.description]

            #print(tuple(col_names))
            #print("="*(10+1+30+1+10))
            plt.figure()
            j=0
            for row in resultset:
                #print(row)
                #print(row[0],row[3])
                x1=row[3]
                x2=x1+row[5]
                x3=x2+row[7]
                y1=row[4]
                y2=y1+row[6]
                y3=y2+row[8]
                x=[0,x1,x2,x3]
                y=[0,y1,y2,y3]
                j+=1
                plt.plot(x,y,linewidth=1,c=toColor(row[1]))
                plt.scatter(x,y,c=toColor(row[1]))
            #plt.show()
            plt.title("GroupID is %s , Total of segments is %s" % (row[0],j))
            plt.savefig("GroupID%s.png"%row[0])
    cur.close()
    conn.close()
except pymssql.DataError as err:
    print("error:",err)

#cur=conn.cursor()
#cur.execute('select top 10 *   FROM [P7].[dbo].[P7_forDraw]')
"""
x=[0,22,34,45,445]
y=[0,12,33,18,456]
plt.figure()
plt.plot(x,y)
plt.scatter(x,y)

x=[12,32,100,200]
y=[121,333,55,4456]
plt.plot(x,y)
plt.scatter(x,y)
plt.show()
#print(cur.fetchall())
#cur.close()
#conn.close()
"""