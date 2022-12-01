# -*- encoding: utf-8 -*-
"""
@File Name      :   export_screen_data.py
@Create Time    :   2022/4/20 15:24
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

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from Common.models.user import User
from Common.viewModels.user import export_users_projects_data


def export_all_user_data(file_path):
    if not file_path:
        file_path = os.path.join(settings.EXPORT_DATA_DIR_PATH, 'user_projects_data.xlsx')
    writer = pd.ExcelWriter(file_path, mode="a", engine="openpyxl")
    student_rows = pd.DataFrame(export_users_projects_data(
        User.objects.filter(student_role__isnull=False).select_related('student_role', 'projects')))
    student_rows.to_excel(writer, sheet_name="Student", index=False)
    teacher_rows = pd.DataFrame(export_users_projects_data(
        User.objects.filter(teacher_role__isnull=False).select_related('teacher_role', 'projects')))
    teacher_rows.to_excel(writer, sheet_name="Teacher", index=False)
    writer.save()


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', action='store_true', help='export all user data')
        parser.add_argument('-f', '--file_path', type=str, help='export data file path')

    def handle(self, *args, **options):
        file_path = options.get('file_path', None)
        if options.get('all', None):
            export_all_user_data(file_path)
        else:
            print('-u or -g or -p or -s is required')
