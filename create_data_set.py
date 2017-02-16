# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.chdir('../dataset/')
import pandas as pd
import datetime
import csv
import numpy as np


def change(item):
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item

def get_day(date):
    return '{}-{}-{}'.format(change(date.year), change(date.month), change(date.day))

t1=pd.read_csv('shop_info_modified.csv').set_index('shop_id')
t2=pd.read_csv('shop_day_pay.csv').set_index('shop_id')
t3=pd.read_csv('shop_day_view.csv').set_index('shop_id')
delta=datetime.timedelta(days=1)
with open('data_set_view_view.csv','w+') as f:
    writer=csv.writer(f)
    writer.writerow([
        u'shop_id',u'city_level', u'location_id', u'per_pay', u'score', u'comment_cnt', u'shop_level',
        u'cate_1_name_chaoshibianlidian', u'cate_1_name_meishi',u'cate_1_name_others',
        u'cate_2_name_bianlidian',u'cate_2_name_chaoshi', u'cate_2_name_hongbeigaodian',u'cate_2_name_huoguo',
        u'cate_2_name_kuaican', u'cate_2_name_others',u'cate_2_name_qitameishi', u'cate_2_name_xiaochi',
        u'cate_2_name_xiuxianchayin', u'cate_2_name_xiuxianshipin',u'cate_2_name_zhongcan',
        u'month',
        u'before_day_view_7', u'before_day_view_6', u'before_day_view_5', u'before_day_view_4',
        u'before_day_view_3',u'before_day_view_2', u'before_day_view_1',
        u'before_day_pay_7', u'before_day_pay_6', u'before_day_pay_5', u'before_day_pay_4',
        u'before_day_pay_3', u'before_day_pay_2', u'before_day_pay_1',
        u'today_view'])
    for i in range(1,2001):
        date = datetime.datetime(2016, 2, 1)
        while date.year != 2016 or date.month != 10 or date.day != 25:
            l=list(t1.ix[i])
            l.insert(0,i)
            d1=d2=date
            for j in range(8):
                #插入view
                l.append(t3.ix[i,get_day(d1)])
                if j==7:
                    l.insert(-7, d1.month)
                d1 += delta
            writer.writerow(l)
            date += delta




'''

t=pd.read_csv('data_set_payandview_pay.csv')
t1=pd.get_dummies(t['month'])
t2=t['today_pay']
del t['month'],t['today_pay']
t=pd.concat([t,t1,t2], axis=1)
with open('data_set_payandview_payy.csv','w+') as f:
    writer=csv.writer(f)
    writer.writerow([
        u'shop_id', u'city_level', u'location_id', u'per_pay', u'score', u'comment_cnt', u'shop_level',
        u'cate_1_name_chaoshibianlidian', u'cate_1_name_meishi', u'cate_1_name_others',
        u'cate_2_name_bianlidian', u'cate_2_name_chaoshi', u'cate_2_name_hongbeigaodian', u'cate_2_name_huoguo',
        u'cate_2_name_kuaican', u'cate_2_name_others', u'cate_2_name_qitameishi', u'cate_2_name_xiaochi',
        u'cate_2_name_xiuxianchayin', u'cate_2_name_xiuxianshipin', u'cate_2_name_zhongcan',
        u'before_day_view_7', u'before_day_view_6', u'before_day_view_5', u'before_day_view_4',
        u'before_day_view_3',u'before_day_view_2', u'before_day_view_1',
        u'before_day_pay_7', u'before_day_pay_6', u'before_day_pay_5', u'before_day_pay_4',
        u'before_day_pay_3',u'before_day_pay_2', u'before_day_pay_1',
        u'month_1', u'month_2', u'month_3', u'month_4', u'month_5', u'month_6',
        u'month_7', u'month_8', u'month_9', u'month_10', u'month_11', u'month_12',
        u'today_pay', ])
    for i in range(978010):
        l=list(t.ix[i])
        writer.writerow(l)

'''