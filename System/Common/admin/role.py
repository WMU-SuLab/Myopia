# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/4/29 16:56
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

from django.contrib import admin

from Common.models.role import *
from .base import BaseAdmin


@admin.register(Manager)
class ManagerAdmin(BaseAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(BaseAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(BaseAdmin):
    pass


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    pass


@admin.register(WeChatPlatformRole)
class WeChatPlatformRoleAdmin(BaseAdmin):
    pass


@admin.register(WeChatAPPRole)
class WeChatAPPRoleAdmin(BaseAdmin):
    pass


@admin.register(QQ)
class QQAdmin(BaseAdmin):
    pass


@admin.register(Weibo)
class WeiboAdmin(BaseAdmin):
    pass
