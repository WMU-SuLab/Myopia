# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/11/11 21:07
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

from .high_myopia import HighMyopiaProjectsManageView
from .tgfbi import TGFBIProjectsManageView
from .index import SampleManagerIndexView
from .user import SampleManagerLoginView

urlpatterns = [
    path('login', SampleManagerLoginView.as_view(), name='login'),
    path('index', SampleManagerIndexView.as_view(), name='index'),
    path('projects/high_myopia', HighMyopiaProjectsManageView.as_view(), name='high_myopia_projects'),
    path('projects/tgfbi', TGFBIProjectsManageView.as_view(), name='tgfbi_projects'),
]
