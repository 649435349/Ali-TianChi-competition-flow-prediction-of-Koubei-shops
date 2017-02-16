# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re
import csv
import pymysql
import datetime

os.chdir('../dataset/')

'''
处理城市信息
s1='1:杭州 北京 上海 广州 深圳'
s21='2:成都 苏州 天津 南京 济南 重庆 青岛 大连 宁波 厦门 '
s22='2.33333333: 武汉 哈尔滨 沈阳 西安 长春 长沙 福州 郑州 石家庄  佛山 东莞 无锡 烟台 太原 '
s23='2.6666:合肥 南昌 南宁 昆明(地级市省会)温州(重要的经济城市)淄博(重要的工业城市)唐山（河北经济强市）'
s3='舟山三亚3:乌鲁木齐（****首府）贵阳（贵州省会）海口（海南省会）兰州（甘肃省会）银川（宁夏**首府）西宁（青海省会）呼和浩特（内蒙古首府）泉州（福建经济第一强市）包头（内蒙古第一大城市，经济第二强市）南通（江苏经济强市）大庆（黑龙江经济强市）徐州（江苏经济强市）潍坊（山东经济强市）常州（江苏经济强市）鄂尔多斯（内蒙古经济第一强市）绍兴（浙江经济强市）济宁（山东经济强市）盐城（江苏经济强市）邯郸（河北经济第三强市）临沂（山东经济强市）洛阳（河南经济强市、古都）东营（山东经济强市）扬州（江苏经济强市）台州（浙江经济强市）嘉兴（浙江经济强市）沧州（河北经济强市）榆林（陕西经济第二强市）泰州（江苏经济强市）镇江（江苏经济强市）昆山（全国百强县第一名）江阴（全国百强县第二名）张家港（全国百强县第三名）义乌（浙江经济强市县级市）金华（浙江经济强市）保定（河北经济强市）吉林（吉林经济第二强市）鞍山（辽宁经济第三强市）泰安（山东经济强市）宜昌（湖北经济第二强市）襄阳（湖北经济第三强市）中山（广东经济强市）惠州（广东经济强市）南阳（河南经济强市）威海（山东经济强市）德州（山东经济强市）岳阳（湖南经济第二强市）聊城（山东经济强市）常德（湖南经济强市）漳州（福建经济第四强市）滨州（山东经济强市）茂名（广东经济强市）淮安（江苏经济强市）江门（广东经济强市）芜湖（安徽经济第二强市）湛江（广东经济强市）廊坊（河北经济强市）菏泽（山东经济强市）柳州（广西经济第二强市）宝鸡（陕西第二大城市、经济第四强市）珠海（特区、广东经济第十强市）绵阳（四川第二大城市）'
s4='铜陵黄山咸宁4:株洲（湖南经济第五强市）枣庄（山东经济第十五强市）许昌（河南经济第四强市）通辽（内蒙古经济第四强市）湖州（浙江经济第八强市）新乡（河南经济第五强市）咸阳（陕西经济第三强市）松原（吉林经济第三强市）连云港（江苏经济第十二强市）安阳（河南经济第六强市）周口（河南经济第七强市）焦作（河南经济第八强市）赤峰（内蒙古经济第五强市）邢台（河北经济第七强市）郴州（湖南经济第六强市）宿迁（江苏经济第十三强市）赣州（江西经济第二强市）平顶山（河南经济第九强市）桂林（广西经济第三强市）肇庆（广东经济第十一强市）曲靖（云南经济第二强市）九江（江西经济第三强市）商丘（河南经济第十强市）汕头（广东经济第十二强市）信阳（河南经济第十一强市）驻马店（河南经济第十二强市）营口（辽宁经济第四强市）揭阳（广东经济第十三强市）龙岩（福建经济第五强市）安庆（安徽经济第三强市）日照（山东经济第十五强市）遵义（贵州经济第二强市）三明（福建经济第六强市）呼伦贝尔（内蒙古经济第六强市）长治（山西经济第二强市）湘潭（湖南经济第七强市）德阳（四川经济第三强市）南充（四川地级市）乐山（四川地级市）达州（四川地级市）盘锦（辽宁地级市）延安（陕西地级市）上饶（江西地级市）锦州（辽宁地级市）宜春（江西地级市）宜宾（四川地级市）张家口（河北地级市）马鞍山（安徽地级市）吕梁（山西地级市）抚顺（辽宁地级市）临汾（山西地级市）渭南（陕西地级市）开封（河南地级市，古都）莆田（福建地级市）荆州（湖北地级市）黄冈（湖北地级市）四平（吉林地级市）承德（河北地级市）齐齐哈尔（黑龙江地级市）三门峡（河南地级市）秦皇岛（河北地级市）本溪（辽宁地级市）玉林（广西地级市）孝感（湖北地级市）牡丹江（黑龙江地级市）荆门（湖北地级市）宁德（湖南地级市）运城（山西地级市）绥化（黑龙江地级市）永州（湖南地级市）怀化（湖南地级市、湘西第一大市）黄石（湖北地级市）泸州（四川地级市）清远（广东地级市）邵阳（湖南地级市）衡水（河北地级市）益阳（湖南地级市）丹东（辽宁地级市、中国口岸第一大市）铁岭（辽宁地级市）晋城（山西地级市）朔州（山西地级市）吉安（江西地级市）娄底（湖南地级市）玉溪（云南地级市）辽阳（辽宁地级市）南平（福建地级市）濮阳（河南地级市）晋中（山西地级市）资阳（四川地级市）都江堰（四川县级市）攀枝花（四川地级市）衢州（浙江地级市）内江（四川地级市）滁州（安徽地级市）阜阳（安徽地级市）十堰（湖北地级市）大同（山西地级市）朝阳（辽宁地级市）六安（安徽地级市）宿州（安徽地级市）通化（吉林地级市）蚌埠（安徽地级市）韶关（广东地级市）丽水（浙江地级市）自贡（四川地级市）阳江（广东地级市）毕节（贵州地级市）'
s5='天门思茅安康汉中葫芦岛梧州汕尾淮北5:拉萨（西藏**首府）克拉玛依（**经济第二强市，地级市）库尔勒（**第二大城市，县级市、州府）昌吉（**县级市、州府）哈密（**县级市、地区行署所在地）伊宁（县级市、州府）喀什（**县级市、地区行署所在地）阿克苏（**县级市、地区行署所在地）石河子（**兵团第一大城市）晋江（福建经济发达县级市）增城（广东经济发达县级市）诸暨（浙江经济发达县级市）丹阳（江苏经济发达县级市）玉环（浙江经济发达县）常熟（江苏经济发达县级市）崇明（上海经济发达县）余姚（浙江经济发达县级市）奉化（浙江经济发达县级市）海宁（浙江经济发达县级市）浏阳市（湖南县级市）大理（云南县级市、州府）丽江（云南地级市）普洱（云南地级市）保山（云南地级市）昭通（云南地级市）西昌（四川县级市、州府）雅安（四川地级市）广安（四川县级市）广元（四川地级市）巴中（四川地级市）遂宁（四川地级市）天水（甘肃第二大城市）酒泉（甘肃地级市）嘉峪关（甘肃地级市）武威（甘肃地级市）张掖，石嘴山，吴忠，北海，百色，虎门镇，长安镇，鳌江-龙港镇'
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004',charset='utf8')
cur = conn.cursor()
cur.execute('use competition')
for i in range(1,2001):
    sql='select city_level from shop_info where shop_id=(%s)'
    cur.execute(sql,(i))
    t=cur.fetchone()[0]
    if t in s1:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (6,i))
        conn.commit()
    elif t in s21:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (5,i))
        conn.commit()
    elif t in s22:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (4.666666,i))
        conn.commit()
    elif t in s23:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (4.333333,i))
        conn.commit()
    elif t in s3:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (3,i))
        conn.commit()
    elif t in s4:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (2,i))
        conn.commit()
    elif t in s5:
        sql1='update shop_info set city_level=(%s) where shop_id=(%s)'
        cur.execute(sql1, (1,i))
        conn.commit()
cur.close()
conn.close()
'''
'''
delta=datetime.timedelta(days=1)
date=datetime.datetime(2015,6,26)
count=0
while date.year != 2016 or date.month != 11 or date.day != 1:
    count+=1
    date+=delta
print count
'''
'''
看看数据对不对
with open('shop_day_pay.csv','a+') as f:
    reader=csv.reader(f)
    s=0
    reader.next()
    for i in reader:
        s+=sum(map(lambda i:int(i),i[1:]))
    print s

'''
def change(item):
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item
with open('shop_day_pay.csv','w+') as f:
    res=['shop_id']
    date = datetime.datetime(2015, 6, 26)
    delta = datetime.timedelta(days=1)
    while date.year != 2016 or date.month != 11 or date.day != 1:
        res.append('{}-{}-{}'.format(change(date.year),change(date.month),change(date.day)))
        date+=delta
    writer=csv.writer(f)
    writer.writerow(res)
