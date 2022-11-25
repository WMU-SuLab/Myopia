# -*- encoding: utf-8 -*-
"""
@File Name      :   project_dev.py
@Create Time    :   2022/11/25 15:54
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

from .project import *

# 阿里云配置
ALIBABACLOUD_OSS_ENDPOINT = ALIBABACLOUD_OSS_ENDPOINT_TEST
ALIBABACLOUD_OSS_BUCKET_NAME = ALIBABACLOUD_OSS_BUCKET_NAME_TEST
ALIBABACLOUD_OSS_BUCKET_DOMAIN = ALIBABACLOUD_OSS_BUCKET_DOMAIN_TEST

# 顺丰快递配置
SF_EXPRESS_URL = SF_EXPRESS_URL_TEST
SF_EXPRESS_SAMPLE_APP_CHECKWORD = SF_EXPRESS_SAMPLE_APP_CHECKWORD_TEST
