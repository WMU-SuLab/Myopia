# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/5/27 11:21
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

import os

from PIL import Image, UnidentifiedImageError


def is_image_file(image_file_path: str = None):
    """
    判断文件是否是图片
    :param image_file_path:
    :return:
    """
    if image_file_path and os.path.exists(image_file_path) and os.path.isfile(image_file_path):
        try:
            Image.open(image_file_path)
            return True
        except UnidentifiedImageError:
            return False
    else:
        return False
