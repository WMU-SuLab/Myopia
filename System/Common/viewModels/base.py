# -*- encoding: utf-8 -*-
"""
@File Name      :   base.py    
@Create Time    :   2022/5/21 15:54
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

from Common.models.base import Base, handle_object_does_not_exist
from Common.utils.http.exceptions import ParameterError


@handle_object_does_not_exist
def retrieve_model(model: type(Base) = None, model_id: int = None, data: dict = None, **kwargs):
    model_id = model_id or data.get('id', None)
    if model_id is None:
        return ParameterError('model_id is None')
    return model.objects.get(id=model_id, **kwargs)
