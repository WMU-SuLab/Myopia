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
from datetime import datetime

from django.conf import settings
from django.http.response import FileResponse
from django.template.loader import render_to_string
from pydantic import BaseModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weasyprint import HTML

from Common.utils.email_handler.report import handle_lack_student_report_data
from Common.utils.http.successes import Success
from UserService.utils.report import generate_student_report_data, generate_report_data


class UserReportSearch(BaseModel):
    name: str
    identification_card_number: str
    user_role: dict = None
    project_name: str = None
    finished_time: datetime = None


class StudentRole(BaseModel):
    name: str
    student_number: str


# todo:后续换成标准化的方式
class StudentReportSearch(BaseModel):
    name: str
    identification_card_number: str
    student_number: str
    project_name: str = None
    finished_time: datetime = None


class TeacherRole(BaseModel):
    name: str
    teacher_number: str


class TeacherReportSearch(UserReportSearch):
    user_role: TeacherRole


@api_view(['POST'])
def get_student_report_data(request):
    data = request.json
    student_info = StudentReportSearch(**data)
    return Response(Success(data=generate_report_data(
        name=student_info.name,
        identification_card_number=student_info.identification_card_number,
        user_role={
            'name': 'student',
            'student_number': student_info.student_number
        })))


@api_view(['POST'])
def lack_student_report_data(request):
    data = request.json
    return Response(handle_lack_student_report_data(data))


@api_view(['POST'])
def get_teacher_report_data(request):
    data = request.json
    teacher_info = TeacherReportSearch(**data)
    return Response(Success(data=generate_report_data(**teacher_info.dict())))


# todo：目前先动态生成，后续改为对象存储的静态文件
@api_view(['GET'])
def get_student_report_pdf_file(request):
    """

    :param request:
    :return:
    """
    data = request.GET.dict()
    student_info = StudentReportSearch(**data)

    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
    file_name = 'student-' + data['student_number'] + '-report.pdf'
    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    report_str = render_to_string(
        template_name='UserService/report/single.html',
        context={'user': generate_student_report_data(**student_info.dict())}
    )
    HTML(string=report_str).write_pdf(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


@api_view(['POST'])
def get_teacher_report_pdf_file(request):
    """
    目前先动态生成，后续改为对象存储的静态文件
    :param request:
    :return:
    """
    data = request.GET.dict()
    teacher_info = TeacherReportSearch(**data)

    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
    file_name = 'teacher-' + data['teacher_number'] + '-report.pdf'
    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    report_str = render_to_string(
        template_name='UserService/report/single.html',
        context={'user': generate_report_data(**teacher_info.dict())}
    )
    HTML(string=report_str).write_pdf(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
