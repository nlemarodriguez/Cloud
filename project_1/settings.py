
"""
Django settings for project_1 project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_9ma-ug03i5)#q)sgm5r=8k3j+!g=dta3!#)b^#yu5m+2xxaah'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'designs.apps.DesignsConfig',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'storages',
]

MIDDLEWARE = [
    'hirefire.contrib.django.middleware.HireFireMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_1.urls'

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

WSGI_APPLICATION = 'project_1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.environ["BD_MONGO"],
        'HOST': os.environ["BD_MONGO_HOST"]
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'designs.CustomUser'

#MEDIA_URL = "/media/"
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MAIN_URL = 'http://127.0.0.1:8000/'
#MAIN_URL = os.environ["MAIN_URL"]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'signup'

EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_DESIGN_USER = os.environ["EMAIL_DESIGN_USER"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_DEFAULT_ACL = None
#AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CLOUD_FRONT_URL = os.environ["CLOUD_FRONT_URL"]

AWS_QUEUE_URL = os.environ["AWS_QUEUE_URL"]
AWS_QUEUE_NAME = os.environ["AWS_QUEUE_NAME"]

HIREFIRE_TOKEN = os.environ["HIREFIRE_TOKEN"]
HIREFIRE_PROCS = ['procs.WorkerProc']
BROKER_BACKEND = 'SQS'
BROKER_URL = 'sqs://{aws_access_key}:{aws_secret_key}@'.format(aws_access_key=AWS_ACCESS_KEY_ID,
                                                               aws_secret_key=AWS_SECRET_ACCESS_KEY)
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',
    'polling_interval': 60,
    'visibility_timeout': 18000,
    # Number of seconds to sleep between unsuccessful polls,
    # default value is 30 seconds
}
CELERY_BROKER_URL = 'sqs://{aws_access_key}:{aws_secret_key}@'.format(aws_access_key=AWS_ACCESS_KEY_ID,
                                                                      aws_secret_key=AWS_SECRET_ACCESS_KEY)
CELERY_DEFAULT_QUEUE = os.environ["AWS_QUEUE_NAME"]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_CONTENT_ENCODING = 'utf-8'
CELERY_ENABLE_REMOTE_CONTROL = False
CELERY_SEND_EVENTS = False
# Reason why we need the above is explained in Configuration Gotchas section.
SQS_QUEUE_NAME = os.environ["AWS_QUEUE_NAME"]

CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS').split(','),
        'OPTIONS': {
                    'username': os.environ.get('MEMCACHIER_USERNAME'),
                    'password': os.environ.get('MEMCACHIER_PASSWORD')
            }
    }
}
