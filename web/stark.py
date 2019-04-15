#!-*- coding:utf-8 -*-
# __author__:"irving"
from django import forms
from web import models
from stark.service.v1 import site, StarkHandler, get_choice_text, StarkModelForm


class SchoolHandler(StarkHandler):
    list_display = ['title', ]


site.register(models.School, SchoolHandler)


class DepartmentHandler(StarkHandler):
    list_display = ['title', ]


site.register(models.Department, DepartmentHandler)


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class UserInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class UserInfoHandler(StarkHandler):
    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart']

    def get_model_form_class(self, is_add=False):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm


site.register(models.UserInfo, UserInfoHandler)
