# -*- encoding: utf-8 -*-
"""
@File Name      :   url.py    
@Create Time    :   2022/4/21 17:13
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

from urllib.parse import unquote, urlparse, parse_qs, parse_qsl, urlencode


def params_dict_to_url_query_string(params_dict: dict, if_quote=False) -> str:
    return urlencode(params_dict, doseq=True) if if_quote else unquote(urlencode(params_dict, doseq=True))


def url_to_params_dict(url: str) -> dict:
    """
    解析url中的查询参数（?之后的内容）为字典
    """
    return parse_qs(urlparse(url).query)


def url_query_string_to_params_dict(url_query_string: str) -> dict:
    """
    解析url中的查询参数（?之后的内容）为字典
    """
    return parse_qs(url_query_string)


def params_list_to_url_query_string(params_list: list, if_quote=False) -> str:
    return urlencode(params_list, doseq=True) if if_quote else unquote(urlencode(params_list, doseq=True))


def url_to_params_list(url: str) -> list:
    """
    解析url中的查询参数（?之后的内容）为字典
    """
    return parse_qsl(urlparse(url).query)


def url_query_string_to_params_list(url_query_string: str) -> list:
    """
    解析url中的查询参数（?之后的内容）为字典
    """
    return parse_qsl(url_query_string)
