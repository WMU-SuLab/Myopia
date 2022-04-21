# -*- encoding: utf-8 -*-
"""
@File Name      :   report.py    
@Create Time    :   2022/4/8 19:19
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

from Common.models.project import Project
from Common.utils.http.exceptions import NotFound
from Common.viewModels.project import generate_report_data_from_project


def student_pdf_file_name(name: str) -> str:
    return 'student-' + name + '-report.pdf'


def teacher_pdf_file_name(name: str) -> str:
    return 'teacher-' + name + '-report.pdf'


def generate_report_data(name: str, identification_card_number: str, user_role: dict = None, project_name: str = None,
                         finished_time=None):
    project = Project.objects.filter(user__name=name)
    if project.exists():
        project = project.filter(
            user__identification_card_number__endswith=identification_card_number,
        ).select_related('user', 'visual_chart', 'tono_meter', 'bio_meter', 'refractometer')
        if not project:
            raise NotFound(msg='error identification_card_number or number', chinese_msg='身份证号错误')
        if project_name:
            project = project.filter(name=project_name)
        if finished_time:
            project = project.filter(finished_time__gt=finished_time)
        if user_role:
            if user_role['name'] == 'student':
                project = project.filter(user__student_role__student_number=user_role['student_number']).prefetch_related(
                    'user__student_role').first()
            elif user_role['name'] == 'teacher':
                project = project.filter(user__teacher_role__teacher_number=user_role['teacher_number']).prefetch_related(
                    'user__teacher_role').first()
            else:
                project = project.first()
        if project:
            return generate_report_data_from_project(project)
        else:
            raise NotFound(msg='identification info error', chinese_msg='身份信息错误')
    else:
        raise NotFound(msg='no this person', chinese_msg='没有找到该用户')


def generate_student_report_data(name, identification_card_number, student_number):
    project = Project.objects.filter(user__name=name)
    if project.exists():
        project = project.filter(
            user__identification_card_number__endswith=identification_card_number,
            user__student_role__student_number=student_number
        ).select_related('user', 'user__student_role', 'visual_chart', 'tono_meter', 'bio_meter',
                           'refractometer', ).first()
        if project:
            return generate_report_data_from_project(project)
        else:
            raise NotFound(
                msg='error identification_card_number or student_number',
                chinese_msg='身份证号或学号错误'
            )
    else:
        raise NotFound(msg='no this student', chinese_msg='没有找到该学生')
