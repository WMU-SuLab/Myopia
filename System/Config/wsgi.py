"""
WSGI config for Manage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"))
env = os.environ.get('DJANGO_ENV', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Config.settings.{env}')

application = get_wsgi_application()
