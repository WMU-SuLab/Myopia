# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/4/15 10:23
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

from cryptography.fernet import Fernet

from .base import *

# Hash
# 必须使用Fernet.generate_key()生成，而且是字节类型
CRYPTOGRAPHY_SECRET_KEY = os.environ.get('CRYPTOGRAPHY_SECRET_KEY', Fernet.generate_key().decode())

# Project settings
SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN', 'localhost')
SERVER_PORT = os.environ.get('SERVER_PORT', '8000')

# 数据文件夹
DATA_DIR_PATH = os.path.join(BASE_DIR, 'data')
# 数据库相关文件夹
EXPORT_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'export')
IMPORT_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'import')
IMPORT_JSON_DATA_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'json')
IMPORT_SQL_DATA_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'sql')
IMPORT_XLSX_DATA_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'xlsx')
IMPORT_XLS_DATA_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'xls')
IMPORT_CSV_DATA_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'csv')

# 用户数据文件夹（非存储到数据库）
USER_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'user')
USER_IMAGES_DATA_DIR_PATH = os.path.join(USER_DATA_DIR_PATH, 'images')
AVATAR_DATA_DIR_PATH = os.path.join(USER_IMAGES_DATA_DIR_PATH, 'avatar')
EYE_GROUND_DATA_DIR_PATH = os.path.join(USER_IMAGES_DATA_DIR_PATH, 'eye_ground')
INFORMED_CONSENT_DATA_DIR_PATH = os.path.join(USER_IMAGES_DATA_DIR_PATH, 'informed_consent')
USER_PDF_DATA_DIR_PATH = os.path.join(USER_DATA_DIR_PATH, 'pdf')
DATA_DIR_PATH_LIST = [
    DATA_DIR_PATH,

    EXPORT_DATA_DIR_PATH,

    IMPORT_DATA_DIR_PATH, IMPORT_JSON_DATA_DIR_PATH,

    USER_DATA_DIR_PATH,
    USER_IMAGES_DATA_DIR_PATH, AVATAR_DATA_DIR_PATH, EYE_GROUND_DATA_DIR_PATH, INFORMED_CONSENT_DATA_DIR_PATH,
    USER_PDF_DATA_DIR_PATH,
]

# 日志文件夹
LOGS_DIR_PATH = os.path.join(BASE_DIR, 'logs')
DJANGO_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'django')
GUNICORN_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'gunicorn')
SUPERVISOR_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'supervisor')
LOGS_DIR_PATH_LIST = [
    LOGS_DIR_PATH,
    DJANGO_LOGS_DIR_PATH,
    GUNICORN_LOGS_DIR_PATH,
    SUPERVISOR_LOGS_DIR_PATH,
]

# SimpleUI settings

# MINA
