#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from django import forms
from web import models
from stark.service.v1 import site, StarkHandler, get_choice_text, StarkModelForm, StarkForm, Option
from django.core.exceptions import ValidationError
from web.utils.hash_md5 import gen_md5
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from .base import PermissionHandler


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data.get('password')
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoAddStudentModelForm(UserInfoAddModelForm, StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email']


class UserInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class ResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoHandler(PermissionHandler, StarkHandler):

    def display_reset_pwd(self, obj=None, is_header=None):
        if is_header:
            return "重置密码"
        reset_url = self.reverse_reset_pwd_url(pk=obj.pk)
        return mark_safe('<a href="%s">重置密码</a>' % reset_url)

    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart', display_reset_pwd]

    search_list = ['nickname__contains', 'name__contains']

    search_group = [
        Option(field='gender'),
        Option(field='depart'),
    ]

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置')
        if request.method == "GET":
            form = ResetPasswordForm()
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            # 密码更新到数据库
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def student_add(self, request, *args, **kwargs):
        """
        添加学生账户视图函数
        :param request:
        :return:
        """
        if request.method == "GET":
            form = UserInfoAddStudentModelForm()
            return render(request, 'stark/change.html', {'form': form})
        form = UserInfoAddStudentModelForm(request.POST)
        if form.is_valid():
            # 账户信息更新到数据库
            self.save(request, form, False, *args, **kwargs)

        return redirect('/stark/web/student/list/')

    def save(self, request, form, is_update, *args, **kwargs):
        form.instance.depart_id = 6
        form.instance.user_id = 6
        form.save()

    @property
    def get_reset_pwd_url_name(self):
        return self.get_url_name('reset_pwd')

    @property
    def get_student_add_url_name(self):
        return self.get_url_name('student_add')

    def reverse_reset_pwd_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的重置密码URL
        :param
        args:
        :param
        kwargs:
        :return:
        """
        return self.reverse_commons_url(self.get_reset_pwd_url_name, *args, **kwargs)

    def extra_urls(self):
        patterns = [
            url(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password), name=self.get_reset_pwd_url_name),
            url(r'^student/add/$', self.wrapper(self.student_add), name=self.get_student_add_url_name),
        ]
        return patterns
