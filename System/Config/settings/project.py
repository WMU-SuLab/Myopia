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

# SimpleUI settings

# Hash
# 必须使用Fernet.generate_key()生成，而且是字节类型
CRYPTOGRAPHY_SECRET_KEY = os.environ.get('CRYPTOGRAPHY_SECRET_KEY', Fernet.generate_key().decode())

# Project settings
SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN', 'localhost')
SERVER_PORT = os.environ.get('SERVER_PORT', '8000')

# 数据文件夹
DATA_DIR_PATH = os.path.join(BASE_DIR, 'data')
RELATIVE_DATA_DIR_PATH = 'data'
# 数据库相关文件夹
EXPORT_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'export')
RELATIVE_EXPORT_DATA_DIR_PATH = os.path.join(RELATIVE_DATA_DIR_PATH, 'export')
IMPORT_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'import')
RELATIVE_IMPORT_DATA_DIR_PATH = os.path.join(RELATIVE_DATA_DIR_PATH, 'import')
IMPORT_JSON_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'json')
RELATIVE_IMPORT_JSON_DIR_PATH = os.path.join(RELATIVE_IMPORT_DATA_DIR_PATH, 'json')
IMPORT_SQL_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'sql')
RELATIVE_IMPORT_SQL_DIR_PATH = os.path.join(RELATIVE_IMPORT_DATA_DIR_PATH, 'sql')
IMPORT_XLSX_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'xlsx')
RELATIVE_IMPORT_XLSX_DIR_PATH = os.path.join(RELATIVE_IMPORT_DATA_DIR_PATH, 'xlsx')
IMPORT_XLS_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'xls')
RELATIVE_IMPORT_XLS_DIR_PATH = os.path.join(RELATIVE_IMPORT_DATA_DIR_PATH, 'xls')
IMPORT_CSV_DIR_PATH = os.path.join(IMPORT_DATA_DIR_PATH, 'csv')
RELATIVE_IMPORT_CSV_DIR_PATH = os.path.join(RELATIVE_IMPORT_DATA_DIR_PATH, 'csv')

# 用户数据文件夹（非存储到数据库）
USER_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'user')
RELATIVE_USER_DATA_DIR_PATH = os.path.join(RELATIVE_DATA_DIR_PATH, 'user')
USER_IMAGES_DIR_PATH = os.path.join(USER_DATA_DIR_PATH, 'images')
RELATIVE_USER_IMAGES_DIR_PATH = os.path.join(RELATIVE_USER_DATA_DIR_PATH, 'images')
AVATAR_DIR_PATH = os.path.join(USER_IMAGES_DIR_PATH, 'avatar')
RELATIVE_AVATAR_DIR_PATH = os.path.join(RELATIVE_USER_IMAGES_DIR_PATH, 'avatar')
EYE_GROUND_DIR_PATH = os.path.join(USER_IMAGES_DIR_PATH, 'eye_ground')
RELATIVE_EYE_GROUND_DIR_PATH = os.path.join(RELATIVE_USER_IMAGES_DIR_PATH, 'eye_ground')
INFORMED_CONSENT_DIR_PATH = os.path.join(USER_IMAGES_DIR_PATH, 'informed_consent')
RELATIVE_INFORMED_CONSENT_DIR_PATH = os.path.join(RELATIVE_USER_IMAGES_DIR_PATH, 'informed_consent')
USER_PDF_DIR_PATH = os.path.join(USER_DATA_DIR_PATH, 'pdf')
RELATIVE_USER_PDF_DIR_PATH = os.path.join(RELATIVE_USER_DATA_DIR_PATH, 'pdf')
DATA_DIR_PATH_LIST = [
    # 数据文件夹
    DATA_DIR_PATH,
    # 数据库导出数据文件夹
    EXPORT_DATA_DIR_PATH,
    # 数据库导入数据文件夹
    IMPORT_DATA_DIR_PATH, IMPORT_JSON_DIR_PATH, IMPORT_SQL_DIR_PATH, IMPORT_XLSX_DIR_PATH,
    IMPORT_XLS_DIR_PATH, IMPORT_CSV_DIR_PATH,
    # 用户数据文件夹
    USER_DATA_DIR_PATH,
    USER_IMAGES_DIR_PATH, AVATAR_DIR_PATH, EYE_GROUND_DIR_PATH, INFORMED_CONSENT_DIR_PATH,
    USER_PDF_DIR_PATH,
]

# 日志文件夹
LOGS_DIR_PATH = os.path.join(BASE_DIR, 'logs')
RELATIVE_LOGS_DIR_PATH = 'logs'
DJANGO_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'django')
RELATIVE_DJANGO_LOGS_DIR_PATH = os.path.join(RELATIVE_LOGS_DIR_PATH, 'django')
GUNICORN_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'gunicorn')
RELATIVE_GUNICORN_LOGS_DIR_PATH = os.path.join(RELATIVE_LOGS_DIR_PATH, 'gunicorn')
SUPERVISOR_LOGS_DIR_PATH = os.path.join(LOGS_DIR_PATH, 'supervisor')
RELATIVE_SUPERVISOR_LOGS_DIR_PATH = os.path.join(RELATIVE_LOGS_DIR_PATH, 'supervisor')
LOGS_DIR_PATH_LIST = [
    LOGS_DIR_PATH,
    DJANGO_LOGS_DIR_PATH,
    GUNICORN_LOGS_DIR_PATH,
    SUPERVISOR_LOGS_DIR_PATH,
]

