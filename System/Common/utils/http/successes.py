# -*- encoding: utf-8 -*-
"""
@File Name      :   successes.py    
@Create Time    :   2022/4/11 9:10
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

from .response_structure import BaseHTTPJSONStructure


class Success(BaseHTTPJSONStructure):
    success = True
    code = 0
    status_code = 200
    msg = 'success'
    chinese_msg = '成功'


class EmailSendSuccess(Success):
    msg = 'email send success'
    chinese_msg = '邮件发送成功'


class PhoneSMSSendSuccess(Success):
    msg = 'phone sms send success'
    chinese_msg = '短信发送成功'


# 用户管理部分
class UserRegisterSuccess(Success):
    msg = 'user register success'
    chinese_msg = '用户注册成功'


class UserLoginSuccess(Success):
    msg = 'user login success'
    chinese_msg = '用户登录成功'


class UserLogoutSuccess(Success):
    msg = 'user logout success'
    chinese_msg = '用户退出成功'


class UserInfoUpdateSuccess(Success):
    msg = 'user update success'
    chinese_msg = '用户信息更新成功'


class UserPasswordUpdateSuccess(Success):
    msg = 'user password update success'
    chinese_msg = '用户密码更新成功'


class UserDeleteSuccess(Success):
    msg = 'user delete success'
    chinese_msg = '用户注销成功'


class FileUploadSuccess(Success):
    status_code = 200
    msg = 'file upload success'
    chinese_msg = '文件上传成功'
