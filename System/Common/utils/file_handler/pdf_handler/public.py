# -*- encoding: utf-8 -*-
"""
@File Name      :   public.py    
@Create Time    :   2022/4/12 14:59
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
from copy import copy

from PyPDF2.pdf import PdfFileReader, PdfFileWriter


def divide_pdf(file_path: str):
    file_reader = PdfFileReader(file_path)
    dir_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    # getNumPages() 获取总页数
    for page_num in range(file_reader.getNumPages()):
        # 实例化对象
        file_writer = PdfFileWriter()
        # 将遍历的每一页添加到实例化对象中
        file_writer.addPage(file_reader.getPage(page_num))
        with open(os.path.join(dir_path, file_name.replace('.pdf', f'{page_num}.pdf')), 'wb') as output_file:
            file_writer.write(output_file)


def merge_pdf(input_file_paths, output_file_path):
    file_writer = PdfFileWriter()
    for input_file_path in input_file_paths:
        # 循环读取需要合并pdf文件
        file_reader = PdfFileReader(input_file_path)
        # 遍历每个pdf的每一页
        for page_num in range(file_reader.getNumPages()):
            # 写入实例化对象中
            file_writer.addPage(file_reader.getPage(page_num))

    with open(output_file_path, 'wb') as out:
        file_writer.write(out)


def rotate_pdf(input_file_path, output_file_path, page_angles: dict):
    file_reader = PdfFileReader(input_file_path)
    file_writer = PdfFileWriter()
    for page_num, angle in page_angles.items():
        page = file_reader.getPage(page_num)
        page.rotateClockwise(page_angles[page_num])
        file_writer.addPage(page)
    with open(output_file_path, 'wb') as output_file:
        file_writer.write(output_file)


def encrypt_pdf(input_file_path, output_file_path, password):
    file_reader = PdfFileReader(input_file_path)
    file_writer = PdfFileWriter()
    for page_num in range(file_reader.getNumPages()):
        file_writer.addPage(file_reader.getPage(page_num))
    # 设置密码
    file_writer.encrypt(password)
    with open(output_file_path, 'wb') as output_file:
        file_writer.write(output_file)


def decrypt_pdf(input_file_path, output_file_path, password):
    file_reader = PdfFileReader(input_file_path)
    file_reader.decrypt(password)
    file_writer = PdfFileWriter()
    for page_num in range(file_reader.getNumPages()):
        file_writer.addPage(file_reader.getPage(page_num))

    with open(output_file_path, 'wb') as output_file:
        file_writer.write(output_file)


def add_watermark(input_file_path, output_file_path, watermark_file_path):
    watermark_pdf = PdfFileReader(watermark_file_path)
    # 水印所在的页数
    watermark_page = watermark_pdf.getPage(0)
    # 读取添加水印的文件
    file_reader = PdfFileReader(input_file_path)
    file_writer = PdfFileWriter()
    for page_num in range(file_reader.getNumPages()):
        # 读取需要添加水印每一页pdf
        source_page = file_reader.getPage(page_num)
        new_page = copy(watermark_page)
        # new_page(水印)在下面，source_page原文在上面
        new_page.mergePage(source_page)
        file_writer.addPage(new_page)

    with open(output_file_path, 'wb') as output_file:
        file_writer.write(output_file)
