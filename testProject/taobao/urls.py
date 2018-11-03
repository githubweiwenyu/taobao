from django.urls import path
from . import views
app_name = 'taobao'

urlpatterns = [
    path('', views.Enter, name='Enter'),
    path('user_BigTitle/', views.user_BigTitle, name='user_BigTitle'),
    path('user_Registered/', views.user_Registered, name='user_Registered'),
    path('user_Registered_2/', views.user_Registered_2, name='user_Registered_2'),
    path('<user_id>/user_TwoTitle/', views.user_TwoTitle, name='user_TwoTitle'),
    path('user_Login/', views.user_Login, name='user_Login'),
    path('user_Login_2/', views.user_Login_2, name='user_Login_2'),
    path('<user_id>/user_look/', views.user_look, name='user_look'),
    path('<user_id>/modify_password/', views.modify_password, name='modify_password'),
    path('<user_id>/modify_modify_password_2/', views.modify_password_2, name='modify_password_2'),
    path('<user_id>/recharge/', views.recharge, name='recharge'),
    path('<user_id>/recharge_2/', views.recharge_2, name='recharge_2'),
    path('user_ModifyPassword/', views.user_ModityPassword, name='user_ModityPassword'),
    path('verify/', views.versfy, name='verify'),
    path('<user_id>/reset_password_2/', views.reset_password_2, name='reset_password_2'),


    path('commodity_login/', views.commodity_login, name='commodity_login'),
    path('commodity_user/', views.commodity_user, name='commodity_user'),
    path('<user_id>/decuct/', views.decuct, name='decuct'),
    path('<user_id>/<user_state>/commodity_pub/', views.commodity_pub, name='commodity_pub'),
    path('<user_id>/<user_state>/commodity_add/', views.commodity_add, name='commodity_add'),
    path('<user_id>/<user_state>/commodity_look_pub/', views.commodity_look_pub, name='commodity_look_pub'),
    path('<user_id>/<user_state>/commodity_BigTitle/', views.commodity_BigTitle, name='commodity_BigTitle'),

    path('<page>/<user_id>/<user_state>/commodity_look_pub_up/', views.up, name='up'),
    path('<page>/<user_id>/<user_state>/commodity_look_pub_next/', views.next, name='next'),
    path('<user_id>/<commodity_id>/buy/', views.buy, name='buy'),
    path('<user_id>/<user_state>/commodity_modify/', views.commodity_modify, name='commodity_modify'),
    path('<commodity_id>/<user_id>/<user_state>/commodity_modify_sub/', views.commodity_modify_usb, name='commodity_modify_sub'),
    path('<commodity_id>/<user_id>/<user_state>/commodity_modify_2/', views.commodity_modify_2, name='commodity_modify_2'),























]