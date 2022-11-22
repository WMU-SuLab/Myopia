# -*- encoding: utf-8 -*-
"""
@File Name      :   exceptions.py    
@Create Time    :   2022/4/7 17:46
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

from django.core.exceptions import ObjectDoesNotExist as DjangoObjectDoesNotExist, \
    ValidationError as DjangoValidationError
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import APIException as RestFrameWorkAPIException
from rest_framework.views import Response
from rest_framework.views import exception_handler as _exception_handler

from .response_structure import BaseHTTPJSONStructure


# 将仅针对由引发的异常生成的响应调用异常处理程序，它不会用于视图直接返回的任何响应
def exception_handler(exc, context):
    if isinstance(exc, APIException):
        # 处理数据库中删除用户账户的情况
        if isinstance(exc, UserNotExist):
            res = Response(exc.to_dict())
            # 是否需要清除cookies?
            # res.delete_cookie('refresh')
            return res
        return Response(exc.to_dict())
    elif isinstance(exc, PydanticValidationError):
        return Response(ParameterError(msg_detail=str(exc)).to_dict())
    elif isinstance(exc, RestFrameWorkAPIException):
        default_detail = str(exc.default_detail)
        return Response(BaseError(
            status_code=exc.status_code,
            msg=exc.default_code,
            msg_detail=default_detail,
            extra={
                'exception': exc.__class__.__name__,
                'full_details': exc.get_full_details(),
                # 'full_details': str(exc),
            },
        ).to_dict())
    # 处理常见的django自带的exceptions
    elif isinstance(exc, DjangoObjectDoesNotExist):
        return Response(NotFound(msg=str(exc), chinese_msg='数据库对象未找到').to_dict())
    elif isinstance(exc, DjangoValidationError):
        return Response(ValidationError(msg='database not valid', msg_detail=str(exc)).to_dict())
    else:
        return _exception_handler(exc, context)


class APIException(BaseHTTPJSONStructure, Exception):
    success = False
    code = 1000

    def __str__(self):
        return f'APIException: {self.to_dict()}'


class BaseError(APIException):
    success = False
    code = 1000
    status_code = 500
    msg = 'error/failure'
    msg_detail = 'error/failure'
    chinese_msg = '错误/失败'


class ServerError(APIException):
    status_code = 500
    msg = 'server error'
    chinese_msg = '服务器错误'


class PhoneError(BaseError):
    msg = 'phone error'
    chinese_msg = '手机相关错误'


class PhoneSendSMSError(PhoneError):
    msg = 'phone send sms error'
    chinese_msg = '手机短信发送错误'


class EmailError(BaseError):
    msg = 'email related error'
    chinese_msg = '邮箱相关错误'


class EmailSendError(EmailError):
    msg = 'email send error'
    chinese_msg = '邮箱发送失败'


class EmailBadHeaderError(EmailError):
    msg = 'email bad header error'
    chinese_msg = '邮件头部错误'


class ParameterError(BaseError):
    status_code = 400
    msg = 'parameter error'
    chinese_msg = '参数错误'


class ValidationError(APIException):
    status_code = 400
    msg = 'validation error'
    chinese_msg = '验证错误'


class VerificationCodeError(APIException):
    status_code = 400
    msg = 'verification code error'
    chinese_msg = '验证码错误'


class ParseError(APIException):
    status_code = 400
    msg = 'parse error'
    chinese_msg = '解析错误'


class UserNotExist(APIException):
    status_code = 404
    msg = 'user not exist'
    chinese_msg = '用户不存在'


class UserExist(APIException):
    status_code = 400
    msg = 'user exist'
    chinese_msg = '用户已存在'


class AuthenticationFailed(APIException):
    status_code = 401
    msg = 'authentication failed'
    chinese_msg = '认证失败'


class NotAuthenticated(APIException):
    status_code = 401
    msg = 'not authenticated'
    chinese_msg = '未认证'


class InvalidToken(APIException):
    status_code = 401
    msg = 'Token is invalid or expired'
    chinese_msg = 'token不合法或过期'


class TokenNotExist(APIException):
    status_code = 401
    msg = 'token not exist'
    chinese_msg = 'token不存在'


class TokenExpired(APIException):
    status_code = 401
    msg = 'token expired'
    chinese_msg = 'token过期'


class NotActive(APIException):
    status_code = 401
    msg = 'account not active'
    chinese_msg = '账户未激活'


class PermissionDenied(APIException):
    status_code = 403
    msg = 'permission denied'
    chinese_msg = '权限不足'


class NotFound(APIException):
    status_code = 404
    msg = 'not found'
    chinese_msg = '未找到'


class MethodNotAllowed(APIException):
    status_code = 405
    msg = 'method not allowed'
    chinese_msg = '方法不允许'


class NotAcceptable(APIException):
    status_code = 406
    msg = 'not acceptable'
    chinese_msg = '不接受'


class ProxyAuthenticationRequired(APIException):
    status_code = 407
    msg = 'proxy authentication required'
    chinese_msg = '代理认证'


class Timeout(APIException):
    status_code = 408
    msg = 'timeout'
    chinese_msg = '超时'


class Conflict(APIException):
    status_code = 409
    msg = 'conflict'
    chinese_msg = '冲突'


class InsufficientPreconditions(APIException):
    status_code = 412
    msg = 'precondition failed'
    chinese_msg = '前提条件不足'


class UnsupportedMediaType(APIException):
    status_code = 415
    msg = 'unsupported media type'
    chinese_msg = '不支持的媒体类型'


class ProcessingError(APIException):
    status_code = 422
    msg = 'processing error'
    chinese_msg = '处理错误'


class Throttled(APIException):
    status_code = 429
    msg = 'throttled'
    chinese_msg = '被限流'


class FileNotFound(APIException):
    status_code = 404
    msg = 'file not found'
    chinese_msg = '文件未找到'


class FileExist(APIException):
    status_code = 400
    msg = 'file exist'
    chinese_msg = '文件已存在'


class FileUploadError(APIException):
    status_code = 400
    msg = 'file upload error'
    chinese_msg = '文件上传错误'


class FileDeleteError(APIException):
    status_code = 400
    msg = 'file delete error'
    chinese_msg = '文件删除错误'


class FileDownloadError(APIException):
    status_code = 400
    msg = 'file download error'
    chinese_msg = '文件下载错误'
