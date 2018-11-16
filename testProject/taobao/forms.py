from django import forms
from .models import *


#   注册用户
class LoginForm(forms.ModelForm):
    # user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
    #                                help_text="账号为6-20位长的字符串,不能为空")
    # user_password = forms.CharField(max_length=20, required=True, min_length=6, label="密码", widget=forms.PasswordInput())
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=200, required=True, min_length=6, label="user_password",
                                    widget=forms.PasswordInput(),
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长200位",
                                                    "min_length": "用户名最短6位"})

    user_question = forms.CharField(max_length=200, required=True, min_length=2, label="user_question",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短2位"})
    user_answer = forms.CharField(max_length=200, required=True, min_length=2, label="user_answer",
                                  error_messages={"required": "不能为空",
                                                  "max_length": "用户名最长200位",
                                                  "min_length": "用户名最短2位"})
    user_name = forms.CharField(max_length=20, required=True, min_length=2, label="user_name",
                                error_messages={"required": "不能为空",
                                                "max_length": "用户名最长20位",
                                                "min_length": "用户名最短2位"})

    user_portrait = forms.ImageField(required=False)

    class Meta:
        model = Users
        fields = ['user_account',
                  'user_password',
                  'user_question',
                  'user_answer',
                  'user_name',
                  'user_portrait']


#   登录用户
class LoginUser(forms.Form):
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=20, required=True, min_length=6, label="user_password",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"})


#   验证用户
class VerifyUser(forms.Form):
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})


#   账号充值
class Recharge(forms.Form):
    user_RMB = forms.DecimalField(max_value=100000000.00, min_value=1, decimal_places=2, required=True,
                                  error_messages={'min_value': '最小金额为￥1',
                                                  'max_value': '最大金额为￥100000000.00',
                                                  'required': '不能为空'})


#   商家登录
class Merchant(forms.Form):
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=20, required=True, min_length=6, label="user_password",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"})


#   发布商品
class CommodityForm(forms.ModelForm):
    commodity_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    commodity_name = forms.CharField(max_length=20, required=True, min_length=2, label="商品名称")

    commodity_price = forms.DecimalField(max_value=100000000.00, min_value=1, decimal_places=0,
                                         required=True,
                                         label='商品单价')

    commodity_sort = forms.ChoiceField(required=True, label='商品分类', choices=(('QX', '【齐胸衫裙】'),
                                                                             ('QY', '【齐腰衫裙】'),
                                                                             ('DX', '【大袖衫裙】'),
                                                                             ('WJ', '【魏晋襦】')))

    stock = forms.IntegerField(max_value=100000000, required=True, min_value=1, label="商品库存")

    commodity_photo = forms.ImageField(required=True, label='上传商品图片')

    class Meta:
        model = Commodity
        fields = ['commodity_id',
                  'commodity_name',
                  'commodity_price',
                  'commodity_sort',
                  'stock',
                  'commodity_photo']
