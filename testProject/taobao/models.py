from django.db import models


class User(models.Model):
    user_account = models.CharField(max_length=20)
    user_password = models.CharField(max_length=6)
    user_question = models.CharField(max_length=50, default='')
    user_answer = models.CharField(max_length=50, default='')
    user_name = models.CharField(max_length=20, default='')
    user_RMB = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_time = models.DateField(auto_now_add=True)
    user_state = models.CharField(max_length=20, default='0')


class Commodity(models.Model):
    commodity_id = models.CharField(max_length=21, primary_key=True)
    commodity_name = models.CharField(max_length=200)
    commodity_price = models.DecimalField(max_digits=10, decimal_places=2)
    commodity_sort = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    commodity_user = models.ForeignKey(User, on_delete=models.CASCADE)
