"""
Django settings for fsmedhro project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os


# --- INSTALL ---
# CHANGE "secret_settings.example.py" to your settings and rename it to "secret_settings.py"
from .secret_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'exoral.apps.ExoralConfig',
    'fsmedhrocore.apps.FachschaftConfig',
    'mediathek.apps.MediathekConfig',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_nyt',
    'cms',
    'mptt',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'sorl.thumbnail',
    'easy_thumbnails',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_column',
    'djangocms_forms',
    'aldryn_apphooks_config',
    'aldryn_bootstrap3',
    'cmsplugin_filer_image',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    'cmsplugin_filer_video',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_utils',
    'cmsplugin_filer_tests_shared',
    'parler',
    'taggit',
    'taggit_autosuggest',
    'meta',
    'djangocms_blog',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'djangocms_icon',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
]
# TODO: Blogs dosn't work --> please have a look

ALDRYN_BOILERPLATE_NAME = 'bootstrap3'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'fsmedhrocore.backends.auth.LdapUniHro',
    'django.contrib.auth.backends.ModelBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email.uni-rostock.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

LOGIN_URL = '/login/'
LOGOUT_URL = 'fsmedhro_logout'
LOGIN_REDIRECT_URL = 'fachschaft:fsmedhro_user'

MIDDLEWARE = [
    #'cms.middleware.utils.ApphookReloadMiddleware'
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware'
]

ROOT_URLCONF = 'fsmedhro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings'

            ],
        },
    },
]

CMS_TEMPLATES = [
    ('home.html', 'Standart'),
    ('sidebar_left.html', 'Sidebar Links'),
    ('sidebar_right.html', 'Sidebar Rechts'),
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

WSGI_APPLICATION = 'fsmedhro.wsgi.application'

ALDRYN_BOOTSTRAP3_ICONSETS = [
    ('glyphicons', 'glyphicons', 'Glyphicons'),
    ('fontawesome', 'fa', 'Font Awesome'),
    ('icons', 'icon', 'Custom Icons'),
]
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': '',
#        'NAME': '',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    }
# }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = [
    ('de', 'German'),
    ('en', 'English'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

THUMBNAIL_HIGH_RESOLUTION = True
META_USE_SITES = True
META_SITE_PROTOCOL = 'https'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
# TODO customizing CKEditor as Richttexteditor --> needed for better writing in Pharos-App
#CKEDItor

# WIKI Settings

WIKI_SHOW_MAX_CHILDREN = 15
WIKI_CHECK_SLUG_URL_AVAILABLE = False

WIKI_ANONYMOUS = False
#treats not logged in users not as other users
WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False
#lock account settings in the wiki

#TODO include CKEditor as texteditor
# WIKI_EDITOR = u'static/ckeditor/ckeditor'

WIKI_ANONYMOUS_CREATE = False
WIKI_ANONYMOUS_UPLOAD = False
WIKI_ANONYMOUS_WRITE = False
#lock anonymous writing

WIKI_URL_CASE_SENSITIVE = True


WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'footnotes',
        'attr_list',
        'headerid',
        'extra',
        'codehilite',
    ]
}
