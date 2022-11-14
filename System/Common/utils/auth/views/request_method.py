# -*- encoding: utf-8 -*-
"""
@File Name      :   request_method.py
@Create Time    :   2022/11/13 20:06
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

from abc import ABCMeta, abstractmethod


class HandlePost(metaclass=ABCMeta):
    @abstractmethod
    def create(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        update_type = request.POST.get('update_type', None) or request.GET.get('update_type', None)
        if update_type and update_type in ['pat', 'patch', 'PAT', 'PATCH']:
            request.method = 'PATCH'
            return self.patch(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)

    @abstractmethod
    def patch(self, request, *args, **kwargs):
        pass
