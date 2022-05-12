# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/11 13:31
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

from rest_framework import serializers

from Common.models.user import User
from . import base_exclude, BaseSerializer

user_exclude = base_exclude + ('password',)


class UserBaseSerializer(BaseSerializer):
    gender_display = serializers.CharField(source='get_gender_display')
    identification_card_type_display = serializers.CharField(source='get_identification_card_type_display')

    class Meta(BaseSerializer.Meta):
        model = User
        # fields = '__all__'
        exclude = user_exclude + ('groups', 'user_permissions')
