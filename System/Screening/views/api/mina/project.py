# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/5/17 17:18
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

from rest_framework.generics import RetrieveAPIView

from Common.models.project import Project
from Common.serializers.project import ProjectEquipmentsBaseSerializer
from Screening.utils.auth.views.api import InsiderIsAuthenticatedGenericAPIView


class ProjectRetrieveAPIView(InsiderIsAuthenticatedGenericAPIView, RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectEquipmentsBaseSerializer
    lookup_url_kwarg = 'project_id'
