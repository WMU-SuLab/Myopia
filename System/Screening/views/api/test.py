# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2022/4/7 19:49
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
from rest_framework.response import Response

from Common.utils.http.successes import Success


@api_view(['GET', 'POST'])
def test(request):
    return Response(Success(msg='test success'))
