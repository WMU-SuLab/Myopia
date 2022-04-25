# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/8 19:00
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

from .user import user_login, user_logout

urlpatterns = [
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
]
