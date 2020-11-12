# -*- coding: utf-8 -*-

"""
from aip import AipFace

APP_ID="22241061"
API_KEY = '0V2oNrUYZFqBgSL68p8DqQNP'
SECRET_KEY = 'sAx5EqEh9G7XpPs8jQH2uHyszCUXvcAc'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
"""

import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=0V2oNrUYZFqBgSL68p8DqQNP&client_secret=sAx5EqEh9G7XpPs8jQH2uHyszCUXvcAc'
response = requests.get(host)
if response:
    print(response.json())