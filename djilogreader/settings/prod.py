from djilogreader.settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['18.223.162.25', 'ec2-18-223-162-25.us-east-2.compute.amazonaws.com']

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
MEDIA_URL = 'http://ec2-18-223-162-25.us-east-2.compute.amazonaws.com/media/profiles/'
