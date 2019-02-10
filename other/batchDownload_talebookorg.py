# coding = UTF-8


import urllib.request
import re
import os

UrlrootPrefix = 'https://www.talebook.org/book/'
filepath = '..\\..\\talebook_org\\'

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
for i in range(0, 3):#19398):
    fileName=str(i)+'.epub'
    Urlroot=UrlrootPrefix+fileName
    req=urllib.request.Request(Urlroot, headers=headers)
    print(Urlroot)
    data=urllib.request.urlopen(req).read()
    if len(data)>1024:
        with open(filepath+fileName,'wb') as code:
            code.write(data)

'''
print(fileName)





'''
