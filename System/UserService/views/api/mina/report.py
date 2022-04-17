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

from Common.utils.email_handler.report import handle_lack_student_report_data
from Common.utils.http.successes import Success
from UserService.utils.report import generate_student_report_data, generate_teacher_report_data


@api_view(['POST'])
def get_student_report_data(request):
    data = request.json
    return Response(Success(data=generate_student_report_data(
        data['name'],
        data['identification_card_number'],
        data['student_number']
    )))


@api_view(['POST'])
def lack_student_report_data(request):
    data = request.json
    return Response(handle_lack_student_report_data(data))


@api_view(['POST'])
def get_teacher_report_data(request):
    data = request.json
    return Response(Success(data=generate_teacher_report_data(
        data['name'],
        data['identification_card_number'],
        data['teacher_number']
    )))


# todo：目前先动态生成，后续改为对象存储的静态文件
@api_view(['GET'])
def get_student_report_pdf_file(request):
    """

    :param request:
    :return:
    """
    data = request.GET

    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_name = 'student-' + data['student_number'] + '-report.pdf'
    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    report_str = render_to_string(
        template_name='UserService/report/single.html',
        context={
            'student': generate_student_report_data(
                data['name'],
                data['identification_card_number'],
                data['student_number']
            )})
    HTML(string=report_str).write_pdf(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)

@api_view(['POST'])
def get_teacher_report_pdf_file(request):
    """
    目前先动态生成，后续改为对象存储的静态文件
    :param request:
    :return:
    """
    data = request.GET

    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_name = 'teacher-' + data['teacher_number'] + '-report.pdf'
    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    report_str = render_to_string(
        template_name='UserService/report/single.html',
        context=generate_teacher_report_data(
            data['name'],
            data['identification_card_number'],
            data['teacher_number']
        ))
    HTML(string=report_str).write_pdf(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
