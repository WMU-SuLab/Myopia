# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/5/11 13:40
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
from rest_framework import serializers

from Common.models.project import Project
from . import base_exclude, BaseSerializer

project_exclude = base_exclude


class ProjectBaseSerializer(BaseSerializer):
    progress_display = serializers.CharField(source='get_progress_display')
    finished_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        # 当时间对象中不带有时区的时候，默认使用的时区
        # default_timezone=utc,
        default_timezone=settings.TZ_INFO,
    )

    class Meta(BaseSerializer.Meta):
        model = Project
        # fields = '__all__'
        exclude = project_exclude
