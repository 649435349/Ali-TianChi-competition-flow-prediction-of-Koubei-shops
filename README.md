README
===========================
****
### Author:冯宇飞
### E-mail:649435349@qq.com
### Wechat:fyf649435349
****

## What is it?
```
仅作校招参考使用……
阿里天池大赛代码，题目链接为https://tianchi.aliyun.com/competition/introduction.htm?spm=5176.100066.333.8.5ccac458TFY2Kg&raceId=231591。
简单来说是预测2000个商家后14天的销售情况。
```
   
## What is used and what is the performance?
```
全部用Python写成，Python也是我最喜欢的语言。
用了大量的库,如Numpy,Pandas,Sklearn,Seaborn,Xgboost……
更多的数据分析工作在ipython中实现了。
最后ranked TOP5%(实习期间实在是没精力打比赛，太累了……)，第一次参加比赛，大量代码看起来真的很还丑陋，在之后的JD的比赛代码有很多改进。
```

## The Structure of the project?
```
`./analyse.py`初步分析数据
`./create_data_set（2）.py`建立数据集（没有用mysql，数据集保存下来，添加特征时导入再加），整合其他特征
`./create_data_set3.py`主要文件，作用：整合数据，修改特征，构造特征，建立数据集，训练，输出结果，交叉验证，模型融合……
`./outcome.py`生成线上和线下结果
`./rf_model.py`用了RF模型
```
