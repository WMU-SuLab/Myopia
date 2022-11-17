# -*- encoding: utf-8 -*-
"""
@File Name      :   api.py    
@Create Time    :   2022/6/29 18:57
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

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Common.utils.http.throttling.role import ManagerSecondRateThrottle, ManagerMinuteRateThrottle, \
    ManagerHourRateThrottle, ManagerDayRateThrottle
from Sample.utils.auth.permissions.user import IsSampleMangerUser
from . import SampleManagerLoginRequiredMixin


class SampleManagerIsAuthenticatedAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsSampleMangerUser)
    throttle_classes = (
        ManagerSecondRateThrottle, ManagerMinuteRateThrottle, ManagerHourRateThrottle, ManagerDayRateThrottle,
    )


class SampleManagerLoginRequiredAPIView(SampleManagerLoginRequiredMixin, SampleManagerIsAuthenticatedAPIView):
    pass
