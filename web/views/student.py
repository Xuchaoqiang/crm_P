#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from stark.service.v1 import StarkHandler, get_choice_text, get_m2m_text, StarkModelForm, Option
from .base import PermissionHandler

from web import models


class StudentModelForm(StarkModelForm):
    class Meta:
        model = models.Student
        fields = ['qq', 'mobile', 'emergency_contract', 'memo']


class StudentHandler(PermissionHandler, StarkHandler):
    model_form_class = StudentModelForm

    def display_score(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '积分管理'

        record_url = reverse('stark:web_scorerecord_list', kwargs={'student_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (record_url, obj.score))

    list_display = ['customer', 'qq', 'mobile', 'emergency_contract', get_m2m_text('已报班级', 'class_list'),
                    display_score, get_choice_text('状态', 'student_status')]

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_list_display(self, request, *args, **kwargs):
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value

    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            url(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    search_list = ['customer__name__contains', 'qq', 'mobile', ]

    search_group = [
        Option('class_list', text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    ]
