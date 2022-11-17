# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py
@Create Time    :   2022/11/12 20:41
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

from Common.models.sundry import Feedback
from Sample.utils.email.feedback import mail_managers_user_feedback
from Sample.utils.schemes.feedback import UserFeedbackModel


def handle_user_feedback(data: dict):
    user_feedback = UserFeedbackModel(**data)
    Feedback.objects.create(
        phone=user_feedback.phone,
        email=user_feedback.email,
        content=user_feedback.feedback_content,
        user_info={
            'name': user_feedback.name,
            'wechat_id': user_feedback.wechat_id,
        })
    mail_managers_user_feedback(user_feedback)
