# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/13 22:00
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

from .report import get_user_report_data, get_user_report_pdf_file
from .sample import InquireSerialNumber, SubmitSampleForm

urlpatterns = [
    # 报告
    path('get_user_report_data', get_user_report_data, name='get_user_report_data'),
    path('get_user_report_pdf_file', get_user_report_pdf_file, name='get_user_report_pdf_file'),
    # 自采样
    path('inquire_serial_number', InquireSerialNumber.as_view(), name='inquire_serial_number'),
    path('submit_sample_form', SubmitSampleForm.as_view(), name='submit_sample_form'),
]
