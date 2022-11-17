# -*- encoding: utf-8 -*-
"""
@File Name      :   file.py    
@Create Time    :   2022/7/14 10:46
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

from . import bucket
from . import handle_oss_exception


def is_obj_file_path(obj_file_path):
    return obj_file_path.startswith('oss:')


def generate_obj_file_path(obj_name):
    return f'oss:{obj_name}'


def parsing_obj_file_path(obj_file_path):
    if is_obj_file_path(obj_file_path):
        return obj_file_path[4:]
    return obj_file_path


@handle_oss_exception
def upload_obj(obj_name, local_file_path):
    obj_name = parsing_obj_file_path(obj_name)
    bucket.put_object_from_file(obj_name, local_file_path)
    return True


@handle_oss_exception
def put_obj(obj_name, data):
    obj_name = parsing_obj_file_path(obj_name)
    bucket.put_object(obj_name, data)
    return True


@handle_oss_exception
def obj_exist(obj_name):
    """
    It checks if the object exists in the bucket
    :param obj_name: The name of the object to be uploaded
    :return: True or False
    """
    obj_name = parsing_obj_file_path(obj_name)
    return bucket.object_exists(obj_name)


@handle_oss_exception
def download_obj(obj_name, local_file_path):
    obj_name = parsing_obj_file_path(obj_name)
    if not obj_exist(obj_name):
        return False
    bucket.get_object_to_file(obj_name, local_file_path)
    return True


@handle_oss_exception
def obj_sign_url(obj_name, expires: int = 60):
    obj_name = parsing_obj_file_path(obj_name)
    if not obj_exist(obj_name):
        return None
    headers = dict()
    # 如果您希望实现浏览器访问时自动下载文件，并自定义下载后的文件名称，配置文件HTTP头中的Content-Disposition为attachment
    headers['content-disposition'] = 'attachment'
    # 如果您希望直接在浏览器中预览文件，配置文件HTTP头中的Content-Disposition为inline并使用Bucket绑定的自定义域名进行访问。
    # headers['content-disposition'] = 'inline'
    return bucket.sign_url(
        'GET',
        obj_name,
        expires,
        headers=headers,
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用
        slash_safe=True
    )


@handle_oss_exception
def delete_obj(obj_name):
    obj_name = parsing_obj_file_path(obj_name)
    if not obj_exist(obj_name):
        return False
    bucket.delete_object(obj_name)
    return True
