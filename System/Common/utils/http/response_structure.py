# -*- encoding: utf-8 -*-
"""
@File Name      :   response_structure.py
@Create Time    :   2022/4/7 17:43
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

import json
from typing import Union, Dict, List, Any, Type

from django.http.response import JsonResponse as _JsonResponse
from pydantic import BaseModel

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


class HTTPJSONStructureModel(BaseModel):
    success: bool
    code: int
    status_code: int
    msg: str = ''
    msg_detail: str | JSON = ''
    chinese_msg: str = ''
    data: str | JSON = None
    extra: str | JSON = {}


class BaseHTTPJSONStructure:
    success = True
    code = 0
    status_code = 200
    msg = ''
    msg_detail = ''
    chinese_msg = ''
    data = None
    extra = {}

    @property
    def error_code(self):
        return self.status_code

    def __init__(
            self, data: dict or list = None, success: bool = None, code: int = None, status_code: int = None,
            msg: str = None, msg_detail: str = None, chinese_msg: str = None, extra: dict = None, **kwargs):
        if extra is None:
            extra = {}
        self.data = data or self.data
        self.success = success or self.success
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.msg = msg or self.msg
        self.msg_detail = msg_detail or self.msg_detail
        self.chinese_msg = chinese_msg or self.chinese_msg
        self.extra = {**extra, **kwargs} or self.extra

    def to_dict(self):
        return {
            'success': self.success,
            'code': self.code,
            'status_code': self.status_code,
            'msg': self.msg,
            'msg_detail': self.msg_detail,
            'chinese_msg': self.chinese_msg,
            'data': self.data,
            'extra': self.extra
        }

    def get_body(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return f'<BaseHTTPJSONResponse: {self.to_dict()}>'


# 重写django原生的JsonResponse
class JsonResponse(_JsonResponse):
    success = True
    code = 0
    status_code = 200
    msg = 'success'
    msg_detail = ''
    chinese_msg = '成功'
    data = None
    extra = {}

    def __init__(
            self, data=None, success: bool = True, code: int = 100, status_code: int = 200,
            msg: str = 'success', msg_detail: str = '', chinese_msg: str = '成功',extra: dict = None, **kwargs):
        self.data = data or self.data
        self.success = success or self.success
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.msg = msg or self.msg
        self.msg_detail = msg_detail or self.msg_detail
        self.chinese_msg = chinese_msg or self.chinese_msg
        self.extra = {**extra, **kwargs} or self.extra

        data = {
            'success': self.success,
            'code': self.code,
            'status_code': self.status_code,
            'msg': self.msg,
            'msg_detail': self.msg_detail,
            'chinese_msg': self.chinese_msg,
            'data': self.data,
            'extra': self.extra
        }
        super().__init__(data, **kwargs)


class RawHTTPJSONStructure:
    def __init__(self, data: JSON):
        self.data = data

    def get_body(self):
        return self.data
