# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/5/6 9:05
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

from django.urls import reverse

from Common.models.project import Project
from Common.utils.alibabacloud.oss.url import generate_image_url, generate_file_url
from Common.utils.http.exceptions import NotFound
from Common.utils.http.url import params_dict_to_url_query_string
from Common.utils.text_handler.hash import encrypt_dict_to_text
from Common.viewModels.project import generate_report_data_from_project


def search_projects(
        identification_card_number: str,
        name: str = None,
        user_role: dict = None,
        project_id: int = None,
        project_name: str = None,
        finished_time=None,
):
    projects = Project.objects.filter(
        user__identification_card_number__endswith=identification_card_number,
    )
    if not projects.exists():
        raise NotFound(msg='no this person', chinese_msg='没有找到该用户，身份证号错误')
    if user_role:
        if user_role['role_name'] == 'student':
            projects = projects.filter(
                user__student_role__student_number=user_role['student_number']).prefetch_related(
                'user__student_role')
        elif user_role['role_name'] == 'teacher':
            projects = projects.filter(
                user__teacher_role__teacher_number=user_role['teacher_number']).prefetch_related(
                'user__teacher_role')
    if not projects.exists():
        raise NotFound(msg='user role error ', chinese_msg='用户身份信息错误')
    if name:
        projects = projects.filter(user__name=name)
    if not projects.exists():
        raise NotFound(msg='user name error ', chinese_msg='用户名称错误')
    if project_id:
        projects = projects.filter(id=project_id)
    if project_name:
        projects = projects.filter(name=project_name)
    if finished_time:
        projects = projects.filter(finished_time__gt=finished_time)
    if not projects.exists():
        raise NotFound(msg='project info error', chinese_msg='无相关数据')
    return projects.select_related('user', 'visual_chart', 'tono_meter', 'bio_meter', 'optometry')


def generate_user_report_data(
        identification_card_number: str,
        name: str = None,
        user_role: dict = None,
        project_id: int = None,
        project_name: str = None,
        finished_time=None):
    print('a')
    projects = search_projects(identification_card_number, name, user_role, project_id, project_name, finished_time)
    project = projects.first()
    print(project)
    if not project:
        raise NotFound(msg='no this project', chinese_msg='没有找到该项目')
    if not project.has_informed_consent or (
            not project.informed_consent.file_path and not project.informed_consent.file_url):
        return {'project_id': project.id}
    if not project.report_file_url:
        report_file_url = f"{reverse('Screening:api:mina:get_user_report_pdf_file')}?" \
                          f"{params_dict_to_url_query_string({'user_info_json': encrypt_dict_to_text({'name': name, 'identification_card_number': identification_card_number, 'user_role': user_role, }), 'project_id': project.id, })}"
    else:
        report_file_url = generate_file_url(project.report_file_url, project.report_file_path)
    project.remarks_json['report_file_full'] = False
    project.save()
    return {
        **generate_report_data_from_project(project),
        # 使用文件而不是图片是因为可能以后使用PDF存储
        'informed_consent_file_url': generate_image_url(
            project.informed_consent.file_url,
            project.informed_consent.file_path),
        'report_file_url': report_file_url,
        'popup': project.remarks_json.get('popup', {}),
    }
