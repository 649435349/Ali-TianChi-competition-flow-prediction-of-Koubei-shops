# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.chdir('../dataset/')
import csv
import pandas as pd
import numpy as np
import datetime

t1=pd.read_csv('shop_info_modified.csv')
t2=pd.read_csv('shop_day_pay.csv').set_index('shop_id')
t3=pd.read_csv('shop_day_view.csv').set_index('shop_id')

os.chdir('./结果集/')
with open('shop_view_view.csv','w+') as f:
    writer=csv.writer(f)
    writer.writerow([
        u'shop_id', u'city_level', u'location_id', u'per_pay', u'score', u'comment_cnt', u'shop_level',
        u'cate_1_name_chaoshibianlidian', u'cate_1_name_meishi', u'cate_1_name_others',
        u'cate_2_name_bianlidian', u'cate_2_name_chaoshi', u'cate_2_name_hongbeigaodian', u'cate_2_name_huoguo',
        u'cate_2_name_kuaican', u'cate_2_name_others', u'cate_2_name_qitameishi', u'cate_2_name_xiaochi',
        u'cate_2_name_xiuxianchayin', u'cate_2_name_xiuxianshipin', u'cate_2_name_zhongcan',
        u'before_day_view_7', u'before_day_view_6', u'before_day_view_5', u'before_day_view_4',
        u'before_day_view_3',u'before_day_view_2', u'before_day_view_1',
        u'month_1', u'month_2', u'month_3', u'month_4', u'month_5', u'month_6',
        u'month_7', u'month_8', u'month_9', u'month_10', u'month_11', u'month_12'])
    for i in range(1,2001):
        q1=t1.ix[i-1,:22].values
        q2=t3.ix[i,-7:].values
        q4=[0,0,0,0,0,0,0,0,0,0,1,0]
        t=list(np.concatenate([q1,q2,q4],axis=0))
        t.extend(q4)
        writer.writerow(t)