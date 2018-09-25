from djilogreader.settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = get_env_variable('SECRET_KEY')


# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE'),
        'USER': get_env_variable('USER'),
        'PASSWORD': get_env_variable('PASSWORD'),
        'HOST': get_env_variable('HOST'),
        'PORT': '5432',
    }
}


# Static files

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'profiles')
MEDIA_URL = '/profiles/'

