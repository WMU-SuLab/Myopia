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

from .base.role import *


class RoleSerializerMeta(RoleBaseSerializer.Meta):
    depth = 1


class ManagerSerializer(ManagerBaseSerializer):
    class Meta(RoleSerializerMeta, ManagerBaseSerializer.Meta):
        pass


class EmployeeSerializer(EmployeeBaseSerializer):
    class Meta(RoleSerializerMeta, EmployeeBaseSerializer.Meta):
        pass


class StudentSerializer(StudentBaseSerializer):
    class Meta(RoleSerializerMeta, StudentBaseSerializer.Meta):
        pass


class TeacherSerializer(TeacherBaseSerializer):
    class Meta(RoleSerializerMeta, TeacherBaseSerializer.Meta):
        pass


class WeChatSerializer(WeChatBaseSerializer):
    class Meta(RoleSerializerMeta, WeChatBaseSerializer.Meta):
        pass


class QQSerializer(QQBaseSerializer):
    class Meta(RoleSerializerMeta, QQBaseSerializer.Meta):
        pass


class WeiboSerializer(WeiboBaseSerializer):
    class Meta(RoleSerializerMeta, WeiboBaseSerializer.Meta):
        pass
