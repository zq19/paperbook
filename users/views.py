from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def login_view(request):
    """用户登录界面"""
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'],password=data['password'])
        if user:
            login(request,user)
            request.session.set_expiry(3600)
            return redirect('learning_logs:index')
        else:
            return render(request,'users/login.html',{'status':'用户名或密码有误，请重新输入！'})
    return render(request,'users/login.html')


def logout_view(request):
    """用户注销界面"""
    logout(request)
    return redirect("learning_logs:index")


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，并且定向到主页
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request,authenticated_user)
            return redirect('learning_logs:index')
        else:
            return render(request,'users/register.html',{'form':form})
    return render(request,'users/register.html',{'form':form})
