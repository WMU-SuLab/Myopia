# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/4/24 9:17
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

from django.urls import path, include

from Common import app_name
from .index import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('api/', include(('Common.views.api', app_name), namespace='api')),
]
