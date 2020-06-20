from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='用户名', max_length=50)
    email = forms.EmailField(label='邮箱',)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise forms.ValidationError("用户名不得少于3个字")
        elif len(username) > 10:
            raise forms.ValidationError("用户名不得多于10个字")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("该用户名已经被占用")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("该邮箱已被注册")
        else:
            raise forms.ValidationError("请输入一个正确的邮箱")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码太短")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不对，请重输！")

        return password2


class LoginForm(forms.Form):

    username = forms.CharField(label='用户名/邮箱', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("邮箱不存在")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("该用户不存在，请先注册")
        return username


class ProfileForm(forms.Form):

    first_name = forms.CharField(label='姓', max_length=50, required=False)
    last_name = forms.CharField(label='名', max_length=50, required=False)
    org = forms.CharField(label='组织', max_length=50, required=False)
    telephone = forms.CharField(label='联系方式', max_length=50, required=False)


class PwdChangeForm(forms.Form):

    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput)

    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 3:
            raise forms.ValidationError("密码过短.")
        elif len(password1) > 10:
            raise forms.ValidationError("密码太长.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不对，请重输")

        return password2
