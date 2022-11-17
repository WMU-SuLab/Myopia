# -*- encoding: utf-8 -*-
"""
@File Name      :   high_myopia.py
@Create Time    :   2022/11/11 21:11
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

from Sample.models.project import HighMyopiaSampleProject
from Common.viewModels.choices import reverse_choices_to_dict
from Sample.utils.auth.views import sample_manage_title, SampleManagerLoginRequiredView


class HighMyopiaProjectsManageView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'Sample/manage/projects_high_myopia.html', context={
            'title': sample_manage_title + '-高度近视遗传风险评估采样管理',
            'user': {
                'username': request.user.username,
            },
            'progress_choices': reverse_choices_to_dict(HighMyopiaSampleProject.progress_choices[1:]),
        })
