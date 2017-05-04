"""
Django settings for smolkinsite project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url
import logging


# Need to have a separate logger configured for the settings file, cannot use the config below for itself
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s", datefmt="%d/%b/%Y %H:%M:%S")
settingsLogger = logging.getLogger(__name__)

# Default application logging verbosity to most abusive setting.
VERBOSITY = os.environ.get('VERBOSITY', 'DEBUG')
settingsLogger.info("The variable VERBOSITY is set to {}".format(VERBOSITY))
# Default django logging verbosity to slightly less abusive.
DJANGO_VERBOSITY = os.environ.get('DJANGO_VERBOSITY', 'INFO')
settingsLogger.info("The variable DJANGO_VERBOSITY is set to {}".format(DJANGO_VERBOSITY))

# Define a basic log configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        # Django Server Logging - handle django.server log requests.
        'django': {
            'handlers': ['console'],
            'level': DJANGO_VERBOSITY,
            'propagate': False,
        },
        # Application Logging - handling logging requests froms songs.views.*, etc.
        'songs': {
            'handlers': ['console'],
            'level': VERBOSITY,
            'propagate': False,
        },
    },
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', "S2yc8RGa7UYB4zHxQDVnhUSWJnY6VCz9CQyhMUZkBx2rwpTGEJDW2VmKFXKR68e")


ALLOWED_HOSTS = []
DEBUG = False

PLATFORM = os.environ.get('C9_HOSTNAME', "remote")
settingsLogger.info("The value of the variable PLATFORM is {}".format(PLATFORM))
if PLATFORM != "remote":
    # local, running on local dev machine
    DEBUG = True
    ALLOWED_HOSTS = ['*']
else:
    # DEBUG should only be True if specifically set to True
    dbgString = os.environ.get('DEBUG', 'False')
    DEBUG = (dbgString == 'True')
    
    # TODO: Not sure what this should be in prod
    try:
        ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(",")
    except KeyError:
        ALLOWED_HOSTS =  "localhost, 127.0.0.1, [::1]".split(",")

settingsLogger.info("The value of the variable DEBUG is {}".format(DEBUG))
settingsLogger.info(" The value of the variable ALLOWED_HOSTS IS {}".format(ALLOWED_HOSTS))

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = not DEBUG

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = not DEBUG

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'songs'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smolkinsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'smolkinsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
