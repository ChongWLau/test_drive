# -*- coding: utf-8 -*-
# Django settings for evezy project.
from .common import *

ALLOWED_HOSTS += ['.ngrok.io']

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'evezy_dj_dev.sqlite',              # Or path to database file if using sqlite3.
        'USER': '',              # Not used with sqlite3.
        'PASSWORD': '',       # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS += ('django_extensions', )

PREPEND_WWW = False
