# -*- coding: utf-8 -*-
import configparser
import psycopg2
import sys

config = configparser.ConfigParser()
config.read('config.ini')

dbname = config.get('DB', 'dbname')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
password = config.get('DB', 'password')

dsn = 'dbname=' + dbname + ' host=' + host + ' user=' + user + ' password=' + password
print(dsn)

try:
    conn = psycopg2.connect(dsn)
except Exception as e:
    print('Unable to connect!')
    print(e)
    sys.exit(1)
else:
    with conn.cursor() as cur:
        sql = '''
            CREATE TABLE RtrUsage (
                created_at timestamp Not Null,
                lan_tx bigint Not Null,
                lan_rx bigint Not Null,
                wan_tx bigint Not Null,
                wan_rx bigint Not Null,
                w2g_tx bigint Not Null,
                w2g_rx bigint Not Null,
                w5g_tx bigint Not Null,
                w5g_rx bigint Not Null  
            );
        '''
        cur.execute(sql)
        conn.commit()
        conn.close()
