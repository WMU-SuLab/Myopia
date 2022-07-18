# -*- encoding: utf-8 -*-
"""
@File Name      :   url.py    
@Create Time    :   2022/7/14 16:54
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

from django.shortcuts import reverse

from .obj import is_obj_file_path
from Common.utils.text_handler.hash import encrypt_text


def generate_file_url(file_url: str = None, file_path: str = None):
    if file_url:
        if is_obj_file_path(file_url):
            return reverse('Common:api:download_file', args=(encrypt_text(file_url),))
        elif file_url.startswith('http'):
            return file_url
    if file_path:
        return reverse('Common:api:download_file', args=(encrypt_text(file_path),))
    return None


def generate_image_url(image_url: str = None, image_path: str = None):
    if image_url:
        if is_obj_file_path(image_url):
            return reverse('Common:api:download_image', args=(encrypt_text(image_url),))
        else:
            return image_url
    if image_path:
        return reverse('Common:api:download_image', args=(encrypt_text(image_path),))
    return None
