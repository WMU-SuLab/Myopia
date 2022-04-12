# -*- encoding: utf-8 -*-
"""
@File Name      :   product.py    
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

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s  %(asctime)s  %(module)s  %(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # 如果使用supervisor可以不用配置file，supervisor的会将控制台的内容输出到日志
        # 'file':{
        #     'level':'INFO',
        #     'class':'logging.handlers.RotatingFileHandler',
        #     'filename':os.path.join(BASE_DIR,'logs','system.log'),
        #     'formatter': 'default',
        #     'maxBytes':1024*1024,
        #     'backupCount':5,
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# 数据库配置
DATABASES = {
    'default': {
        # 如果使用MySQL数据库，会重新建一个test_项目名称_db的数据库，或者自己手动配置
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 'PORT': '33060',
        'NAME': 'Myopia',
        'USER': 'root',
        'PASSWORD': os.environ.get('DATABASE_DEFAULT_PASSWORD', ''),
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB;',
            'charset': 'utf8mb4',
            # 'timezone': 'Asia/Shanghai',
            # 'timeout': 60,
        },
        # gevent和多线程的时候不要用
        # 'CONN_MAX_AGE': 36000,
        'TEST': {
            'NAME': 'MyopiaTest'
        }
    },
}
