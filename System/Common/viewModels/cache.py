# -*- encoding: utf-8 -*-
"""
@File Name      :   cache.py    
@Create Time    :   2022/7/4 17:34
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

from django.core.cache import cache


def get_cache(key):
    return cache.get(key)


def set_cache(key, value, timeout: int = None):
    cache.set(key, value, timeout)


def delete_cache(key):
    cache.delete(key)


def clear_cache():
    cache.clear()


def get_cache_keys():
    return cache.keys()


def get_cache_info():
    return cache.info()


def get_cache_set():
    return cache.get_many(cache.keys())


def get_cache_set_by_key(key):
    return cache.get_many([key])
