#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from stark.service.v1 import StarkHandler


class CourseHandler(StarkHandler):
    list_display = ['name', ]
