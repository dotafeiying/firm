"""
Django settings for firm project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ijq1iyu#6*q=l*k$h9ucmacd23_v+=9^m1_rio)8e)_6b*f=r!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'jet.dashboard',
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'app.apps.AppConfig',
    'app',
    'order',
    'DjangoUeditor',
    'import_export',
    # 'fontawesome',
    'crispy_forms',

    # login
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.weixin',
    'allauth.socialaccount.providers.github',

    'widget_tweaks',

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

# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'midware.cuser.RequestUser',
# )

ROOT_URLCONF = 'firm.urls'

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

                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'firm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

# JET_SIDE_MENU_COMPACT = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SOCIALACCOUNT_PROVIDERS = {
    'weixin': {
        'AUTHORIZE_URL': 'https://open.weixin.qq.com/connect/oauth2/authorize',  # for media platform
        'SCOPE': ['snsapi_base'],
    }
}

SITE_ID = 2
# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/app/home/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/app/home/'
# 可选值为：mandatory optional none, mandatory本地注册的用户必须先验证邮箱才可以登录，optional和none都不要求验证邮箱，区别是optional仍然会发送验证邮件
# ACCOUNT_EMAIL_VERIFICATION = mandatory
# 既可以使用用户名也可以使用email， 其他可选的值是'username'、'email'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 登出直接退出，不用确认
ACCOUNT_LOGOUT_ON_GET = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '843514174@qq.com'
EMAIL_HOST_PASSWORD = 'sgvzvluuzayrbdcj'
EMAIL_USE_TLS = True
EMAIL_FROM = '路希捷网络商城<843514174@qq.com>'
# 默认的发件人
DEFAULT_FROM_EMAIL = '843514174@qq.com'

ALIPAY_APPID = '2021000121694528'
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'order/app_private_key.pem')
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'order/alipay_public_key.pem')


LOG_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            # 'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(module)s] %(message)s',
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]- %(message)s'
        },
        'collect': {
            'format': '%(asctime)s %(levelname)-2s %(pathname)s[line:%(lineno)d]- %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "info.log"),     #日志输出文件
            'maxBytes': 1024*1024*50,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'SF': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据文件大小自动切
            'filename': os.path.join(LOG_PATH, "xxx_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 备份数为3  xx.log --> xx.log.1 --> xx.log.2 --> xx.log.3
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(LOG_PATH, "firm.log"),  # 日志文件
            'backupCount': 3,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            'when': 'D',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOG_PATH, "error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 'collect': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(LOG_PATH, "xxx_collect.log"),
        #     'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
        #     'backupCount': 5,
        #     'formatter': 'collect',
        #     'encoding': "utf-8"
        # }
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['TF', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'django': {
        #     'handlers': ['default', 'console'],
        #     'level': 'INFO',
        #     'propagate': False
        # },
        # 'collect': {  # 名为 'collect'的logger还单独处理
        #     'handlers': ['console', 'collect'],
        #     'level': 'INFO',
        # }
    },
}