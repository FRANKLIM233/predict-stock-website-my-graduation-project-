"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mysite import settings
from stock.views import *
from msg.views import add as msg_add, liuyan_add
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', index, ),
    path('index/', index, name='index'),
    path('search/', search, name='search'),
    path('predict/', predict, name='predict'),
    path('msg/add/', msg_add, name='msg_add'),
    path('liuyan/add/', liuyan_add, name='liuyan_add'),
    path('news/latest/', latest_news, name='latest_news'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL) # 配置静态资源的路径

