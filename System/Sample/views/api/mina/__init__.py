# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/11/11 21:08
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

from .feedback import UserFeedbackToAPIView, UserFeedbackToEmailAPIView
from .high_myopia import SerialNumberList, SerialNumberRetrieve, SubmitHighMyopiaFormAPIView
from .project import ProjectsListAPIView, ProjectRetrieveAPIView
from .sf_express import CancelSFExpressAPIView
from .tgfbi import SubmitTGFBISampleBindingFormAPIView, SubmitTGFBISampleSendFormAPIView
from .user import SendPhoneSMSAPIView

urlpatterns = [
    path('user/send_phone_sms', SendPhoneSMSAPIView.as_view(), name='send_phone_sms'),
    # 用户反馈
    path('user/feedback_to', UserFeedbackToAPIView.as_view(), name='user_feedback_to'),
    path('user/feedback_to_email', UserFeedbackToEmailAPIView.as_view(), name='user_feedback_to_email'),
    path('user/cancel_order/<str:order_id>', CancelSFExpressAPIView.as_view(), name='user_cancel_order'),
    # 项目
    path('project/serial_numbers', ProjectsListAPIView.as_view(), name='project_list'),
    path('project/serial_numbers/<str:serial_number>', ProjectRetrieveAPIView.as_view(), name='project_retrieve'),
    # 高度近视遗传风险评估
    path('high_myopia/serial_numbers', SerialNumberList.as_view(), name='high_myopia_list_serial_numbers'),
    path('high_myopia/serial_numbers/<str:serial_number>', SerialNumberRetrieve.as_view(),
         name='high_myopia_retrieve_serial_number'),
    path('high_myopia/submit_form', SubmitHighMyopiaFormAPIView.as_view(), name='high_myopia_submit_form'),
    # TGFBI角膜营养不良基因检测
    path('tgfbi/submit_binding_form', SubmitTGFBISampleBindingFormAPIView.as_view(),
         name='tgfbi_submit_binding_form'),
    path('tgfbi/submit_send_form', SubmitTGFBISampleSendFormAPIView.as_view(), name='tgfbi_submit_send_form'),
]
