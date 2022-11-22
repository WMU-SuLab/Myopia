# -*- encoding: utf-8 -*-
"""
@File Name      :   high_myopia.py
@Create Time    :   2022/11/11 21:13
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
from django.db.models import F
from rest_framework.response import Response

from Common.utils.http.exceptions import ParameterError
from Common.utils.http.responses.xlsx import xlsx_response
from Common.utils.http.successes import Success
from Common.utils.pagination import array_range
from Sample.models.project import HighMyopiaSampleProject
from Sample.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView
from Sample.utils.auth.views.project import ProjectUploadReportFileAPIView
from Sample.utils.forms.high_myopia import HighMyopiaManageForm


class HighMyopiaProjectsAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = HighMyopiaSampleProject.objects.filter(name='高度近视遗传风险评估采样')
        # 过滤
        if serial_number := request.GET.get('serial_number', ''):
            projects = projects.filter(sequence__serial_number__contains=serial_number)
        if name := request.GET.get('name', ''):
            projects = projects.filter(remarks_json__name__icontains=name)
        if contact_phone := request.GET.get('contact_phone', ''):
            projects = projects.filter(remarks_json__contact_phone__icontains=contact_phone)
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
            'native_place': project.remarks_json.get('native_place', None),
            'contact_phone': project.remarks_json.get('contact_phone', ''),
            'nationality': project.remarks_json.get('nationality', None),
            'education': project.remarks_json.get('education', None),
            'progress': project.get_progress_display(),
            'wear_glasses_first_time': project.remarks_json.get('wear_glasses_first_time', None),
            'optometry_left': project.remarks_json.get('optometry_left', None),
            'optometry_right': project.remarks_json.get('optometry_right', None),
            'family_history': project.remarks_json.get('family_history', None),
            'report_file_name': os.path.basename(project.report_file_path) if project.report_file_path else '无',
            'created_time': project.created_time.strftime('%Y-%m-%d')
        } for project in projects]
        return Response(Success({'count': count, 'rows': rows}))


class HighMyopiaProjectUpdateAPIView(ProjectUploadReportFileAPIView):
    def post(self, request):
        form = HighMyopiaManageForm(request.POST, request.FILES)
        if form.is_valid():
            project = HighMyopiaSampleProject.objects.get(id=form.cleaned_data['project_id'])
            project.progress = form.cleaned_data['progress'] or project.progress
            project.save()
            return Response(Success(chinese_msg='更新数据成功'))
        else:
            return Response(ParameterError(msg='form not valid', msg_detail=str(form.errors)))


class HighMyopiaProjectUploadReportFileAPIView(ProjectUploadReportFileAPIView):
    project_class = HighMyopiaSampleProject

    def after_post(self, project: project_class):
        project.progress = 6
        project.save()


class HighMyopiaProjectsExportAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = HighMyopiaSampleProject.objects.filter(name='高度近视遗传风险评估采样').prefetch_related('sequence')
        rows = [{
            'id': project.id,
            'serial_number': project.sequence.serial_number,
            'name': project.remarks_json.get('name', None),
            'gender': project.remarks_json.get('gender', None),
            'age': project.remarks_json.get('age', None),
            'birthday': project.remarks_json.get('birthday', None),
            'native_place': project.remarks_json.get('native_place', None),
            'contact_phone': project.remarks_json.get('contact_phone', ''),
            'nationality': project.remarks_json.get('nationality', None),
            'education': project.remarks_json.get('education', None),
            'progress': project.get_progress_display(),
            'wear_glasses_first_time': project.remarks_json.get('wear_glasses_first_time', None),
            'optometry_left': project.remarks_json.get('optometry_left', None),
            'optometry_right': project.remarks_json.get('optometry_right', None),
            'family_history': project.remarks_json.get('family_history', None),
            'report_file_name': f'{project.report_file_url} or {project.report_file_path}',
            'created_time': project.created_time.strftime('%Y-%m-%d')
        } for project in projects]
        df = pd.DataFrame(rows)
        return xlsx_response(df)
