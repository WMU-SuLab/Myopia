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

from django.db import models

from .base import Base
from .user import User


class Project(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name='用户')
    name = models.CharField(max_length=63, null=True, blank=True, default=None, verbose_name='项目名称')
    is_finished = models.BooleanField(default=False, verbose_name='是否完成')
    finished_time = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='完成时间')
    report_file_url = models.URLField(max_length=512, null=True, blank=True, default=None, verbose_name='报告文件url')

    class Meta:
        verbose_name = verbose_name_plural = '项目'

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

    def __str__(self):
        return f'<Project : {self.id}-user:{self.user_id}>'
