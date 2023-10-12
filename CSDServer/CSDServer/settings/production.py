from .base import *

# 운영환경

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # 운영하는 서버

ALLOWED_HOSTS = ['54.180.116.175', '*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
