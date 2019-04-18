#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from stark.service.v1 import StarkHandler
from .base import PermissionHandler


class CourseHandler(PermissionHandler, StarkHandler):
    list_display = ['name', ]
