# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import pymysql

os.chdir('../dataset/')

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004',charset='utf8')
cur = conn.cursor()
cur.execute('use competition')
with open('user_view.txt') as f:
    l=f.readlines()

for i in l:
    tmp=i.split(',')
    sql='insert into user_view(user_id,shop_id,time_stamp) values (%s,%s,%s)'
    cur.execute(sql,tmp)
    conn.commit()

cur.close()
conn.close()
