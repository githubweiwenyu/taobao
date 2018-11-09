from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.db.models import F
from django.http import response, HttpResponse, HttpResponseRedirect
from django.template import loader ,Context
# from .forms import LoginForm
from django import forms
import time
import math
import random


def index(request):
    return render(request, 'index.html')


def Enter(request):
    return render(request, 'taobao/Enter.html')


def user_BigTitle(request):
    return render(request, 'taobao/user_BigTitle.html')



#   定义验证用户的类
class LoginForm(forms.Form):
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=20, required=True, min_length=6, label="user_password",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"},
                                    widget=forms.PasswordInput())
    user_question = forms.CharField(max_length=200, required=True, min_length=6, label="user_question",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"})
    user_answer = forms.CharField(max_length=200, required=True, min_length=6, label="user_answer",
                                  error_messages={"required": "不能为空",
                                                  "max_length": "用户名最长200位",
                                                  "min_length": "用户名最短6位"})
    user_name = forms.CharField(max_length=20, required=True, min_length=6, label="user_name",
                                error_messages={"required": "不能为空",
                                                "max_length": "用户名最长20位",
                                                "min_length": "用户名最短6位"})


#   利用django的form框架注册用户
def user_Registered(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        # is_valid()方法用于验证提交的数据是否符合Form类的字段定义
        if form.is_valid():
            if User.objects.filter(user_account=form.cleaned_data['user_account']).exists():
                error_msg = "账号重复，请重新输入"
                context = dict()
                context['form'] = form
                context['error_msg'] = error_msg
                return render(request, 'taobao/user_Registered.html', context)
            user = User(user_account=form.cleaned_data['user_account'],
                        user_password=form.cleaned_data['user_password'],
                        user_question=form.cleaned_data['user_question'],
                        user_answer=form.cleaned_data['user_answer'],
                        user_name=form.cleaned_data['user_name'])
            user.save()
            request.session['user_id'] = user.id
            User_login_history.objects.create(loginuser_id=user, login_time=timezone.now())
            return render(request, 'taobao/user_TwoTitle.html', {'user_id': user.id})
    context = dict()
    context['form'] = form
    return render(request, 'taobao/user_Registered.html', context)



#   登录用户
class user_Login(forms.Form):
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=20, required=True, min_length=6, label="user_password",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"})


#   登录用户验证
def user_Login_2(request):
    form = user_Login()
    if request.method == 'POST':
        form = user_Login(request.POST)

        if form.is_valid():
            if User.objects.filter(user_account=form.cleaned_data['user_account']).exists():
                a = User.objects.get(user_account=request.POST['user_account'])

                if a.user_password == form.cleaned_data['user_password']:

                    request.session['user_id'] = a.id
                    return render(request, 'taobao/user_TwoTitle.html', {'user_id': a.id})

                else:
                    error = '密码错误'
                    context = dict()
                    context['form'] = form
                    context['errors'] = error
                    return render(request, 'taobao/user_Login.html', context)
            else:
                error = '账号不存在'
                context = dict()
                context['form'] = form
                context['errors'] = error
                return render(request, 'taobao/user_Login.html', context)
    context = dict()
    context['form'] = form
    return render(request, 'taobao/user_Login.html', context)


#   用户大标题
def user_TwoTitle(request, user_id):
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})


#   查看用户登录记录
def user_history(request):
    user_history = User_login_history.objects.all()
    print(user_history)
    return render(request, 'taobao/user_history.html', {'user_historys': user_history})


#   查看用户信息
def user_look(request, user_id):
    user = User.objects.get(pk=user_id)
    user_id_session = request.session.get('user_id')
    return render(request, 'taobao/user_look.html', {'user': user, 'user_id': user_id_session})


#   购买商品
def buy(request, user_id):
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   加入购物车
def add_cart(request, user_id, commodity_id):
    Commodity.objects.filter(pk=commodity_id).update(stock=F('stock') - 1)
    user = User.objects.get(pk=user_id)

    a = Commodity.objects.get(pk=commodity_id)
    b = Shopping_cart.objects.filter(commodity_id=commodity_id)

    if len(b) == 0:
        Shopping_cart.objects.create(user=user,
                                     commodity_id=commodity_id,
                                     commodity_name=a.commodity_name,
                                     commodity_price=int(a.commodity_price),
                                     commodity_num=1,
                                     commodity_sum=int(a.commodity_price),
                                     )
    else:
        Shopping_cart.objects.filter(commodity_id=commodity_id).update(commodity_num=F('commodity_num')+1,
                                                                       commodity_sum=F('commodity_num') * int(a.commodity_price))
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   查看购物车
def look_cart(request, user_id):
    user = User.objects.get(pk=user_id)
    a = user.shopping_cart_set.all()
    return render(request, 'taobao/look_cart.html', {'user_id': user_id, 'commoditys': a})


#   结算购物车
def buy_summarize(request, user_id):
    user = User.objects.get(pk=user_id)
    a = Shopping_cart.objects.get(user=user)
    User.objects.filter(pk=user_id).update(user_RMB=F('user_RMB') - a.commodity_sum)
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   清空购物车
def buy_empty(request, user_id):
    user = User.objects.get(pk=user_id)
    a = Shopping_cart.objects.get(user=user)
    a.delete()
    Commodity.objects.filter(commodity_user=user).update(stock=F('stock') + a.commodity_num)
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   修改账户密码
def modify_password(request, user_id):
    return render(request, 'taobao/modify_password.html', {'user_id': user_id})


def modify_password_2(request, user_id):
    User.objects.filter(pk=user_id).update(user_password=request.POST['user_password'])
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})

