# -*- encoding: utf-8 -*-
"""
@File Name      :   report.py    
@Create Time    :   2022/4/15 11:39
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

from typing import Union

from pydantic import BaseModel

from Common.utils.email import mail_managers
from UserService.models.user import Feedback
from UserService.utils.schemes.role import StudentRole, TeacherRole


class UserFeedback(BaseModel):
    name: str
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    phone: str = '无'
    email: str = '无'
    feedback_content: str = '无'


def handle_user_feedback(data: dict):
    user_feedback = UserFeedback(**data)
    Feedback.objects.create(
        phone=user_feedback.phone,
        email=user_feedback.email,
        content=user_feedback.feedback_content,
        user_info={
            'name': user_feedback.name,
            'identification_card_number': user_feedback.identification_card_number,
            'user_role': str(user_feedback.user_role)
        })
    email_message = f"""用户反馈信息如下：
        姓名:{user_feedback.name}
        身份证号后四位:{user_feedback.identification_card_number}
        身份:{str(user_feedback.user_role)}
        手机号:{user_feedback.phone}
        邮箱:{user_feedback.email}
        留言:{user_feedback.feedback_content}
    """
    return mail_managers('用户反馈', email_message, fail_silently=False)
