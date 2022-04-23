from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Msg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(verbose_name='反馈内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间 默认为当前时间
    class Meta:
        verbose_name = "反馈管理"  # 设置模型的别名
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)  # 设置排序的字段

class Liuyan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(verbose_name='留言内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建时间 默认为当前时间
    class Meta:
        verbose_name = "留言管理"  # 设置模型的别名
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)  # 设置排序的字段