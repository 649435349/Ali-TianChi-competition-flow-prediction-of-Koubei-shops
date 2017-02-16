# -*- coding: utf-8 -*-
'''
ubuntu 可以直接运行
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.chdir('../dataset/训练集/')
import csv

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold,cross_val_score
from sklearn.externals import joblib

import pandas as pd
import numpy as np

'''
#用模型训练
x,y=t.ix[:,1:-1].values,t.ix[:,-1].values
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,random_state=0)
forest=RandomForestRegressor(n_estimators=100,random_state=0,n_jobs=-1)
forest=forest.fit(x_train,y_train)
print forest.score(x_test,y_test)


print 'forest'
#导入数据
t=pd.read_csv('data_set_payandview_pay.csv')
feat_labels=t.columns[1:-1]

#交叉验证
x,y=t.ix[:,1:-1].values,t.ix[:,-1].values
forest=RandomForestRegressor(n_estimators=100,random_state=0,n_jobs=-1)
kf = KFold(n_splits=10)
for train,test in kf.split(x):
    forest=forest.fit(x[train],y[train])
    print forest.score(x[test],y[test])

#查看特征重要性

importances=forest.feature_importances_
indices=np.argsort(importances)[::-1]
for f in range(x.shape[1]):
    print feat_labels[f],importances[indices[f]]

print 'forest1'
#导入数据
t=pd.read_csv('data_set_view_view.csv')
feat_labels=t.columns[1:-1]

#交叉验证
x,y=t.ix[:,1:-1].values,t.ix[:,-1].values
forest1=RandomForestRegressor(n_estimators=100,random_state=0,n_jobs=-1)
kf = KFold(n_splits=10)
for train,test in kf.split(x):
    forest1=forest1.fit(x[train],y[train])
    print forest1.score(x[test],y[test])

#查看特征重要性

importances=forest1.feature_importances_
indices=np.argsort(importances)[::-1]
for f in range(x.shape[1]):
    print feat_labels[f],importances[indices[f]]

#保存模型
os.chdir('../模型集/')
joblib.dump(forest,'rf_payandview_pay_0212.model')
joblib.dump(forest1,'rf_view_view_0212.model')

#交叉验证
kf = KFold(n_splits=10)
forest=RandomForestRegressor(n_estimators=100,random_state=0,n_jobs=-1)
for train,test in kf.split(x):
    forest=forest.fit(x[train],y[train])
    print forest.score(x[test],y[test])


交叉验证计算准确率
scores = cross_val_score(forest, x, y, cv=10)
print scores
'''

os.chdir('../模型集/')
forest=joblib.load('rf_payandview_pay_0212.model')
forest1=joblib.load('rf_view_view_0212.model')
os.chdir('../结果集/')
t=pd.read_csv('shop_payandview_pay.csv').ix[:,1:].values
tv=pd.read_csv('shop_view_view.csv').ix[:,1:].values
res=[]
before=1
before1=1
for i in range(1,2001):
    res.append([i])

for i in range(1,15):
    if i==1:
        tt=forest.predict(t)
        before=np.array([[i] for i in tt])
        tt1=forest1.predict(tv)
        before1=np.array([[i] for i in tt1])
        for i,j in enumerate(list(tt)):
            res[i].append(int(round(float(j))))
    else:
        t1=t[:,:20]
        t2=t[:,20:27]
        t3=t[:,27:]
        t2=np.concatenate([t2[:,1:],before1],axis=1)
        t3 = np.concatenate([t3[:, 1:], before], axis=1)
        t=np.concatenate([t1,t2,t3],axis=1)
        tt = forest.predict(t)
        before = np.array([[i] for i in tt])

        t1 = tv[:, :20]
        t2 = tv[:, 20:]
        t2 = np.concatenate([t2[:, 1:], before1], axis=1)
        tv = np.concatenate([t1, t2], axis=1)
        tt1 = forest1.predict(tv)
        before1 = np.array([[i] for i in tt1])
        for i, j in enumerate(list(tt)):
            res[i].append(int(round(float(j))))

with open('0213_new.csv','w+') as f:
    writer=csv.writer(f)
    writer.writerows(res)