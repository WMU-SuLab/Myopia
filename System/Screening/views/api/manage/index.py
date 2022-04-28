# -*- encoding: utf-8 -*-
"""
@File Name      :   index.py    
@Create Time    :   2022/4/27 15:29
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

from rest_framework.decorators import api_view
from rest_framework.views import Response

from Common.utils.http.successes import Success
from Screening.libs.menus import init_json
from Screening.views.manage.index import screening_manage_login_required


@screening_manage_login_required
@api_view(['GET'])
def init(request):
    return Response(data=init_json, status=200)


@screening_manage_login_required
@api_view(['GET'])
def clear(request):
    return Response(Success(msg='清除成功'))