'''
#输出成csv
def change(item):
    item = str(item)
    if len(item) < 2:
        item = '0' + item
    return item
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004',charset='utf8')
cur = conn.cursor()
cur.execute('use competition')
delta=datetime.timedelta(days=1)
with open('shop_day_pay.csv','a+') as f:
    for i in range(1,2001):
        s=str(i)+','
        date = datetime.datetime(2015, 6, 26)
        while date.year != 2016 or date.month != 11 or date.day != 1:
            sql='select count(*) from user_pay where shop_id=(%s) and  time_stamp=(%s);'
            cur.execute(sql,(i,'{}-{}-{}'.format(change(date.year),change(date.month),change(date.day))))
            t=cur.fetchone()[0]
            if date.year != 2016 or date.month != 10 or date.day != 31:
                if t==0:
                    s+='0,'
                else:
                    s+=str(t)+','
            else:
                if t==0:
                    s+='0'
                else:
                    s+=str(t)
            date += delta
        f.write(s)
        f.write('\n')
cur.close()
conn.close()
'''
'''
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004',charset='utf8')
cur = conn.cursor()
cur.execute('use competition')
with open('shop_info_modified.csv') as f:
    reader=csv.reader(f)
    reader.next()
    for i in range(2000):
        l=[i.decode('utf-8') for i in reader.next()]
        sql="update shop_info set cate_2_name=(%s) where shop_id=(%s)"
        cur.execute(sql,(l[-2],l[0]))
        conn.commit()
cur.close()
conn.close()
'''




