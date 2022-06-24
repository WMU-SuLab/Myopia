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

from rest_framework.response import Response

from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.successes import Success, EmailSendSuccess
from UserService.viewModels.feedback import handle_user_feedback


class UserFeedbackToAPIView(AllowAnyAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Success(data={
            'phone': '15996335768',
            'email': '1061995104@qq.com'
        }))


class UserFeedbackToEmailAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(EmailSendSuccess(handle_user_feedback(data)))
