# -*- coding: utf-8 -*-
import configparser
import datetime
import re
import requests
from requests.auth import HTTPDigestAuth
import psycopg2
import sys

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
    w2g_tx.group(1) + ',' +
    w2g_rx.group(1) + ',' +
    w5g_tx.group(1) + ',' +
    w5g_rx.group(1))

dbname = config.get('DB', 'dbname')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
password = config.get('DB', 'password')

dsn = 'dbname=' + dbname + ' host=' + host + ' user=' + user + ' password=' + password
try:
    conn = psycopg2.connect(dsn)
except Exception as e:
    print('Unable to connect!')
    print(e)
    sys.exit(1)
else:
    with conn.cursor() as cur:
        sql = '''
            INSERT INTO RtrUsage (
                created_at, 
                lan_tx, 
                lan_rx, 
                wan_tx, 
                wan_rx,
                w2g_tx,
                w2g_rx,
                w5g_tx,
                w5g_rx
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        cur.execute(sql, (
                            dt_now.strftime('%Y-%m-%d %H:%M:%S'),
                            lan_tx.group(1),
                            lan_rx.group(1),
                            wan_tx.group(1),
                            wan_rx.group(1),
                            w2g_tx.group(1),
                            w2g_rx.group(1),
                            w5g_tx.group(1),
                            w5g_rx.group(1)
                        ))

        conn.commit()
        conn.close()
