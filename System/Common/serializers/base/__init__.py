# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/5/11 13:30
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

base_exclude = ()


class BaseSerializer(serializers.ModelSerializer):
    """
    基础序列化器
    """
    status_display = serializers.CharField(source='get_status_display', required=False)
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    modified_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        # fields 是 result 接口需要返回的字段
        # 可以指定 "__all__" 展示全部参数，不推荐，因为改变model时，可能无意会泄露数据
        # fields = '__all__'
        # exclude 为不展示的字段名，和 fields 不能同时设置
        exclude = base_exclude
        # 当一个model有外键的时候，默认显示的是外键的id，此时要显示外键的所有值可以使用depth，外键的值还可以显示它外键的值，即增加depth，depth最大为10
        # depth = 1
        # 把一个字段变成只读字段,自增字段默认是只读的，不显式表示也是可以的
        # read_only_fields = []
        # extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
        extra_kwargs = {
            'created_time': {'required': False, 'read_only': True},
            'modified_time': {'required': False, 'read_only': True},
            'status': {'required': False},
            'remarks': {'required': False},
            'remarks_json': {'required': False},
        }
