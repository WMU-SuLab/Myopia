# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/4/14 16:22
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


def count_spherical_equivalent(spherical: float, column: float) -> float:
    """
    计算等效球镜
    :param spherical: 球镜
    :param column: 柱镜
    :return:
    """
    return spherical + 1 / 2 * column
