# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2022/4/26 17:07
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

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        # 只显示数据库查询语句
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DATABASE_DEFAULT_DOMAIN_TEST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASE_DEFAULT_PORT_TEST', '3306'),
        'NAME': os.environ.get('DATABASE_DEFAULT_NAME_TEST', 'Myopia'),
        'USER': os.environ.get('DATABASE_DEFAULT_USER_TEST', 'root'),
        'PASSWORD': os.environ.get('DATABASE_DEFAULT_PASSWORD_TEST', ''),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'TEST': {
            'NAME': os.environ.get('DATABASE_DEFAULT_NAME_TEST', 'MyopiaTest'),
        }
    },
}

MANAGERS = (
    ('diklios', '1061995104@qq.com'),
)
