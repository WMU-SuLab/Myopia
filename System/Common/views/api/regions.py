# -*- encoding: utf-8 -*-
"""
@File Name      :   region.py    
@Create Time    :   2022/5/27 14:58
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

from Common.models.regions import Country, Province, City, Area, Street
from Common.serializers.base.regions import CountryBaseSerializer, ProvinceBaseSerializer, CityBaseSerializer, \
    AreaBaseSerializer, StreetBaseSerializer
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.successes import Success


class CountryListAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, *args, **kwargs):
        return Response(Success(data=CountryBaseSerializer(Country.objects.all(), many=True).data, many=True))


class ProvinceListAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, country_id, *args, **kwargs):
        return Response(
            Success(data=ProvinceBaseSerializer(Province.objects.filter(country_id=country_id), many=True).data))


class CityListAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, province_id, *args, **kwargs):
        return Response(Success(data=CityBaseSerializer(City.objects.filter(province_id=province_id), many=True).data))


class AreaListAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, city_id, *args, **kwargs):
        return Response(Success(data=AreaBaseSerializer(Area.objects.filter(city_id=city_id), many=True).data))


class StreetListAPIView(AllowAnyAPIView):
    # throttle_scope = 'api_user_info'

    def get(self, request, area_id, *args, **kwargs):
        return Response(Success(data=StreetBaseSerializer(Street.objects.filter(area_id=area_id), many=True).data))
