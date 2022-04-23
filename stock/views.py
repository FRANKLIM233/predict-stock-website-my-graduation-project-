from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .core.main import *
from django.contrib import messages
from mysite.settings import MEDIA_ROOT
import pandas as pd
# Create your views here.

# 读取股票列表

def read_stocklist():
    path = MEDIA_ROOT / 'stock_list.csv'
    df = pd.read_csv(path, header=0, dtype=str)
    df = df.set_index('symbol')
    return df

stock_list_df = read_stocklist()


def index(request):
    """
    """
    return render(request, 'stock/index.html')

def latest_news(request):
    news_df  = pd.read_csv(MEDIA_ROOT / 'newslistTs.csv', header=0)
    news_df = news_df[['datetime', 'content']]
    news_df['main'] = news_df['content'].apply(lambda x: x[:30])
    news_df['datetime'] = pd.to_datetime(news_df['datetime'])
    news_df = news_df.sort_values('datetime', ascending=False)
    news_data = news_df.sample(30).sort_values('datetime', ascending=False)
    news_data = news_data[['datetime', 'main']]
    news_data = news_data.values.tolist()   
    return render(request, 'stock/news_list.html', {'news': news_data}) 

def search(request):
    """
    查询
    """
    code = request.GET.get('code')
    try:
        item = stock_list_df.loc[code]
        if item.shape[0] == 0:
            messages.error(request, '股票代码有误!请重新输入')
            return redirect('/')
    except:
        messages.error(request, '股票代码有误!请重新输入')
        return redirect('/')
    
    _type = item['ts_code'].split('.')[1]
        
    start = request.GET.get('start')
    end = request.GET.get('end')
    stock = Stock(code, _type, start, end)
    r = stock.crawl() # 爬取
    if r is False:
        messages.error(request, '查询出错!请稍后再试!')
        return redirect('/')
    stock.plot_kline() # 生成K线图
    messages.success(request, '查询成功')
    return render(request, 'stock/search_result.html', {'code': code, 'start': start, 'end': end, 'info': dict(item)})

def predict(request):
    """
    预测
    """
    code = request.GET.get('code')
    item = stock_list_df.loc[code]
    if item.shape[0] == 0:
        result = {'error': '1', 'msg': '不存在该股票'}
    else:
        _type = item['ts_code'].split('.')[1]
        start = request.GET.get('start')
        end = request.GET.get('end')
        stock = Stock(code, _type, start, end)
        stock.predict_by_svm()
        result = {'error': '0', 'msg': '预测成功'}
    return JsonResponse(result)
