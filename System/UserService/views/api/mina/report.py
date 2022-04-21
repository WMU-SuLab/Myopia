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
from typing import Union

from django.conf import settings
from django.http.response import FileResponse
from django.template.loader import render_to_string
from pydantic import BaseModel, validator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weasyprint import HTML

from Common.utils.http.successes import Success
from UserService.utils.schemes.role import StudentRole, TeacherRole
from UserService.viewModels.report import generate_user_report_data


class UserReportSearchForm(BaseModel):
    name: str
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    project_name: str = None
    finished_time: datetime = None

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 20:
            raise ValueError('姓名长度不能超过20个字符')
        return v

    @validator('identification_card_number')
    def validate_identification_card_number(cls, v):
        if len(v) != 4:
            raise ValueError('只需要输入身份证号后4位')
        return v


@api_view(['POST'])
def get_user_report_data(request):
    data = request.json
    user_info = UserReportSearchForm(**data)
    return Response(Success(data=generate_user_report_data(**user_info.dict())))


# todo：目前先动态生成，后续改为对象存储的静态文件
@api_view(['GET'])
def get_user_report_pdf_file(request):
    data = request.GET.dict()
    user_info = UserReportSearchForm(**data)

    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
    file_name = str(user_info.user_role) + '-report.pdf'
    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    report_str = render_to_string(
        template_name='UserService/report/single.html',
        context={'user': generate_user_report_data(**user_info.dict())}
    )
    HTML(string=report_str).write_pdf(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
