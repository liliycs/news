from django import forms
from captcha.fields import CaptchaField
from newsapp.models import UserInfo, Comment
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
#CaptchaField验证码字段类型
# SignupForm用于验证用户名，密码，和验证码
class SignupForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

    class Meta:
        model = UserInfo
        fields = ["username", "password","email", "mobile", "gender"]
        error_messages = {
            "username": {"invalid": "用户名错误"},
            "password": {"invalid": "密码错误"},
        }
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['gender', 'mobile', 'birthday','image', 'email']

class PasswordForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    re_password = forms.CharField(required=True, min_length=5)

@login_required(login_url="/login")
def password_reset(request, user_id):
    if request.method == "GET":
        return render(request, "password_reset.html", locals())
    elif request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd1 = request.POST.get("password")
            pwd2 = request.POST.get("re_password")
            if pwd1 == pwd2:
                user = UserInfo.objects.get(id=user_id)
                user.password = make_password(pwd1)
                user.save()
                return redirect("/login")
    return render(request, "password_reset.html", locals())

class ForGetPassWordForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"},label="验证码")
    username = forms.CharField(max_length=30)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
