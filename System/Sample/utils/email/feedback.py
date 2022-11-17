# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py
@Create Time    :   2022/11/11 21:09
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

from Common.utils.email import server_send_mail
from Sample.utils.schemes.feedback import UserFeedbackModel


def mail_managers_user_feedback(user_feedback: UserFeedbackModel):
    email_message = f"""用户反馈信息如下：
        姓名:{user_feedback.name}
        微信号:{user_feedback.wechat_id}
        手机号:{user_feedback.phone}
        邮箱:{user_feedback.email}
        留言:{user_feedback.feedback_content}
    """
    return server_send_mail('用户反馈', email_message, ['dzl@psi-gene.com'], fail_silently=False)
