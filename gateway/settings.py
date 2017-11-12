"""
Django settings for gateway project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import configparser
import os
import sys
import dj_database_url
import django_cache_url
from kombu import Exchange, Queue


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jksd@$=t_y2_epxck%_^%6mk$l8e6&mq)*++s%q6%yyk3!1v&x'

try:
    gateway_config = configparser.ConfigParser()
    with open(os.path.join(BASE_DIR, 'gateway.cfg')) as gateway_config_file:
        gateway_config.read_file(gateway_config_file)

    DASHD_RPCUSER = gateway_config.get('dashd_credentials', 'rpcuser')
    DASHD_RPCPASSWORD = gateway_config.get('dashd_credentials', 'rpcpassword')
    DASHD_ACCOUNT_NAME = gateway_config.get(
        'dashd_credentials', 'account_name'
    )
    DASHD_MINIMAL_CONFIRMATIONS = int(
        gateway_config.get('dashd_credentials', 'minimal_confirmations'),
    )

    RIPPLE_ACCOUNT = gateway_config.get('ripple_credentials', 'account')
    RIPPLE_SECRET = gateway_config.get('ripple_credentials', 'secret')
    RIPPLE_API_DATA = [
        {'RIPPLE_API_URL': 'https://s1.ripple.com:51234'},
    ]
except (configparser.NoOptionError, configparser.NoSectionError) as e:
    raise Exception(
        "Please add all needed credentials to 'gateway.cfg'. {}".format(e)
    )
except IOError:
    raise Exception(
        "Please make sure a configuration file 'gateway.cfg' exists"
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('Yaroslav Luzin', 'jardev@gmail.com'),
)
MANAGERS = ADMINS

# Application definition
sys.path.append(os.path.join(BASE_DIR, 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ripple_api',
    'compressor',
    'webpack_loader',
    'ckeditor',

    'apps.core',
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

ROOT_URLCONF = 'gateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'string_if_invalid': '<< MISSING VARIABLE "%s" >>' if DEBUG else ''
        },
    },
]

WSGI_APPLICATION = 'gateway.wsgi.application'

CACHES = {'default': django_cache_url.config()}

if os.environ.get('REDIS_URL'):
    CACHES['default'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL')}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://gw_user:gw_pass@localhost:5432/gateway',
        conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# DJANGO COMPRESS
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile} --autoprefix="last 2 versions"'),
)
COMPRESS_YUI_BINARY = ('java -jar "/usr/share/yui-compressor/'
                       'yui-compressor.jar"')

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WEBPACK LOADER
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'gateway': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'ripple': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Redis
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')

RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL',
                            '')
if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq,
# so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10

# Celery configuration

# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively,
# change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

# Set redis as celery result backend
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_REDIS_MAX_CONNECTIONS = 1

# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000

# Try to load settings from ``settings_local.py`` file
try:
    from settings_local import *  # NOQA
except ImportError, e:
    sys.stderr.write('settings_local.py not found. Using default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
