# -*- encoding: utf-8 -*-
"""
@File Name      :   informed_consent.py    
@Create Time    :   2022/6/21 16:01
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
from rest_framework.response import Response

from Common.models.equipments import InformedConsent
from Common.models.project import Project
from Common.utils.file_handler import handle_uploaded_file, remove_file
from Common.utils.http.exceptions import ParameterError, NotFound, ServerError, Conflict, MethodNotAllowed
from Common.utils.http.successes import Success
from Common.utils.text_handler.boolean import strtobool


def generate_project_informed_consent_file_name(informed_consent, file_type: str = 'jpg') -> str:
    """
    生成项目提供的informed consent文件名
    :param informed_consent:
    :param file_type:
    :return:
    """
    return f'{informed_consent.project.user.username}-{informed_consent.project_id}-{informed_consent.id}.{file_type}'


def handle_upload_informed_consent(request, *args, **kwargs):
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
    if request.method == 'POST' and project.has_informed_consent:
        raise Conflict(msg='informed consent already exists', chinese_msg='已经存在知情同意书文件')
    if request.method == 'PATCH' and (not project.has_informed_consent or not project.informed_consent.file_path):
        raise NotFound(msg='informed consent not found', chinese_msg='知情同意书文件不存在，无法更新')


    informed_consent, informed_consent_created = InformedConsent.objects.get_or_create(project=project)
    file_name = generate_project_informed_consent_file_name(informed_consent=informed_consent)
    file_path = os.path.join(settings.INFORMED_CONSENT_DATA_DIR_PATH, file_name)
    if handle_uploaded_file(informed_consent_file, file_path):
        if informed_consent.file_path:
            remove_file(informed_consent.file_path)
        informed_consent.file_path = file_path
        informed_consent.save()
        if informed_consent_created:
            return Response(data=Success(msg='update success', chinese_msg='更新成功'))
        else:
            return Response(data=Success(msg='upload success', chinese_msg='上传成功'))
    else:
        return Response(data=ServerError(msg='upload failed', chinese_msg='上传失败'))
