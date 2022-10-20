# -*- encoding: utf-8 -*-
"""
@File Name      :   dir.py    
@Create Time    :   2022/1/15 15:04
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
from shutil import copytree, move, rmtree


def make_dir(make_dir_path: str) -> bool:
    """
    没有就创建这个文件夹，有就直接返回True
    """
    # 为了防止是WindowsPath而报错，先转换一下
    path = str(make_dir_path).strip()
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(str(e))
            return False
    return True


def copy_dir(source_dir_path, target_dir_path):
    """
    把指定的文件夹连文件夹一起，全部拷贝到新的指定的文件夹（必须是不存在到文件夹，会自动重新创建）
    """
    if os.path.isdir(source_dir_path) and os.path.isdir(target_dir_path):
        copytree(source_dir_path, target_dir_path)
        return True
    else:
        return False


def move_dir(source_dir_path, target_dir_path):
    """
    如果目标是已存在的目录，则 src 会被移至该目录下。 如果目标已存在但不是目录，它可能会被覆盖
    如果是不存在的目录，将直接创建这个目录，再把文件夹中的内容移过去（不是包括文件夹本身的移动）
    """
    if os.path.isdir(source_dir_path) and os.path.isdir(target_dir_path):
        move(source_dir_path, target_dir_path)
        return True
    else:
        return False


def remove_dir(dir_path):
    """
    有文件夹，则删除文件夹，如果没有文件，则什么都不做
    """
    if os.path.isdir(dir_path):
        rmtree(dir_path)
        return True
    else:
        return False


def rename_dir(dir_path, new_dir_path):
    """
    重命名目录
    """
    if os.path.isdir(dir_path):
        os.rename(dir_path, new_dir_path)
        return True
    else:
        return False


def rename_dir_by_name(dir_path, new_name):
    """
    重命名目录，目录名为 new_name
    """
    if os.path.isdir(dir_path):
        os.rename(dir_path, os.path.join(os.path.dirname(dir_path), new_name))
        return True
    else:
        return False
