# coding=utf-8
import tushare as ts    # 导入库
import numpy as np
import pandas as pd
import datetime
import time
# 指定保存的文件名
token='replace your token'
ts.set_token(token)
pro = ts.pro_api()
time_1 = datetime.datetime.now()
time_2 = time_1 + datetime.timedelta(hours=-1)
times_1 = time_1.strftime("%Y-%m-%d %H:%M:%S")
times_2 = time_2.strftime("%Y-%m-%d %H:%M:%S")
fileName='newslistTs.csv'
stockList=pd.DataFrame(pro.news(src='sina', start_date=times_2, end_date=times_1))    # 调用方法得到信息
print(stockList)        
stockList.to_csv(fileName,encoding='utf-8')   # 保存到csv中
