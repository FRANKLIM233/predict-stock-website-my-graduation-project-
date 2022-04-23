app_name = 'account'
from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout, name="logout"),  # 注销登录
    path('register/', register, name='register'),  # 注册
]