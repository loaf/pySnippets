#coding=utf-8
import requests
import time


# 登录验证地址
check_url = 'http://readfree.me/accounts/checkin'

# 记录程序运行时的时间
fp = open('/home/loaf/auto_signon_readfree.log','a')
ISOTIMEFORMAT='%Y-%m-%d %X'
curtime = time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
print 'at %s'%curtime
fp.write('at %s\n'%curtime)

# 准备cookie
print '准备cookie中……'
fp.write('准备cookie中……\n')
cookie_str = '_ga=GA1.2.1588588561.1525966483; csrftoken=TXvRk7iqkTJjRWcFmHOkrKhf7SIA9Ls6nglNwDCag7i8WRCOsau28X94z3l5naZ6; sessionid=eod4hlqh5x9bwf8agoyxe62ke9yh0bcp'
cookie = {}
for line in cookie_str.split(';'):
    name,value=line.strip().split('=',1)
    cookie[name]=value
print cookie
fp.write('%s\n'%cookie)

# 使用cookie访问网站
print '签到中……'
fp.write('签到中……\n')
res = requests.get(check_url,cookies=cookie)
print res
fp.write('%s\n\n'%res)
