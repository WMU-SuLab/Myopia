# -*- encoding: utf-8 -*-
"""
@File Name      :   xlsx.py
@Create Time    :   2022/11/22 21:21
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

import pandas as pd
from django.http import HttpResponse

from Common.utils.file_handler.table_handler.xlsx import generate_xlsx_file_io


def xlsx_response(df: pd):
    file = generate_xlsx_file_io(df)
    response = HttpResponse(
        file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment;filename=all_data.xlsx'
    # response['Content-Disposition'] = 'inline;filename=文件名.txt'
    return response
