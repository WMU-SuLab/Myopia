# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/9 9:57
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

from .sample import SampleManagerLoginView, SampleManagerIndexView, SampleUserManageView

urlpatterns = [
    path('sample/manager_login', SampleManagerLoginView.as_view(), name='sample_manager_login'),
    path('sample/index', SampleManagerIndexView.as_view(), name='sample_manager_index'),
    path('sample/user', SampleUserManageView.as_view(), name='sample_user_manage'),
]
