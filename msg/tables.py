import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class LTable(tables.Table):
    class Meta:
        model = Liuyan
        fields = ('user', 'content', 'create_at')
        attrs = {"class": "table table-striped"} # 自定义属性