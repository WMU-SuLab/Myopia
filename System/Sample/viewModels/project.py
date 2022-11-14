# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py
@Create Time    :   2022/11/13 17:02
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

from django.utils.timezone import localtime, get_current_timezone_name

from Common.models.project import Project
from Common.utils.alibabacloud.oss.url import generate_file_url


def get_project_info(project: Project):
    return {
        'serial_number': project.sequence.serial_number,
        'project_name': project.name,
        'username': project.remarks_json.get('name', None),
        'progress': project.get_progress_display(),
        # 数据库中取出来的是UTC时间
        'created_time': localtime(project.created_time).strftime('%Y-%m-%d %H:%M:%S'),
        'tzname': get_current_timezone_name(),
        # 但是不知道为什么timestamp是本地时间
        'created_time_timestamp': project.created_time.timestamp(),
        'report_file_url': generate_file_url(project.report_file_url, project.report_file_path),
    }
