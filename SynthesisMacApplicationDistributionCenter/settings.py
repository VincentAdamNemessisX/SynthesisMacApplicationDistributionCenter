"""
Django settings for SynthesisMacApplicationDistributionCenter project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^jm+at6%5or6_@a-nkx0a_u%sxqp=oo%4szjeqpz_h!6+#)+(h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'django_router',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testunit.apps.TestunitConfig',
    'analytics.apps.AnalyticsConfig',
    'announcements.apps.AnnouncementsConfig',
    'category.apps.CategoryConfig',
    'commentswitharticles.apps.CommentsWithArticlesConfig',
    # 'favorites.apps.FavoritesConfig',
    'frontenduser.apps.FrontEndUserConfig',
    'questions.apps.QuestionsConfig',
    'software.apps.SoftwareConfig',
    "error_handler.apps.ErrorHandlerConfig",
    "components.apps.ComponentsConfig"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'personal_components.append_middleware.AppendMiddleware'
]

ROOT_URLCONF = 'SynthesisMacApplicationDistributionCenter.urls'

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
        },
    },
]

WSGI_APPLICATION = 'SynthesisMacApplicationDistributionCenter.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'HOST': 'localhost',
        'USER': 'root',  # 'localhost database'
        'PASSWORD': 'ic3344',
        # 'HOST': 'vincentadam.icu', # 'remote database'
        # 'USER': 'vincent',
        # 'PASSWORD': '2',
        'NAME': 'synthesisyouwantmacapplicationdistributioncenter',  # database Name dismiss caps
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379',  # local redis
        # 'LOCATION': 'redis://vincentadam.icu:6379', # remote redis
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "DECODE_RESPONSE": True,
            "PASSWORD": "2",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'PRC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# simpleui that backend settings
SIMPLEUI_HOME_PAGE = '/analytics/'
SIMPLEUI_HOME_TITLE = '概览'
SIMPLEUI_LOGO = '/static/favicon.ico'  # left top logo
SIMPLEUI_DEFAULT_THEME = 'e-purple.css'  # default theme
SIMPLEUI_HOME_INFO = False  # disabled home page info in the backend
LOGIN_URL = '/login/'  # login url
