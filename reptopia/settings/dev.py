# 개발 설정
import os

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_4)b6r!_+d5ywsyj-ra#txsm+&0x5v#*esn+xi8$5h$%hfn5ky'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS += [
    'gallery',
]

WSGI_APPLICATION = 'reptopia.wsgi.dev.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


EMAIL_HOST_PASSWORD = 'WOwls*#73'
