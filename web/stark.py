#!-*- coding:utf-8 -*-
# __author__:"irving"

from web import models
from stark.service.v1 import site
from web.views.school import SchoolHandler
from web.views.depart import DepartmentHandler
from web.views.userinfo import UserInfoHandler
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler

site.register(models.School, SchoolHandler)

site.register(models.Department, DepartmentHandler)

site.register(models.UserInfo, UserInfoHandler)

site.register(models.Course, CourseHandler)

site.register(models.ClassList, ClassListHandler)
