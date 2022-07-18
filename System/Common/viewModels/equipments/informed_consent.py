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
from django.core.files.uploadedfile import UploadedFile
from rest_framework.response import Response

from Common.models.equipments import InformedConsent
from Common.models.project import Project
from Common.utils.alibabacloud.oss.obj import generate_obj_file_path, upload_obj, delete_obj
from Common.utils.file_handler import handle_upload_file, remove_file
from Common.utils.file_handler.image_handler import is_image_file
from Common.utils.http.exceptions import ParameterError, NotFound, Conflict
from Common.utils.http.successes import Success


def generate_project_informed_consent_file_name(informed_consent, file_type: str = 'jpg') -> str:
    """
    生成项目提供的informed consent文件名
    :param informed_consent:
    :param file_type:
    :return:
    """
    return f'{informed_consent.project.user.username}-{informed_consent.project_id}-{informed_consent.id}.{file_type}'


def handle_upload_informed_consent(project: Project, informed_consent_file: UploadedFile):
    informed_consent, informed_consent_created = InformedConsent.objects.get_or_create(project=project)
    raw_file_url = informed_consent.file_url
    raw_file_path = informed_consent.file_path
    # 上传本地
    file_name = generate_project_informed_consent_file_name(
        informed_consent=informed_consent, file_type=informed_consent_file.name.split('.')[-1])
    file_path = os.path.join(settings.INFORMED_CONSENT_DIR_PATH, file_name)
    # 必须先上传再判断
    handle_upload_file(informed_consent_file, file_path)
    if not is_image_file(file_path):
        return Response(ParameterError(chinese_msg='上传的不是图片文件'))
    informed_consent.file_path = file_path
    # 上传oss
    file_obj_name = os.path.join(settings.RELATIVE_INFORMED_CONSENT_DIR_PATH, file_name)
    upload_obj(file_obj_name, file_path)
    informed_consent.file_url = generate_obj_file_path(file_obj_name)
    # 删除旧文件
    if raw_file_url and raw_file_url != file_obj_name:
        delete_obj(raw_file_url)
    if raw_file_path and raw_file_path != file_path and os.path.exists(raw_file_path):
        remove_file(raw_file_path)
    informed_consent.full_clean(exclude=['file_url'], validate_unique=True)
    informed_consent.save()
    if informed_consent_created:
        return Response(data=Success(msg='update success', chinese_msg='更新成功'))
    else:
        return Response(data=Success(msg='upload success', chinese_msg='上传成功'))


def handle_upload_informed_consent_request(request, *args, **kwargs):
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
    if request.method == 'POST' and project.has_informed_consent and project.informed_consent.has_file:
        raise Conflict(msg='informed consent already exists', chinese_msg='已经存在知情同意书文件，请使用其他请求方法')
    if request.method == 'PATCH' and (not project.has_informed_consent or not project.informed_consent.has_file):
        raise NotFound(msg='informed consent not found', chinese_msg='知情同意书文件不存在，无法更新')

    return handle_upload_informed_consent(project=project, informed_consent_file=informed_consent_file)
