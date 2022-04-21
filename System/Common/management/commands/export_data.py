# -*- encoding: utf-8 -*-
"""
@File Name      :   export_data.py    
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

from abc import ABCMeta

from django.core.management.base import BaseCommand

from Common.models.user import User
from Common.viewModels.user import export_users_projects_data


def export_all_user_data(file_name):
    student_rows = export_users_projects_data(
        User.objects.filter(student_role__isnull=False).select_related('student_role', 'projects'))
    teacher_rows = export_users_projects_data(
        User.objects.filter(teacher_role__isnull=False).select_related('teacher_role', 'projects'))
    # todo

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
