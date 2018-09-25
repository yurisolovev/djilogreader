import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'bootstrap4',
    'sorl.thumbnail',
    'django_countries',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djilogreader.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'djilogreader.wsgi.application'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'


# Authentication settings

LOGOUT_REDIRECT_URL = 'core:login'


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'profiles')
MEDIA_URL = '/profiles/'


# Date input settings

DATE_INPUT_FORMATS = [
    '%d.%m.%Y%', '%m.%d.%Y', '%d.%m.%y',  # '25.10.2006', '10.25.2006', '25.10.06'
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',   # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',              # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',              # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',              # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',              # '25 October 2006', '25 October, 2006'
]
