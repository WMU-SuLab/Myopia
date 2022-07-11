# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2022/4/24 10:10
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

from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Common.utils.http.successes import Success


@extend_schema(
    description='测试接口',
    parameters=[
        OpenApiParameter(name='test', description='Not required', required=False, type=str),
    ],
    examples=[
        OpenApiExample(name='test', value=[{'test': 'test'}]),
        OpenApiExample(name='test2', value=[{'test2': 'test2'}]),
    ],
    responses={
        200: inline_serializer(name='success', fields={'code': serializers.IntegerField()}),
    }
)
@api_view(['GET', 'HEAD', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
@permission_classes([AllowAny])
@authentication_classes([])
def test(request):
    return Response(Success(data={
        'headers': request.headers,
        'query': request.GET.dict(),
        'method': request.method,
        'cookies': request.COOKIES,
        'encoding': request.encoding,
        'form_data': request.POST.dict(),
        'json': request.data,
        'env': settings.DJANGO_ENV,
    }, msg='test success'))
