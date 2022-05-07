# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/5/5 21:19
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
from .base import base_exclude

role_exclude = base_exclude


class RoleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        # fields = '__all__'
        exclude = role_exclude


class RoleSerializerMeta(RoleBaseSerializer.Meta):
    depth = 1


class ManagerBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Manager


class ManagerSerializer(ManagerBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = Manager


class EmployeeBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Employee


class EmployeeSerializer(EmployeeBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = Employee


class StudentBaseSerializer(RoleBaseSerializer):
    student_type = serializers.CharField(source='get_student_type_display')

    class Meta(RoleBaseSerializer.Meta):
        model = Student


class StudentSerializer(StudentBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = Student


class TeacherBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Teacher


class TeacherSerializer(TeacherBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = Teacher


class WeChatBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = WeChat


class WeChatSerializer(WeChatBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = WeChat


class QQBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = QQ


class QQSerializer(QQBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = QQ


class WeiboBaseSerializer(RoleBaseSerializer):
    class Meta(RoleBaseSerializer.Meta):
        model = Weibo


class WeiboSerializer(WeiboBaseSerializer):
    class Meta(RoleSerializerMeta):
        model = Weibo
