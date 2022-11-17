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
from io import BytesIO

import pandas as pd
from django.db.models import F
from django.http import HttpResponse
from rest_framework.response import Response

from Sample.models.project import HighMyopiaSampleProject
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import Success, FileUploadSuccess
from Common.viewModels.project import handle_upload_project_report
from Sample.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView
from Sample.utils.forms.high_myopia import HighMyopiaManageForm


class HighMyopiaProjectsAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = HighMyopiaSampleProject.objects.filter(name='高度近视遗传风险评估采样')
        # 过滤
        if serial_number := request.GET.get('serial_number', ''):
            projects = projects.filter(sequence__serial_number__contains=serial_number)
        if name := request.GET.get('name', ''):
            projects = projects.annotate(remarks_json_name=F('remarks_json__name')).filter(
                remarks_json_name__icontains=name)
        if phone_number := request.GET.get('phone_number', ''):
            projects = projects.filter(user__phone_number__icontains=phone_number)
        count = projects.count()
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        projects = projects.order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        projects = projects.prefetch_related('user', 'sequence')
        rows = [{
            'id': project.id,
            'phone_number': project.user.phone_number,
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


class HighMyopiaProjectUpdateAPIView(SampleManagerIsAuthenticatedAPIView):
    def post(self, request):
        form = HighMyopiaManageForm(request.POST, request.FILES)
        if form.is_valid():
            project = HighMyopiaSampleProject.objects.get(id=form.cleaned_data['project_id'])
            project.progress = form.cleaned_data['progress'] or project.progress
            project.save()
            return Response(Success(chinese_msg='更新数据成功'))
        else:
            return Response(ParameterError(msg='form not valid', msg_detail=str(form.errors)))


class HighMyopiaProjectUploadReportFileAPIView(SampleManagerIsAuthenticatedAPIView):
    def post(self, request, project_id):
        project_id = request.POST.get('project_id', project_id)
        if not project_id:
            return Response(ParameterError(chinese_msg='项目id不能为空'))
        report_file = request.FILES.get('file', None)
        if not report_file:
            return Response(ParameterError(chinese_msg='上传文件为空'))
        project = HighMyopiaSampleProject.objects.get(id=project_id)
        handle_upload_project_report(project, report_file)
        return Response(FileUploadSuccess(chinese_msg='上传文件成功'))


class HighMyopiaProjectsExportAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = HighMyopiaSampleProject.objects.filter(name='高度近视遗传风险评估采样').prefetch_related('user', 'sequence')
        rows = [{
            'id': project.id,
            'phone_number': project.user.phone_number,
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
            'created_time': project.created_time.strftime('%Y-%m-%d')
        } for project in projects]
        df = pd.DataFrame(rows)
        file = BytesIO()
        # By setting the 'engine' in the ExcelWriter constructor.
        writer = pd.ExcelWriter(file, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # Save the workbook
        writer.save()
        # Seek to the beginning and read to copy the workbook to a variable in memory
        file.seek(0)
        response = HttpResponse(
            file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment;filename=all_data.xlsx'
        # response['Content-Disposition'] = 'inline;filename=文件名.txt'
        return response
