# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/24 9:18
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

from Common.models.user import User
from Common.models.role import *
from Common.models.equipments import *
from Common import app_name
from .test import test

urlpatterns = [
    path('test', test, name='test'),
    path('user/', include(('Common.views.api.user', app_name), namespace='user')),
]