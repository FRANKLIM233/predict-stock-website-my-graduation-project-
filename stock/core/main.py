# coding=utf-8
import requests
import re
from mysite.settings import MEDIA_ROOT
from traceback import print_exc
import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.ticker import MultipleLocator
from sklearn import svm,preprocessing
import os
import fix_yahoo_finance as yf


from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"/workspace/django_scripts/stock/mysite/STFANGSO.TTF", size=14)


class Stock():
    def __init__(self, code, _type, start_date, end_date):
        self.csv_path = MEDIA_ROOT / f'{code}-{start_date}-{end_date}.csv'
        self.kline_path = MEDIA_ROOT / f'{code}-{start_date}-{end_date}.png'
        self.svm_pred_path = MEDIA_ROOT / f'{code}-{start_date}-{end_date}-pred.png'
        self._type = _type
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
    
    def crawl(self):
        """
        爬取数据
        """
        if os.path.exists(self.csv_path):
            return True # 文件存在则不爬取
        try:
            code_map = {
                'SZ': 'sz',
                'SH': 'ss',
            }
            yf.pdr_override()
            stock = pandas_datareader.get_data_stooq(f'{self.code}.{code_map[self._type]}', self.start_date, self.end_date)
            stock.to_csv(self.csv_path)
            return True
        except:
            print_exc()
            return False


    def plot_kline(self):
        """
        绘制K线图
        """
        if os.path.exists(self.kline_path):
            return True # 文件存在不生成
        df = pd.read_csv(self.csv_path)
        # 设置大小，共享x坐标轴
        figure, (axPrice, axVol) = plt.subplots(2, sharex=True, figsize=(15, 8))
        # 调用方法绘制K线图
        candlestick2_ochl(ax=axPrice,
                        opens=df["Open"].values, closes=df["Close"].values,
                        highs=df["High"].values, lows=df["Low"].values,
                        width=0.75, colorup='red', colordown='green')
        axPrice.set_title("K线图和均线图", fontproperties=font)  # 设置子图标题
        df['Close'].rolling(window=3).mean().plot(
            ax=axPrice, color="red", label='3-day-moving averages')
        df['Close'].rolling(window=5).mean().plot(
            ax=axPrice, color="blue", label='5-day-moving averages')
        df['Close'].rolling(window=10).mean().plot(
            ax=axPrice, color="green", label='10-day-moving averages')
        axPrice.legend(loc='best')  # 绘制图例
        axPrice.set_ylabel("价格（单位：元）", fontproperties=font)
        axPrice.grid(True)          # 带网格线
        # 如下绘制成交量子图
        # 直方图表示成交量，用for循环处理不同的颜色
        for index, row in df.iterrows():
            if(row['Close'] >= row['Open']):
                axVol.bar(row['Date'], row['Volume'] /
                        1000000, width=0.5, color='red')
            else:
                axVol.bar(row['Date'], row['Volume'] /
                        1000000, width=0.5, color='green')
        axVol.set_ylabel("成交量（单位：万手）", fontproperties=font)   # 设置y轴标题
        axVol.set_title("成交量", fontproperties=font)    # 设置子图的标题
        axVol.set_ylim(0, df['Volume'].max()/1000000*1.2)    # 设置y轴范围
        xmajorLocator = MultipleLocator(5)                  # 将x轴主刻度设置为5的倍数
        axVol.xaxis.set_major_locator(xmajorLocator)
        axVol.grid(True)    # 带网格线
        # 旋转x轴的展示文字角度
        for xtick in axVol.get_xticklabels():
            xtick.set_rotation(15)
        #plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.savefig(self.kline_path)

    def predict_by_svm(self):
        """
        预测
        """
        origDf=pd.read_csv(self.csv_path)
        df=origDf[['Close', 'High', 'Low','Open' ,'Volume','Date']]
        # diff列表示本日和上日收盘价的差
        df['diff'] = df["Close"]-df["Close"].shift(1)
        df['diff'].fillna(0, inplace = True)
        # up列表示本日是否上涨，1表示涨，0表示跌
        df['up'] = df['diff']   
        df['up'][df['diff']>0] = 1
        df['up'][df['diff']<=0] = 0
        # 预测值暂且初始化为0
        df['predictForUp'] = 0

        # 目标值是真实的涨跌情况
        target = df['up']

        length=len(df)
        trainNum=int(length*0.8)
        predictNum=length-trainNum
        # 选择指定列作为特征列
        feature=df[['Close', 'High', 'Low','Open' ,'Volume']]
        # 标准化处理特征值
        feature=preprocessing.scale(feature)

        # 训练集的特征值和目标值
        featureTrain=feature[0:trainNum]
        targetTrain=target[0:trainNum]
        svmTool = svm.SVC(kernel='linear')
        svmTool.fit(featureTrain,targetTrain)

        print(svmTool.score(featureTrain,targetTrain))

        predictedIndex=trainNum
        # 逐行预测测试集
        while predictedIndex<length:
            testFeature=feature[predictedIndex:predictedIndex+1]            
            predictForUp=svmTool.predict(testFeature)    
            # df.ix[predictedIndex,'predictForUp']=predictForUp  
            df.loc[predictedIndex,'predictForUp']=predictForUp    
            predictedIndex = predictedIndex+1    

        # 该对象只包含预测数据，即只包含测试集
        dfWithPredicted = df[trainNum:length]

        # 开始绘图，创建两个子图
        figure = plt.figure()
        # 创建子图     
        (axClose, axUpOrDown) = figure.subplots(2, sharex=True)
        dfWithPredicted['Close'].plot(ax=axClose)
        dfWithPredicted['predictForUp'].plot(ax=axUpOrDown,color="red", label='Predicted Data')
        dfWithPredicted['up'].plot(ax=axUpOrDown,color="blue",label='Real Data')
        plt.legend(loc='best')      # 绘制图例

        # 设置x轴坐标的标签和旋转角度
        major_index=dfWithPredicted.index[dfWithPredicted.index%2==0]
        major_xtics=dfWithPredicted['Date'][dfWithPredicted.index%2==0]
        plt.xticks(major_index,major_xtics)
        plt.setp(plt.gca().get_xticklabels(), rotation=30) 
        plt.title("通过SVM预测涨跌情况", fontproperties=font)
        #plt.rcParams['font.sans-serif']=['SimHei']
        plt.savefig(self.svm_pred_path)
