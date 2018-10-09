from djilogreader.settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['13.58.80.238', 'djilogreader.ml']

SECRET_KEY = get_env_variable('SECRET_KEY')


# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('PASSWORD'),
        'HOST': get_env_variable('HOST'),
        'PORT': '5432',
    }
}


# Static files

STATIC_ROOT = '/home/ubuntu/static/'


# Media files

MEDIA_ROOT = '/home/ubuntu/media/profiles/'
MEDIA_URL = 'https://djilogreader.ml/media/profiles/'


# Email settings

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'djilogreader@yandex.ru'
