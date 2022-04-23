from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .tables import *

# Create your views here.
@login_required
def add(request):
    """
    """
    if request.method == 'GET':
        user_form = MsgForm() # 生成form
        return render(request, 'msg/add.html', {'user_form': user_form})
    else:
        user_form = MsgForm(request.POST) # 把Post中的数据添加到form中
        if user_form.is_valid():
            user_form.instance.user = request.user
            user_form.save()
            
            messages.success(request, '添加成功!')
            return redirect('/')
        else:
            return render(request, 'msg/add.html', {'user_form': user_form})

@login_required
def liuyan_add(request):
    context = {

    }
    liuyans = Liuyan.objects.all()
    table = LTable(liuyans)
    context['table'] = table
    if request.method == 'GET':
        user_form = LiuyanForm() # 生成form
        context['user_form'] = user_form
        return render(request, 'msg/add_liuyan.html', context=context)
    else:
        user_form = LiuyanForm(request.POST) # 把Post中的数据添加到form中
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.instance.user = request.user
            user_form.save()
            messages.success(request, '添加成功!')
            return redirect('/liuyan/add/')
            # TODO reverse
        else:
            messages.error(request, '添加失败')
            return render(request, 'msg/add_liuyan.html', context=context)