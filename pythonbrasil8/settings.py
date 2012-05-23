# coding: utf-8
import os
# Django settings for pythonbrasil8 project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pythonbrasil8.sqlite3',
    }
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en-us', 'English'),
    ('pt-br', u'Português'),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static_files'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = 'i)=$2sz)alxoe0v9qtpur*_cmwyxuft!#w=#i3)=+4fvu1*)ex'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pythonbrasil8.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pythonbrasil8.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = ['--quiet', "-sd", '--nologcapture']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'pythonbrasil8.core',
    'mittun.events',
    'mittun.registration',
    'mittun.sponsors',
    'django.contrib.admin',
    'django_nose',
    'compressor',
    'south',
    'registration',
    'pythonbrasil8.dashboard',
    'pythonbrasil8.schedule',
    'pythonbrasil8.subscription',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/dashboard/'

EMAIL_PORT = 25
EMAIL_USE_TLS = True

AUTH_PROFILE_MODULE = 'dashboard.AccountProfile'

PAGSEGURO = {
    'email': 'ps@pythonbrasil.org.br',
    'charset': 'UTF-8',
    'token': 'radiogaga',
    'currency': 'BRL',
    'itemId1': '0001',
    'itemDescription1': u'Inscrição na PythonBrasil 2012',
    'itemQuantity1': 1,
}

PAGSEGURO_BASE = 'https://ws.pagseguro.uol.com.br/v2'
PAGSEGURO_CHECKOUT = '%s/checkout' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS = '%s/transactions' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS_NOTIFICATIONS = '%s/notifications' % PAGSEGURO_TRANSACTIONS

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = False

try:
    from settings_local import *
except ImportError:
    pass
>>>>>>> upstream/master
