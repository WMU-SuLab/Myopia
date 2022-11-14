# -*- encoding: utf-8 -*-
"""
@File Name      :   index.py
@Create Time    :   2022/11/11 21:10
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

from django.shortcuts import render

from Sample.utils.auth.views import sample_manage_title, SampleManagerLoginRequiredView


class SampleManagerIndexView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'Sample/manage/index.html', context={
            'title': sample_manage_title,
            'user': {
                'username': request.user.username,
            }
        })
