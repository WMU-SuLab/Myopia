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


def generate_project_informed_consent_file_name(informed_consent, file_type: str = 'jpg') -> str:
    """
    生成项目提供的informed consent文件名
    :param informed_consent:
    :param file_type:
    :return:
    """
    return f'{informed_consent.project.user.username}-{informed_consent.project_id}-{informed_consent.id}.{file_type}'


def count_spherical_equivalent(spherical: float, column: float) -> float:
    """
    计算等效球镜
    :param spherical: 球镜
    :param column: 柱镜
    :return:
    """
    if spherical and column:
        return spherical + 1 / 2 * column
    else:
        return 0
