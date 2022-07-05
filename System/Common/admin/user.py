# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/29 16:56
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

from Common.models.user import User
from .base import BaseAdmin


@admin.register(User)
class UserAdmin(BaseAdmin):
    # 设置 list_display 来控制哪些字段显示在管理的变更列表页面。
    list_display = ['id', 'username', 'nickname', 'name', 'email', 'phone_number', 'is_confirmed', 'is_active', 'is_staff',
                    'is_superuser']
    # 使用 list_display_links 来控制 list_display 中的字段是否以及哪些字段应该被链接到对象的 “更改” 页面
    # 默认情况下，更改列表页将把第一列 —— list_display 中指定的第一个字段 —— 链接到每个项目的更改页面
    list_display_links = ['id']
    # 将 list_editable 设置为模型上允许在更改列表页上编辑的字段名称列表
    # 设置 list_filter 来激活管理更改列表页面右侧侧栏的过滤器
    list_filter = ['is_confirmed', 'is_active', 'is_staff', 'is_superuser', 'created_time', 'status']
    search_fields = ['username', 'email']
    fieldsets = [
        ('基本信息', {
            'fields': [
                'username', 'nickname', 'openid', 'password', 'is_confirmed', 'is_active',
            ]}),
        ('详细信息', {
            'fields': [
                ('name', 'email', 'phone_number',),
                ('identification_card_type', 'identification_card_number', 'gender', 'age', 'birthday')
            ]}),
        ('家庭信息', {
            'fields': [
                ('native_place', 'home_address', 'language'),
                ('street', 'city', 'province', 'country')
            ]}),
        ('权限', {'fields': ['is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('备注', {'fields': ['remarks', 'remarks_json', 'status', ]}),
    ]

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.filter(is_superuser=False)
        if not request.user.is_superuser:
            qs = qs.filter(is_staff=False)
        if not request.user.is_admin:
            qs = qs.filter(manager_role__isnull=True)
        if not request.user.is_manager:
            qs = qs.filter(employee_role__isnull=True)
        return qs
