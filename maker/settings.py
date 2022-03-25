from datetime import timedelta
from pathlib import Path

import django.middleware.cache

import parametrs

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = parametrs.SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # APPS
    'core',

    # LIBRARIES
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    'djoser',
    'django_celery_beat',
    # 'loadtest'

    # SOCIAL OAUTH
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
]

# This is counter-intuitive, but correct: ``UpdateCacheMiddleware`` needs to run
# last during the response phase, which processes middleware bottom-up;
# ``FetchFromCacheMiddleware`` needs to run last during the request phase, which
# processes middleware top-down.

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
]

ROOT_URLCONF = 'maker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'maker.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CACHES REDIS

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379',
#     }
# }

# Password validation

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

AUTHENTICATION_BACKENDS = (
    # FACEBOOK
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # GOOGLE
    'social_core.backends.google.GoogleOAuth2',
    # DRF
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    # DJANGO
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '<your app id goes here>'
SOCIAL_AUTH_FACEBOOK_SECRET = '<your app secret goes here>'
DCS_SESSION_COOKIE_SAMESITE = "None"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}
SESSION_COOKIE_SECURE = False
# GOOGLE configuration

# GOOGLE
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = parametrs.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = parametrs.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

LOGIN_URL = '/complete/google-oauth2/'

LOGIN_REDIRECT_URL = '/api/'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

# Email settings for SMTP (done - checked)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = parametrs.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = parametrs.EMAIL_HOST_PASSWORD

#  JWT SETTINGS

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

#  DRF SETTINGS

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

#  DJOSER SETTINGS

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'test/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'test/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'test/users/activation/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
}

#  CELERY SETTINGS

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
