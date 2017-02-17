# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import csv
import re
import copy
import datetime
import pymysql
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score
from sklearn.externals import joblib
import pandas as pd
import numpy as np


def change(item):
    # 主要用于处理年月日的问题。统一为2017-01-01格式
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item


def mysqll():
    # 插入天气数据
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='fyf!!961004',
        db='competition',
        charset='utf8')
    cur = conn.cursor()
    os.chdir('../dataset/')
    with open('city_weather.csv') as f:
        reader = csv.reader(f)
        reader.next()
        sql = 'insert into city_weather VALUES (%s,%s,%s,%s,%s,%s,%s)'
        for i in reader:
            cur.execute(sql, i)
            conn.commit()
    cur.close()
    conn.close()


def create_tianqi():
    # 创建每个商家所在城市每一天的天气数据
    os.chdir('../dataset/')
    t = pd.read_csv('shop_info.csv').set_index('shop_id')
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='fyf!!961004',
        db='competition',
        charset='utf8')
    cur = conn.cursor()
    delta = datetime.timedelta(days=1)
    os.chdir('../')
    with open('shop_day_wind_level.csv', 'w+') as f:
        writer = csv.writer(f)
        date = datetime.datetime(2015, 7, 1)
        res = ['shop_id']
        while date.year != 2016 or date.month != 11 or date.day != 15:
            res.append('{}-{}-{}'.format(change(date.year),
                                         change(date.month), change(date.day)))
            date += delta
        writer.writerow(res)
        for i in range(1, 2001):
            res = [i]
            date = datetime.datetime(2015, 7, 1)
            city_name = t.ix[i, 'city_name']
            while date.year != 2016 or date.month != 11 or date.day != 15:
                try:
                    sql = 'select wind_level from city_weather where city_name=(%s) and date=(%s)'
                    cur.execute(sql,
                                [city_name,
                                 '{}-{}-{}'.format(change(date.year),
                                                   change(date.month),
                                                   change(date.day))])
                    res.append(int(cur.fetchone()[0]))
                    '''
                    if '雨' in weather or '雪' in weather or '雾' in weather or '霾' in weather:
                        res.append(1)
                    elif '阴' in weather:
                        res.append(2)
                    elif '云' in weather:
                        res.append(3)
                    elif '晴' in weather:
                        res.append(4)
                    else:
                        print weather
                    '''
                    date += delta
                except:
                    date -= delta
                    sql = 'select wind_level from city_weather where city_name=(%s) and date=(%s)'
                    cur.execute(sql,
                                [city_name,
                                 '{}-{}-{}'.format(change(date.year),
                                                   change(date.month),
                                                   change(date.day))])
                    before = int(cur.fetchone()[0])
                    '''
                    if '雨' in weather or '雪' in weather or '雾' in weather or '霾' in weather:
                        res.append(1)
                    elif '阴' in weather:
                        res.append(2)
                    elif '云' in weather:
                        res.append(3)
                    elif '晴' in weather:
                        res.append(4)
                    else:
                        print weather
                    '''
                    date += 2 * delta
                    cur.execute(sql,
                                [city_name,
                                 '{}-{}-{}'.format(change(date.year),
                                                   change(date.month),
                                                   change(date.day))])
                    after = int(cur.fetchone()[0])
                    res.append((before + after) / 2)
            writer.writerow(res)
    cur.close()
    conn.close()


def my_error(Exception):
    pass


def create_tianqi2():
    # 创建每个商家所在城市每一天的风力等级
    os.chdir('../dataset/')
    tt = pd.read_csv('shop_info.csv').set_index('shop_id')
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='fyf!!961004',
        db='competition',
        charset='utf8')
    cur = conn.cursor()
    delta = datetime.timedelta(days=1)
    os.chdir('../')
    with open('shop_day_wind_level.csv', 'w+') as f:
        writer = csv.writer(f)
        date = datetime.datetime(2015, 7, 1)
        res = ['shop_id']
        while date.year != 2016 or date.month != 11 or date.day != 15:
            res.append('{}-{}-{}'.format(change(date.year),
                                         change(date.month), change(date.day)))
            date += delta
        writer.writerow(res)
        for i in range(1, 2001):
            res = [i]
            date = datetime.datetime(2015, 7, 1)
            city_name = tt.ix[i, 'city_name']
            while date.year != 2016 or date.month != 11 or date.day != 15:
                try:
                    sql = 'select wind,wind_level from city_weather where city_name=(%s) and date=(%s)'
                    cur.execute(sql,
                                [city_name,
                                 '{}-{}-{}'.format(change(date.year),
                                                   change(date.month),
                                                   change(date.day))])
                    t = ''.join(cur.fetchone())
                    if '微' in t:
                        wind_level = 0
                    else:
                        if re.findall(r'\d+', t):
                            levels = [int(i) for i in re.findall(r'\d+', t)]
                            wind_level = sum(levels) / len(levels)
                        else:
                            raise Exception
                    res.append(wind_level)
                    date += delta
                except:
                    try:
                        date -= delta
                        sql = 'select wind,wind_level from city_weather where city_name=(%s) and date=(%s)'
                        cur.execute(sql,
                                    [city_name,
                                     '{}-{}-{}'.format(change(date.year),
                                                       change(date.month),
                                                       change(date.day))])
                        t = ''.join(cur.fetchone())
                        if '微' in t:
                            wind_level = 0
                        else:
                            if re.findall(r'\d+', t):
                                levels = [int(i)
                                          for i in re.findall(r'\d+', t)]
                                wind_level = sum(levels) / len(levels)
                            else:
                                raise Exception
                        date += 2 * delta
                        res.append(wind_level)
                    except:
                        print t, city_name, date
                        break
            writer.writerow(res)
    cur.close()
    conn.close()


