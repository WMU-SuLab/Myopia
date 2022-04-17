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

from . import mail_managers

# todo:是否需要把反馈写入数据库？
def handle_lack_student_report_data(data: dict):
    message = f"""学生信息如下：
        姓名:{data.get('name', '无')}
        学号:{data.get('student_number', '无')}
        身份证号:{data.get('identification_card_number', '无')}
        手机号:{data.get('phone', '无')}
        邮箱:{data.get('email', '无')}
        留言:{data.get('message', '无')}
    """
    return mail_managers('学生报告信息缺少反馈', message, fail_silently=False)
