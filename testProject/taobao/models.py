from django.db import models
import os
from django.utils import timezone
import random

def user_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    fn = "%s_%s%s" % (timezone.now().strftime("%Y%m%d%H%M%S"),
                      random.randint(100000, 999999),
                      ext)
    return "portrait/%s" % fn


class Users(models.Model):
    user_account = models.CharField(max_length=20, blank=False)
    user_password = models.CharField(max_length=200, blank=False)
    user_question = models.CharField(max_length=50, default='', blank=False)
    user_answer = models.CharField(max_length=50, default='', blank=False)
    user_name = models.CharField(max_length=20, default='', blank=False)
    user_RMB = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False)
    user_time = models.DateTimeField(auto_now_add=True, blank=False)
    user_state = models.CharField(max_length=20, default='0', blank=False)
    user_portrait = models.FileField(upload_to=user_upload_to, default='portrait/default.jpg')

    class Meta:
        db_table = 'User'


class User_login_history(models.Model):
    loginuser_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_login_history'


class Commodity_sort(models.Model):
    sort_name = models.CharField(max_length=200, blank=False)
    sort_shortcut = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'commodity_sort'




def commodity_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    fn = "%s_%s%s" % (timezone.now().strftime("%Y%m%d%H%M%S"),
                      random.randint(100000, 999999),
                      ext)
    return "photos/%s" % fn


class Commodity(models.Model):
    commodity_id = models.CharField(max_length=200, primary_key=True, blank=False)
    commodity_name = models.CharField(max_length=200, blank=False)
    commodity_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    commodity_sort = models.CharField(max_length=200, blank=False)
    stock = models.IntegerField(default=0, blank=False)
    commodity_photo = models.FileField(upload_to=commodity_upload_to, blank=False)

    publish_date = models.DateTimeField(default=timezone.now())
    modify_date = models.DateTimeField(auto_now=True, blank=False)
    commodity_user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False)

    class Meta:
        db_table = 'Commodity'


# class Commodity_modify_log(models.Model):
#     commodity_id = models.ForeignKey(Commodity, on_delete=models.CASCADE)
#     modify_time = models.DateField(auto_now_add=True)
#     modify_detail = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'Commodity_modify_log'


class Shopping_cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    commodity_id = models.CharField(max_length=200, primary_key=True)
    commodity_name = models.CharField(max_length=200)
    commodity_price = models.DecimalField(max_digits=10, decimal_places=2)
    commodity_num = models.IntegerField()
    commodity_sum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Shopping_cart'



