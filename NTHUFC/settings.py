#-*- encoding=UTF-8 -*-
"""
Django settings for NTHUFC project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from func import get_config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6(22##hs25803n-k!cx!$^l@16-$_ke-8s9h=bkw+ytcx%mc8e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'index',
    'photos',
    'users',
    'crispy_forms',
    'locationMarker',
    'axes',
    'djangobower',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'users.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'NTHUFC.urls'

WSGI_APPLICATION = 'NTHUFC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

CONFIG_PATH = os.path.join(BASE_DIR, 'NTHUFC/config/NTHUFC.cfg')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': CONFIG_PATH,
        },
    }
};
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#django-crispy-forms setting
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#axe-settings
AXES_USE_USER_AGENT = True
AXES_LOGIN_FAILURE_LIMIT = 5
#hours
AXES_COOLOFF_TIME = 24
AXES_LOCKOUT_URL = '/users/locked'

# django-bower settings
BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_INSTALLED_APPS = (
    'jquery',
    'https://github.com/FortAwesome/Font-Awesome.git',
    'https://github.com/bootstrap-tagsinput/bootstrap-tagsinput.git',
    'https://github.com/twitter/typeahead.js.git',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_config('client', 'email_account')
EMAIL_HOST_PASSWORD = get_config('client', 'email_password')

EMAIL_PORT = 587


