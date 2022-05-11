# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/5 15:25
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

from .base.project import ProjectBaseSerializer
from .base.user import UserBaseSerializer


class UserSerializer(UserBaseSerializer):
    # 正向关联
    # 法1一对多关联对象序列化：此字段将被序列化为关联对象的主键
    # projects = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # 法2一对多关联对象序列化：此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）
    # projects = serializers.StringRelatedField(read_only=True,many=True)
    # 法3一对多关联对象序列化：使用关联对象的序列化器
    projects = ProjectBaseSerializer(many=True)

    class Meta(UserBaseSerializer.Meta):
        depth = 1