def get_averaget():
    # 为了建平均温度的表
    os.chdir('../dataset/')
    with open('shop_day_upt.csv') as f1, open('shop_day_lowt.csv') as f2, open('shop_day_averaget.csv', 'w+') as f3:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)
        writer = csv.writer(f3)
        writer.writerow(reader1.next())
        reader2.next()
        for i in range(2000):
            res = []
            t1 = reader1.next()
            t2 = reader2.next()
            for j in range(504):
                if j == 0:
                    res.append((int(t1[j]) + int(t2[j])) / 2)
                else:
                    res.append((int(t1[j]) + int(t2[j])) / 2.0)
            writer.writerow(res)


def get_jiejiari():
    # 改善节假日
    os.chdir('../dataset/')
    t = pd.read_csv('holiday.csv').set_index('date')
    date = datetime.datetime(2015, 7, 1)
    delta = datetime.timedelta(days=1)
    res = []
    os.chdir('../')
    with open('shop_day_holiday.csv', 'w+') as f:
        writer = csv.writer(f)
        while date.year != 2016 or date.month != 11 or date.day != 15:
            res.append('{}-{}-{}'.format(change(date.year),
                                         change(date.month), change(date.day)))
            date += delta
        writer.writerow(res)
        date = datetime.datetime(2015, 7, 1)
        res = []
        while date.year != 2016 or date.month != 11 or date.day != 1:
            res.append(t.ix[int('{}{}{}'.format(change(date.year), change(
                date.month), change(date.day))), 'holiday'])
            date += delta
        writer.writerow(res)


def get_weekday():
    # 得到每天是星期几
    os.chdir('../dataset/')
    date = datetime.datetime(2015, 7, 1)
    delta = datetime.timedelta(days=1)
    res = []
    with open('shop_day_weekday.csv', 'w+') as f:
        writer = csv.writer(f)
        while date.year != 2016 or date.month != 11 or date.day != 15:
            res.append('{}-{}-{}'.format(change(date.year),
                                         change(date.month), change(date.day)))
            date += delta
        writer.writerow(res)
        date = datetime.datetime(2015, 7, 1)
        res = []
        while date.year != 2016 or date.month != 11 or date.day != 15:
            res.append(date.weekday() + 1)
            date += delta
        writer.writerow(res)


def get_average_pay():
    # 得到每天的所有商家的支付和浏览人数的平均数
    os.chdir('../dataset/')
    t = pd.read_csv('shop_day_view.csv').set_index('shop_id')
    date = datetime.datetime(2016, 2, 1)
    delta = datetime.timedelta(days=1)
    res = []
    with open('all_shop_day_average_view.csv', 'w+') as f:
        writer = csv.writer(f)
        while date.year != 2016 or date.month != 11 or date.day != 1:
            res.append('{}-{}-{}'.format(change(date.year),
                                         change(date.month), change(date.day)))
            date += delta
        writer.writerow(res)
        date = datetime.datetime(2016, 2, 1)
        res = []
        while date.year != 2016 or date.month != 11 or date.day != 1:
            res.append(
                np.mean(
                    t.ix[
                        :, '{}-{}-{}'.format(
                            change(
                                date.year), change(
                                date.month), change(
                                date.day))]))
            date += delta
        writer.writerow(res)


def get_first_no0_date():
    # 得到每个商家不是0的第一天的日期，支付和浏览
    os.chdir('../dataset/')
    with open('shop_first_no0_date1.csv', 'w+') as f1, open('shop_day_pay.csv') as f2, open('shop_day_view.csv') as f3:
        reader1 = csv.reader(f2)
        reader2 = csv.reader(f3)
        writer = csv.writer(f1)
        datef1 = reader1.next()
        datef2 = reader2.next()
        writer.writerow(
            ['shop_id', 'first_no0_pay_date', 'first_no0_view_date'])
        for i, j in enumerate(reader2):
            res = [i + 1]
            index = 1
            for m, n in enumerate(j[1:]):
                if int(n) != 0:
                    index = m + 1
                    break
            res.append(datef2[index])
            writer.writerow(res)


def analyse():
    # 分析用
    os.chdir('../dataset/')
    with open('shop_first_no0_date.csv') as f:
        reader = csv.reader(f)
        reader.next()
        res = []
        for i in reader:
            date = string_to_date(i[2])
            res.append(datetime.date(2016, 11, 1) - date)
        print max(res)


def create_shop_average():
    # 输出每个商家的平均浏览和平均
    os.chdir('../dataset/')
    shop_first_no0_date = pd.read_csv(
        'shop_first_no0_date.csv').set_index('shop_id')
    shop_day_pay = pd.read_csv('shop_day_pay.csv').set_index('shop_id')
    shop_day_view = pd.read_csv('shop_day_view.csv').set_index('shop_id')
    with open('shop_average.csv', 'w+') as f:
        date_11_1 = datetime.date(2017, 11, 1)
        writer = csv.writer(f)
        writer.writerow(['shop_id', 'average_pay', 'average_view'])
        for i in range(1, 2001):
            res = [i]
            date = string_to_date(
                shop_first_no0_date.ix[
                    i, 'first_no0_view_date'])
            days = (date_11_1 - date).days
            res.append(shop_day_pay.ix[i, (-days):].mean())
            res.append(shop_day_view.ix[i, (-days):].mean())
            writer.writerow(res)


def string_to_date(s):
    l = re.findall(r'\d+', s)
    return datetime.date(year=int(l[0]), month=int(l[1]), day=int(l[2]))


def date_to_string(date):
    return '{}-{}-{}'.format(change(date.year),
                             change(date.month), change(date.day))


