# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/7/4 19:01
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

from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi import models as open_api_models
from django.conf import settings

# SMS配置
sms_config = open_api_models.Config(
    # 您的AccessKey ID,
    access_key_id=settings.ALIBABACLOUD_SMS_ACCESS_KEY_ID,
    # 您的AccessKey Secret,
    access_key_secret=settings.ALIBABACLOUD_SMS_ACCESS_KEY_SECRET,
)
# 访问的域名
sms_config.endpoint = 'dysmsapi.aliyuncs.com'
# config.endpoint='sms@1659548102989549.onaliyun.com'

# 创建客户端
sms_client = Client(sms_config)
