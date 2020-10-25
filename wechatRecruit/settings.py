"""
Django settings for wechatRecruit project.

Generated by 'django-admin startproject' using Django 2.1.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import configparser
import os
# *******configThis******** get form config.conf 快速切换环境
import sys
from collections import OrderedDict

import djcelery

env = 'dev'
# env = 'prod'
# ***************configThis********************

cf = configparser.ConfigParser()
cf.read(r"./config.conf")

database_name = cf.get(env + '-config', 'NAME')
database_user = cf.get(env + '-config', 'USER')
database_password = cf.get(env + '-config', 'PASSWORD')
database_host = cf.get(env + '-config', 'HOST')
database_port = cf.getint(env + '-config', 'PORT')
invalid_time = cf.getint(env + '-config', 'INVALID_TIME')
log_level = cf.getboolean(env + '-config', 'DEBUG')
email_host = cf.get(env + '-config', 'EMAIL_HOST')
email_port = cf.getint(env + '-config', 'EMAIL_PORT')
email_host_user = cf.get(env + '-config', 'EMAIL_HOST_USER')
email_host_password = cf.get(env + '-config', 'EMAIL_HOST_PASSWORD')
email_use_tls = cf.getboolean(env + '-config', 'EMAIL_USE_TLS')
email_from = cf.get(env + '-config', 'EMAIL_FROM')
REPORTS_HOST = cf.get(env + '-config', 'REPORTS_HOST')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extract_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+)x)!nq*end3=ryl#6^6)m^z0#wj^=9^#b(l-fx7xptn8-7+0^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = log_level

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'auth.User'

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'password_reset',
    'crispy_forms',
    'DjangoUeditor',
    'recruit',
    'djcelery',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'constance',
    'constance.backends.database',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wechatRecruit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'wechatRecruit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': database_name,
        'USER': database_user,
        'PASSWORD': database_password,
        'HOST': database_host,
        'PORT': database_port
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 默认是Ture，时间是utc时间，由于要用本地时间，所用手动修改为false

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 处理跨域
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# rest_framework config

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # json form 渲染
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser',
                               'rest_framework.parsers.FormParser',
                               'rest_framework.parsers.MultiPartParser',
                               'rest_framework.parsers.FileUploadParser',
                               ],
    'DEFAULT_PAGINATION_CLASS': 'wechatRecruit.pagination.MyPageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# 日志处理

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] - [%(filename)s:%(lineno)s] - %(message)s'}
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'maxBytes': 1073741824,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/run.log'),
            'maxBytes': 1073741824,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'script_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/run.log'),
            'maxBytes': 1073741824,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'recruit': {
            'handlers': ['script_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# 常量动态管理
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

CONSTANCE_CONFIG = OrderedDict({
    'BALANCE': (3, '各项分数小于此值是面面俱到性格', int),
    'COMMON': (3, '某两项分均超过此值, 大众性格', int),
    'PROMINENT': (5, '某一项分高于其它四项中此值以上，性格突出'),
    'URL': ('http://172.16.4.110:8000', '分析结果的跳转地址')
})

djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 40
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_TASK_RESULT_EXPIRES = 3600
CELERYD_CONCURRENCY = 1 if DEBUG else 4  # 并发的worker数量
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行100次任务被销毁，防止内存泄漏
CELERY_FORCE_EXECV = True  # 有些情况可以防止死锁
CELERY_TASK_TIME_LIMIT = 3 * 60 * 60  # 单个任务最大运行时间

# 邮件
EMAIL_HOST = email_host
EMAIL_PORT = email_port
EMAIL_HOST_USER = email_host_user
EMAIL_HOST_PASSWORD = email_host_password
EMAIL_USE_TLS = email_use_tls
EMAIL_FROM = email_from

# RespondentToken 过期时间
RESPONDENT_TOKEN_EXPIRED = 3600 * 7

# 在导入数据时使用数据库事务，默认False
IMPORT_EXPORT_USE_TRANSACTIONS = True
# 关闭LOADING
SIMPLEUI_LOADING = False
# 加载本地静态资源
SIMPLEUI_STATIC_OFFLINE = True
# 不收集分析信息
SIMPLEUI_ANALYSIS = False
# 是否隐藏首页最近动作
SIMPLEUI_HOME_ACTION = False
# 快速操作
SIMPLEUI_HOME_QUICK = True
# 服务器信息
SIMPLEUI_HOME_INFO = False
# 顶部首页跳转地址
SIMPLEUI_INDEX = 'http://47.113.120.14/'
# 自定义SIMPLEUI的Logo
# SIMPLEUI_LOGO = "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1313600584,226648524&fm=26&gp=0.jpg"

import time

SIMPLEUI_CONFIG = {
    'system_keep': True,
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus':
        [
            {
                'name': '答题测试界面',
                'icon': 'fas fa-code',
                'url': 'http://47.113.120.14'
            },
            {
                'name': '用户分析图表',
                'icon': 'fas fa-code',
                'url': 'http://127.0.0.1:8000/recruit/result/'
            },
        ]
}
