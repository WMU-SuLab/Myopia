# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/15 21:45
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

from Sample.models.project import TGFBISampleProject
from Common.viewModels.choices import reverse_choices_to_dict
from Sample.utils.auth.views import sample_manage_title, SampleManagerLoginRequiredView


class TGFBIProjectsManageView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'Sample/manage/projects_tgfbi.html', context={
            'title': sample_manage_title + '-TGFBI角膜营养不良基因检测采样管理',
            'user': {
                'username': request.user.username,
            },
            'progress_choices': reverse_choices_to_dict(TGFBISampleProject.progress_choices[1:]),
        })
