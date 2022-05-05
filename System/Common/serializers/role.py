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


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class WeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChat
        fields = '__all__'


class QQSerializer(serializers.ModelSerializer):
    class Meta:
        model = QQ
        fields = '__all__'


class WeiboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weibo
        fields = '__all__'
