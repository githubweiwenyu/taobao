from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, min_length=6,
                               label="账号")
    password = forms.CharField(max_length=20, required=True, min_length=6,
                               label="密码", widget=forms.PasswordInput())