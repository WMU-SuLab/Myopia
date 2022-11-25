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

from .project_dev import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DJANGO_ENV = 'develop'

# 日志配置
LOGGING = {
    # 使用的python内置的logging模块，python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'version': 1,
    # 是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭。
    'disable_existing_loggers': False,
    # 日志记录格式
    'formatters': {
        # levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    # 过滤器：可以对日志进行输出时的过滤用的
    'filters': {
        # 在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # 和上面相反
        # 'require_debug_false': {
        #     '()': 'django.utils.log.RequireDebugFalse',
        # },
    },
    # 日志处理方式，日志实例
    'handlers': {
        # 在控制台输出时的实例
        'console': {
            # 日志等级；debug是最低等级，那么只要比它高等级的信息都会被记录
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],
            # 使用的python的logging模块中的StreamHandler来进行输出
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            # 注意，你的文件应该有读写权限。
            'filename': os.path.join(DJANGO_LOGS_DIR_PATH, "system.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'default',
            # 设置默认编码，否则打印出来汉字乱码
            'encoding': 'utf-8',
        },
    },
    # 日志对象
    'loggers': {
        # 和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
        # 'django': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
        # # 只显示数据库查询语句
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     # 冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True
        #     # 不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
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
    #         'NAME': os.environ.get('TEST_DATABASE_DEFAULT_NAME_DEV', 'MyopiaTest'),
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

