# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/9 19:32
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

from Common.utils.http.successes import EmailSendSuccess
from UserService.viewModels.feedback import handle_user_feedback


@api_view(['POST'])
def user_feedback(request):
    data = request.json
    return Response(EmailSendSuccess(handle_user_feedback(data)))


def register(request):
    """
    注册
    :param request:
    :return:
    """
    pass
