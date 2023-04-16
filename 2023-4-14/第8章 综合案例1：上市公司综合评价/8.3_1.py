# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:53:57 2018

@author: Administrator
"""
import pandas as pd
data=pd.read_excel('data.xlsx')
# data2=data.iloc[data['Accper'].values=='2016-12-31',[ 0,2,3,4,5,6,7,8,9,10,11]]
# dataframe删除某中间列
data2=data.iloc[data['Accper'].values=='2016-12-31'].drop(["Accper"], axis=1)
# 改行每个值都大于0
data2=data2[data2>0]
# 有空值的行整行删除
data2.dropna(how="any", inplace=True)
# 避免指标间scale(数量级)差别太大
from sklearn.preprocessing import StandardScaler
# 排除不参与标准化的列，通常为非数值列
X=data2.iloc[:,1:]
# 初始化一个标注正态变换器
scaler = StandardScaler()
# scaler.fit(X)
# X = scaler.transform()
scaler.fit(X) 
X=scaler.transform(X)  
from sklearn.decomposition import PCA 
pca=PCA(n_components=5)      #累计贡献率为95%
Y=pca.fit_transform(X)            #满足累计贡献率为95%的主成分数据
gxl=pca.explained_variance_ratio_   #贡献率


import numpy as np

# F=np.zeros((len(Y)))
# for i in range(len(gxl)):
#     f=Y[:,i]*gxl[i]
#     F=F+f
#
# fs1=pd.Series(F,index=data2['Stkcd'].values)
# Fscore1=fs1.sort_values(ascending=False)   #降序，True为升序

import numpy as np
# 特征值*特征向量代替原输入矩阵
Fscore1 = pd.DataFrame()
Fscore1["score"] = pd.DataFrame(gxl*Y).apply(sum,axis=1)
Fscore1["Stkcd"] = data2["Stkcd"]
# Fscore1.sort_values(by="score", ascending=False,inplace=True)
# 读取上市公司股票代码机器机器名称的对应表
co=pd.read_excel('TRD_Co.xlsx')
# 将有名称拼接到原结果Fscore1上
Fscore2=pd.merge(Fscore1.dropna(), co, how="left", on="Stkcd").sort_values(by="score", ascending=False)
# 将上海证券交易所挂牌的00开头的代码左补0
Fscore2["Stkcd"]=Fscore2["Stkcd"].apply(lambda  a:str(int(a)).zfill(6))
# Fscore2=fs2.sort_values(ascending=False)   #降序，True为升序


# 选出的前30公司真的在未来股价受益了吗？
trd=pd.read_excel('trd_2017.xlsx')
trd=trd[trd["Stkcd"] in Fscore1]
r_list=[]
for i in range(30):
    code=Fscore1.index[i]
    trd['Stkcd']=Fscore2["Stkcd"].apply(lambda  a:str(int(a)).zfill(6))
    # dt=trd.iloc[trd.iloc[:,0].values==code,:]
    dt = trd[trd['Stkcd']==code]
    I1=dt['Trddt'].values>='2017-05-01'
    I2=dt['Trddt'].values<='2017-12-31'
    dtt=dt.iloc[I1&I2,:].sort_values('Trddt')
    # 若该股票有被收录的日期，避免下表越界index out of range
    if len(dtt)>1:
        p1=dtt['Adjprced'][0]
        p2=dtt['Adjprced'][-1]
        r_list.append((p2-p1)/p1)
   
# r_total=sum(r_list)
r_mean = np.mean(r_list)

