# -*- coding: utf-8 -*-
import configparser
import datetime
import re
import requests
from requests.auth import HTTPDigestAuth

config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('Credential', 'username')
password = config.get('Credential', 'password')
url = config.get('General', 'url')

res = requests.get(url,auth=HTTPDigestAuth(username,password))

html_text = res.text
result = re.search(r'var uptime = "(\d+)";', html_text)

dt_now = datetime.datetime.now()
print(dt_now.strftime('%Y-%m-%d %H:%M:%S') + ',' + result.group(1))

