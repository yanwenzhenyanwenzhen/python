import pandas as pd
x=pd.read_excel('TRD_Cale.xlsx')

list1_m=[]      #list1放的是每周第一天
list2_m=[]      #list2放的是每周的最后一天
import numpy as np
for m in np.arange(1,13):
    #转换字符串
   if m<10:
     d1='2017-0'+str(m)+'-01'
     d2='2017-0'+str(m)+'-31'
   else:
     d1='2017-'+str(m)+'-01'
     d2='2017-'+str(m)+'-31'
   I1=x.iloc[:,1]>=d1
   I2=x.iloc[:,1]<=d2
   I=I1&I2
   xs=x.iloc[I.values,[1]]['Clddt'].sort_values()
   if len(xs)>1:
       # 第1个数据即为当月最小交易日期，添加到list1中
      list1_m.append(xs.values[0])
      # 最后1个数据即为当月最大交易日期，添加到list2中
      list2_m.append(xs.values[len(xs)-1])

data=pd.read_excel('IDX_Idxtrd.xlsx')

import numpy as np
# 返回一个给定形状和类型的用0填充的数组
r=np.zeros(len(list1_m))
for i in range(len(list1_m)):
    #最大交易日的收盘指数
    p1=data.loc[data['Idxtrd01'].values==list1_m[i],'Idxtrd05'].values
    #最大交易日的收盘指数
    p2=data.loc[data['Idxtrd01'].values==list2_m[i],'Idxtrd05'].values
    # 利用月收益率计算公式计算获得月收益率指标数据
    r[i]=(p2-p1)/p1*100
sorted(r, reverse=True)
print(r)

