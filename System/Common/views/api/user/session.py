# -*- encoding: utf-8 -*-
"""
@File Name      :   session.py    
@Create Time    :   2022/4/24 15:45
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
from Common.utils.http.exceptions import AuthenticationFailed, NotActive, ParameterError
from Common.utils.http.successes import UserLoginSuccess


@api_view(['POST'])
def session_login(request):
    if request.json:
        data = request.json
        username = data.get('username', 'admin')
        password = data.get('password', 'admin')
    else:
        username = request.POST.get('username', 'admin')
        password = request.POST.get('password', 'admin')
    if not username or not password:
        return Response(ParameterError())
    user:User = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.is_manager:
                return redirect('Screening:manage:index')
            else:
                # 暂时没确定好普通用户重定向的路径
                return Response(UserLoginSuccess())
        else:
            return Response(NotActive())
    else:
        return Response(AuthenticationFailed(message='用户名或密码错误'))


@api_view(['GET'])
def session_logout(request):
    logout(request)
    return redirect('Screening:manage:index')
