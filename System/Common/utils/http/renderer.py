# -*- encoding: utf-8 -*-
"""
@File Name      :   renderer.py    
@Create Time    :   2022/4/7 17:44
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

from pydantic import ValidationError
from rest_framework.renderers import JSONRenderer as _JSONRenderer

from .response_structure import HTTPJSONStructureModel, BaseHTTPJSONStructure, RawHTTPJSONStructure
from .successes import Success


# 重写drf的JSONRenderer
class JSONRenderer(_JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # print(renderer_context)
        if renderer_context:
            # 判断实例的类型，返回的数据可能是列表也可能是字典
            if isinstance(data, BaseHTTPJSONStructure):
                data = data.to_dict()
            elif isinstance(data, RawHTTPJSONStructure):
                data = data.get_body()
            else:
                try:
                    data = HTTPJSONStructureModel(**data).dict()
                except ValidationError as e:
                    # data = Success(data=data, msg_detail=str(e)).to_dict()
                    data = Success(data=data).to_dict()
        # 返回JSON数据
        return super().render(data, accepted_media_type, renderer_context)
