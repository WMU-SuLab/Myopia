# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/15 23:47
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

import os

import pandas as pd
from rest_framework.response import Response

from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.responses.xlsx import xlsx_response
from Common.utils.http.successes import Success, FileUploadSuccess
from Common.utils.pagination import array_range
from Common.viewModels.project import handle_upload_project_report
from Sample.models.project import TGFBISampleProject
from Sample.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView
from Sample.utils.auth.views.project import ProjectUploadReportFileAPIView
from Sample.utils.forms.tgfbi import TGFBIManageForm
from Sample.utils.forms.tgfbi import TGFBIReportForm
from Sample.viewModels.tgfbi import decrypt_tgfbi_text


class TGFBISampleLIMSUpdateReportAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        form = TGFBIReportForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ParameterError(chinese_msg='数据格式错误', msg_detail=form.errors)
        project = decrypt_tgfbi_text(form.cleaned_data['encrypted_text'])
        if not project:
            raise ParameterError('加密字段验证错误')
        handle_upload_project_report(project, form.cleaned_data['report_file'])
        project.progress = 6
        project.save()
        return Response(FileUploadSuccess(chinese_msg='上传文件成功'))


class TGFBIProjectsAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = TGFBISampleProject.objects.filter(name='TGFBI角膜营养不良基因检测采样')
        # 过滤
        if serial_number := request.GET.get('serial_number', ''):
            projects = projects.filter(sequence__serial_number__contains=serial_number)
        if name := request.GET.get('name', ''):
            projects = projects.filter(remarks_json__name__icontains=name)
        if express_code := request.GET.get('express_code', ''):
            projects = projects.filter(remarks_json__courier__waybillNoInfoList__0__waybillNo=express_code)
        if order_code := request.GET.get('order_code', ''):
            projects = projects.filter(remarks_json__lims_full_info__orderCode=order_code)
        count = projects.count()
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        projects = array_range(projects.order_by('-id'), page, limit)
        projects = projects.prefetch_related('sequence')
        rows = [{
            'id': project.id,
            'serial_number': project.sequence.serial_number,
            'name': project.remarks_json.get('name', None),
            'gender': project.remarks_json.get('gender', None),
            'age': project.remarks_json.get('age', None),
            'birthday': project.remarks_json.get('birthday', None),
            'contact_phone_number': project.remarks_json.get('contact_phone_number', None),
            'bind_time': project.remarks_json.get('bind_time', None),
            'send_time': project.remarks_json.get('courier', {}).get('send_time', None),
            'express_code': project.remarks_json.get('courier', {}).
            get('waybillNoInfoList', [{}])[0].get('waybillNo', None),
            'order_code': project.remarks_json.get('lims_full_info', {}).get('orderCode', None),
            'progress': project.get_progress_display(),
            'report_file_name': os.path.basename(project.report_file_path) if project.report_file_path else '无',
            'created_time': project.created_time.strftime('%Y-%m-%d')
        } for project in projects]
        return Response(Success({'count': count, 'rows': rows}))


class TGFBIProjectUpdateAPIView(SampleManagerIsAuthenticatedAPIView):
    def post(self, request):
        form = TGFBIManageForm(request.POST, request.FILES)
        if form.is_valid():
            project = TGFBISampleProject.objects.get(id=form.cleaned_data['project_id'])
            project.progress = form.cleaned_data['progress'] or project.progress
            project.save()
            return Response(Success(chinese_msg='更新数据成功'))
        else:
            return Response(ParameterError(msg='form not valid', msg_detail=str(form.errors)))


class TGFBIProjectUploadReportFileAPIView(ProjectUploadReportFileAPIView):
    project_class = TGFBISampleProject

    def after_post(self, project: project_class):
        project.progress = 6
        project.save()


class TGFBIProjectsExportAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = TGFBISampleProject.objects.filter(name='TGFBI角膜营养不良基因检测采样').prefetch_related('sequence')
        rows = [{
            'id': project.id,
            'serial_number': project.sequence.serial_number,
            'name': project.remarks_json.get('name', None),
            'gender': project.remarks_json.get('gender', None),
            'age': project.remarks_json.get('age', None),
            'birthday': project.remarks_json.get('birthday', None),
            'contact_phone_number': project.remarks_json.get('contact_phone_number', None),
            'bind_time': project.remarks_json.get('bind_time', None),
            'send_time': project.remarks_json.get('courier', {}).get('send_time', None),
            'express': project.remarks_json.get('courier', {}).get('waybillNoInfoList', [{}])[0].get('waybillNo', None),
            'order_code': project.remarks_json.get('lims_full_info', {}).get('orderCode', None),
            'progress': project.get_progress_display(),
            'report_file_name': f'{project.report_file_url} or {project.report_file_path}',
            'created_time': project.created_time.strftime('%Y-%m-%d')
        } for project in projects]
        df = pd.DataFrame(rows)
        return xlsx_response(df)
