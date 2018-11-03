from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.db.models import F
from django.http import response, HttpResponse
from django.template import loader ,Context
import time
import math
import random


def Enter(request):
    return render(request, 'taobao/Enter.html')


def user_BigTitle(request):
    return render(request, 'taobao/user_BigTitle.html')


def user_Registered(request):
    return render(request, 'taobao/user_Registered.html')


def user_Registered_2(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        a = '账号重复，请重新输入'
        return render(request, 'taobao/user_Registered.html', {'a': a})
    elif User.objects.filter(user_account=request.POST['user_account']).exists() is False:
        user = User(user_account=request.POST['user_account'],
                    user_password=request.POST['user_password'],
                    user_question=request.POST['user_question'],
                    user_answer=request.POST['user_answer'],
                    user_name=request.POST['user_name'])
        user.save()
        return render(request, 'taobao/user_TwoTitle.html', {'user_id': user.id})


def user_Login(request):
    return render(request, 'taobao/user_Login.html')


def user_Login_2(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        a = User.objects.get(user_account=request.POST['user_account'])
        if a.user_password == request.POST['user_password']:
            user_id = User.objects.get(user_account=request.POST['user_account']).id
            q = Commodity.objects.all()
            return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id, 'commodity_list': q})
        else:
            a = '密码错误'
            return render(request, 'taobao/user_Login.html', {'password_error': a})
    else:
        b = '账号错误'
        return render(request, 'taobao/user_Login.html', {'account_error': b})


def user_TwoTitle(request, user_id):
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})


def user_look(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'taobao/user_look.html', {'user': user, 'user_id': user_id})


def modify_password(request, user_id):
    return render(request, 'taobao/modify_password.html', {'user_id': user_id})


def modify_password_2(request, user_id):
    User.objects.filter(pk=user_id).update(user_password=request.POST['user_password'])
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})


def recharge(request, user_id):
    return render(request, 'taobao/recharge.html', {'user_id': user_id})


def recharge_2(request, user_id):
    User.objects.filter(pk=user_id).update(user_RMB=request.POST['RMB'] + F('user_RMB'))
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id})


def user_ModityPassword(request):
    return render(request, 'taobao/verify.html')


def versfy(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        user = User.objects.get(user_account=request.POST['user_account'])
        user_id = User.objects.get(user_account=request.POST['user_account']).id
        return render(request, 'taobao/reset_password.html', {'user': user, 'user_id': user_id})
    else:
        b = '账号错误'
        return render(request, 'taobao/verify.html', {'account_error': b})


def reset_password_2(request, user_id):
    q = User.objects.get(pk=user_id)
    if q.user_question == request.POST['user_question']:
        User.objects.filter(pk=user_id).update(user_password=request.POST['user_password'])
        return render(request, 'taobao/user_BigTitle.html')
    else:
        a = '密码问题错误'
        return render(request, 'taobao/reset_password.html', {'user': q, 'user_id': q.id, 'question_error': a})




#商品
def commodity_login(request):
    return render(request, 'taobao/commodity_login.html')


def commodity_user(request):
    if User.objects.filter(user_account=request.POST['user_account']).exists():
        a = User.objects.get(user_account=request.POST['user_account'])
        if a.user_password == request.POST['user_password']:

            return render(request, 'taobao/commodity_BigTitle.html', {'user_state': a.user_state, 'user_id': a.id})
        else:
            a = '密码错误'
            return render(request, 'taobao/commodity_Login.html', {'password_error': a})
    else:
        b = '账号错误'
        return render(request, 'taobao/commodity_Login.html', {'account_error': b})


def decuct(request, user_id):
    a = User.objects.get(pk=user_id)

    if int(a.user_RMB) < 100000:
        b = '金额不足'
        return render(request, 'taobao/recharge.html', {'user_id': user_id, 'b': b})
    else:
        User.objects.filter(pk=user_id).update(user_RMB=F('user_RMB') - 100000, user_state='1')
        c = User.objects.get(pk=user_id)
        return render(request, 'taobao/commodity_BigTitle.html', {'user_id': c.id, 'user_state': c.user_state})


def commodity_pub(request, user_id, user_state):
    print(user_id)
    return render(request, 'taobao/pub_commodity.html', {'user_id': user_id, 'user_state': user_state})


def commodity_add(request, user_id, user_state):
    user = User.objects.get(pk=user_id)
    a = math.ceil(time.time())
    Commodity.objects.create(commodity_id=request.POST['commodity_sort'] + str(a) + str(random.randint(1, 10)) * 6,
                             commodity_name=request.POST['commodity_name'],
                             commodity_price=request.POST['commodity_price'],
                             commodity_sort=request.POST['commodity_sort'],
                             stock=request.POST['stock'],
                             commodity_user=user
                             )
    return render(request, 'taobao/commodity_BigTitle.html', {'user_id': user_id, 'user_state': user_state})


def commodity_look_pub(request, user_id, user_state):
    a = User.objects.get(pk=user_id)
    page = 1
    b = Commodity.objects.filter(commodity_user=a)[(int(page) - 1) * 2:int(page) * 2]
    return render(request, 'taobao/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id, 'user_state': user_state})


def commodity_BigTitle(request, user_id, user_state):
    return render(request, 'taobao/commodity_BigTitle.html', {'user_id': user_id, 'user_state': user_state})


def up(request, page, user_id, user_state):
    a = User.objects.get(pk=user_id)
    b = Commodity.objects.filter(commodity_user=a)[(int(page)-1) * 2:(int(page)) * 2]
    return render(request, 'taobao/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id, 'user_state': user_state})


def next(request, page, user_id, user_state):
    a = User.objects.get(pk=user_id)
    b = Commodity.objects.filter(commodity_user=a)[(int(page)) * 2:(int(page)+1) * 2]
    return render(request, 'taobao/commodity_look_pub.html', {'commodity': b, 'page': page, 'user_id': user_id, 'user_state': user_state})


def buy(request, user_id, commodity_id):
    a = Commodity.objects.get(pk=commodity_id)
    a.stock = F('stock')-1
    a.save()
    User.objects.filter(pk=user_id).update(user_RMB=F('user_RMB')-a.commodity_price)
    b = Commodity.objects.all()
    return render(request, 'taobao/user_TwoTitle.html', {'user_id': user_id, 'commodity_list': b})


def commodity_modify(request, user_id, user_state):
    for k, v in request.GET.items():
        print('%s=%s' % (k, request.GET.get(k)))

    a = User.objects.get(pk=user_id)
    return render(request, 'taobao/commodity_modity.html', {'commodity_list': a, 'user_id': user_id, 'user_state': user_state})


def commodity_modify_usb(request, commodity_id, user_id, user_state):
    commodity = Commodity.objects.get(pk=commodity_id)
    return render(request, 'taobao/commodity_modity.html', {'commodity_id': commodity_id, 'commodity': commodity, 'user_id': user_id, 'user_state': user_state})


def commodity_modify_2(request, commodity_id, user_id, user_state):
    Commodity.objects.filter(commodity_id=commodity_id).update(commodity_name=request.POST['commodity_name'],
                                                               commodity_price=request.POST['commodity_price'],
                                                               stock=request.POST['stock'])
    return render(request, 'taobao/commodity_BigTitle.html', {'user_id': user_id, 'user_state': user_state})