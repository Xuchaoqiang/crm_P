#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from web import models
from stark.service.v1 import site, StarkHandler


class DepartmentHandler(StarkHandler):
    list_display = ['title', ]


site.register(models.Department, DepartmentHandler)
