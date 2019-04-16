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
    class_teacher = models.ForeignKey(verbose_name="班主任", to=UserInfo, related_name='classes',
                                      limit_choices_to={'depart__title': '教质部'}, on_delete=models.CASCADE)
    tech_teachers = models.ManyToManyField(verbose_name="任课老师", to=UserInfo, related_name='teach_classes',
                                           blank=True,
                                           limit_choices_to={'depart__title__in': ['Linux教学部', 'Python教学部']})
    memo = models.TextField(verbose_name="说明", blank=True, null=True)

    def __str__(self):
        return "{0}（{1}期）".format(self.course.name, self.semester)


class Customer(models.Model):
    """
    客户表
    """
    MAX_PRIVATE_CUSTOMER_COUNT = 150

    name = models.CharField(verbose_name='姓名', max_length=32)
    qq = models.CharField(verbose_name='联系方式', max_length=64, unique=True, help_text='QQ号/微信/手机号')
    status_choices = [
        (1, '未报名'),
        (2, '已报名')
    ]
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=1)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    source_choices = [
        (1, "qq群"),
        (2, "内部转介绍"),
        (3, "官方网站"),
        (4, "百度推广"),
        (5, "360推广"),
        (6, "搜狗推广"),
        (7, "腾讯课堂"),
        (8, "广点通"),
        (9, "高校宣讲"),
        (10, "渠道代理"),
        (11, "51cto"),
        (12, "智汇推"),
        (13, "网盟"),
        (14, "DSP"),
        (15, "SEO"),
        (16, "其它"),
    ]
    source = models.SmallIntegerField('客户来源', choices=source_choices, default=1)

    referral_form = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name='转介绍自学员',
        help_text='若此客户是转介绍自内部学员,请在此处选择内部学员姓名',
        related_name="internal_referral",
        on_delete=models.CASCADE
    )

    course = models.ManyToManyField(verbose_name="咨询课程", to=Course)
    consultant = models.ForeignKey(verbose_name="课程顾问", to='UserInfo', related_name='consultant',
                                   null=True, blank=True,
                                   limit_choices_to={'depart__title': '销售部'},
                                   on_delete=models.CASCADE)

    education_choices = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办专科'),
        (7, '高中'),
        (8, '其他')
    )
    education = models.IntegerField(verbose_name='学历', choices=education_choices, blank=True, null=True)
    graduation_school = models.CharField(verbose_name="毕业学校", max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name="所学专业", max_length=64, blank=True, null=True)

    experience_choices = [
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    ]
    experience = models.IntegerField(verbose_name='工作经验', blank=True, null=True, choices=experience_choices)
    work_status_choices = [
        (1, '在职'),
        (2, '无职')
    ]
    work_status = models.IntegerField(verbose_name="职业状态", choices=work_status_choices, default=1, blank=True,
                                      null=True)

    company = models.CharField(verbose_name="目前就职公司", max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name="当前薪资", max_length=64, blank=True, null=True)

    date = models.DateField(verbose_name="咨询日期", auto_now_add=True)
    last_consult_date = models.DateField(verbose_name="最后跟进日期", auto_now_add=True)

    def __str__(self):
        return "姓名:{0}, 联系方式{1}".format(self.name, self.qq, )


class ConsultRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name="所咨询客户", to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="跟踪人", to='UserInfo', on_delete=models.CASCADE)
    note = models.TextField(verbose_name="跟进内容")
    date = models.DateField(verbose_name="跟进日期", auto_now_add=True)
