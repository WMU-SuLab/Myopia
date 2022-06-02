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
from Common.serializers.project import ProjectEquipmentSerializer
from Screening.utils.auth.views.api import InsiderIsAuthenticatedGenericAPIView


class ProjectRetrieveAPIView(InsiderIsAuthenticatedGenericAPIView, RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectEquipmentSerializer
    lookup_field = 'project_id'

    # def get(self, request, *args, **kwargs):
    #     data = request.data
    #     project_id = data.get('project_id', None)
    #     if project_id:
    #         self.kwargs['pk'] = project_id
    #         return super().get(request, *args, **kwargs)
    #     else:
    #         return Response(ParameterError(msg='项目id不能为空'))
