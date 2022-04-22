# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py    
@Create Time    :   2022/4/22 15:31
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


class Feedback(Base):
    progress_choices = (
        (0, '未查看'),
        (1, '已查看，未处理'),
        (2, '正在处理'),
        (3, '处理完毕'),
    )
    phone = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='手机号')
    email = models.EmailField(max_length=32, blank=True, null=True, default=None,  verbose_name='邮箱')
    content = models.TextField(max_length=1024, blank=True, null=True, default=None, verbose_name='反馈内容')
    user_info = models.JSONField(blank=True, null=True, default=None, verbose_name='用户额外信息')
    progress = models.IntegerField(choices=progress_choices, blank=True, null=True, default=0, verbose_name='处理进度')
    start_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='开始处理时间')
    end_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='处理完毕时间')

    @property
    def handle_all_time(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return '未开始处理'

    class Meta:
        verbose_name = verbose_name_plural = '用户反馈'

    def __str__(self):
        return f'<feedback :phone:{self.phone},email:{self.email}>'
