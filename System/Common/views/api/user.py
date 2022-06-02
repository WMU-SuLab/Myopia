# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/31 17:35
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

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from Common.models.user import User
from Common.utils.forms.user import PhoneUserForm
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import UserRegisterSuccess, UserPasswordUpdateSuccess


@api_view(['POST'])
@authentication_classes([])
def register(request):
    phone_user_form = PhoneUserForm(request.POST)
    if phone_user_form.is_valid():
        User.objects.create_user(
            username=phone_user_form.cleaned_data['phone'],
            password=phone_user_form.cleaned_data['password'],
            phone=phone_user_form.cleaned_data['phone'])
        return Response(UserRegisterSuccess())
    else:
        return Response(ParameterError(msg_detail=str(phone_user_form.errors)))


@api_view(['POST'])
def reset_password():
    # todo:
    return Response(UserPasswordUpdateSuccess())
