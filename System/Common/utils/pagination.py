# -*- encoding: utf-8 -*-
"""
@File Name      :   pagination.py
@Create Time    :   2022/11/22 21:44
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


def array_range(array: list, current_page, limit):
    return array[(int(current_page) - 1) * int(limit):int(current_page) * int(limit)]
