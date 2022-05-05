# -*- encoding: utf-8 -*-
"""
@File Name      :   base.py    
@Create Time    :   2022/4/7 18:44
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

import os

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from Common.utils.file_handler.table_handler.xlsx import generate_xlsx_file


class BaseAdmin(admin.ModelAdmin):
    # 具体详细参考：https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/#modeladmin-objects
    using = 'default'
    # 要在变更列表页上提供的动作列表
    actions = ['export_data_to_txt', 'export_data_to_excel']
    # 控制动作栏在页面的哪个位置出现。默认情况下，管理员更改列表在页面顶部显示动作（actions_on_top = True; actions_on_bottom = False）
    # actions_on_top = False
    # actions_on_bottom = True
    # 控制是否在动作下拉菜单旁边显示选择计数器。默认情况下，管理员变更列表会显示它（actions_selection_counter = True）。
    # actions_selection_counter = True

    # 导出数据到txt
    def export_data_to_txt(self, request, queryset):
        # 判断超级用户
        if request.user.is_superuser:
            table_head = list(queryset[0].to_dict().keys())
            table = [[str(item) for item in list(item.to_dict().values())] for item in queryset]
            table.insert(0, table_head)
            with open(os.path.join(settings.BASE_DIR, 'data.txt'), 'a') as f:
                for row in table:
                    f.write('\t'.join(row) + '\r\n')
            # 设置提示信息
            self.message_user(request, '数据导出成功！')
        else:
            # 非超级用户提示警告
            self.message_user(request, '数据导出失败，没有权限！', level=messages.WARNING)

    # 设置函数的显示名称
    export_data_to_txt.short_description = '导出所选数据到txt'

    def export_data_to_excel(self, request, queryset):
        # 判断超级用户
        if request.user.is_superuser:
            table_head = list(queryset[0].to_dict().keys())
            table = [[str(item) for item in list(item.to_dict().values())] for item in queryset]
            table.insert(0, table_head)
            table_sheets = [{'sheet_name': '', 'sheet_data': table}]
            generate_xlsx_file('data.xlsx', table_sheets, settings.BASE_DIR)
            # 设置提示信息
            self.message_user(request, '数据导出成功！')
        else:
            # 非超级用户提示警告
            self.message_user(request, '数据导出失败，没有权限！', level=messages.WARNING)

    export_data_to_excel.short_description = '导出所选数据到excel'

    # 将 date_hierarchy 设置为你的模型中 DateField 或 DateTimeField 的名称，变化列表页将包括一个基于日期的向下扩展。
    date_hierarchy = 'created_time'
    # 该属性覆盖记录字段为空（None、空字符串等）的默认显示值。默认值是 - （破折号）。
    empty_value_display = '-'
    # exclude 是一个要从表单中排除的字段名列表
    # fields 选项在 “添加” 和 “更改” 页面的表单中进行简单的布局修改，比如只显示可用字段的子集，修改它们的顺序，或者将它们分成几行
    # fieldsets 控制管理员 “添加” 和 “更改” 页面的布局。可以完成更复杂的布局需求
    # filter_horizontal 未选择和选择的选项并排出现在两个框中
    # filter_vertical 与 filter_horizontal 相同，但使用垂直显示过滤界面，未选择的选项框出现在选择选项框的上方
    # 设置 list_per_page 来控制每个分页的管理变更列表页面上出现多少个项目。默认情况下，设置为 100。
    list_per_page = 50
    # 设置 list_max_show_all 来控制 “全部显示” 的管理员更改列表页面上可以出现多少个项目
    # 只有当总结果数小于或等于此配置时，管理才会在更改列表中显示 “全部显示” 链接默认情况下，这个配置为 200。
    list_select_related=True
    ordering = ['id']



class BaseUserAdminModel(BaseAdmin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # ('Personal info', {'fields': ('is_staff',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    # 创建用户时显示
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'phone', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'phone')
    ordering = ('username',)
