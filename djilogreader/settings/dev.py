from djilogreader.settings.base import *


SECRET_KEY = 'dev_secret_key'


# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djilogreader_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Email settings

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'djilogreader@yandex.ru'
