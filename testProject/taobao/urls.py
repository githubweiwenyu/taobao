from django.urls import path
from . import views, Email
app_name = 'taobao'

urlpatterns = [
    #   首页
    path('', views.index, name='index'),

    #   用户管理
    path('user_control', views.user_control, name='user_control'),

    #   注册用户
    path('user_Registered/', views.user_Registered, name='user_Registered'),

    #   登录用户
    path('user_Login/', views.user_Login, name='user_Login'),

    #   退出登录
    path('logout/', views.logout, name='logout'),

    #   查看账户信息
    path('user_look/', views.user_look, name='user_look'),

    #   商城预览
    path('shopping/', views.shopping, name='shopping'),

    #   忘记密码
    path('verify/', views.verify, name='verify'),
    path('reset_password/', views.reset_password, name='reset_password'),

    #   查看用户登录记录
    path('user_history/', views.user_history, name='user_history'),

    #   修改密码
    path('modify_password/', views.modify_password, name='modify_password'),
    path('modify_modify_password_2/', views.modify_password_2, name='modify_password_2'),

    #   账号充值
    path('recharge/', views.recharge, name='recharge'),

















    #   购买商品
    path('<user_id>/buy/', views.buy, name='buy'),

    #   加入购物车
    path('<user_id>/<commodity_id>/add_cart/', views.add_cart, name='add_cart'),

    #   查看购物车
    path('<user_id>/look_cart/', views.look_cart, name='look_cart'),


    #   结算购物车
    path('<user_id>/buy_summarize/', views.buy_summarize, name='buy_summarize'),

    #   清空购物车
    path('<user_id>/buy_empty/', views.buy_empty, name='buy_empty'),





]


urlpatterns += [
    #   验证是否是商家
    path('permission/', views.permission, name='permission'),

    #   升级商家支付金额
    path('deduct/', views.deduct, name='deduct'),

    #   发布商品
    path('commodity_pub/', views.commodity_pub, name='commodity_pub'),

    #   查看发布的商品
    path('commodity_look_pub/', views.commodity_look_pub, name='commodity_look_pub'),

    #   向上翻页
    path('<page>/commodity_look_pub_up/', views.up, name='up'),

    #   向下翻页
    path('<page>/commodity_look_pub_next/', views.next, name='next'),


















    #   验证账号是否正确
    # path('commodity_login/', views.commodity_login, name='commodity_login'),

    #   验证是否是商家
    # path('commodity_user/', views.commodity_user, name='commodity_user'),



    #   查看商品的分类
    path('<user_id>/commodity_sort/', views.commodity_sort, name='commodity_sort'),

    #   添加商品分类
    path('<user_id>/add_sort/', views.add_sort, name='add_sort'),

    #   确认添加商品分类
    path('<user_id>/check_add_sort/', views.check_add_sort, name='check_add_sort'),




    #   添加商品
    # path('<user_id>/commodity_add/', views.commodity_add, name='commodity_add'),


    #   商品的大标题
    path('<user_id>/commodity_BigTitle/', views.commodity_BigTitle, name='commodity_BigTitle'),


    #   修改商品
    path('<user_id>/commodity_modify/', views.commodity_modify, name='commodity_modify'),

    #   发布修改后商品
    path('<commodity_id>/<user_id>/commodity_modify_sub/', views.commodity_modify_usb, name='commodity_modify_sub'),
    path('<commodity_id>/<user_id>/commodity_modify_2/', views.commodity_modify_2, name='commodity_modify_2'),

]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('send/', Email.send, name='send')
]