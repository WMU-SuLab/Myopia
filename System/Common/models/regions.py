# -*- encoding: utf-8 -*-
"""
@File Name      :   regions.py    
@Create Time    :   2022/5/26 19:28
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

from django.db import models

from Common.models.base import Base


class Country(Base):
    """
    国家
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='国家名称')

    class Meta:
        verbose_name = verbose_name_plural = '国家'

    def __str__(self):
        return self.name


class Province(Base):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='provinces', verbose_name='所属国家')
    name = models.CharField(max_length=20, unique=True, verbose_name='省份名称')

    class Meta:
        verbose_name = verbose_name_plural = '省份/直辖市/州'

    def __str__(self):
        return self.name


class City(Base):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities', verbose_name='省份')
    name = models.CharField(max_length=20, verbose_name='城市名称')

    class Meta:
        verbose_name = verbose_name_plural = '城市'

    def __str__(self):
        return self.name


class Area(Base):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='areas', verbose_name='城市')
    name = models.CharField(max_length=20, verbose_name='区域名称')

    class Meta:
        verbose_name = verbose_name_plural = '区域'

    def __str__(self):
        return self.name


class Street(Base):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='streets', verbose_name='区域')
    name = models.CharField(max_length=20, verbose_name='街道名称')

    class Meta:
        verbose_name = verbose_name_plural = '街道'

    def __str__(self):
        return self.name
