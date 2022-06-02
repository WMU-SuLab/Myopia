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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weasyprint import HTML

from Common.models.project import Project
from Common.utils.http.exceptions import NotFound
from Common.utils.http.successes import Success
from Common.utils.text_handler.hash import decrypt_text_to_dict
from Common.viewModels.project import generate_project_report_filename
from UserService.utils.schemes.report import UserReportSearchForm
from UserService.viewModels.project import generate_user_report_data


@api_view(['POST'])
def get_user_report_data(request):
    data = request.json
    user_info = UserReportSearchForm(**data)
    return Response(Success(data=generate_user_report_data(**user_info.dict())))


@api_view(['GET'])
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
        dir_path = settings.PDF_DATA_DIR_PATH
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
