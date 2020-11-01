from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from django.contrib.auth.decorators import login_required


# 注册页面
def regitser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = User.objects.create(username=username, email=email, password=password)
            user_profile = UserProfile(user=user)
            user_profile.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form':form})


# 登录页面
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 该Django版本下的以下验证方法不能用3.0.7
            # user = auth.authenticate(username=username, password=password)
            user = User.objects.get(username=username)
            pwd = user.password
            if password == pwd:
                # 验证用户信息是否正确
                if user.is_active:
                    auth.login(request, user)
                    return redirect('users:profile', pk=user.id)
            else:
                return render(request, 'users/login.html', {'form': form,
                                                            'message': '用户名或密码错误'})
    else:
         form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# 个人信息展示页面,需要登录才能看到
# @login_required
def profile(request, pk):
    print(pk)
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'user': user})


# 更改个人信息，同样需要登录
# @login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
            return redirect('users:profile', pk=user.id)
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileForm(default_data)
    return render(request, 'users/profile_update.html', {'form': form})



# 登出
# @login_required
def logout(request):
    auth.logout(request)
    return redirect('users:login')


# 修改密码，需登录才行
# @login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            pwd = user.password
            username = user.username
            if password == pwd and user.is_active:
                new_password = form.cleaned_data['password2']
                User.objects.filter(username__exact=username).update(password=new_password)
                return redirect('users:login')
            else:
                return render(request, 'users/pwd_change.html', {'form': form,
                                                                 'user': user,
                                                                 'message': '旧密码输的不对，重输吧'})
    else:
        form = PwdChangeForm()
    return render(request, 'users/pwd_change.html', {'form': form})







