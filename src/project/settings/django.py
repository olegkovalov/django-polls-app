import os
import sys

import environ

from ._django_apps import DJANGO_APPS, CONTRIB_APPS, PROJECT_APPS

_ = lambda x: x

env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()
root = environ.Path(__file__) - 3

SITE_ROOT = root()

DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = DJANGO_APPS + CONTRIB_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates'), ],
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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': env.db(default='postgresql://postgres@localhost:5432/polls_db')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = env.str('LANGUAGE_CODE', default='en')

TIME_ZONE = env.str('TIME_ZONE', default='UTC')

USE_I18N = env.bool('USE_I18N', default=True)

USE_L10N = env.bool('USE_L10N', default=True)

USE_TZ = env.bool('USE_TZ', default=True)

DATE_INPUT_FORMATS = env.list('DATE_INPUT_FORMATS', default=('%Y.%m.%d',))
DATE_FORMAT = env.str('DATE_FORMAT', default='%Y.%m.%d')
DATETIME_INPUT_FORMATS = env.list('DATETIME_INPUT_FORMATS', default=('%Y-%m-%dT%H:%M:%S.%f%z',))
DATETIME_FORMAT = env.str('DATETIME_FORMAT', default='%Y-%m-%dT%H:%M:%S.%f%z')

PUBLIC_ROOT = root.path('public')
MEDIA_ROOT = PUBLIC_ROOT('media')
STATIC_ROOT = PUBLIC_ROOT('static')
STATICFILES_DIRS = [os.path.join(SITE_ROOT, 'static'), ]
MEDIA_URL = env.str('MEDIA_URL', default='/m/')
STATIC_URL = env.str('STATIC_URL', default='/s/')

AUTH_USER_MODEL = 'accounts.User'

FEATURES = env.tuple('FEATURES', default=())

IS_TESTS_RUN = 'test' in sys.argv

if 'DJANGO_EXTENSIONS' in FEATURES:  # noqa
    INSTALLED_APPS += ['django_extensions']

if IS_TESTS_RUN:  # noqa

    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return "notmigrations"

    MIGRATION_MODULES = DisableMigrations()

    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher', ]

    SECRET_KEY = 'fake-secret-key-for-testing'

    INSTALLED_APPS += ('django_nose', )

else:
    SECRET_KEY = env.str('SECRET_KEY')

    # 'sgbackend.SendGridBackend'
    EMAIL_BACKEND = env.str('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

    REDIS_HOST = env.str('REDIS_HOST', default='localhost')

    CACHE_REDIS_DB = env.int('REDIS_DB', default=4)

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '{}:6379'.format(REDIS_HOST),
            'OPTIONS': {
                'DB': CACHE_REDIS_DB,
            }
        },
    }

    if 'LOG_SQL' in FEATURES:  # noqa
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'sql': {
                    '()': 'loggers.SQLFormatter',
                    'format': '[%(duration).3f] %(statement)s',
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                },
                'sql': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'sql',
                    'level': 'DEBUG',
                },
            },
            'loggers': {
                'django.db.backends': {
                    'handlers': ['sql'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                'django.db.backends.schema': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
            }
        }

if not DEBUG:  # noqa
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', ]
        },
    }