def create_dataset():

    os.chdir('../dataset/')
    all_shop_day_average_pay = pd.read_csv('all_shop_day_average_pay.csv')
    all_shop_day_average_view = pd.read_csv('all_shop_day_average_view.csv')
    shop_day_averaget = pd.read_csv(
        'shop_day_averaget.csv').set_index('shop_id')
    shop_day_holiday = pd.read_csv('shop_day_holiday.csv')
    shop_day_lowt = pd.read_csv('shop_day_lowt.csv').set_index('shop_id')
    shop_day_pay = pd.read_csv('shop_day_pay.csv').set_index('shop_id')
    shop_day_upt = pd.read_csv('shop_day_upt.csv').set_index('shop_id')
    shop_day_view = pd.read_csv('shop_day_view.csv').set_index('shop_id')
    shop_day_weather = pd.read_csv('shop_day_weather.csv').set_index('shop_id')
    shop_day_weekday = pd.read_csv('shop_day_weekday.csv')
    shop_first_no0_date = pd.read_csv(
        'shop_first_no0_date.csv').set_index('shop_id')
    shop_info_modified = pd.read_csv(
        'shop_info_modified.csv').set_index('shop_id')
    shop_average = pd.read_csv('shop_average.csv').set_index('shop_id')
    os.chdir('./train/')
    for q in range(1, 15):
        with open('dataset{}.csv'.format(q), 'w+') as f:  # 改
            writer = csv.writer(f)
            writer.writerow(['shop_id',
                             'day_date',
                             'city_level',
                             'location_id',
                             'per_pay',
                             'score',
                             'comment_cnt',
                             'shop_level',
                             'cate_1_name_chaoshibianlidian',
                             'cate_1_name_meishi',
                             'cate_1_name_others',
                             'cate_2_name_bianlidian',
                             'cate_2_name_chaoshi',
                             'cate_2_name_hongbeigaodian',
                             'cate_2_name_huoguo',
                             'cate_2_name_kuaican',
                             'cate_2_name_others',
                             'cate_2_name_qitameishi',
                             'cate_2_name_xiaochi',
                             'cate_2_name_xiuxianchayin',
                             'cate_2_name_xiuxianshipin',
                             'cate_2_name_zhongcan',
                             'average_pay',
                             'average_view',
                             'average_divide',
                             'upt',
                             'lowt',
                             'averaget',
                             'weather',
                             'weekday',
                             'holiday',
                             'before_day_pay_14',
                             'before_day_pay_13',
                             'before_day_pay_12',
                             'before_day_pay_11',
                             'before_day_pay_10',
                             'before_day_pay_9',
                             'before_day_pay_8',
                             'before_day_pay_7',
                             'before_day_pay_6',
                             'before_day_pay_5',
                             'before_day_pay_4',
                             'before_day_pay_3',
                             'before_day_pay_2',
                             'before_day_pay_1',
                             'before_day_pay_14_average',
                             'before_day_pay_7_average',
                             'before_day_pay_3_average',
                             'before_day_view_14',
                             'before_day_view_13',
                             'before_day_view_12',
                             'before_day_view_11',
                             'before_day_view_10',
                             'before_day_view_9',
                             'before_day_view_8',
                             'before_day_view_7',
                             'before_day_view_6',
                             'before_day_view_5',
                             'before_day_view_4',
                             'before_day_view_3',
                             'before_day_view_2',
                             'before_day_view_1',
                             'before_day_view_14_average',
                             'before_day_view_7_average',
                             'before_day_view_3_average',
                             'before_divide_14',
                             'before_divide_13',
                             'before_divide_12',
                             'before_divide_11',
                             'before_divide_10',
                             'before_divide_9',
                             'before_divide_8',
                             'before_divide_7',
                             'before_divide_6',
                             'before_divide_5',
                             'before_divide_4',
                             'before_divide_3',
                             'before_divide_2',
                             'before_divide_1',
                             'before_14_average_divide',
                             'before_7_average_divide',
                             'before_3_average_divide',
                             'before_all_average_pay_14',
                             'before_all_average_pay_13',
                             'before_all_average_pay_12',
                             'before_all_average_pay_11',
                             'before_all_average_pay_10',
                             'before_all_average_pay_9',
                             'before_all_average_pay_8',
                             'before_all_average_pay_7',
                             'before_all_average_pay_6',
                             'before_all_average_pay_5',
                             'before_all_average_pay_4',
                             'before_all_average_pay_3',
                             'before_all_average_pay_2',
                             'before_all_average_pay_1',
                             'before_all_average_pay_average_14',
                             'before_all_average_pay_average_7',
                             'before_all_average_pay_average_3',
                             'before_all_average_view_14',
                             'before_all_average_view_13',
                             'before_all_average_view_12',
                             'before_all_average_view_11',
                             'before_all_average_view_10',
                             'before_all_average_view_9',
                             'before_all_average_view_8',
                             'before_all_average_view_7',
                             'before_all_average_view_6',
                             'before_all_average_view_5',
                             'before_all_average_view_4',
                             'before_all_average_view_3',
                             'before_all_average_view_2',
                             'before_all_average_view_1',
                             'before_all_average_view_average_14',
                             'before_all_average_view_average_7',
                             'before_all_average_view_average_3',
                             'before_all_divide_14',
                             'before_all_divide_13',
                             'before_all_divide_12',
                             'before_all_divide_11',
                             'before_all_divide_10',
                             'before_all_divide_9',
                             'before_all_divide_8',
                             'before_all_divide_7',
                             'before_all_divide_6',
                             'before_all_divide_5',
                             'before_all_divide_4',
                             'before_all_divide_3',
                             'before_all_divide_2',
                             'before_all_divide_1',
                             'before_all_14_average_divide',
                             'before_all_7_average_divide',
                             'before_all_3_average_divide',
                             'day'])
            for i in range(1, 2001):
                z = float(shop_average.ix[i, 'average_view'])
                zz = float(shop_average.ix[i, 'average_pay'])
                if z == 0:
                    z = 1
                    zz += 1
                basic = [i] + list(shop_info_modified.ix[i, :]) + \
                    list(shop_average.ix[i, :]) + [zz / z]
                begin_date = string_to_date(
                    shop_first_no0_date.ix[
                        i, 'first_no0_view_date'])
                #强制从2016-07-01开始，减小数据凉并且认为前面的数据不重要
                if begin_date>datetime.date(2016,7,1):
                    begin_date=begin_date
                else:
                    begin_date = datetime.date(2016, 7, 1)
                end_date = datetime.date(2016, 10, 19 - q)  # 改
                delta = datetime.timedelta(days=1)
                gap = (end_date - begin_date).days
                for j in range(gap):
                    res = copy.deepcopy(basic)
                    d = begin_date + (13 + q) * delta  # 改
                    str_d = date_to_string(d)
                    res.append(shop_day_upt.ix[i, str_d])
                    res.append(shop_day_lowt.ix[i, str_d])
                    res.append(shop_day_averaget.ix[i, str_d])
                    res.append(shop_day_weather.ix[i, str_d])
                    res.append(shop_day_weekday.ix[0, str_d])
                    res.append(shop_day_holiday.ix[0, str_d])
                    # 插入此商家前14天的信息
                    l1 = []
                    l2 = []
                    d = begin_date
                    for m in range(14):
                        res.append(shop_day_pay.ix[i, date_to_string(d)])
                        l1.append(shop_day_pay.ix[i, date_to_string(d)])
                        d += delta
                    tmp = sum(res[-14:]) / 14.0
                    res.append(tmp)
                    l1.append(tmp)
                    tmp = sum(res[-8:-1]) / 7.0
                    res.append(tmp)
                    l1.append(tmp)
                    tmp = sum(res[-5:-2]) / 3.0
                    res.append(tmp)
                    l1.append(tmp)
                    d = begin_date
                    for m in range(14):
                        res.append(shop_day_view.ix[i, date_to_string(d)])
                        l2.append(shop_day_view.ix[i, date_to_string(d)])
                        d += delta
                    tmp = sum(res[-14:]) / 14.0
                    res.append(tmp)
                    l2.append(tmp)
                    tmp = sum(res[-8:-1]) / 7.0
                    res.append(tmp)
                    l2.append(tmp)
                    tmp = sum(res[-5:-2]) / 3.0
                    res.append(tmp)
                    l2.append(tmp)
                    for m, n in enumerate(l1):
                        if l2[m] != 0:
                            res.append(n / float(l2[m]))
                        else:
                            res.append(n + 1)
                    # 插入所有商家的平均信息
                    l1 = []
                    l2 = []
                    d = begin_date
                    for m in range(14):
                        res.append(
                            all_shop_day_average_pay.ix[
                                0, date_to_string(d)])
                        l1.append(
                            all_shop_day_average_pay.ix[
                                0, date_to_string(d)])
                        d += delta
                    tmp = sum(res[-14:]) / 14.0
                    res.append(tmp)
                    l1.append(tmp)
                    tmp = sum(res[-8:-1]) / 7.0
                    res.append(tmp)
                    l1.append(tmp)
                    tmp = sum(res[-5:-2]) / 3.0
                    res.append(tmp)
                    l1.append(tmp)
                    d = begin_date
                    for m in range(14):
                        res.append(
                            all_shop_day_average_view.ix[
                                0, date_to_string(d)])
                        l2.append(
                            all_shop_day_average_view.ix[
                                0, date_to_string(d)])
                        d += delta
                    tmp = sum(res[-14:]) / 14.0
                    res.append(tmp)
                    l2.append(tmp)
                    tmp = sum(res[-8:-1]) / 7.0
                    res.append(tmp)
                    l2.append(tmp)
                    tmp = sum(res[-5:-2]) / 3.0
                    res.append(tmp)
                    l2.append(tmp)
                    for m, n in enumerate(l1):
                        if l2[m] != 0:
                            res.append(n / float(l2[m]))
                        else:
                            res.append(n + 1)
                    # 插入预测天数的信息
                    res.append(shop_day_pay.ix[
                               i, date_to_string(d + (q - 1) * delta)])  # 改
                    res.insert(1, date_to_string(d + (q - 1) * delta))  # 改
                    begin_date += delta
                    writer.writerow(res)

    # one hot coding
    for i in range(1, 15):
        dataset = pd.read_csv('dataset{}.csv'.format(i))
        os.remove('dataset{}.csv'.format(i))
        t1 = pd.get_dummies(dataset['city_level'], prefix='city_level')
        t2 = pd.get_dummies(dataset['weather'], prefix='weather')
        t3 = pd.get_dummies(dataset['weekday'], prefix='weekday')
        t4 = pd.get_dummies(dataset['holiday'], prefix='holiday')
        del dataset['city_level'], dataset[
            'weather'], dataset['weekday'], dataset['holiday']
        dataset = pd.concat([dataset.ix[:, :-1], t1, t2,
                             t3, t4, dataset.ix[:, -1]], axis=1)
        dataset.to_csv(path_or_buf='dataset{}.csv'.format( i), index=False)


