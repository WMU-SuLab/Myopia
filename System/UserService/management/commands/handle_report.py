# -*- encoding: utf-8 -*-
"""
@File Name      :   handle_report.py    
@Create Time    :   2022/4/8 11:09
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
from PyPDF2 import PdfFileMerger

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from weasyprint import HTML

from Common.models.role import Student, Teacher
from UserService.utils.report import generate_report_data_from_project, student_pdf_file_name,teacher_pdf_file_name


def generate_student_reports(file_path):
    students_report_data = [
        generate_report_data_from_project(project)
        for student in Student.objects.all() for project in
        student.user.projects.prefetch_related(
            'user', 'user__student_role', 'visual_chart', 'tono_meter', 'bio_meter', 'optometry').all()
    ]
    report_str = render_to_string(template_name='UserService/report/multiple.html', context=students_report_data)
    HTML(string=report_str).write_pdf(file_path)


def generate_teacher_reports(file_path):
    teachers_report_data = [
        generate_report_data_from_project(project)
        for teacher in Teacher.objects.all() for project in
        teacher.user.projects.prefetch_related(
            'user', 'user__teacher_role', 'visual_chart', 'tono_meter', 'bio_meter', 'optometry').all()
    ]
    report_str = render_to_string(template_name='UserService/report/multiple.html', context=teachers_report_data)
    HTML(string=report_str).write_pdf(file_path)

def merge_pdf(dir_path):
    student_file_paths=[[
        os.path.join(dir_path, student_pdf_file_name(student.user.name)),
        # todo:
    ] for student in Student.objects.all()]
    teacher_file_paths=[[
        os.path.join(dir_path, teacher_pdf_file_name(teacher.user.name)),
        # todo:
    ] for teacher in Teacher.objects.all()]
    merger = PdfFileMerger()
    for file_paths in [*student_file_paths, *teacher_file_paths]:
        for file_path in file_paths:
            merger.append(file_path)
        file_name = os.path.basename(file_paths[0])
        merger.write(os.path.join(dir_path,'joint-'+file_name))


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-S', '--students', action='store_true', help='generate students\' reports')
        parser.add_argument('-T', '--teachers', action='store_true', help='generate teachers\' reports')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not file_path:
            file_path = './reports.pdf'
        if options['students']:
            generate_student_reports(file_path=file_path)
        if options['teachers']:
            generate_teacher_reports(file_path=file_path)
