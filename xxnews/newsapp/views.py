from django.http import HttpResponse
from django.shortcuts import render, redirect
from newsapp.models import Type,Content,UserInfo,Comment
from django.contrib.auth import login, logout, authenticate
from django.views import View
from newsapp.forms import SignupForm, ForGetPassWordForm, CommentForm
from django.contrib.auth.hashers import make_password
import hashlib
import random
import json
import newsapp.zhenzismsclient as smsclient
def index(request):
    # 获取所有新闻类型
    types = Type.objects.all()
    search = request.GET.get("search")  # NONE
    type_id = request.GET.get("type_id")
    print(request.user)
    if search:
        content_list_all = Content.objects.filter(title__regex="\w*%s\w*" % search).order_by('-id')
    elif type_id:
        # 过滤出不同新闻类型的数据
        type_id = int(type_id)
        content_list_all = Content.objects.filter(type_id=type_id).order_by('-id')
    else:
        content_list_all = Content.objects.all().order_by('-id')
    return render(request, "index.html", locals())


def news(request, id):
    # 通过id找到文章内容
    types = Type.objects.all()
    contents = Content.objects.get(id=id)
    contents.read_count = int(contents.read_count) + 1
    contents.save()
    return render(request, "news.html", locals())


class LoginView(View):
    def get(self, request):
        types = Type.objects.all()
        return render(request, "login.html", locals())

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error = "用户名或密码错误登录失败！"
            return render(request, "login.html", locals())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")
# class Signup(View):
#     def get(self, request):
#         form = SignupForm()
#         return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # 保存注册信息到数据库
            form.save()
            # 注册成功跳转到登录页面
            return redirect("/login")
        else:
            return render(request, "signup.html", {"form": form})

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # 保存注册信息到数据库
            # 我们自己加密
            pwd = make_password(request.POST.get("password"))
            # 使用自定义的方法保存用户信息
            UserInfo.objects.create(
                password=pwd,
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                mobile=request.POST.get("mobile"),
                gender=request.POST.get("gender"),
            )
            # 注册成功跳转到登录页面
            return redirect("/login")
class SetUserView(View):
    def get(self, request, user_id):
        user = UserInfo.objects.get(id=user_id)
        return render(request, "setuser.html", locals())

    def post(self, request, user_id):
        user = UserInfo.objects.get(id=user_id)
        form = UserInfo.Form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/")
        return render(request, "setuser.html", locals())


def hash_code(code):
    m = hashlib.md5()
    m.update(code.encode('utf-8'))
    return m.hexdigest()

def send_dx(mobile):
    yzm = "".join([str(random.randint(0, 9)) for i in range(4)])
    api_url = "http://sms_developer.zhenzikj.com"
    app_id = 100097
    app_secret = "NTI3ZjUyN2EtYjc2Yi00N2FiLTgwYjMtOGQ5MzE2NjJhN2Uz"
    client = smsclient.ZhenziSmsClient(api_url, app_id, app_secret)
    result = client.send(mobile, "您的验证码是%s" % yzm)
    return json.loads(result), yzm


class ForGetPassword(View):
    def get(self, request):
        form = ForGetPassWordForm()
        return render(request, "forgetpwd.html", locals())

    def post(self, request):
        form = ForGetPassWordForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            user = UserInfo.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user:
                result, yzm = send_dx(user.mobile)
                print(result, yzm)
                if result.get("code") == 0:
                    return redirect('/getyzm/%s/%s' % (user.id, hash_code(yzm)))
            return render(request, "forgetpwd.html", locals())



def getyzm(request, user_id, code):
    if request.method == "GET":
        return render(request, "getyzm.html", locals())
    elif request.method == "POST":
        new_code = request.POST.get("new_code")
        user = UserInfo.objects.get(id=user_id)
        if user and code == hash_code(new_code):
            login(request, user)
            return redirect("/password_reset/%s" % user_id)
        else:
            return render(request, "getyzm.html", locals())

class News(View):
    def get(self, request, content_id):
        types = Type.objects.all()
        data = Content.objects.get(id=content_id)
        data.clicked = int(data.clicked) + 1
        data.save()
        form = CommentForm()
        comment = Comment.objects.filter(news_id=data)
        return render(request, "news.html", locals())

    def post(self, request, content_id):
        form = CommentForm(request.POST)
        ip = request.META['REMOTE_ADDR']
        if form.is_valid():
            if request.user.id:
                Comment.objects.create(
                    user_id=request.user,
                    news_id=Content.objects.get(id=content_id),
                    content=request.POST.get("content"),
                    ip=ip
                )
            else:
                return HttpResponse("登陆后才能评论！")
        return redirect("/news/%s" % content_id)

