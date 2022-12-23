# -*- encoding: utf-8 -*-
"""
@File Name      :   file.py
@Create Time    :   2022/10/20 16:50
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
from shutil import move, copy2

from Common.utils.http.exceptions import FileUploadError, FileDeleteError


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


def upload_file(f, file_path):
    """
    上传文件
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True


def handle_upload_file(f, file_path):
    """
    处理上传文件
    :param f:
    :param file_path:
    :return:
    """
    try:
        upload_file(f, file_path)
    except Exception as e:
        handle_remove_file(file_path)
        raise FileUploadError(msg_detail=str(e))


def copy_file(source_file_path, target_file_path):
    """
    如果目标是目录，使用原文件名，否则使用目标路径的文件名
    """
    if os.path.isfile(source_file_path):
        copy2(source_file_path, target_file_path)
        return True
    else:
        return False


def move_file(source_file_path, target_file_path):
    """
    同复制，如果目标是目录，使用原文件名，否则使用目标路径的文件名
    """
    if os.path.isfile(source_file_path):
        move(source_file_path, target_file_path)
        return True
    else:
        return False


def remove_file(file_path):
    """
    有文件就删除文件，没有文件就什么都不做
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def handle_remove_file(file_path):
    try:
        remove_file(file_path)
    except Exception as e:
        raise FileDeleteError(msg_detail=str(e))


def rename_file(file_path, new_file_path):
    """
    重命名文件
    """
    if os.path.isfile(file_path):
        os.rename(file_path, new_file_path)
        return True
    else:
        return False


def rename_file_by_name(file_path, new_name):
    """
    重命名文件，文件名为new_name
    """
    if os.path.isfile(file_path):
        os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))
        return True
    else:
        return False
