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

from Common.libs.choices import gender_choices, education_choices
from Common.models.user import Nationality
from Common.serializers.base.user import NationalityBaseSerializer
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.successes import Success
from Common.viewModels.choices import choices_to_dict


class GenderAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, *args, **kwargs):
        return Response(Success(data=choices_to_dict(gender_choices)))


class EducationAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, *args, **kwargs):
        return Response(Success(data=choices_to_dict(education_choices)))


class NationalityAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, *args, **kwargs):
        return Response(Success(data=NationalityBaseSerializer(Nationality.objects.all(), many=True).data))
