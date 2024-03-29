# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
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

from Common.models.project import Project
from .base import BaseAdmin


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    pass