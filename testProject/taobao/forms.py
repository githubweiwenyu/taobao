from django import forms


class LoginForm(forms.Form):
    # user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
    #                                help_text="账号为6-20位长的字符串,不能为空")
    # user_password = forms.CharField(max_length=20, required=True, min_length=6, label="密码", widget=forms.PasswordInput())
    user_account = forms.CharField(max_length=20, required=True, min_length=6, label="user_account",
                                   error_messages={"required": "不能为空",
                                                   "max_length": "用户名最长20位",
                                                   "min_length": "用户名最短6位"})
    user_password = forms.CharField(max_length=20, required=True, min_length=6, label="user_password",
                                    error_messages={"required": "不能为空",
                                                    "max_length": "用户名最长20位",
                                                    "min_length": "用户名最短6位"})


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