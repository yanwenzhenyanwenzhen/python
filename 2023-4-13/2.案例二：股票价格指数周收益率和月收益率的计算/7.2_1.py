import pandas as pd
x=pd.read_excel('TRD_Cale.xlsx')

#根据日期正序
x.sort_values(by='Clddt', ascending=False, inplace=True)

list1=['2017-01-03']    #list1放的是每周第一天
list2=[]                #list2放的是每周的最后一天
for t in range(1,len(x)-1):
    p = x.iloc[t - 1, [2]][0]   #前一天的Daywk
    q = x.iloc[t, [2]][0]       #当天的Daywk
    if q < p:
        list1.append(x.iloc[t, [1]][0])     #第1个数据即为当月最小交易日期，添加到list1中
        list2.append(x.iloc[t - 1, [1]][0]) #最后1个数据即为当月最大交易日期，添加到list2中
list2.append('2017-12-29')
data=pd.read_excel('IDX_Idxtrd.xlsx')

import numpy as np
# 返回一个给定形状和类型的用0填充的数组
r=np.zeros(len(list1))
for i in range(len(list1)):
    #取最大交易日的收盘指数
    p1=data.loc[data['Idxtrd01'].values==list1[i],'Idxtrd05'].values
    #取最小交易日的收盘指数
    p2=data.loc[data['Idxtrd01'].values==list2[i],'Idxtrd05'].values
    #利用月收益率计算公式计算获得月收益率指标数据
    r[i]=(p2-p1)/p1
  