#   充值账户余额
def recharge(request, user_id):
    return render(request, 'taobao/recharge.html', {'user_id': user_id})


def recharge_2(request, user_id):
    User.objects.filter(pk=user_id).update(user_RMB=request.POST['RMB'] + F('user_RMB'))
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})


#   忘记密码
def user_ModifyPassword(request):
    return render(request, 'taobao/verify.html')

#   忘记密码验证账号
def versfy(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        user = User.objects.get(user_account=request.POST['user_account'])
        user_id = User.objects.get(user_account=request.POST['user_account']).id
        return render(request, 'taobao/reset_password.html', {'user': user, 'user_id': user_id})
    else:
        b = '账号错误'
        return render(request, 'taobao/verify.html', {'account_error': b})

#   忘记密码验证问题并修改密码
def reset_password_2(request, user_id):
    q = User.objects.get(pk=user_id)
    if q.user_question == request.POST['user_question']:
        User.objects.filter(pk=user_id).update(user_password=request.POST['user_password'])
        return render(request, 'taobao/user_BigTitle.html')
    else:
        a = '密码问题错误'
        return render(request, 'taobao/reset_password.html', {'user': q, 'user_id': q.id, 'question_error': a})



#   商品
def commodity_login(request):
    return render(request, 'commodity/commodity_login.html')

#   验证账号
def commodity_user(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        a = User.objects.get(user_account=request.POST['user_account'])
        if a.user_password == request.POST['user_password']:
            if a.user_state == '0':
                return render(request, 'commodity/commodity_init.html', {'user_id': a.id})
            else:
                return render(request, 'commodity/commodity_BigTitle.html', {'user_id': a.id})
        else:
            a = '密码错误'
            return render(request, 'commodity/commodity_Login.html', {'password_error': a})
    else:
        b = '账号错误'
        return render(request, 'commodity/commodity_Login.html', {'account_error': b})

#   验证商家
def decuct(request, user_id):
    a = User.objects.get(pk=user_id)

    if int(a.user_RMB) < 100000:
        b = '金额不足,请前往用户页面进行充值'
        c = User.objects.get(pk=user_id)
        return render(request, 'commodity/commodity_init.html', {'user_id': c.id, 'b': b})
    else:
        User.objects.filter(pk=user_id).update(user_RMB=F('user_RMB') - 100000, user_state='1')
        c = User.objects.get(pk=user_id)
        return render(request, 'commodity/commodity_BigTitle.html', {'user_id': c.id})


#   发布商品
def commodity_pub(request, user_id):
    a = Commodity_sort.objects.all()
    return render(request, 'commodity/pub_commodity.html', {'user_id': user_id, 'commodity_sort': a})


#   添加商品
def commodity_add(request, user_id):
    user = User.objects.get(pk=user_id)
    a = math.ceil(time.time())
    Commodity.objects.create(commodity_id=request.POST['commodity_sort'] + str(a) + str(random.randint(1, 10)) * 6,
                             commodity_name=request.POST['commodity_name'],
                             commodity_price=request.POST['commodity_price'],
                             commodity_sort=request.POST['commodity_sort'],
                             stock=request.POST['stock'],
                             commodity_user=user
                             )
    return render(request, 'commodity/commodity_BigTitle.html', {'user_id': user_id})


#   查看发布的商品
def commodity_look_pub(request, user_id):
    a = User.objects.get(pk=user_id)
    page = 1
    b = Commodity.objects.filter(commodity_user=a)[(int(page) - 1) * 2:int(page) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id})


#   查看商品的分类
def commodity_sort(request, user_id):
    a = Commodity_sort.objects.all()
    return render(request, 'commodity/commodity_sort.html', {'commodity_sort': a, 'user_id': user_id})


#   添加商品分类
def add_sort(request, user_id):
    return render(request, 'commodity/add_sort.html', {'user_id': user_id})


#   确认添加商品分类
def check_add_sort(request, user_id):
    Commodity_sort.objects.create(sort_name=request.POST['sort_name'],
                                  sort_shortcut=request.POST['sort_shortcut'])
    return render(request, 'commodity/commodity_BigTitle.html', {'user_id': user_id})


def commodity_BigTitle(request, user_id):
    return render(request, 'commodity/commodity_BigTitle.html', {'user_id': user_id})


#   向上翻页
def up(request, page, user_id):
    a = User.objects.get(pk=user_id)
    b = Commodity.objects.filter(commodity_user=a)[(int(page)-1) * 2:(int(page)) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id})


# 向下翻页
def next(request, page, user_id):
    a = User.objects.get(pk=user_id)
    b = Commodity.objects.filter(commodity_user=a)[(int(page)) * 2:(int(page)+1) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id})


#   修改商品信息
def commodity_modify(request, user_id):
    for k, v in request.GET.items():
        print('%s=%s' % (k, request.GET.get(k)))

    a = User.objects.get(pk=user_id)
    return render(request, 'commodity/commodity_modity.html', {'user': a, 'user_id': user_id})


#   确认修改的商品
def commodity_modify_usb(request, commodity_id, user_id):
    commodity = Commodity.objects.get(pk=commodity_id)
    return render(request, 'commodity/commodity_modity_usb.html', {'commodity_id': commodity_id, 'commodity': commodity, 'user_id': user_id})


#   更新修改后的商品
def commodity_modify_2(request, commodity_id, user_id):
    Commodity.objects.filter(commodity_id=commodity_id).update(commodity_name=request.POST['commodity_name'],
                                                               commodity_price=request.POST['commodity_price'],
                                                               stock=request.POST['stock'])
    return render(request, 'commodity/commodity_BigTitle.html', {'user_id': user_id})