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

from .response import BaseHTTPJSONStructure


class Success(BaseHTTPJSONStructure):
    success = True
    code = 0
    status_code = 200
    msg = 'success'
    chinese_msg = '成功'
