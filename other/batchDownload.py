# coding = UTF-8


import urllib.request
import re
import os

Urlroot = 'https://bible.fhl.net/new/gm.php?fn=b000/m00_001_000_001_000.jpg'
filepath = '..\\..\\pic\\'
bookid='b000' #书名ID
ArticleID='m00'#篇名
beginChapterId='000'#章
endChapterID='000'
beginSectionID='000'#节
endSectionID='000'

fileName=os.path.split(Urlroot)[1]
fileNamePrefix=bookid+'/'
fileNameList=[]
Oldarray = [ "創世記","出埃及記","利未記","民數記","申命記","約書亞記", "士師記","路得記","撒母耳記上","撒母耳記下","列王紀上","列王紀下",
             "歷代志上","歷代志下","以斯拉記","尼希米記","以斯帖記","約伯記","詩篇","箴言","傳道書","雅歌","以賽亞書","耶利米書","耶利米哀歌","以西結書","但以理書"," 何西阿書","約珥書","阿摩司書","俄巴底亞書","約拿書","彌迦書","那鴻書","哈巴谷書","西番雅書","哈該書","撒迦利亞書","瑪拉基書" ]
Oldcnum=[50,40,27,36,34,24,21,4,31,24,22,25,29,36,10,13,10,42,150,31,12,8,66,52,5,48,12,14,3,9,1,4,7,3,3,3,2,14,4]
Newarray = [ "馬太福音","馬可福音","路加福音","約翰福音","使徒行傳","羅馬書","哥林多前書","哥林多後書","加拉太書","以弗所書","腓立比書","歌羅西書","帖撒羅尼迦前書","帖撒羅尼迦後書","提摩太前書","提摩太後書","提多書","腓利門書","希伯來書","雅各書","彼得前書","彼得後書","約翰壹書","約翰貳書","約翰參書","猶大書","啟示錄"]
Newcnum=[28,16,24,21,28,16,16,13,6,6,4,4,5,3,6,4,3,1,13,5,5,3,5,1,1,1,22]
for i in range(0,90):
    ArticleID='m'+str(100+i)[-2:] #篇
    for j in range(0,100):
        beginChapterId=str(1000+j)[-3:] #章

        endChapterID = beginChapterId
        for bs in range(0, 100): #开始节
            beginSectionID=str(1000+bs)[-3:]
            for es in range(bs,bs+4): #结束节
                endSectionID=str(1000+es)[-3:]
                fileName=fileNamePrefix+ArticleID+'_'+beginChapterId+'_'+beginSectionID+'_'+endChapterID+'_'+endSectionID+'.jpg'
                fileNameList.append(fileName)


        
        endChapterID=str(1000+j+1)[-3:]
        for k in range(0,1000):
            k=1

        endChapterID=str(1000+j+2)[-3:]
        for k in range(0,1000):
            k=1
        

print(len(fileNameList))
'''
print(fileName)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
req=urllib.request.Request(Urlroot, headers=headers)
data=urllib.request.urlopen(req).read()
if len(data)>1024:
    with open(filepath+fileName,'wb') as code:
        code.write(data)

'''
