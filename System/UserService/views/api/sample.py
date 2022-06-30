# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2022/6/30 11:36
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

from UserService.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView


class UpdateProjectProgress(SampleManagerIsAuthenticatedAPIView):
    pass


class UploadReportFile(SampleManagerIsAuthenticatedAPIView):
    pass
