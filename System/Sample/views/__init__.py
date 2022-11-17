# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/11/11 21:06
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

from Sample import app_name

urlpatterns = [
    path('', include(('Sample.views.web', app_name), namespace='web')),
    path('api/', include(('Sample.views.api', app_name), namespace='api')),
    path('manage/', include(('Sample.views.manage', app_name), namespace='manage')),
]
