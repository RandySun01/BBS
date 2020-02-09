"""
@author RansySun
@create 2019-11-03-11:35
"""
from django import forms
from django.forms import widgets
from app import models


class MyRegForm(forms.Form):
    """创建注册标签"""
    username = forms.CharField(min_length=3, max_length=9, label='用户名',
                               error_messages={
                                   'min_length': '用户名不能少于六位',
                                   'max_length': '用户名不能大于九位',
                                   'required': '用户名不能为空'
                               }, widget=widgets.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(min_length=3, max_length=8, label='密 码',
                               error_messages={
                                   'min_length': '密码不能少于六位',
                                   'max_length': '密码不能多于八位',
                                   'required': '密码不能为空'
                               }, widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(min_length=3, max_length=8, label='确认密码',
                                       error_messages={
                                           'min_length': '确认密码不能少于六位',
                                           'max_length': '确认密码不能多于八位',
                                           'required': '确认密码不能为空'
                                       }, widget=widgets.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'required': '邮箱不能为空',
                                 'invalid': '邮箱格式不正确'
                             }, widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        """局部钩子,判断用户是否已经存在"""
        username = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=username)
        if user_obj:
            self.add_error('username', "用户已经存在")

        return username

    def clean(self):
        """全局钩子, 判断用户名是否相同"""
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not (password == confirm_password):
            self.add_error('confirm_password', '两次密码不一致')

        return self.cleaned_data
