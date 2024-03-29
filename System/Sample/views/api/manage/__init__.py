# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/11/11 21:12
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

from .high_myopia import HighMyopiaProjectsAPIView, HighMyopiaProjectUpdateAPIView, \
    HighMyopiaProjectUploadReportFileAPIView, HighMyopiaProjectsExportAPIView
from .tgfbi import TGFBISampleLIMSUpdateReportAPIView, TGFBIProjectsAPIView, TGFBIProjectUpdateAPIView, \
    TGFBIProjectUploadReportFileAPIView, TGFBIProjectsExportAPIView
from .user import SampleManagerLoginAPIView, SampleManagerLogoutAPIView

urlpatterns = [
    path('login', SampleManagerLoginAPIView.as_view(), name='login'),
    path('logout', SampleManagerLogoutAPIView.as_view(), name='logout'),
    # 高度近视遗传风险评估
    path('high_myopia/projects', HighMyopiaProjectsAPIView.as_view(), name='high_myopia_projects'),
    path('high_myopia/update_project', HighMyopiaProjectUpdateAPIView.as_view(), name='high_myopia_project_update'),
    path('high_myopia/upload_report_file/<int:project_id>', HighMyopiaProjectUploadReportFileAPIView.as_view(),
         name='high_myopia_project_upload_report_file'),
    path('high_myopia/export_all_data', HighMyopiaProjectsExportAPIView.as_view(),
         name='high_myopia_projects_export'),
    # TGFBI角膜营养不良基因检测
    path('tgfbi/lims_upload_report_file', TGFBISampleLIMSUpdateReportAPIView.as_view(),
         name='tgfbi_lims_upload_report_file'),
    path('tgfbi/projects', TGFBIProjectsAPIView.as_view(), name='tgfbi_projects'),
    path('tgfbi/update_project', TGFBIProjectUpdateAPIView.as_view(), name='tgfbi_project_update'),
    path('tgfbi/upload_report_file/<int:project_id>', TGFBIProjectUploadReportFileAPIView.as_view(),
         name='tgfbi_project_upload_report_file'),
    path('tgfbi/export_all_data', TGFBIProjectsExportAPIView.as_view(), name='tgfbi_projects_export'),
]
