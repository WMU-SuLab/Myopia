# -*- encoding: utf-8 -*-
"""
@File Name      :   info.py    
@Create Time    :   2022/6/1 11:29
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

from Common.viewModels import choices_to_dict
from Common.models.user import User, Nationality
from Common.serializers.base.user import NationalityBaseSerializer
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.successes import Success


class GenderAPIView(AllowAnyAPIView):
    def get(self, request):
        return Response(Success(data=choices_to_dict(User.gender_choices)))


class EducationAPIView(AllowAnyAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Success(data=choices_to_dict(User.education_choices)))


class NationalityAPIView(AllowAnyAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Success(data=NationalityBaseSerializer(Nationality.objects.all(), many=True).data))
