# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/4/4 15:53
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from django.conf import settings
from django.db import models

from Common.libs.choices import student_type_choices
from Common.viewModels.choices import list_to_choices
from .base import Base
from .user import User


class Manager(Base):
    """
    管理员
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_role', verbose_name='用户')
    entry_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='入职时间')
    departure_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='离职时间')
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name='是否在职')

    class Meta:
        verbose_name = verbose_name_plural = '管理员'

    def __str__(self):
        return f'<Manager :{self.user.username}>'


class Employee(Base):
    """
    员工
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_role', verbose_name='用户')
    entry_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='入职时间')
    departure_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='离职时间')
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name='是否在职')

    class Meta:
        verbose_name = verbose_name_plural = '员工'

    def __str__(self):
        return f'<Employee :{self.user.username}>'


class Student(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_role', verbose_name='用户')
    student_number = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='学号')
    student_type = models.FloatField(
        choices=student_type_choices, blank=True, null=True, default=0, verbose_name='学生类型')
    PE_classname = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='体育课班级')

    grade = models.CharField(max_length=10, verbose_name='年级')
    classname = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='班级')
    profession = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='专业')
    academy = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='学院')
    campus = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='校区')
    school = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='学校')

    class Meta:
        verbose_name = verbose_name_plural = '学生'

    def __str__(self):
        return f'<Student : {self.student_number}>'


class Teacher(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_role', verbose_name='用户')
    teacher_number = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='教工号')

    profession = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='专业')
    academy = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='学院')
    campus = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='校区')
    school = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='学校')

    class Meta:
        verbose_name = verbose_name_plural = '教师'

    def __str__(self):
        return f'<Teacher : {self.teacher_number}>'


class WeChatBaseRole:
    session_key = models.CharField(max_length=128, verbose_name='微信session_key')

    nickname = models.CharField(blank=True, null=True, default=None, max_length=32, verbose_name='微信昵称')
    avatar_url = models.URLField(blank=True, null=True, default=None, verbose_name='微信头像地址')


class WeChatPlatformRole(Base, WeChatBaseRole):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wechat_platform_roles', verbose_name='用户')

    platform_name = models.CharField(max_length=32, choices=list_to_choices(settings.WECHAT_OPEN_PLATFORMS.keys()),
                                     db_index=True, verbose_name='微信开放平台名称')
    union_id = models.CharField(max_length=32, unique=True, db_index=True, verbose_name='微信开放平台union_id')

    class Meta:
        verbose_name = verbose_name_plural = '微信开放平台角色'
        unique_together = (('platform_name', 'union_id'),)

    def __str__(self):
        return f'<WeChatPlatformRole : {self.nickname}>'


class WeChatAPPRole(Base, WeChatBaseRole):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wechat_app_roles', verbose_name='用户')
    # 根据https://developers.weixin.qq.com/doc/oplatform/Mobile_App/Launching_a_Mini_Program/Launching_a_Mini_Program.html
    # 和https://developers.weixin.qq.com/community/develop/doc/0000ae1a3f0c386e24c7542245b400
    # 同一个小程序只能绑定一个微信开放平台
    platform_role = models.ForeignKey(WeChatPlatformRole, blank=True, null=True, default=None,
                                      on_delete=models.SET_NULL, related_name='app_roles',
                                      verbose_name='微信开放平台身份')
    app_name = models.CharField(max_length=32, choices=list_to_choices(settings.WECHAT_MINAS.keys()),
                                db_index=True, verbose_name='微信应用名称')

    open_id = models.CharField(max_length=32, blank=True, null=True, default=None, db_index=True,
                               verbose_name='微信open_id')

    class Meta:
        verbose_name = verbose_name_plural = '微信应用角色'
        unique_together = (('app_name', 'open_id'),)

    def __str__(self):
        return f'<WeChatAPPRole : {self.nickname}>'


class QQ(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='QQ_role', verbose_name='用户')

    qq_id = models.CharField(max_length=32, unique=True, db_index=True, verbose_name='QQ号')
    nickname = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='QQ昵称')
    avatar_url = models.URLField(blank=True, null=True, default=None, verbose_name='QQ头像地址')

    class Meta:
        verbose_name = verbose_name_plural = 'QQ'

    def __str__(self):
        return f'<QQ : {self.nickname}>'


class Weibo(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='weibo_role', verbose_name='用户')
    nickname = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='微博昵称')
    avatar_url = models.URLField(blank=True, null=True, default=None, verbose_name='微博头像地址')

    class Meta:
        verbose_name = verbose_name_plural = '微博'

    def __str__(self):
        return f'<Weibo : {self.nickname}>'
