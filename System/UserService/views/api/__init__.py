# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/4 16:06
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

from UserService import app_name
from .user import UserFeedbackToAPIView, UserFeedbackToEmailAPIView

urlpatterns = [
    path('user/feedback_to', UserFeedbackToAPIView.as_view(), name='user_feedback_to'),
    path('user/feedback_to_email', UserFeedbackToEmailAPIView.as_view(), name='user_feedback_to_email'),
    path('mina/', include(('UserService.views.api.mina', app_name), namespace='mina')),
]
