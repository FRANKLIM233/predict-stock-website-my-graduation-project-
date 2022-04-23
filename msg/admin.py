from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Msg)
class MA(admin.ModelAdmin):
    list_display = ('user', 'content', 'create_at')


@admin.register(Liuyan)
class LA(admin.ModelAdmin):
    list_display = ('user', 'content', 'create_at')