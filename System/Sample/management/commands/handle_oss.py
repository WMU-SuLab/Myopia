# -*- encoding: utf-8 -*-
"""
@File Name      :   handle_oss.py    
@Create Time    :   2022/7/15 16:57
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
from abc import ABCMeta

from django.conf import settings
from django.core.management.base import BaseCommand

from Common.models.project import Project
from Common.utils.alibabacloud.oss.obj import generate_obj_file_path, parsing_obj_file_path
from Common.utils.time import print_accurate_execute_time


@print_accurate_execute_time
def upload_to_oss():
    # 选择有本地路径，但是没有云端路径的项目
    projects = Project.objects.filter(report_file_url__isnull=True, report_file_path__isnull=False)
    for project in projects:
        obj_name_index = project.report_file_path.find(settings.RELATIVE_USER_PDF_DIR_PATH)
        project.report_file_url = generate_obj_file_path(project.report_file_path[obj_name_index:])
    Project.objects.bulk_update(projects, ['report_file_url'])


@print_accurate_execute_time
def download_from_oss():
    # 选择有云端路径，但是没有本地路径的项目
    projects = Project.objects.filter(report_file_url__isnull=False, report_file_path__isnull=True)
    for project in projects:
        relative_file_path = parsing_obj_file_path(project.report_file_url)
        file_name = os.path.basename(relative_file_path)
        project.report_file_path = os.path.join(settings.USER_PDF_DIR_PATH, file_name)
    Project.objects.bulk_update(projects, ['report_file_url'])


@print_accurate_execute_time
def delete_local_files():
    # 选择两个路径都有的项目
    projects = Project.objects.filter(report_file_url__isnull=False, report_file_path__isnull=False)
    for project in projects:
        project.report_file_path = None
    Project.objects.bulk_update(projects, ['report_file_url'])


@print_accurate_execute_time
def delete_oss_files():
    # 选择两个路径都有的项目
    projects = Project.objects.filter(report_file_url__isnull=False, report_file_path__isnull=False)
    for project in projects:
        project.report_file_url = None
    Project.objects.bulk_update(projects, ['report_file_url'])


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-a', '--action', type=str,
                            choices=['upload_to_oss', 'download_from_oss', 'delete_local', 'delete_oss'], )

    def handle(self, *args, **options):
        """
        对于文件，应该使用管理工具上传下载删除
        对于数据库，应该使用模型进行操作，但本文件只是提供了示例方法，！！！此命令不能使用！！！应当根据你的数据库模型进行自定义操作
        整体操作这样速度会快很多，混在一起代码还多
        """
        action = options['action']
        if action == 'upload_to_oss':
            upload_to_oss()
        elif action == 'download_from_oss':
            download_from_oss()
        elif action == 'delete_local':
            delete_local_files()
        elif action == 'delete_oss':
            delete_oss_files()
        else:
            raise Exception('action error')