def one_hot_encoding():
    # 函如其名
    os.chdir('../dataset/train/')
    for i in range(1, 8):
        dataset = pd.read_csv('dataset{}.csv'.format(i))
        t1 = pd.get_dummies(dataset['city_level'], prefix='city_level')
        t2 = pd.get_dummies(dataset['weather'], prefix='weather')
        t3 = pd.get_dummies(dataset['weekday'], prefix='weekday')
        t4 = pd.get_dummies(dataset['holiday'], prefix='holiday')
        del dataset['city_level'], dataset[
            'weather'], dataset['weekday'], dataset['holiday']
        dataset = pd.concat([dataset.ix[:, :-1], t1, t2,
                             t3, t4, dataset.ix[:, -1]], axis=1)
        dataset.to_csv(path_or_buf='dataset{}{}.csv'.format(i, i), index=False)

def train():
    os.chdir('../dataset/')
    for i in range(1, 15):
        # 导入数据
        os.chdir('./train/')
        t = pd.read_csv('dataset{}.csv'.format(i))

        # 用模型训练
        feat_labels = t.columns[2:-1]
        x, y = t.ix[:, 2:-1].values, t.ix[:, -1].values
        forest = RandomForestRegressor(
            n_estimators=100,
            random_state=0,
            n_jobs=-1,
            max_depth=8,
            max_features=0.4,
            oob_score=True,criterion='mse')  # oob_score代替交叉验证
        forest = forest.fit(x, y)
        print forest.score(x, y)

        # 查看特征重要性
        print 'forest:', i
        importances = forest.feature_importances_
        indices = np.argsort(importances)[::-1]
        for f in range(x.shape[1]):
            print feat_labels[indices[f]], importances[indices[f]]

        # 保存模型
        os.chdir('../model/0216/')
        joblib.dump(forest, 'rf_day{}.model'.format(i))
        os.chdir('../')
        os.chdir('../')

