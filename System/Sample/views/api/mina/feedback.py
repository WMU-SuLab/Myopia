# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py
@Create Time    :   2022/11/11 21:28
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
from Common.utils.http.successes import EmailSendSuccess
from Common.utils.http.successes import Success
from Sample.viewModels.feedback import handle_user_feedback


class UserFeedbackToAPIView(AllowAnyAPIView):
    """
    获取反馈需要的信息
    """

    def get(self, request, *args, **kwargs):
        return Response(Success(data={
            'tel': '021-52188588',
            'email': 'dzl@psi-gene.com',
            'mobile': '',
            'msg': '',
        }))


class UserFeedbackToEmailAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(EmailSendSuccess(handle_user_feedback(data)))
