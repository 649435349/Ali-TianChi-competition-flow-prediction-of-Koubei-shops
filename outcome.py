# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import csv

from sklearn.externals import joblib
import pandas as pd
import numpy as np

os.chdir('../dataset/模型集/')
rf_pay_pay_model=joblib.load('rf_pay_pay.model')
os.chdir('../结果集/')
t=pd.read_csv('shop_day_pay.csv').ix[:,1:].values
res=[]
before=1
for i in range(1,2001):
    res.append([i])

for i in range(1,15):
    if i==1:
        tt=rf_pay_pay_model.predict(t)
        before=np.array([[i] for i in tt])
        for i,j in enumerate(list(tt)):
            res[i].append(int(round(float(j))))
    else:
        t1=t[:,:20]
        t2=t[:,20:-12]
        t3=t[:,-12:]
        t2=np.concatenate([t2[:,1:],before],axis=1)
        t=np.concatenate([t1,t2,t3],axis=1)
        tt = rf_pay_pay_model.predict(t)
        before = np.array([[i] for i in tt])
        for i, j in enumerate(list(tt)):
            res[i].append(int(round(float(j))))

with open('outcome_021216.csv','w+') as f:
    writer=csv.writer(f)
    writer.writerows(res)