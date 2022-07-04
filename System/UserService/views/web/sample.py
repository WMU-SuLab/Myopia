# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2022/6/29 15:28
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

from Common.models.project import Project
from Common.utils.auth.views.api import AllowAnyAPIView
from UserService.utils.auth.views import sample_manage_title, SampleManagerLoginRequiredView
from Common.viewModels import reverse_choices_to_dict

class SampleManagerLoginView(AllowAnyAPIView):
    def get(self, request):
        return render(request, 'UserService/sample/login.html', context={'title': sample_manage_title})


class SampleManagerIndexView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'UserService/sample/index.html', context={
            'title': sample_manage_title,
            'user': {
                'username': request.user.username,
            }
        })


class SampleUserManageView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'UserService/sample/user_projects.html', context={
            'title': sample_manage_title + '-用户数据管理',
            'user': {
                'username': request.user.username,
            },
            'progress_choices': reverse_choices_to_dict(Project.progress_choices),
        })
