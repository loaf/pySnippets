# coding=utf-8


'''
#说明
先从东方财富网拉到股票列表（代码列表）
然后到网易的财经接口拉到股票的历史数据
http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=20150911&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
上面的URL中
code=股票代码，第一位0代表沪市，1代表深市
start和end是起止日期
fields代表选中项，TCLOSE，HIGH，LOW，TOPEN表示收盘价、最高价、最低价和开盘价，LCLOSE代表昨日收盘价，
CHG：涨跌额、PCHG：涨跌幅、VOTURNOVER：成交量、VATURNOVER：成交金额
TURNOVER:换手率;TCAP：总市值;MCAP：流通市值
其实，直接用http://quotes.money.163.com/service/chddata.html?code=0601398&start=20000720&end=20150508可以得到全部信息，但是发现里面没有平均价

下面是获取工商银行0601398，从2008年07月20日到2015年05月08日之间的历史数据，文件为CSV格式
http://quotes.money.163.com/service/chddata.html?code=0601398&start=20000720&end=20150508
财务指标下载（CSV格式）
http://quotes.money.163.com/service/zycwzb_601398.html?type=report
利润表下载（CSV格式）
http://quotes.money.163.com/service/lrb_601398.html
现金流表（CSV格式）
http://quotes.money.163.com/service/xjllb_601398.html
'''


#导入需要使用到的模块
import urllib
import re
import pandas as pd
#import pymysql
import os

#爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html

#抓取网页股票代码函数
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


Url = 'http://quote.eastmoney.com/stocklist.html'#东方财富网股票数据连接地址
filepath = '..\\..\\Quant\\stock\\Data\\NewDown\\'#定义数据文件保存路径
#实施抓取
code = getStackCode(getHtml(Url))
#获取所有股票代码（以6开头的，应该是沪市数据）集合
CodeList = []
for item in code:
    if item[0:6]=='000835':
        CodeList.append(item)
#抓取数据并保存到本地csv文件
for code in CodeList:
    print('正在获取股票%s数据'%code)
    url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
        '&start=20170101&end=20180801&fields=TOPEN;HIGH;LOW;TCLOSE;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    urllib.request.urlretrieve(url, filepath+code+'.csv')