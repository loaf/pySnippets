# encoding: utf-8
import time
import sys
import os
#reload(sys)
#sys.setdefaultencoding('utf-8')
time1 = time.time()
#import urllib, urllib2, base64
import urllib.request,urllib.parse,base64
import json
import re


dataPath='e:/6/xin/'
ocroutPath='e:/6/xin_text/'

def get_token(API_Key,Secret_Key):
    # 获取access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_Key+'&client_secret='+Secret_Key
    #request = urllib2.Request(host)
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    #response = urllib2.urlopen(request)
    response = urllib.request.urlopen(request)
    content = response.read()
    content_json=json.loads(content)
    access_token=content_json['access_token']
    return access_token

def recognition_word_high(filepath,filename,access_token):
    #url='https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
    # 二进制方式打开图文件
    f = open(filepath + filename, 'rb')  # 二进制方式打开图文件
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    #params = urllib.urlencode(params)
    params=urllib.parse.urlencode(params).encode(encoding='UTF8')
    #request = urllib2.Request(url, params)
    request = urllib.request.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    #response = urllib2.urlopen(request)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf8")
    #print(content)
    retStr=""

    if (content):
        # print(content)
        world=re.findall('"words": "(.*?)"}',str(content),re.S)
        for each in world:
            retStr += each

    return retStr



if __name__ == '__main__':
    API_Key = "Ta45HPVPVc1PYMkoL52Gr0Vh"
    Secret_Key = "GFCAYKjltuzUkma9m3q4FDoSrXIhV42g"

    access_token = get_token(API_Key, Secret_Key)
    for f in os.listdir(dataPath):
        fi = os.path.join(dataPath, f)

        if os.path.isdir(fi) or os.path.splitext(f)[1] != ".jpg":
            continue

        outFileName=os.path.splitext(f)[0]+".txt"

        fo=open(os.path.join(ocroutPath, outFileName),'w')


        #access_token = get_token(API_Key, Secret_Key)
        s =  recognition_word_high(dataPath, f, access_token)
        fo.write(s)
        fo.close()



    '''
    filepath = "E:/6/five/"
    filename="f049.jpg"
    fo=open('e:/6/five_text/f049.txt','w')


    print(str)
    fo.write(str)
    fo.close()
    '''
