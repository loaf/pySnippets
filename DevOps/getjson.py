#coding=utf-8
import json
from urllib.request import Request, urlopen


import json
html = urlopen(r'https://pm.xb969.com:8844')
hjson = json.loads(html.read())
print(hjson['code'])
print(hjson['msg'])