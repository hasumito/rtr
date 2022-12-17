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
try:
    conn = psycopg2.connect(dsn)
except Exception as e:
    print('Unable to connect!')
    print(e)
    sys.exit(1)
else:
    with conn.cursor() as cur:
        sql = '''
            SELECT created_at, lan_tx, lan_rx, wan_tx, wan_rx, w2g_tx, w2g_rx,
            w5g_tx, w5g_rx FROM RtrUsage ORDER BY created_at ASC
        '''        
        cur.execute(sql)
        rows = cur.fetchall()

        print('timestamp, lan_tx, lan_rx, wan_tx, wan_rx, w2g_tx, w2g_rx, w5g_tx, w5g_rx')
        for row in rows:
            record = str(row[0])
            record = record + ',' + str(row[1])
            record = record + ',' + str(row[2])
            record = record + ',' + str(row[3])
            record = record + ',' + str(row[4])
            record = record + ',' + str(row[5])
            record = record + ',' + str(row[6])
            record = record + ',' + str(row[7])
            record = record + ',' + str(row[8])
            print(record)

        conn.close()
