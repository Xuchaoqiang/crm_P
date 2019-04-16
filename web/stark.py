#!-*- coding:utf-8 -*-
# __author__:"irving"

from web import models
from stark.service.v1 import site
from web.views.school import SchoolHandler
from web.views.depart import DepartmentHandler
from web.views.userinfo import UserInfoHandler
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler
from web.views.public_customer import PublicCustomerHandler
from web.views.private_customer import PrivateCustomerHandler

site.register(models.School, SchoolHandler)

site.register(models.Department, DepartmentHandler)

site.register(models.UserInfo, UserInfoHandler)

site.register(models.Course, CourseHandler)

site.register(models.ClassList, ClassListHandler)

site.register(models.Customer, PublicCustomerHandler, 'pub')

site.register(models.Customer, PrivateCustomerHandler, 'priv')
