# -*- encoding: utf-8 -*-
"""
@File Name      :   regions.py    
@Create Time    :   2022/5/27 15:05
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

from Common.models.regions import *

from . import base_exclude, BaseSerializer

regions_exclude = list({*base_exclude, 'status', 'remarks', 'remarks_json'})


class CountryBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Country
        # fields = '__all__'
        exclude = regions_exclude


class ProvinceBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Province
        # fields = '__all__'
        exclude = regions_exclude


class CityBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = City
        # fields = '__all__'
        exclude = regions_exclude


class AreaBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Area
        # fields = '__all__'
        exclude = regions_exclude


class StreetBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Street
        # fields = '__all__'
        exclude = regions_exclude
