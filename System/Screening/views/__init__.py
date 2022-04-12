# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/4 16:09
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

from Screening import app_name

urlpatterns = [
    path('', include(('Screening.views.web',app_name),namespace='web')),
    path('api/', include(('Screening.views.api', app_name), namespace='api')),
    path('manage/', include(('Screening.views.manage', app_name), namespace='manage')),
]
