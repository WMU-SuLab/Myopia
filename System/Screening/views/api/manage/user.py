# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/25 14:56
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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.views import Response

from Common.models.user import User
from Common.utils.http.exceptions import AuthenticationFailed, PermissionDenied, ParameterError
from Screening.views.manage.index import redirect_field_name


@api_view(['POST'])
def user_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    next_url = request.POST.get(redirect_field_name, 'Screening:manage:index')
    if not username or not password:
        return Response(ParameterError())
    user: User = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active and user.is_manager:
            login(request, user)
            return redirect(next_url)
        else:
            return Response(PermissionDenied())
    else:
        return Response(AuthenticationFailed(message='用户名或密码错误'))


def user_logout(request):
    logout(request)
    return redirect('Screening:manage:login')
