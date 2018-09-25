from djilogreader.settings.base import *


SECRET_KEY = get_env_variable('SECRET_KEY')


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