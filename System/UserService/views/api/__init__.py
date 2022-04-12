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

from django.urls import path

from Common.utils.auth.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .report import get_student_report_data, get_teacher_report_data, get_student_report_pdf_file, \
    get_teacher_report_pdf_file
from .test import test

urlpatterns = [
    path('test', test, name='test'),
    path('get_student_report_data', get_student_report_data, name='get_student_report_data'),
    path('get_student_report_pdf_file', get_student_report_pdf_file, name='get_student_report_pdf_file'),
    path('get_teacher_report_data', get_teacher_report_data, name='get_teacher_report_data'),
    path('get_teacher_report_pdf_file', get_teacher_report_pdf_file, name='get_teacher_report_pdf_file'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
]
