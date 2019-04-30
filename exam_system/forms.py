import re
from django import forms

# from .models import Person


class LoginForm(forms.Form):
    """登录信息验证"""
    userId = forms.CharField(required=True)
    passWord = forms.CharField(required=True, min_length=6, max_length=20)