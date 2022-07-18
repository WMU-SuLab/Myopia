# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/3/31 20:53
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

from datetime import datetime

from django.conf import settings
from django.db import models

from .base import Base, handle_object_does_not_exist
from .user import User


class Project(Base):
    progress_choices = (
        (-1, '未知'),
        (1, '已登记'),
        (2, '采样中'),
        (3, '已收样'),
        (4, '分析中'),
        (5, '出报告'),
        (6, '已完成'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name='用户')
    name = models.CharField(max_length=63, null=True, blank=True, default=None, verbose_name='项目名称')
    progress = models.IntegerField(choices=progress_choices, null=True, blank=True, default=-1, verbose_name='当前进度')
    finished_time = models.DateTimeField(null=True, blank=True, default=None, verbose_name='完成时间')
    report_data = models.JSONField(null=True, blank=True, default=dict, verbose_name='报告数据')
    report_file_url = models.URLField(max_length=512, null=True, blank=True, default=None, verbose_name='报告文件url')
    report_file_path = models.CharField(max_length=512, null=True, blank=True, default=None, verbose_name='报告文件路径')

    class Meta:
        verbose_name = verbose_name_plural = '项目'

    def start(self):
        self.progress = 0
        self.save()

    def finish(self):
        self.progress = 1
        self.finished_time = datetime.now().astimezone(settings.TZ_INFO)
        self.save()

    @property
    def completed_time(self):
        return self.finished_time

    @property
    def project_name_school_rule(self):
        year, school, school_region, user_role = self.name.split('-')
        return year, school, school_region, user_role

    def set_project_name_school_rule(self, year, school, school_region, user_role):
        self.name = f'{year}-{school}-{school_region}-{user_role}'

    @property
    def project_name_city_rule(self):
        year, city, city_region, user_role = self.name.split('-')
        return year, city, city_region, user_role

    def set_project_name_city_rule(self, year, city, city_region, user_role):
        self.name = f'{year}-{city}-{city_region}-{user_role}'

    @property
    def has_report_file(self):
        if self.report_file_path or self.report_file_url:
            return True
        return False

    def has_equipment(self, equipment_type):
        return getattr(self, 'has_' + equipment_type)

    @property
    @handle_object_does_not_exist
    def has_visual_chart(self):
        return True if self.visual_chart else False

    @property
    @handle_object_does_not_exist
    def has_bio_meter(self):
        return True if self.bio_meter else False

    @property
    @handle_object_does_not_exist
    def has_optometry(self):
        return True if self.optometry else False

    @property
    @handle_object_does_not_exist
    def has_tono_meter(self):
        return True if self.tono_meter else False

    @property
    @handle_object_does_not_exist
    def has_eye_ground(self):
        return True if self.eye_ground else False

    @property
    @handle_object_does_not_exist
    def has_sequence(self):
        return True if self.sequence else False

    @property
    @handle_object_does_not_exist
    def has_informed_consent(self):
        return True if self.informed_consent else False

    @property
    @handle_object_does_not_exist
    def has_questionnaire(self):
        return True if self.questionnaire else False

    def __str__(self):
        return f'<Project : {self.id}-user:{self.user_id}>'
