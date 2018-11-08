from django.db import models


class User(models.Model):
    user_account = models.CharField(max_length=20)
    user_password = models.CharField(max_length=6)
    user_question = models.CharField(max_length=50, default='')
    user_answer = models.CharField(max_length=50, default='')
    user_name = models.CharField(max_length=20, default='')
    user_RMB = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_time = models.DateTimeField(auto_now_add=True)
    user_state = models.CharField(max_length=20, default='0')

    class Meta:
        db_table = 'User'

#
# class User_login_history():
#     loginuser_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     login_time = models.DateField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'user_login_history'


# class Commodity_sort(models.Model):
#     sort_name = models.CharField(max_length=200)
#     sort_shortcut = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'commodity_sort'


class Commodity(models.Model):
    commodity_id = models.CharField(max_length=200, primary_key=True)
    commodity_name = models.CharField(max_length=200)
    commodity_price = models.DecimalField(max_digits=10, decimal_places=2)
    commodity_sort = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    commodity_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Commodity'

#
# class Commodity_modify_log(models.Model):
#     commodity_id = models.ForeignKey(Commodity, on_delete=models.CASCADE)
#     modify_time = models.DateField(auto_now_add=True)
#     modify_detail = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'Commodity_modify_log'


class Shopping_cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity_id = models.CharField(max_length=200, primary_key=True)
    commodity_name = models.CharField(max_length=200)
    commodity_price = models.DecimalField(max_digits=10, decimal_places=2)
    commodity_num = models.IntegerField()
    commodity_sum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Shopping_cart'



