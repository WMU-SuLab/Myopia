# -*- encoding: utf-8 -*-
"""
@File Name      :   report.py    
@Create Time    :   2022/4/8 16:27
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
from django.shortcuts import redirect
from django.conf import settings
from django.http.response import FileResponse
from django.template.loader import render_to_string
from django.utils.timezone import localtime, get_current_timezone_name
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from weasyprint import HTML

from Common.models.project import Project
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.exceptions import InsufficientPreconditions, NotFound
from Common.utils.http.successes import Success
from Common.utils.text_handler.hash import decrypt_text_to_dict
from Common.viewModels.equipments.informed_consent import handle_upload_informed_consent
from Common.viewModels.project import generate_project_report_filename
from UserService.utils.schemes.report import UserReportSearchForm
from UserService.viewModels.project import search_projects, generate_user_report_data


class ReportProjectsAPIView(AllowAnyAPIView):
    def get(self, request, *args, **kwargs):
        """
        获取用户可以查看的项目列表
        """
        data = request.data
        user_info = UserReportSearchForm(**data)
        projects = search_projects(**user_info.dict())
        return Response(Success(data=[{
            'project_id': project.id,
            'name': project.name,
            'finished_time': localtime(project.finished_time).strftime('%Y-%m-%d %H:%M:%S'),
            'tzname': get_current_timezone_name(),
            'finished_time_timestamp': project.finished_time.timestamp(),
            'informed_consent': project.has_informed_consent,
            'report_file_full': project.remarks_json.get('report_file_full', False),
        } for project in projects]))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@authentication_classes([])
def get_user_report_data(request):
    data = request.data
    user_info = UserReportSearchForm(**data)
    report_data = generate_user_report_data(**user_info.dict())
    if not report_data.get('report_file_url', None):
        return Response(InsufficientPreconditions(data=report_data, msg='no informed consent', chinese_msg='没有填写知情同意书'))
    return Response(Success(data=report_data))


class UploadInformedConsentAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        return handle_upload_informed_consent(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return handle_upload_informed_consent(request, *args, **kwargs)


@api_view(['GET'])
@authentication_classes([])
def get_user_report_pdf_file(request):
    data = request.GET.dict()
    project_id = data.get('project_id', None)
    if not Project.objects.filter(id=project_id).exists():
        return Response(NotFound(msg='project not exist', chinese_msg='项目不存在'))
    project = Project.objects.get(id=project_id)
    if project.report_file_url:
        return redirect(project.report_file_url)
    elif project.report_file_path and os.path.exists(project.report_file_path):
        return FileResponse(open(project.report_file_path, 'rb'), as_attachment=True,
                            filename=project.report_file_path.split('/')[-1])
    else:
        user_info_json = decrypt_text_to_dict(data['user_info_json'])
        user_info = UserReportSearchForm(**user_info_json)
        # 创建文件
        dir_path = settings.USER_PDF_DATA_DIR_PATH
        file_name = generate_project_report_filename(project)
        file_path = os.path.join(dir_path, file_name)
        if not os.path.exists(file_path):
            report_str = render_to_string(
                template_name='UserService/report/single.html',
                context={'user': generate_user_report_data(**user_info.dict())}
            )
            HTML(string=report_str).write_pdf(file_path)
            project.report_file_path = file_path
            project.save()
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)