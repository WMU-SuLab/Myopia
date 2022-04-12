# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/12/1 14:57
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import os


def validate_file_path(file_path):
    """
    检查文件路径是否存在
    :param file_path:
    :return:
    """
    if file_path and os.path.exists(file_path) and os.path.isfile(file_path):
        return True
    else:
        print('file path is required or path error')
        return False