# MINA微信小程序应用配置
# 谱希基因采样小程序应用配置
SAMPLE_APP_ID = os.environ.get('SAMPLE_APP_ID', '')
SAMPLE_APP_SECRET = os.environ.get('SAMPLE_APP_SECRET', '')

# 高度近视筛查小程序应用配置
SCREENING_APP_ID = os.environ.get('SCREENING_APP_ID', '')
SCREENING_APP_SECRET = os.environ.get('SCREENING_APP_SECRET', '')

# 高度近视报告小程序应用配置
SCREENING_REPORT_APP_ID = os.environ.get('SCREENING_REPORT_APP_ID', '')
SCREENING_REPORT_APP_SECRET = os.environ.get('SCREENING_REPORT_APP_SECRET', '')

WECHAT_MINAS = {
    'sample': {
        'app_id': SAMPLE_APP_ID,
        'app_secret': SAMPLE_APP_SECRET,
        'secret_key': SAMPLE_APP_SECRET,
    },
    'screening': {
        'app_id': SCREENING_APP_ID,
        'app_secret': SCREENING_APP_SECRET,
        'secret_key': SCREENING_APP_SECRET,
    },
    'screening_report': {
        'app_id': SCREENING_REPORT_APP_ID,
        'app_secret': SCREENING_REPORT_APP_SECRET,
        'secret_key': SCREENING_REPORT_APP_SECRET,
    },
}

# 微信开放平台配置
WECHAT_OPEN_PLATFORMS = {

}

# 阿里云API配置
ALIBABACLOUD_ACCOUNT_ID = os.environ.get('ALIBABACLOUD_ACCOUNT_ID', '')
ALIBABACLOUD_SMS_ACCESS_KEY_ID = os.environ.get('ALIBABACLOUD_SMS_ACCESS_KEY_ID', '')
ALIBABACLOUD_SMS_ACCESS_KEY_SECRET = os.environ.get('ALIBABACLOUD_SMS_ACCESS_KEY_SECRET', '')
ALIBABACLOUD_OSS_ACCESS_KEY_ID = os.environ.get('ALIBABACLOUD_OSS_ACCESS_KEY_ID', '')
ALIBABACLOUD_OSS_ACCESS_KEY_SECRET = os.environ.get('ALIBABACLOUD_OSS_ACCESS_KEY_SECRET', '')
ALIBABACLOUD_OSS_ENDPOINT = os.environ.get('ALIBABACLOUD_OSS_ENDPOINT', '')
ALIBABACLOUD_OSS_ENDPOINT_TEST = os.environ.get('ALIBABACLOUD_OSS_ENDPOINT_TEST','')
ALIBABACLOUD_OSS_BUCKET_NAME = os.environ.get('ALIBABACLOUD_OSS_BUCKET_NAME', '')
ALIBABACLOUD_OSS_BUCKET_NAME_TEST = os.environ.get('ALIBABACLOUD_OSS_BUCKET_NAME_TEST', '')
ALIBABACLOUD_OSS_BUCKET_DOMAIN = os.environ.get('ALIBABACLOUD_OSS_BUCKET_DOMAIN', '')
ALIBABACLOUD_OSS_BUCKET_DOMAIN_TEST = os.environ.get('ALIBABACLOUD_OSS_BUCKET_DOMAIN_TEST', '')

# 短信过期时间
SMS_EXPIRED_TIME = int(os.environ.get('SMS_EXPIRED_TIME', 600))

# 验证码长度
VERIFICATION_CODE_LENGTH = int(os.environ.get('VERIFICATION_CODE_LENGTH', 6))

# 顺丰API配置
SF_EXPRESS_URL = os.environ.get('SF_EXPRESS_URL', 'https://bspgw.sf-express.com/std/service')
SF_EXPRESS_URL_TEST = os.environ.get('SF_EXPRESS_URL_TEST', 'https://sfapi-sbox.sf-express.com/std/service')
SF_EXPRESS_URL_HK = os.environ.get('SF_EXPRESS_URL_HK', 'https://sfapi-hk.sf-express.com/std/service')
# 采样小程序应用配置
SF_EXPRESS_SAMPLE_APP_PARTNER_ID = os.environ.get('SF_EXPRESS_SAMPLE_APP_PARTNER_ID', '')
SF_EXPRESS_SAMPLE_APP_CHECKWORD = os.environ.get('SF_EXPRESS_SAMPLE_APP_CHECKWORD', '')
SF_EXPRESS_SAMPLE_APP_CHECKWORD_TEST = os.environ.get('SF_EXPRESS_SAMPLE_APP_CHECKWORD_TEST', '')

# 谱希基因额外配置
SAMPLE_APP_LIMS_TGFBI_URL = os.environ.get('SAMPLE_APP_LIMS_TGFBI_URL', '')
