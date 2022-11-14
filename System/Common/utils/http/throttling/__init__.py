# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/3/31 18:55
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

from rest_framework.throttling import SimpleRateThrottle


class BaseThrottle(SimpleRateThrottle):
    # cache = caches['default']
    scope = 'base'

    # 根据IP地址获得cache key
    def get_cache_key(self, request, view):
        return self.get_ident(request)

    # 根据用户id获取cache key
    # def get_cache_key(self, request, view):
    #     return request.user.pk
