from django.db import models
from rbac.models import UserInfo as RbacUserInfo


# Create your models here.

class School(models.Model):
    """
    校区表：
        北京昌平校区
        上海浦东校区
        深圳南山校区
    """
    title = models.CharField(verbose_name="校区名称", max_length=32)

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):
    """
    员工表
    """
    nickname = models.CharField(verbose_name='姓名', max_length=16)
    phone = models.CharField(verbose_name='手机号', max_length=32)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)

    depart = models.ForeignKey(verbose_name='部门', to="Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(verbose_name="课程名称", max_length=32)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    如：
        Python全栈    面授班     5期      10000       2017-11-11      2018-5-11
    """
    school = models.ForeignKey(verbose_name="校区", to='School', on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name="课程名称", to='Course', on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(verbose_name="班级(期)")
    price = models.PositiveIntegerField(verbose_name="学费")
    start_date = models.DateTimeField(verbose_name="开班日期")
    graduate_date = models.DateTimeField(verbose_name="结课日期", null=True, blank=True)
    class_teacher = models.ForeignKey(verbose_name="班主任", to=UserInfo, related_name='classes', on_delete=models.CASCADE)
    tech_teachers = models.ManyToManyField(verbose_name="任课老师", to=UserInfo, related_name='teach_classes', null=True,
                                           blank=True)
    memo = models.TextField(verbose_name="说明", blank=True, null=True)

    def __str__(self):
        return "{0}（{1}期）".format(self.course.name, self.semester)
