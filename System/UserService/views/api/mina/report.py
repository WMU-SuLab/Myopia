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

from django.conf import settings
from django.http.response import FileResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from weasyprint import HTML

from Common.models.equipments import InformedConsent
from Common.models.project import Project
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.file_handler import handle_uploaded_file
from Common.utils.http.exceptions import InsufficientPreconditions, ParameterError, NotFound, ServerError, Conflict
from Common.utils.http.successes import Success
from Common.utils.text_handler.boolean import strtobool
from Common.utils.text_handler.hash import decrypt_text_to_dict
from Common.viewModels.equipments import generate_project_informed_consent_file_name
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
        return Response(Success(data= [{
            'project_id':project.id,
            'project_name':project.name,
            'project_finished_time':project.finished_time,
        } for project in projects]))


@api_view(['GET'])
@authentication_classes([])
def get_user_report_data(request):
    data = request.data
    user_info = UserReportSearchForm(**data)
    report_data = generate_user_report_data(**user_info.dict())
    if not report_data.get('report_file_url', None):
        return Response(InsufficientPreconditions(data=report_data, msg='no informed consent', chinese_msg='没有填写知情同意书'))
    return Response(Success(data=report_data))


class UploadInformedConsent(AllowAnyAPIView):
    def post(self, request):
        print(request.POST)
        project_id = request.POST.get('project_id', None)
        if not project_id:
            raise ParameterError(msg='project_id is required', chinese_msg='请上传项目id')
        project = Project.objects.filter(id=project_id).first()
        if not project:
            raise NotFound(msg='project not found', chinese_msg='项目不存在')
        if not request.FILES:
            raise ParameterError(msg='please upload informed consent file', chinese_msg='请上传知情同意书文件')
        informed_consent_file = request.FILES.get('informed_consent_file', None)
        if not informed_consent_file:
            raise ParameterError(msg='please use right field to upload', chinese_msg='请使用正确的字段上传文件')
        print(type(strtobool(request.POST.get('cover', None))))
        if project.has_informed_consent and not strtobool(request.POST.get('cover', None)):
            raise Conflict(msg='informed consent already exists', chinese_msg='已经存在知情同意书文件')

        informed_consent, informed_consent_created = InformedConsent.objects.get_or_create(project=project)
        file_name = generate_project_informed_consent_file_name(informed_consent=informed_consent)
        file_path = os.path.join(settings.INFORMED_CONSENT_DATA_DIR_PATH, file_name)
        if handle_uploaded_file(informed_consent_file, file_path):
            informed_consent.file_path = file_path
            informed_consent.save()
            return Response(data=Success(msg='upload success', chinese_msg='上传成功'))
        else:
            return Response(data=ServerError(msg='upload failed', chinese_msg='上传失败'))


@api_view(['GET'])
@authentication_classes([])
def get_user_report_pdf_file(request):
    data = request.GET.dict()
    project_id = data.get('project_id', None)
    if not Project.objects.filter(id=project_id).exists():
        return Response(NotFound(msg='project not exist', chinese_msg='项目不存在'))
    project = Project.objects.get(id=project_id)
    if not project.report_file_path:
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
    else:
        return FileResponse(open(project.report_file_path, 'rb'), as_attachment=True,
                            filename=project.report_file_path.split('/')[-1])
