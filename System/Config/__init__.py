import os

import pymysql

pymysql.install_as_MySQLdb()

from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
load_dotenv(env_path)
env = os.environ.get('DJANGO_ENV', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Config.settings.{env}')
