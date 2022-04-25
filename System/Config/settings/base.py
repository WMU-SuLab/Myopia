# -*- encoding: utf-8 -*-
"""
@File Name      :   base.py    
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

import os
from datetime import timedelta
from zoneinfo import ZoneInfo

from . import BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
DEFAULT_CHARSET = 'utf-8'
# SECURITY WARNING: keep the secret key used in production secret!
# 使用from django.core.management.utils import get_random_secret_key 生成 secret_key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-secret-key')
# django-hashid-field插件的id加密配置
HASHID_FIELD_SALT = os.environ.get('HASHID_FIELD_SALT', 'WMU-SuLab hashids salt secret key')
# 允许的主机
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # simpleui需要保证在django.contrib.admin之前，以保证admin页面会被覆盖和自定义的admin模板能够正常使用
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mysql',
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'Common',
    'Screening',
    'UserService',
]

AUTH_USER_MODEL = 'Common.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Common.utils.middlewares.JSONMiddleware',
    'Common.utils.middlewares.DisableDRFCSRFCheckMiddleware'
]

ROOT_URLCONF = 'Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Common', 'templates'),
            os.path.join(BASE_DIR, 'Screening', 'templates'),
            os.path.join(BASE_DIR, 'UserService', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['django.templatetags.static'],
        },
    },
]

WSGI_APPLICATION = 'Config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 缓存配置
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
TZ_INFO = ZoneInfo(TIME_ZONE)

USE_TZ = True

USE_I18N = True
# 数据和时间格式
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'Common', 'static')
# 引用位于 STATIC_ROOT 中的静态文件时要使用的 URL
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    'Common/static_dev',
    'Screening/static',
    'UserService/static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 插件配置
# django-rest-framework插件配置
REST_FRAMEWORK = {
    # 权限
    # 'DEFAULT_PERMISSION_CLASSES': (
    # 'rest_framework.permissions.DjangoModelPermissions',
    # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    # 'rest_framework.permissions.IsAuthenticated',
    # ),
    # jwt
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 返回格式
    'DEFAULT_RENDERER_CLASSES': [
        # 自定义的JSONRenderer
        'Common.utils.http.renderer.JSONRenderer',
        # 原版drf的JSONRenderer
        # 'rest_framework.renderers.JSONRenderer',
        # drf在api查看界面的数据显示模式，加上这个模式后，会显示页面
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 异常处理
    'EXCEPTION_HANDLER': 'Common.utils.http.exceptions.exception_handler',
    # 文档
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 节流
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}

# 校验后端
# AUTHENTICATION_BACKENDS 的顺序很重要，所以如果同一个用户名和密码在多个后端都有效，Django 会在第一个正向匹配时停止处理
# 如果一个后端抛出 PermissionDenied 异常，则验证流程立马终止，Django 不会继续检查其后的后端
AUTHENTICATION_BACKENDS = (
    'Common.utils.auth.backends.UserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# django-rest-framework-simplejwt插件配置：https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    # ACCESS_TOKEN有效时间
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # REFRESH_TOKEN有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # 刷新REFRESH_TOKEN
    'ROTATE_REFRESH_TOKENS': False,
    # 刷新REFRESH_TOKEN之后把之前的那个REFRESH_TOKEN放入黑名单
    'BLACKLIST_AFTER_ROTATION': False,
    # 登录一次更新一下数据库，如果设置为True最好进行节流，否则会让数据库访问变慢
    'UPDATE_LAST_LOGIN': False,

    # 要使用对称HMAC签名和验证，可以使用以下算法可选:'HS256','HS384','HS512'
    # 当选择HMAC算法时，SIGNING_KEY设置将被用作签名密钥和验证密钥。在这种情况下，VERIFYING_KEY设置将被忽略
    # 要使用非对称RSA签名和验证，可以使用以下算法:'RS256','RS384','RS512'
    # 当选择RSA算法时，SIGNING_KEY必须设置为包含RSA私钥的字符串。同样，VERIFYING_KEY设置必须设置为包含RSA公钥的字符串
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    # 对判断TOKEN是否过期进行一些时间的延长，int类型或者datetime.timedelta
    'LEEWAY': 0,

    # 需要身份验证的视图将接受的授权头类型，形如：('Bearer', 'JWT')
    'AUTH_HEADER_TYPES': ('Bearer',),
    # 用于身份验证的授权头名称。默认值是HTTP_AUTHORIZATION，它将接受请求中的Authorization头。
    # 例如，如果你想在你的请求头中使用X_Access_Token，请在你的设置中将AUTH_HEADER_NAME指定为HTTP_X_ACCESS_TOKEN。
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 来自用户模型的数据库字段，将包含在生成的标识用户的令牌中
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    # 确定是否允许用户进行身份验证，此规则在处理有效的令牌后应用。用户对象作为参数传递给可调用对象。
    # 默认规则是检查is_active标志是否仍然为True。可调用对象必须返回一个布尔值，如果被授权则返回True，否则返回False，结果是401状态码。
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    # 指定允许验证身份的令牌类型
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
        # 'rest_framework_simplejwt.tokens.SlidingToken'
    ),
    # 指定类中那个字段指明了TOKEN的类型
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'Common.models.user.User',
    # 'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    # 'TOKEN_USER_CLASS': 'django.contrib.auth.models.User',

    # 用于存储令牌唯一标识符的声明名称。该标识符用于识别黑名单应用程序中被撤销的令牌。在某些情况下，可能需要使用默认的“jti”声明之外的另一个声明来存储该值。
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# drf-spectacular文档配置
SPECTACULAR_SETTINGS = {
    'TITLE': 'Myopia Project API',
    'DESCRIPTION': 'Myopia System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# 跨域相关设置
# 允许所有人访问
CORS_ORIGIN_ALLOW_ALL = True
# 或者指定白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://localhost:8000',
)
# 指明在跨域访问中，后端是否支持对cookie的操作
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 邮件配置
# 管理员邮箱配置
ADMINS = (
    ('diklios', '1061995104@qq.com'),
)
MANAGERS = (
    ('xingsl', 'xingsl@wmu.edu.cn'),
)
# 发送邮件的后端
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件smtp服务地址
EMAIL_HOST = 'smtp.126.com'
# EMAIL_HOST = "smtp.163.com"
# EMAIL_HOST = 'smtp.qq.com'
# SMTP端口号
# 默认是25，当其他端口号Connection unexpectedly closed的时候不妨试试默认的
# EMAIL_PORT = 25
# 服务器默认不能使用25端口，需要根据使用的邮件服务商情况改为别的端口
# EMAIL_USE_SSL和EMAIL_USE_TLS是互斥的，即只能有一个为True。
EMAIL_PORT = 465
# 是否启动SSL链接(安全链接)，默认False，它通常在 465 端口使用
EMAIL_USE_SSL = True
# EMAIL_PORT = 587
# 与SMTP服务器通信时，是否启动TLS链接(安全链接)，默认False，这用于显式 TLS 连接，一般在 587 端口
# EMAIL_USE_TLS = True
# ssl_certfile
EMAIL_SSL_CERTFILE = None
# ssl_keyfile
EMAIL_SSL_KEYFILE = None
# 超时，单位：s（秒）
# EMAIL_TIMEOUT= None
EMAIL_TIMEOUT = 20
# 是否以当地时区（True）或UTC（False）发送SMTP Date 邮件头
EMAIL_USE_LOCALTIME = True
# 邮箱登录用户名
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# 邮箱登录密码
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# 邮件标题前缀，默认是'[django]'
EMAIL_SUBJECT_PREFIX = '[WMU-IBBD]'
# 错误信息来自的电子邮件地址，例如发送到 ADMINS 和 MANAGERS 的邮件，这个地址只用于错误信息，它不是用 send_mail() 发送普通邮件的地址
SERVER_EMAIL= EMAIL_HOST_USER
# 邮件发送人地址，默认电子邮件地址，用于网站管理员的各种自动通信
# fred @ example.com 和 Fred < fred @ example.com > 形式都是合法的
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
