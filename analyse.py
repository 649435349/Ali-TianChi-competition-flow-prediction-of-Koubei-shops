# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.chdir('../dataset/')
import datetime
import csv

import numpy as np
import pandas as pd
import calendar

def change(item):
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item

def get_first_nonzero_index(array):
    for i,j in list(array):
        if j:
            return i
    return -1


date = datetime.datetime(2015, 6, 26)
delta = datetime.timedelta(days=1)
while date.year != 2016 or date.month != 11 or date.day != 1:
    '{}-{}-{}'.format(change(date.year), change(date.month), change(date.day))
    date += delta

t=pd.read_csv('data_set_pay_pay.csv').set_index('shop_id')
for i in range(1,2001):
    date = datetime.datetime(2015, 6, 26)
    delta = datetime.timedelta(days=1)

    while date.year != 2016 or date.month != 11 or date.day != 1:
        for i in range(7):
            pass