def create_predictset():
    '''
    # 用于获得预测的数据
    '''
    os.chdir('../dataset/')
    all_shop_day_average_pay = pd.read_csv('all_shop_day_average_pay.csv')
    all_shop_day_average_view = pd.read_csv('all_shop_day_average_view.csv')
    shop_day_averaget = pd.read_csv(
        'shop_day_averaget.csv').set_index('shop_id')
    shop_day_holiday = pd.read_csv('shop_day_holiday.csv')
    shop_day_lowt = pd.read_csv('shop_day_lowt.csv').set_index('shop_id')
    shop_day_pay = pd.read_csv('shop_day_pay.csv').set_index('shop_id')
    shop_day_upt = pd.read_csv('shop_day_upt.csv').set_index('shop_id')
    shop_day_view = pd.read_csv('shop_day_view.csv').set_index('shop_id')
    shop_day_weather = pd.read_csv('shop_day_weather.csv').set_index('shop_id')
    shop_day_weekday = pd.read_csv('shop_day_weekday.csv')
    #shop_first_no0_date = pd.read_csv('shop_first_no0_date.csv').set_index('shop_id')
    shop_info_modified = pd.read_csv(
        'shop_info_modified.csv').set_index('shop_id')
    shop_average = pd.read_csv('shop_average.csv').set_index('shop_id')
    os.chdir('./model/0216/online/')
    for q in range(1, 15):
        with open('predictset{}.csv'.format(q), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['shop_id',
                             'day_date',
                             'city_level',
                             'location_id',
                             'per_pay',
                             'score',
                             'comment_cnt',
                             'shop_level',
                             'cate_1_name_chaoshibianlidian',
                             'cate_1_name_meishi',
                             'cate_1_name_others',
                             'cate_2_name_bianlidian',
                             'cate_2_name_chaoshi',
                             'cate_2_name_hongbeigaodian',
                             'cate_2_name_huoguo',
                             'cate_2_name_kuaican',
                             'cate_2_name_others',
                             'cate_2_name_qitameishi',
                             'cate_2_name_xiaochi',
                             'cate_2_name_xiuxianchayin',
                             'cate_2_name_xiuxianshipin',
                             'cate_2_name_zhongcan',
                             'average_pay',
                             'average_view',
                             'average_divide',
                             'upt',
                             'lowt',
                             'averaget',
                             'weather',
                             'weekday',
                             'holiday',
                             'before_day_pay_14',
                             'before_day_pay_13',
                             'before_day_pay_12',
                             'before_day_pay_11',
                             'before_day_pay_10',
                             'before_day_pay_9',
                             'before_day_pay_8',
                             'before_day_pay_7',
                             'before_day_pay_6',
                             'before_day_pay_5',
                             'before_day_pay_4',
                             'before_day_pay_3',
                             'before_day_pay_2',
                             'before_day_pay_1',
                             'before_day_pay_14_average',
                             'before_day_pay_7_average',
                             'before_day_pay_3_average',
                             'before_day_view_14',
                             'before_day_view_13',
                             'before_day_view_12',
                             'before_day_view_11',
                             'before_day_view_10',
                             'before_day_view_9',
                             'before_day_view_8',
                             'before_day_view_7',
                             'before_day_view_6',
                             'before_day_view_5',
                             'before_day_view_4',
                             'before_day_view_3',
                             'before_day_view_2',
                             'before_day_view_1',
                             'before_day_view_14_average',
                             'before_day_view_7_average',
                             'before_day_view_3_average',
                             'before_divide_14',
                             'before_divide_13',
                             'before_divide_12',
                             'before_divide_11',
                             'before_divide_10',
                             'before_divide_9',
                             'before_divide_8',
                             'before_divide_7',
                             'before_divide_6',
                             'before_divide_5',
                             'before_divide_4',
                             'before_divide_3',
                             'before_divide_2',
                             'before_divide_1',
                             'before_14_average_divide',
                             'before_7_average_divide',
                             'before_3_average_divide',
                             'before_all_average_pay_14',
                             'before_all_average_pay_13',
                             'before_all_average_pay_12',
                             'before_all_average_pay_11',
                             'before_all_average_pay_10',
                             'before_all_average_pay_9',
                             'before_all_average_pay_8',
                             'before_all_average_pay_7',
                             'before_all_average_pay_6',
                             'before_all_average_pay_5',
                             'before_all_average_pay_4',
                             'before_all_average_pay_3',
                             'before_all_average_pay_2',
                             'before_all_average_pay_1',
                             'before_all_average_pay_average_14',
                             'before_all_average_pay_average_7',
                             'before_all_average_pay_average_3',
                             'before_all_average_view_14',
                             'before_all_average_view_13',
                             'before_all_average_view_12',
                             'before_all_average_view_11',
                             'before_all_average_view_10',
                             'before_all_average_view_9',
                             'before_all_average_view_8',
                             'before_all_average_view_7',
                             'before_all_average_view_6',
                             'before_all_average_view_5',
                             'before_all_average_view_4',
                             'before_all_average_view_3',
                             'before_all_average_view_2',
                             'before_all_average_view_1',
                             'before_all_average_view_average_14',
                             'before_all_average_view_average_7',
                             'before_all_average_view_average_3',
                             'before_all_divide_14',
                             'before_all_divide_13',
                             'before_all_divide_12',
                             'before_all_divide_11',
                             'before_all_divide_10',
                             'before_all_divide_9',
                             'before_all_divide_8',
                             'before_all_divide_7',
                             'before_all_divide_6',
                             'before_all_divide_5',
                             'before_all_divide_4',
                             'before_all_divide_3',
                             'before_all_divide_2',
                             'before_all_divide_1',
                             'before_all_14_average_divide',
                             'before_all_7_average_divide',
                             'before_all_3_average_divide'])
            for i in range(1, 2001):
                z = float(shop_average.ix[i, 'average_view'])
                zz = float(shop_average.ix[i, 'average_pay'])
                if z == 0:
                    z = 1
                    zz += 1
                basic = [i] + list(shop_info_modified.ix[i, :]) + \
                    list(shop_average.ix[i, :]) + [zz / z]
                begin_date = datetime.date(2016, 10, 18)
                delta = datetime.timedelta(days=1)
                res = copy.deepcopy(basic)
                d = begin_date + (13 + q) * delta  # 改
                str_d = date_to_string(d)
                res.append(shop_day_upt.ix[i, str_d])
                res.append(shop_day_lowt.ix[i, str_d])
                res.append(shop_day_averaget.ix[i, str_d])
                res.append(shop_day_weather.ix[i, str_d])
                res.append(shop_day_weekday.ix[0, str_d])
                res.append(shop_day_holiday.ix[0, str_d])
                # 插入此商家前14天的信息
                l1 = []
                l2 = []
                d = begin_date
                for m in range(14):
                    res.append(shop_day_pay.ix[i, date_to_string(d)])
                    l1.append(shop_day_pay.ix[i, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l1.append(tmp)
                d = begin_date
                for m in range(14):
                    res.append(shop_day_view.ix[i, date_to_string(d)])
                    l2.append(shop_day_view.ix[i, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l2.append(tmp)
                for m, n in enumerate(l1):
                    if l2[m] != 0:
                        res.append(n / float(l2[m]))
                    else:
                        res.append(n + 1)
                # 插入所有商家的平均信息
                l1 = []
                l2 = []
                d = begin_date
                for m in range(14):
                    res.append(
                        all_shop_day_average_pay.ix[
                            0, date_to_string(d)])
                    l1.append(
                        all_shop_day_average_pay.ix[
                            0, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l1.append(tmp)
                d = begin_date
                for m in range(14):
                    res.append(
                        all_shop_day_average_view.ix[
                            0, date_to_string(d)])
                    l2.append(
                        all_shop_day_average_view.ix[
                            0, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l2.append(tmp)
                for m, n in enumerate(l1):
                    if l2[m] != 0:
                        res.append(n / float(l2[m]))
                    else:
                        res.append(n + 1)
                res.insert(1, date_to_string(d + (q - 1) * delta))  # 改
                writer.writerow(res)
    # one hot coding
    for i in range(1, 15):
        dataset = pd.read_csv('predictset{}.csv'.format(i))
        os.remove('predictset{}.csv'.format(i))
        t1 = pd.get_dummies(dataset['city_level'], prefix='city_level')
        t2 = pd.get_dummies(dataset['weather'], prefix='weather')
        #注意天气可能出现
        t33 = pd.get_dummies(dataset['weekday'], prefix='weekday')
        weekday = int(dataset.ix[1,'weekday'])
        if weekday!=1 and weekday!=7:
            k1 = pd.DataFrame([[0] * (weekday-1)] * 2000,
                             columns=['weekday_{}'.format(j) for j in range(1,
                                                                            weekday)])
            k2=pd.DataFrame([[0] * (7 - weekday)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(weekday + 1,
                                                                                        8)])
            t3 = pd.concat([k1,
                            t33,
                            k2],
                           axis=1)
        elif weekday==1:
            k=pd.DataFrame([[0] * (7 - weekday)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(weekday + 1,
                                                                                        8)])
            t3 = pd.concat([t33,
                            k],
                           axis=1)
        else:
            k = pd.DataFrame([[0] * (weekday - 1)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(1,
                                                                                        weekday)])
            t3 = pd.concat([k,
                            t33],
                           axis=1)
        t44 = pd.get_dummies(dataset['holiday'], prefix='holiday')
        holiday = int(dataset.ix[1,'holiday'])
        if holiday==0:
            k=pd.DataFrame([[0] * (2 - holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday + 1,
                                                                                        3)])
            t4 = pd.concat([t44,
                            k],
                           axis=1)
        elif holiday==1:
            k1=pd.DataFrame([[0] * (holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday)])
            k2=pd.DataFrame([[0] * (2 - holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday + 1,
                                                                                        3)])
            t4 = pd.concat([k1,
                            t44,
                            k2],
                           axis=1)
        else:
            k=pd.DataFrame([[0] * (holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday)])
            t4 = pd.concat([k,
                            t44],
                           axis=1)
        del dataset['city_level'], dataset[
            'weather'], dataset['weekday'], dataset['holiday']
        dataset = pd.concat([dataset.ix[:, :], t1, t2, t3, t4], axis=1)
        dataset.to_csv(path_or_buf='predictset{}.csv'.format(i), index=False)

def outcome():
    #线上答案生成
    os.chdir('../dataset/model/0216/')
    res = []
    for i in range(1, 2001):
        res.append([i])
    for i in range(1, 8):
        forest=joblib.load('rf_day{}.model'.format(i))
        os.chdir('./online/')
        t = pd.read_csv('predictset{}{}.csv'.format(i, i)).ix[:,2:].values
        os.chdir('../')
        tt = list(forest.predict(t))
        for i in range(2000):
            res[i].append(int(round(float(tt[i]))))
    os.chdir('./online/')
    with open('outcome.csv','w+') as f:
        writer = csv.writer(f)
        for i in range(2000):
            writer.writerow(res[i] + res[i][1:])

def create_offline_predictset():
    '''
    # 用于获得线下预测的数据
    '''
    os.chdir('../dataset/')
    all_shop_day_average_pay = pd.read_csv('all_shop_day_average_pay.csv')
    all_shop_day_average_view = pd.read_csv('all_shop_day_average_view.csv')
    shop_day_averaget = pd.read_csv(
        'shop_day_averaget.csv').set_index('shop_id')
    shop_day_holiday = pd.read_csv('shop_day_holiday.csv')
    shop_day_lowt = pd.read_csv('shop_day_lowt.csv').set_index('shop_id')
    shop_day_pay = pd.read_csv('shop_day_pay.csv').set_index('shop_id')
    shop_day_upt = pd.read_csv('shop_day_upt.csv').set_index('shop_id')
    shop_day_view = pd.read_csv('shop_day_view.csv').set_index('shop_id')
    shop_day_weather = pd.read_csv('shop_day_weather.csv').set_index('shop_id')
    shop_day_weekday = pd.read_csv('shop_day_weekday.csv')
    #shop_first_no0_date = pd.read_csv('shop_first_no0_date.csv').set_index('shop_id')
    shop_info_modified = pd.read_csv(
        'shop_info_modified.csv').set_index('shop_id')
    shop_average = pd.read_csv('shop_average.csv').set_index('shop_id')
    os.chdir('./model/0216/offline/')
    for q in range(1, 15):
        with open('predictset{}.csv'.format(q), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['shop_id',
                             'day_date',
                             'city_level',
                             'location_id',
                             'per_pay',
                             'score',
                             'comment_cnt',
                             'shop_level',
                             'cate_1_name_chaoshibianlidian',
                             'cate_1_name_meishi',
                             'cate_1_name_others',
                             'cate_2_name_bianlidian',
                             'cate_2_name_chaoshi',
                             'cate_2_name_hongbeigaodian',
                             'cate_2_name_huoguo',
                             'cate_2_name_kuaican',
                             'cate_2_name_others',
                             'cate_2_name_qitameishi',
                             'cate_2_name_xiaochi',
                             'cate_2_name_xiuxianchayin',
                             'cate_2_name_xiuxianshipin',
                             'cate_2_name_zhongcan',
                             'average_pay',
                             'average_view',
                             'average_divide',
                             'upt',
                             'lowt',
                             'averaget',
                             'weather',
                             'weekday',
                             'holiday',
                             'before_day_pay_14',
                             'before_day_pay_13',
                             'before_day_pay_12',
                             'before_day_pay_11',
                             'before_day_pay_10',
                             'before_day_pay_9',
                             'before_day_pay_8',
                             'before_day_pay_7',
                             'before_day_pay_6',
                             'before_day_pay_5',
                             'before_day_pay_4',
                             'before_day_pay_3',
                             'before_day_pay_2',
                             'before_day_pay_1',
                             'before_day_pay_14_average',
                             'before_day_pay_7_average',
                             'before_day_pay_3_average',
                             'before_day_view_14',
                             'before_day_view_13',
                             'before_day_view_12',
                             'before_day_view_11',
                             'before_day_view_10',
                             'before_day_view_9',
                             'before_day_view_8',
                             'before_day_view_7',
                             'before_day_view_6',
                             'before_day_view_5',
                             'before_day_view_4',
                             'before_day_view_3',
                             'before_day_view_2',
                             'before_day_view_1',
                             'before_day_view_14_average',
                             'before_day_view_7_average',
                             'before_day_view_3_average',
                             'before_divide_14',
                             'before_divide_13',
                             'before_divide_12',
                             'before_divide_11',
                             'before_divide_10',
                             'before_divide_9',
                             'before_divide_8',
                             'before_divide_7',
                             'before_divide_6',
                             'before_divide_5',
                             'before_divide_4',
                             'before_divide_3',
                             'before_divide_2',
                             'before_divide_1',
                             'before_14_average_divide',
                             'before_7_average_divide',
                             'before_3_average_divide',
                             'before_all_average_pay_14',
                             'before_all_average_pay_13',
                             'before_all_average_pay_12',
                             'before_all_average_pay_11',
                             'before_all_average_pay_10',
                             'before_all_average_pay_9',
                             'before_all_average_pay_8',
                             'before_all_average_pay_7',
                             'before_all_average_pay_6',
                             'before_all_average_pay_5',
                             'before_all_average_pay_4',
                             'before_all_average_pay_3',
                             'before_all_average_pay_2',
                             'before_all_average_pay_1',
                             'before_all_average_pay_average_14',
                             'before_all_average_pay_average_7',
                             'before_all_average_pay_average_3',
                             'before_all_average_view_14',
                             'before_all_average_view_13',
                             'before_all_average_view_12',
                             'before_all_average_view_11',
                             'before_all_average_view_10',
                             'before_all_average_view_9',
                             'before_all_average_view_8',
                             'before_all_average_view_7',
                             'before_all_average_view_6',
                             'before_all_average_view_5',
                             'before_all_average_view_4',
                             'before_all_average_view_3',
                             'before_all_average_view_2',
                             'before_all_average_view_1',
                             'before_all_average_view_average_14',
                             'before_all_average_view_average_7',
                             'before_all_average_view_average_3',
                             'before_all_divide_14',
                             'before_all_divide_13',
                             'before_all_divide_12',
                             'before_all_divide_11',
                             'before_all_divide_10',
                             'before_all_divide_9',
                             'before_all_divide_8',
                             'before_all_divide_7',
                             'before_all_divide_6',
                             'before_all_divide_5',
                             'before_all_divide_4',
                             'before_all_divide_3',
                             'before_all_divide_2',
                             'before_all_divide_1',
                             'before_all_14_average_divide',
                             'before_all_7_average_divide',
                             'before_all_3_average_divide'])
            for i in range(1, 2001):
                z = float(shop_average.ix[i, 'average_view'])
                zz = float(shop_average.ix[i, 'average_pay'])
                if z == 0:
                    z = 1
                    zz += 1
                basic = [i] + list(shop_info_modified.ix[i, :]) + \
                    list(shop_average.ix[i, :]) + [zz / z]
                begin_date = datetime.date(2016, 10, 4)
                delta = datetime.timedelta(days=1)
                res = copy.deepcopy(basic)
                d = begin_date + (13 + q) * delta  # 改
                str_d = date_to_string(d)
                res.append(shop_day_upt.ix[i, str_d])
                res.append(shop_day_lowt.ix[i, str_d])
                res.append(shop_day_averaget.ix[i, str_d])
                res.append(shop_day_weather.ix[i, str_d])
                res.append(shop_day_weekday.ix[0, str_d])
                res.append(shop_day_holiday.ix[0, str_d])
                # 插入此商家前14天的信息
                l1 = []
                l2 = []
                d = begin_date
                for m in range(14):
                    res.append(shop_day_pay.ix[i, date_to_string(d)])
                    l1.append(shop_day_pay.ix[i, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l1.append(tmp)
                d = begin_date
                for m in range(14):
                    res.append(shop_day_view.ix[i, date_to_string(d)])
                    l2.append(shop_day_view.ix[i, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l2.append(tmp)
                for m, n in enumerate(l1):
                    if l2[m] != 0:
                        res.append(n / float(l2[m]))
                    else:
                        res.append(n + 1)
                # 插入所有商家的平均信息
                l1 = []
                l2 = []
                d = begin_date
                for m in range(14):
                    res.append(
                        all_shop_day_average_pay.ix[
                            0, date_to_string(d)])
                    l1.append(
                        all_shop_day_average_pay.ix[
                            0, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l1.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l1.append(tmp)
                d = begin_date
                for m in range(14):
                    res.append(
                        all_shop_day_average_view.ix[
                            0, date_to_string(d)])
                    l2.append(
                        all_shop_day_average_view.ix[
                            0, date_to_string(d)])
                    d += delta
                tmp = sum(res[-14:]) / 14.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-8:-1]) / 7.0
                res.append(tmp)
                l2.append(tmp)
                tmp = sum(res[-5:-2]) / 3.0
                res.append(tmp)
                l2.append(tmp)
                for m, n in enumerate(l1):
                    if l2[m] != 0:
                        res.append(n / float(l2[m]))
                    else:
                        res.append(n + 1)
                res.insert(1, date_to_string(d + (q - 1) * delta))  # 改
                writer.writerow(res)
    # one hot coding
    for i in range(1, 15):
        dataset = pd.read_csv('predictset{}.csv'.format(i))
        os.remove('predictset{}.csv'.format(i))
        t1 = pd.get_dummies(dataset['city_level'], prefix='city_level')
        t2 = pd.get_dummies(dataset['weather'], prefix='weather')
        #注意天气可能出现
        t33 = pd.get_dummies(dataset['weekday'], prefix='weekday')
        weekday = int(dataset.ix[1,'weekday'])
        if weekday!=1 and weekday!=7:
            k1 = pd.DataFrame([[0] * (weekday-1)] * 2000,
                             columns=['weekday_{}'.format(j) for j in range(1,
                                                                            weekday)])
            k2=pd.DataFrame([[0] * (7 - weekday)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(weekday + 1,
                                                                                        8)])
            t3 = pd.concat([k1,
                            t33,
                            k2],
                           axis=1)
        elif weekday==1:
            k=pd.DataFrame([[0] * (7 - weekday)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(weekday + 1,
                                                                                        8)])
            t3 = pd.concat([t33,
                            k],
                           axis=1)
        else:
            k = pd.DataFrame([[0] * (weekday - 1)] * 2000,
                                         columns=['weekday_{}'.format(j) for j in range(1,
                                                                                        weekday)])
            t3 = pd.concat([k,
                            t33],
                           axis=1)
        t44 = pd.get_dummies(dataset['holiday'], prefix='holiday')
        holiday = int(dataset.ix[1,'holiday'])
        if holiday==0:
            k=pd.DataFrame([[0] * (2 - holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday + 1,
                                                                                        3)])
            t4 = pd.concat([t44,
                            k],
                           axis=1)
        elif holiday==1:
            k1=pd.DataFrame([[0] * (holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday)])
            k2=pd.DataFrame([[0] * (2 - holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday + 1,
                                                                                        3)])
            t4 = pd.concat([k1,
                            t44,
                            k2],
                           axis=1)
        else:
            k=pd.DataFrame([[0] * (holiday)] * 2000,
                                         columns=['holiday_{}'.format(j) for j in range(holiday)])
            t4 = pd.concat([k,
                            t44],
                           axis=1)
        del dataset['city_level'], dataset[
            'weather'], dataset['weekday'], dataset['holiday']
        dataset = pd.concat([dataset.ix[:, :], t1, t2, t3, t4], axis=1)
        dataset.to_csv(
            path_or_buf='predictset{}.csv'.format(
                i, i), index=False)

def offline_outcome():
    os.chdir('../dataset/model/0216/')
    res = []
    for i in range(1, 2001):
        res.append([i])
    for i in range(1, 15):
        forest=joblib.load('rf_day{}.model'.format(i))
        os.chdir('./offline/')
        t = pd.read_csv('predictset{}.csv'.format(i, i)).ix[:,2:].values
        os.chdir('../')
        tt = list(forest.predict(t))
        for i in range(2000):
            res[i].append(int(round(float(tt[i]))))
    os.chdir('./offline/')
    with open('outcome.csv','w+') as f:
        writer = csv.writer(f)
        for i in range(2000):
            writer.writerow(res[i] + res[i][1:])

def offline_score():
    os.chdir('../dataset/')
    shop_day_pay=pd.read_csv('shop_day_pay.csv').set_index('shop_id')
    os.chdir('./model/0216/offline/')
    outcome=pd.read_csv('outcome.csv',header=None)
    total=0.0
    date=datetime.date(2016,10,18)
    delta=datetime.timedelta(days=1)
    for i in range(1,2001):
        d=date
        for j in range(14):
            total+=abs(float((shop_day_pay.ix[i,date_to_string(d)]-outcome.ix[i-1,j+1])/float((shop_day_pay.ix[i,date_to_string(d)]+outcome.ix[i-1,j+1]))))
            d+=delta
    print float(total/28000)

if __name__ == '__main__':
    offline_outcome()
    offline_score()

