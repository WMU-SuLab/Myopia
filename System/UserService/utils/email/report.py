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

from UserService.utils.schemes.role import StudentRole, TeacherRole
from Common.utils.email import mail_managers


class StudentFeedback(BaseModel):
    name: str
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    phone: str = '无'
    email: str = '无'
    feedback: str = '无'


# todo:是否需要把反馈写入数据库？
def handle_user_feedback(data: dict):
    feedback_info = StudentFeedback(**data)
    message = f"""用户反馈信息如下：
        姓名:{feedback_info.name}
        身份证号后四位:{feedback_info.identification_card_number}
        身份:{str(feedback_info.user_role)}
        手机号:{feedback_info.phone}
        邮箱:{feedback_info.email}
        留言:{feedback_info.feedback}
    """
    return mail_managers('用户反馈', message, fail_silently=False)
