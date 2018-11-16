from django.shortcuts import render
from .models import *
from .forms import *
from django.utils import timezone
from django.db.models import F

from django.http import response, HttpResponse, HttpResponseRedirect

import time
import math
import random
import hashlib
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.decorators import login_required


def index2(request):
    return render(request, 'taobao/index2.html')

#   首页
def index(request):
    return render(request, 'taobao/index.html')


#   用户管理
def user_control(request):
    return render(request, 'taobao/user_control.html')


#   注册用户
def user_Registered(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST, request.FILES)
        print(request.FILES)
        # is_valid()方法用于验证提交的数据是否符合Form类的字段定义
        if form.is_valid():
            if Users.objects.filter(user_account=form.cleaned_data['user_account']).exists():
                error_msg = "账号重复，请重新输入"
                context = dict()
                context['form'] = form
                context['error_msg'] = error_msg
                return render(request, 'taobao/user_Registered.html', context)

            result = form.save()
            if result:
                a = Users.objects.get(user_account=form.cleaned_data['user_account'])
                request.session['user_id'] = a.id
                User_login_history.objects.create(loginuser_id=a, login_time=timezone.now())
                return render(request, 'taobao/index.html')
    context = dict()
    context['form'] = form
    return render(request, 'taobao/user_Registered.html', context)


#   登录用户
# def user_Login(request):
#     if request.session.get('user_id'):
#         error = '你已经登录用户'
#         context = dict()
#         context['errors'] = error
#         return render(request, 'taobao/user_login.html', context)
#     form = LoginUser()
#     if request.method == 'POST':
#         form = LoginUser(request.POST)
#
#         if form.is_valid():
#             if User.objects.filter(user_account=form.cleaned_data['user_account']).exists():
#                 a = User.objects.get(user_account=form.cleaned_data['user_account'])
#                 user_password = make_password(form.cleaned_data['user_password'])
#                 if a.user_password == user_password:
#                     User_login_history.objects.create(loginuser_id=a, login_time=timezone.now())
#                     request.session['user_id'] = a.id
#                     return render(request, 'taobao/index.html')
#             error = '账号或密码错误'
#             context = dict()
#             context['form'] = form
#             context['errors'] = error
#             return render(request, 'taobao/user_login.html', context)
#
#
#     context = dict()
#     context['form'] = form
#     return render(request, 'taobao/user_login.html', context)
#

#   登录用户
def user_Login(request):
    if request.session.get('user_id'):
        error = '你已经登录用户'
        context = dict()
        context['errors'] = error
        return render(request, 'taobao/user_login.html', context)
    form = LoginUser()
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            if Users.objects.filter(user_account=form.cleaned_data['user_account']).exists():
                a = Users.objects.get(user_account=form.cleaned_data['user_account'])
                if a.user_password == form.cleaned_data['user_password']:
                    User_login_history.objects.create(loginuser_id=a, login_time=timezone.now())
                    request.session['user_id'] = a.id
                    return render(request, 'taobao/index.html')
            error = '账号或密码错误'
            context = dict()
            context['form'] = form
            context['errors'] = error
            return render(request, 'taobao/user_login.html', context)
    context = dict()
    context['form'] = form
    return render(request, 'taobao/user_login.html', context)


#   查看用户登录记录
def user_history(request):
    user_history = User_login_history.objects.all()
    print(user_history)
    return render(request, 'taobao/user_history.html', {'user_history': user_history})


#   查看用户账号信息
def user_look(request):
    user_id = request.session.get('user_id', '游客')
    if user_id == '游客':
        return render(request, 'taobao/user_look.html', {'user_id': user_id})
    user = Users.objects.get(pk=user_id)
    a = str(user.user_portrait)
    return render(request, 'taobao/user_look.html', {'user_id': user.user_account, 'user_user': user, 'a': a})


#   退出登录
def logout(request):
    user_id = request.session.get('user_id')
    if user_id:
        request.session.pop("user_id")
    return render(request, 'taobao/index.html')


#   购物商城
def shopping(request):
    return render(request, 'taobao/shopping.html')


#   充值账户余额
def recharge(request):
    user_id = request.session.get('user_id', '游客')
    context = dict()
    form = Recharge()
    if user_id == '游客':
        context['error'] = '你暂时没有登录，请登录'
        context['form'] = form
        return render(request, 'taobao/recharge.html', context)
    if request.method == 'POST':
        form = Recharge(request.POST)
        if form.is_valid():
                Users.objects.filter(pk=user_id).update(user_RMB=form.cleaned_data['user_RMB'] + F('user_RMB'))
                return render(request, 'taobao/index.html')
    context['a'] = '不是游客'
    context['form'] = form
    context['user_id'] = user_id
    return render(request, 'taobao/recharge.html', context)


#   忘记密码的验证账号
def verify(request):
    form = VerifyUser()
    url = 'verify.html'
    if request.method == 'POST':

        form = VerifyUser(request.POST)

        if form.is_valid():
            if Users.objects.filter(user_account=form.cleaned_data['user_account']).exists():
                user = Users.objects.get(user_account=form.cleaned_data['user_account'])
                request.session['user_id'] = user.id
                return render(request, 'taobao/reset_password.html', {'user': user})
            else:
                error = '账号不存在'
            context = dict()
            context['error'] = error
            context['form'] = form
            return render(request, 'taobao/' + url, context)

    context = dict()
    context['form'] = form
    return render(request, 'taobao/' + url, context)


