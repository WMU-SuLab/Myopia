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

from .project import *

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
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'myopia-test.sqlite3'),
        }
    },
    # 'default': {
    #     # 如果使用MySQL数据库，会重新建一个test_项目名称_db的数据库，或者自己手动配置
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': os.environ.get('DATABASE_DEFAULT_DOMAIN_DEV', '127.0.0.1'),
    #     'PORT': os.environ.get('DATABASE_DEFAULT_PORT_DEV', '3306'),
    #     # 'PORT': os.environ.get('DATABASE_DEFAULT_PORT_DEV','33060'),
    #     'NAME': os.environ.get('DATABASE_DEFAULT_NAME_DEV', 'Myopia'),
    #     'USER': os.environ.get('DATABASE_DEFAULT_USER_DEV', 'root'),
    #     'PASSWORD': os.environ.get('DATABASE_DEFAULT_PASSWORD_DEV', '123456'),
    #     'OPTIONS': {
    #         # 'init_command': 'SET default_storage_engine=INNODB;',
    #         'charset': 'utf8mb4',
    #         # 'timezone': 'Asia/Shanghai',
    #         # 'timeout': 60,
    #     },
    #     # gevent和多线程的时候不要用
    #     # 'CONN_MAX_AGE': 36000,
    #     'TEST': {
    #         'NAME': os.environ.get('DATABASE_DEFAULT_NAME_TEST_DEV', 'MyopiaTest'),
    #     }
    # },
}

# 开发环境下的邮件配置
EMAIL_PORT = 25
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
MANAGERS = (
    ('diklios', '1061995104@qq.com'),
)
