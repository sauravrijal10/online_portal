"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import logging
from datetime import timedelta



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z+!*wbas2g3i87ap)g#&63)fju5k$dt0#91b#cid5@y9*ke)-9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','0.0.0.0','3.108.66.167','13.232.127.195']

SITE_ID = 1


# Application definition
SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.sites',

]
APPS = [
    'country',
    'branch',
    'user',
    'customer.apps.CustomerConfig',
    'invoice',
    'customer_log',
    'payment',
]
THIRD_PARTY_APPS = [
    "corsheaders",
    'rest_framework',
    "rest_framework.authtoken",
    "drf_api_logger",
    'drf_yasg',
    "rest_framework_simplejwt",

]
INSTALLED_APPS = SYSTEM_APPS + APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
   
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "online_portal.middleware.CurrentUserMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware",
    "online_portal.middleware.RequestLogMiddleware",
    
    
]

ROOT_URLCONF = 'online_portal.urls'

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

WSGI_APPLICATION = 'online_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASS'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ),
}



SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SECURITY_DEFINITIONS': None,
    'excluded_models': ['country.Country','user.User','branch.Branch'],
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

LOGGING_DIR = os.path.join(BASE_DIR, 'var','log')  # Change 'logs' to your desired directory
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# class ExcludeUnwantedLogs(logging.Filter):
#     def filter(self, record):
#         # Exclude WARNING level logs from the basehttp module
#         return not (record.levelno == logging.WARNING and record.name.startswith('basehttp'))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # "filters": {
    #     "exclude_unwanted_logs": {
    #         "()": "__main__.ExcludeUnwantedLogs",
    #     },
    # },
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {module} {pathname} {processName:s} {msg} {process:d} {thread:d}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "info": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'filename': os.path.join(LOGGING_DIR, 'info.log'),
            "when": "midnight",
            "interval": 1,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'filename': os.path.join(LOGGING_DIR, 'warning.log'),
            "when": "midnight",
            "interval": 1,
            "backupCount": 5,
            "formatter": "verbose",
            # "filters": ["exclude_unwanted_logs"], 
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            "when": "midnight",
            "interval": 1,
            "backupCount": 5,
            "formatter": "verbose",
         },
         "application": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'filename': os.path.join(LOGGING_DIR, 'application.log'),
            "when": "midnight",
            "interval": 1,
            "backupCount": 5,
            "formatter": "verbose",
        },
       
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ['console'],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins", "warning"],
            "level": "ERROR",
            "propagate": False,
        },
        # "basehttp": {
        #     "handlers": ["console"],  # You can adjust the handlers as needed
        #     "level": "ERROR",  # Adjust the log level as needed
        #     "propagate": False,
        # },
        "root": {
            "handlers": ["console", "warning",'application'],
            "level": "INFO",
        },
        "application_logger": {
            "handlers": ["application",'console'],
            "level": "INFO",
            "propagate": False,
        },
    },
}# CORS_ORIGIN_ALLOW_ALL = True

# class ExcludeUnwantedLogs(logging.Filter):
#     def filter(self, record):
#         # Exclude log entries related to unwanted files
#         unwanted_strings = [
#             '/usr/local/lib/python3.9/site-packages/django/contrib/auth/migrations/',
#             '/online_portal/user/migrations/',
#             '/usr/local/lib/python3.9/site-packages/django/contrib/',
#             # Add more strings as needed
#         ]
#         return not any(unwanted_string in record.getMessage() for unwanted_string in unwanted_strings)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'exclude_unwanted_logs': {
#             '()': 'online_portal.log_filters.ExcludeUnwantedLogs',
#         },
#     },
#     'handlers': {
#         'api_file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/log/api_calls.log',  # Specify the path to your API log file
#         },
#         'app_file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/log/application_logs.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['api_file', 'app_file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
#     'root': {
#         'handlers': ['api_file', 'app_file'],
#         'level': 'DEBUG',
#     },
#     'handlers': {
#         'api_file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/log/api_calls.log',  # Specify the path to your API log file
#         },
#         'app_file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'var/log/application_logs.log',  # Specify the path to your application log file
#         },
#     },
# }

# # Add separate loggers for each app
# for app in ['branch', 'country', 'user']:
#     LOGGING['loggers'][app] = {
#         'handlers': ['app_file'],
#         'level': 'DEBUG',
#         'propagate': True,
#     }

# Set the custom payload handler
REST_USE_JWT = True
JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'user.utils.custom_payload_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    # 'SLIDING_TOKEN_REFRESH_DELTA': timedelta(hours=6),
}


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")

AUTH_USER_MODEL = "user.User"
 
# CELERY_BROKER_URL = "redis://redis:6379"
# CELERY_RESULT_BACKEND = "redis://redis:6379"


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'programmingthing1011@gmail.com'
# EMAIL_HOST_PASSWORD = "mwmjvczrrmmrocvg" 
# EMAIL_USE_TLS = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAVJ5WIBK3QGAYV2PC'
AWS_SECRET_ACCESS_KEY = 'dLRLFsvvzZw29YAa+VV7kbCnZmOJQx4MlVhTVXuL'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'