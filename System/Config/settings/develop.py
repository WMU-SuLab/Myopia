# -*- encoding: utf-8 -*-
"""
@File Name      :   develop.py    
@Create Time    :   2022/4/4 11:54
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

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
    },
}

# 设置数据库
DATABASES = {
    'default': {
        # 这个数据库是默认的sqlite数据库，测试用的数据库默认是存放于内存中
        'ENGINE': 'django.db.backends.sqlite3',
        # 测试环境的时候保持长连接
        'CONN_MAX_AGE': None,
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'myopia.sqlite3'),
        'OPTIONS': {
            'timeout': 60,
        },
    },
}
