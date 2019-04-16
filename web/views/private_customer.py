#!-*- coding:utf-8 -*-
# __author__:"irving"
from stark.service.v1 import StarkHandler


class PrivateCustomerHandler(StarkHandler):
    list_display = ['name', ]
