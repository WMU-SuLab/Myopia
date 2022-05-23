# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/17 16:26
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

from rest_framework.response import Response

from Common.utils.http.successes import Success
from Screening.utils.auth.views.api import EmployeeLoginRequiredAPIView


class UserPermissionsAPIView(EmployeeLoginRequiredAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Success(data=request.user.get_all_permissions()))
