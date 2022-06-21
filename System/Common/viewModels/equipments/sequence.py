# -*- encoding: utf-8 -*-
"""
@File Name      :   sequence.py    
@Create Time    :   2022/6/21 17:43
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

from rest_framework.response import Response

from Common.models.equipments import *
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import Success


def handle_upload_sequence(request, *args, **kwargs):
    serial_number = request.data.get('serial_number', None)
    if not serial_number:
        raise ParameterError(chinese_msg='序列号不能为空')
    sequence, created = Sequence.objects.get_or_create(project_id=request.data.get('project_id', None))
    sequence.serial_number = serial_number
    sequence.save()
    if created:
        return Response(Success(chinese_msg='更新成功'))
    else:
        return Response(Success(chinese_msg='上传成功'))
