# -*- encoding: utf-8 -*-
"""
@File Name      :   json.py    
@Create Time    :   2022/4/7 20:51
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


def obj_to_json(data):
    if isinstance(data, list):
        return [obj_to_json(item) for item in data]
    elif isinstance(data, dict):
        return {key: obj_to_json(value) for key, value in data.items()}

    return data
