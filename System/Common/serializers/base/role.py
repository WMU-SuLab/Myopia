# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/5/11 13:31
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

from rest_framework import serializers

from Common.models.role import *
from . import base_exclude, BaseSerializer

role_exclude = base_exclude


class RoleBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        # fields = '__all__'
        exclude = role_exclude


class ManagerBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Manager


class EmployeeBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Employee


class StudentBaseSerializer(RoleBaseSerializer):
    student_type_display = serializers.CharField(source='get_student_type_display')

    class Meta(RoleBaseSerializer.Meta):
        model = Student


class TeacherBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Teacher


class WeChatBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = WeChat


class QQBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = QQ


class WeiboBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Weibo
