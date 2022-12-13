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
url = config.get('URL', 'packet')

res = requests.get(url,auth=HTTPDigestAuth(username,password))
html_text = res.text
dt_now = datetime.datetime.now()

lan_tx = re.search(r'\("#lan_tx"\).text\("(\d+)"\);', html_text)
lan_rx = re.search(r'\("#lan_rx"\).text\("(\d+)"\);', html_text)

wan_tx = re.search(r'\("#wan_tx"\).text\("(\d+)"\);', html_text)
wan_rx = re.search(r'\("#wan_rx"\).text\("(\d+)"\);', html_text)

w2g_tx = re.search(r'\("#2g_tx"\).text\("(\d+)"\);', html_text)
w2g_rx = re.search(r'\("#2g_rx"\).text\("(\d+)"\);', html_text)

w5g_tx = re.search(r'\("#5g_tx"\).text\("(\d+)"\);', html_text)
w5g_rx = re.search(r'\("#5g_rx"\).text\("(\d+)"\);', html_text)

print(dt_now.strftime('%Y-%m-%d %H:%M:%S') + ',' + 
    lan_tx.group(1) + ',' +
    lan_rx.group(1) + ',' +
    wan_tx.group(1) + ',' +
    wan_rx.group(1) + ',' +
    w5g_tx.group(1) + ',' +
    w5g_rx.group(1))
