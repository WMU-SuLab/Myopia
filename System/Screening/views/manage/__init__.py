# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/8 19:01
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

from django.urls import path

from .index import index
from .user import login

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
]
