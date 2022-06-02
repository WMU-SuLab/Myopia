# -*- encoding: utf-8 -*-
"""
@File Name      :   thumbnail.py    
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

from PIL import Image


def make_thumbnail_file_path(file_path, width:int=50, height:int=50):
    thumbnail_file_name = f'{width}x{height}-' + os.path.basename(file_path)
    thumbnail_file_dir = os.path.dirname(file_path)
    thumbnail_file_path = os.path.join(thumbnail_file_dir, thumbnail_file_name)
    return thumbnail_file_path


def make_thumbnail(file_path, width:int=50, height:int=50):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        image = Image.open(file_path)
        image.thumbnail((width, height))
        thumbnail_file_path = make_thumbnail_file_path(file_path, width=width, height=height)
        image.save(thumbnail_file_path)
        return thumbnail_file_path
    else:
        return None
