# -*- coding: utf-8 -*-
from pathlib import Path

import tldextract

BASE_DIR = Path(__file__).resolve().parent.parent

REPO_NAME = str(BASE_DIR.name)

# TLD Extract allows repository names to be domain names for
# website repositories, using the TLD as the PROJECT_NAME.
# Hyphens must be removed as they are not valid in Python modules.
PROJECT_NAME = tldextract.extract(REPO_NAME).domain.replace("-", "")

ALLOWED_HOSTS = [
    'localhost'
]

"""
Define email settings
"""

MANAGERS = ADMINS = (
    ('Nick Jones', 'nick@evezy.co.uk'),
)


"""
Define localisation settings
"""

LANGUAGE_CODE = 'en-gb'

LANGUAGES = (('en-gb', 'English'),)

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True

"""
Define media settings
"""

MEDIA_ROOT = str(BASE_DIR.joinpath(PROJECT_NAME).joinpath("media"))

MEDIA_URL = '/media/'

STATIC_ROOT = str(BASE_DIR.joinpath("_collectstatic"))

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(BASE_DIR.joinpath(PROJECT_NAME).joinpath("static")),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


"""
Define project operation settings
"""

PREPEND_WWW = True

SITE_ID = 1

WSGI_APPLICATION = "config.wsgi.application"


"""
Define request and response settings
"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR.joinpath(PROJECT_NAME).joinpath("templates")),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
            ],
        },
    },
]

"""
Define debug & test settings
"""

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'


"""
Define applications
"""

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    # 'django.contrib.redirects',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.staticfiles',
    'rvme.users',
)

THIRD_PARTY_APPS = (
    # 'cms',
    # 'filer',
    # 'cmsplugin_filer_file',
    # 'cmsplugin_filer_folder',
    # 'cmsplugin_filer_link',
    # 'cmsplugin_filer_image',
    # 'cmsplugin_filer_teaser',
    # 'cmsplugin_filer_video',
    # 'cmsplugin_form_handler',
    # 'crispy_forms',
    # 'crispy_forms_foundation',
    # Wait for 1.11 support
    # 'djangocms_column',
    # 'django_filters',
    # 'django_select2',
    # 'djangocms_snippet',
    # 'djangocms_style',
    # 'djangocms_text_ckeditor',
    # 'djstripe',
    # 'easy_thumbnails',
    # 'core',
    # 'core.contrib.djangocms_generics',
    # 'djangocms_admin_style',
    # 'macros',
    # 'menus',
    # 'mptt',
    # 'multiselectfield',
    # 'oauth2_provider',
    # 'ordered_model',
    # 'private_storage',
    # 'qurl_templatetag',
    # 'rest_framework',
    # 'reversion',
    # 'sekizai',
    # 'treebeard',
)

LOCAL_APPS = (
    'rvme',
    'rvme.bookings',
    'rvme.core',
    'rvme.services',
    'rvme.services.surecam',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


"""
Define remaining settings
"""
ROOT_URLCONF = 'rvme.urls'


"""
Common settings
"""

AUTH_USER_MODEL = 'users.User'

DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'EVezy <no-reply@evezy.co.uk>'
REPLY_TO_EMAIL = [DEFAULT_FROM_EMAIL]

EMAIL_SUBJECT_PREFIX = '[Django: EVezy] '

INFO_EMAIL = "info@evezy.co.uk"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*btr#)=*fk3gvdb9mbp(*9af#vs+62qx&$bmi_vikevb5wk_h9'