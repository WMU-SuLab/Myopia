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

from django.db import models

from .base import Base
from .user import User


class Manager(Base):
    """
    管理员
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_role', verbose_name='用户')

    class Meta:
        verbose_name = verbose_name_plural = '管理员'

    def __str__(self):
        return f'<Manager :{self.user.username}>'


class Employee(Base):
    """
    员工
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_role', verbose_name='用户')

    class Meta:
        verbose_name = verbose_name_plural = '员工'

    def __str__(self):
        return f'<Employee :{self.user.username}>'


class Student(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_role', verbose_name='用户')
    student_number = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='学号')
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


class WeChat(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wechat_role', verbose_name='用户')
    open_id = models.CharField(max_length=32, verbose_name='微信open_id')
    union_id = models.CharField(max_length=32, unique=True, db_index=True, verbose_name='微信union_id')
    session_key = models.CharField(max_length=128, verbose_name='微信session_key')

    nickname = models.CharField(blank=True, null=True, default=None, max_length=32, verbose_name='微信昵称')
    avatar_url = models.URLField(blank=True, null=True, default=None, verbose_name='微信头像地址')


class QQ(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wechat_role', verbose_name='用户')
    nickname = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='QQ昵称')
    avatar_url = models.URLField(blank=True, null=True, default=None, verbose_name='QQ头像地址')
