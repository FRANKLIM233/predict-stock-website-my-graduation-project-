from django import forms
from .models import *

class MsgForm(forms.ModelForm):
  class Meta:
    """
    规定了要为哪一个model创建表单
    """
    model = Msg # 指定模型
    fields = '__all__' # 指定字段
    exclude = ['user', 'create_at'] # 指定排除的字段


class LiuyanForm(forms.ModelForm):
  class Meta:
    """
    规定了要为哪一个model创建表单
    """
    model = Liuyan # 指定模型
    fields = '__all__' # 指定字段
    exclude = ['user', 'create_at'] # 指定排除的字段