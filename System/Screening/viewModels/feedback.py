# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py    
@Create Time    :   2022/4/22 16:54
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
from Screening.utils.email.feedback import mail_managers_user_report_feedback
from Screening.utils.schemes.feedback import UserReportFeedbackModel


def handle_user_report_feedback(data: dict):
    user_feedback = UserReportFeedbackModel(**data)
    Feedback.objects.create(
        phone=user_feedback.phone,
        email=user_feedback.email,
        content=user_feedback.feedback_content,
        user_info={
            'name': user_feedback.name,
            'identification_card_number': user_feedback.identification_card_number,
            'user_role': str(user_feedback.user_role)
        })
    mail_managers_user_report_feedback(user_feedback)
