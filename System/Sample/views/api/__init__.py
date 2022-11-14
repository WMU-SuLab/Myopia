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

from django.urls import path, include

from Sample import app_name
from Sample.views.api.mina.feedback import UserFeedbackToAPIView

urlpatterns = [
    path('user/feedback_to', UserFeedbackToAPIView.as_view(), name='user_feedback_to'),
    path('mina/', include(('Sample.views.api.mina', app_name), namespace='mina')),
    path('manage/', include(('Sample.views.api.manage', app_name), namespace='manage')),
]
