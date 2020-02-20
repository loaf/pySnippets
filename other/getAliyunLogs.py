#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkdcdn.request.v20180115.DescribeDcdnDomainLogRequest import DescribeDcdnDomainLogRequest

client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')

request = DescribeDcdnDomainLogRequest()
request.set_accept_format('json')

request.set_DomainName("www.96369.net")
request.set_PageSize(1000)
request.set_StartTime("2019-12-01T00:00:00Z")
request.set_EndTime("2020-01-01T00:00:00Z")

response = client.do_action_with_exception(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))
