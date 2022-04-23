from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout, hashers
from django.contrib import messages

# Create your views here.
from account.forms import LoginForm, RegisterForm


def user_login(request):
    # if request.user.is_authenticated():
    #     return render(request, 'account/login.html', {'message': "您已登录!请先退出"})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('用户目前禁用')
            else:
                return render(request, 'account/login.html', {'message' : "用户名或者密码错误"})
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'message' : "用户名或者密码错误"})
    else:

        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

@login_required
def change_profile(request):
    """
    修改个人信息
    https://www.cnblogs.com/wcwnina/p/9246228.html
    https://www.cnblogs.com/NeedEnjoyLife/p/6842809.html
    :param request:
    :return:
    """
    if request.method == 'POST':
        msg = ''
        user = request.user
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if username == '' and password == '':
            msg = '用户名以及密码都为空!'
        else:
            if password:
                if password != repassword:
                    msg = '两次密码输入不一致'
                else:
                    user.password = hashers.make_password(password)  # 正式修改密码，自动加密
            if username:
                user.username = username
            user.save()
            # return render(request, 'account/profile.html', {'message' : msg})
            return redirect('/account/login')
        return render(request, 'account/profile.html', {'message' : msg})
    else:
        return render(request, 'account/profile.html')

def register(request):
    """
    注册逻辑
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/account/login/')
            #render(request, 'account/login.html')
        else:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'account/register.html', {'message': '用户已经注册!'})
            except:
                return render(request, 'account/register.html', {'message' : '两次密码输入不一致！'})
    else:
        # 已经登录需要先退出登录
        if request.user is not None:
            # if request.user.is_authenticated():
            auth_logout(request)
        return render(request, 'account/register.html')
#
def logout(request):
    auth_logout(request)
    return HttpResponse('<script>window.alert("注销成功!");location.href="/account/login"</script>')
#
# @login_required
# def center(request):
#     """
#     个人中心主页
#     :param request:
#     :return:
#     """
#     user = request.user
#
#     return render(request, 'account/center.html', {
#     })




