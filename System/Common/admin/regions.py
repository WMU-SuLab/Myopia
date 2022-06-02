# -*- encoding: utf-8 -*-
"""
@File Name      :   regions.py    
@Create Time    :   2022/5/27 15:02
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

from django.contrib import admin

from Common.models.regions import *
from .base import BaseAdmin


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    pass


@admin.register(Province)
class ProvinceAdmin(BaseAdmin):
    pass


@admin.register(City)
class CityAdmin(BaseAdmin):
    pass


@admin.register(Area)
class AreaAdmin(BaseAdmin):
    pass


@admin.register(Street)
class StreetAdmin(BaseAdmin):
    pass