#   忘记密码的修改密码
def reset_password(request):
    a = request.session.get('user_id')
    b = Users.objects.get(pk=a)
    if b.user_answer == request.POST['user_answer']:
        Users.objects.filter(pk=a).update(user_password=request.POST['user_password'])
        return render(request, 'taobao/index.html')
    else:
        c = '密码问题错误'
        return render(request, 'taobao/reset_password.html', {'user': b, 'question_error': c})


#   修改账户密码
def modify_password(request):
    a = request.session.get('user_id')
    return render(request, 'taobao/modify_password.html', {'user_id': a})


#   修改账户密码
def modify_password_2(request):
    a = request.session.get('user_id')
    Users.objects.filter(pk=a).update(user_password=request.POST['user_password'])
    return render(request, 'taobao/index.html')


#   验证商家权限
def permission(request):
    a = request.session.get('user_id', None)
    if a is None:
        error = '你暂时没有登录，请登录'
        content = dict()
        content['error'] = error
        return render(request, 'commodity/permission.html', content)
    b = Users.objects.get(pk=a)
    if b.user_state == '0':
        a = '不是商家'
        content = dict()
        content['a'] = a
        return render(request, 'commodity/permission.html', content)
    if b.user_state == '1':
        return render(request, 'commodity/index.html')


#   扣除100000金额成为商家
def deduct(request):
    a = Users.objects.get(pk=request.session.get('user_id'))
    if int(a.user_RMB) < 100000:
        b = '金额不足,请进行充值'
        return render(request, 'commodity/permission.html', {'b': b})
    else:
        Users.objects.filter(pk=a.id).update(user_RMB=F('user_RMB') - 100000, user_state='1')
        return render(request, 'commodity/index.html')


#   发布商品
def commodity_pub(request):
    form = CommodityForm()
    content = dict()
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES)
        if form.is_valid():
            a = math.ceil(time.time())
            b = form.cleaned_data['commodity_sort'] + str(a) + str(random.randint(1, 10)) * 6
            form.instance.commodity_id = b
            form.instance.commodity_user = Users.objects.get(pk=request.session.get('user_id'))
            form.save()
            return render(request, 'commodity/index.html')
    content['form'] = form
    return render(request, 'commodity/pub_commodity.html', content)


#   查看发布的商品
def commodity_look_pub(request):
    a = Users.objects.get(pk=request.session.get('user_id'))
    page = 1
    b = Commodity.objects.filter(commodity_user=a)[(int(page) - 1) * 2:int(page) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page})





#   向上翻页
def up(request, page):
    a = Users.objects.get(pk=request.session.get('user_id'))
    b = Commodity.objects.filter(commodity_user=a)[(int(page)-1) * 2:(int(page)) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page})


# 向下翻页
def next(request, page):
    a = Users.objects.get(pk=request.session.get('user_id'))
    b = Commodity.objects.filter(commodity_user=a)[(int(page)) * 2:(int(page)+1) * 2]
    return render(request, 'commodity/commodity_look_pub.html', {'commodity': b, 'page': page})


























#   购买商品
def buy(request, user_id):
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   加入购物车
def add_cart(request, user_id, commodity_id):
    Commodity.objects.filter(pk=commodity_id).update(stock=F('stock') - 1)
    user = Users.objects.get(pk=user_id)

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
    user = Users.objects.get(pk=user_id)
    a = user.shopping_cart_set.all()
    return render(request, 'taobao/look_cart.html', {'user_id': user_id, 'commoditys': a})


#   结算购物车
def buy_summarize(request, user_id):
    user = Users.objects.get(pk=user_id)
    a = Shopping_cart.objects.get(user=user)
    Users.objects.filter(pk=user_id).update(user_RMB=F('user_RMB') - a.commodity_sum)
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})


#   清空购物车
def buy_empty(request, user_id):
    user = Users.objects.get(pk=user_id)
    a = Shopping_cart.objects.get(user=user)
    a.delete()
    Commodity.objects.filter(commodity_user=user).update(stock=F('stock') + a.commodity_num)
    commoditys = Commodity.objects.all()
    return render(request, 'taobao/buy.html', {'user_id': user_id, 'commoditys': commoditys})






    # if request.method == 'POST':
    #     if a:
    #         if User.objects.get(pk=a).user_state == '0':
    #             return render(request, 'commodity/pay.html')







#   商品
# def commodity_login(request):
#     form = Merchant()
#     content = dict()
#     a = request.session.get('user_id', None)
#     if a is None:
#         error = '你暂时没有登录，请登录'
#         content['form'] = form
#         content['error'] = error
#         return render(request, 'commodity/merchant.html', content)
#
#
#     # if request.method == 'POST':
#     #     if a:
#     #         if User.objects.get(pk=a).user_state == '0':
#     #             return render(request, 'commodity/pay.html')
#
#     content['a'] = '不是游客'
#     content['form'] = form
#     return render(request, 'commodity/merchant.html', content)







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



#   修改商品信息
def commodity_modify(request, user_id):
    for k, v in request.GET.items():
        print('%s=%s' % (k, request.GET.get(k)))

    a = Users.objects.get(pk=user_id)
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