"""
Django settings for project project.

"""
import os
import sys
from distutils.util import strtobool
from pathlib import Path
from dotenv import dotenv_values
from datetime import timedelta 
import sentry_sdk
from django.utils.log import DEFAULT_LOGGING
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'Um2ga1-#2secret#p!ezs0^!^o#0'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
COMPANY_NAME = 'Django-Starter'
AWS_SES_EMAIL = EMAIL_HOST_USER

# Application definition
INSTALLED_APPS = [
    'ramailo.apps.RamailoConfig',
    'rest_framework',
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework_simplejwt',
    'django_extensions',
    'user',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.middleware.UserLoggingMiddleware'
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': int(config('POSTGRES_PORT', default=5432)),

    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL', default='redis://localhost:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE = "default"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE ='UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATICFILES_DIRS = (('static'),)
STATIC_URL = config('STATIC_URL', default='static/')
STATIC_ROOT = os.path.join(BASE_DIR, config('STATIC_ROOT', default='static'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'EXCEPTION_HANDLER': 'ramailo.error_handling.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    "ALGORITHM": "HS512",
    'SIGNING_KEY': config("JWT_SIGNING_KEY"),
    'AUTH_HEADER_TYPES': ("Bearer",),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    "VERIFYING_KEY": "",
    "JTI_CLAIM": None,
    "USER_ID_CLAIM": "id"
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'USE_SESSION_AUTH': False
}

ENV_ALLOWED_HOSTS = config('ALLOWED_HOSTS')
ALLOWED_HOSTS = ENV_ALLOWED_HOSTS.split(',') if ENV_ALLOWED_HOSTS is not None else []
DEBUG = bool(strtobool(config('DEBUG', default='True')))

# Ramailo
COMPANY_NAME = "Ramailo"

# User
DUMMY_USER_IMAGE = 'https://ramailo-logos.s3.ap-south-1.amazonaws.com/misc/dummy_user.png'

# Email
EMAIL_OTP_EXPIRY = 5 * 60
EMAIL_LINK_EXPIRY = 5 * 60
EMAIL_REQUEST_RATE_LIMIT = '3/5m' # 3 requests in 5 min

# # App URL
# APP_URL = config("APP_URL")
# WEB_URL = config("WEB_URL")

# Subscription
AUTO_EXPIRES_ON=3650 # days

#sentry
sentry_sdk.init(
    dsn=config("SENTRY_DSN", ""),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

#loggers
LOGGING = {
    # Define the logging version
    'version': 1,

    # Enable the existing loggers
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'user_idx': {
            '()': 'shared.helpers.logging_helper.UserIDXFilter'
        },
    },

    # Define the formatters
    'formatters': {
            'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] [%(lineno)s] [%(user_idx)s] [%(message)s] ',
            },
    },

    # Define the handlers
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['user_idx'],
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['user_idx'],
            'filename': 'logs.log',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },

   # Define the loggers
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },

        #database query logger
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    },

}

#celery
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")

CSRF_TRUSTED_ORIGINS = ["https://ramailo.uat.ramailo.tech"]

# #refer
# REFERRAL_URL = config("REFERRAL_URL")

#razorpay-ifsc
# RAZORPAY_IFSC_URL=config("RAZORPAY_IFSC_URL")


#s3 configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 

# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_VERIFY = True

# aws ses
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_REGION_NAME = config("AWS_SES_REGION_NAME")
# AWS_SES_EMAIL = config("AWS_SES_EMAIL")

#fcm
# FCM_API_KEY = config("FCM_API_KEY")

# testers
TESTERS = ["9975319000", "8864208000"]

# Name matching threshold
NAME_MATCH_THRESHOLD = 70.0


# Debug: Print final settings values
print("Settings CELERY_BROKER_URL:", CELERY_BROKER_URL)