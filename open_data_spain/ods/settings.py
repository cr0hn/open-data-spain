from pathlib import Path
from datetime import timedelta

import redis
import decouple
import dj_database_url

from django.contrib import messages
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.core.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-69)4fn*kxdmr(xl82mu7ikdhamk&)w($)xi2rd9c4ipw!a5(b4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config('DEBUG', cast=bool, default=True)

ENABLE_API = decouple.config('ENABLE_API', cast=bool, default=True)
ENABLE_DASHBOARD = decouple.config('ENABLE_DASHBOARD', cast=bool, default=True)
ENABLE_DJANGO_ADMIN = decouple.config('ENABLE_DASHBOARD', cast=bool, default=True)
ENABLE_CRAWLERS = decouple.config('ENABLE_CRAWLERS', cast=bool, default=True)


ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://open-data-spain.io',
    'https://open-data-spain.io',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Global apps
    'sdk',

    # Local apps
    'apps.cache',
    'apps.billing',
    'apps.geopolitico',
    'apps.subastas_boe',

    'authentication',

    # Dashboard
    'dashboard.home',
    'dashboard.login',
    'dashboard.api_keys',
    'dashboard.billing',

    # Third party apps
    'djstripe',

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
]


ROOT_URLCONF = 'ods.urls'

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
                # 'django.template.context_processors.csrf'
            ],
        },
    },
]

WSGI_APPLICATION = 'ods.wsgi.application'

COOKIE_NAME = 'odsSessionId'

# Database
# https://docs.core.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.config(
        default=decouple.config('DATABASE_DSN', default='postgres://postgres:postgres@localhost:6432/open_data_spain')
    )
}

# Password validation
# https://docs.core.com/en/4.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

AUTH_USER_MODEL = 'authentication.ODSUser'

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True

# THOUSAND_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.core.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# -------------------------------------------------------------------------
# Static root
# -------------------------------------------------------------------------
STATIC_ROOT = decouple.config('STATIC_ROOT', default=None)

# Default primary key field type
# https://docs.core.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'ods': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# -------------------------------------------------------------------------
# Almacena de datos para las subastas
# -------------------------------------------------------------------------
MINIO_BUCKET = decouple.config('MINIO_BUCKET', default='open-data-spain')
MINIO_HOST = decouple.config('MINIO_HOST', default='localhost:9000')
MINIO_SECURE = decouple.config('MINIO_SECURE', cast=bool, default=False)
MINIO_ACCESS_KEY = decouple.config('MINIO_ACCESS_KEY', default='AKWL6Lr4fN7FdWa2SOPK')
MINIO_SECRET_KEY = decouple.config('MINIO_SECRET_KEY', default='OvSlULQnmz4ivYpFv5MewZTje1hqVI6WovAnnXkH')

DATA_FOLDER = decouple.config('DATA_FOLDER', default=BASE_DIR / 'data')

# -------------------------------------------------------------------------
# Celery settings
# -------------------------------------------------------------------------
REDIS_URL = decouple.config("REDIS_URL", default="redis://127.0.0.1:7379/0")
REDIS_CONNECTION = redis.Redis.from_url(REDIS_URL, db=0, decode_responses=True)
CELERY_BROKER_URL = decouple.config('CELERY_BROKER_URL', default=REDIS_URL)
CELERY_TIMEZONE = 'Europe/Madrid'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

## Add periodic tasks
CELERY_BEAT_SCHEDULE = {
    'update_boe': {
        'task': 'subastas-boe-crawler',
        'schedule': 60 * 60 * 24,  # 1 day
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# -------------------------------------------------------------------------
# MongoDB settings
# -------------------------------------------------------------------------
MONGO_DSN = decouple.config('MONGO_DSN', default='mongodb://root:root@127.0.0.1:31291/open_data_spain?authSource=admin')
MONGO_USER = decouple.config('MONGO_USER', default='root')
MONGO_PASSWORD = decouple.config('MONGO_PASSWORD', default='root')

## Mongo Collections
MONGO_DB = "open_data_spain"
MONGO_COLLECTION_SUBASTAS = "subastas-boe"

MASTER_API_TOKEN = "973fba4c011537e04e2a81fc82f3fc95ad020dd87cc8778525b4c20207f24db35c6d04643a03cdfe29f457e132cbe93d7f8398fe0e36303f168633"

# -------------------------------------------------------------------------
# Google Maps API
# -------------------------------------------------------------------------
GOOGLE_MAPS_API_KEY = decouple.config('GOOGLE_MAPS_API_KEY', default="AIzaSyDy2Xj2pGaDAaO8RvTkJbnpYAWGlMM_SSk")


# -------------------------------------------------------------------------
# Stripe keys
# -------------------------------------------------------------------------
STRIPE_TEST_PUBLIC_KEY = decouple.config('STRIPE_TEST_PUBLIC_KEY',
                                         default="pk_test_51OKjnJE8pSFaHKuVLKdaXpPbR42V9Qb0jon8TkpV69uBFOPngKxWpI6RkAq0qbxambf8nzfMQe76xmDOjlkFjjNb00VPwhnRD5")
STRIPE_TEST_SECRET_KEY = decouple.config('STRIPE_TEST_SECRET_KEY',
                                         default="sk_test_51OKjnJE8pSFaHKuV0RNt8q06yxiuKlz2eph0vtiZfZknn7ZnjOItYbOgK4PVkZG1HWTPJ7wdR7KYNSK9VujK6gsC00Lk7RBf7U")

STRIPE_LIVE_PUBLIC_KEY = decouple.config('STRIPE_LIVE_SECRET_KEY', default=None)
STRIPE_LIVE_SECRET_KEY = decouple.config('STRIPE_LIVE_SECRET_KEY', default=None)

STRIPE_WEBHOOK_SECRET_TEST = decouple.config('STRIPE_WEBHOOK_SECRET',
                                             default="whsec_69ad6f5cea3b7384a036562ddead2ae047493a8b80ba9fac98c4c6656d153110")
STRIPE_WEBHOOK_SECRET_LIVE = decouple.config('STRIPE_WEBHOOK_SECRET', default=None)

DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_WEBHOOK_VALIDATION = "verify_signature"  # or "verify_events"

STRIPE_LIVE_MODE = not DEBUG
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations

if DEBUG:
    STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY
    STRIPE_WEBHOOK_SECRET = STRIPE_WEBHOOK_SECRET_TEST
else:
    STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY
    STRIPE_WEBHOOK_SECRET = STRIPE_WEBHOOK_SECRET_LIVE

# -------------------------------------------------------------------------
# Sentry
# -------------------------------------------------------------------------
SENTRY_DSN = decouple.config('SENTRY_DSN', default=None)

if SENTRY_DSN:
    import sentry_sdk

    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# -------------------------------------------------------------------------
#
# Configuration depending on the enabled configuration
#
# -------------------------------------------------------------------------
if ENABLE_CRAWLERS:
    INSTALLED_APPS += [
        # Crawlers
        'crawlers.subastas_boe_crawler',
    ]

    BOE_MAX_PER_TERRITORY = 100
    BOE_GLOBAL_MAX_COUNT = 1000

    OPEN_CAGE_DATA_TOKEN = decouple.config('OPENCAGEDATA_TOKEN', default="27c056655cd44ff39d9e3dc0a6318559")

if ENABLE_DJANGO_ADMIN:
    INSTALLED_APPS += [
        # Django Admin
        'django.contrib.admin',
        'django_json_widget',
    ]

if ENABLE_API:
    INSTALLED_APPS += [
        # API

        # Third party apps
        'drf_spectacular',
        'rest_framework',

        'prettyjson',
    ]

    # Rest Framework
    AUTHENTICATION_HEADER = 'HTTP_X_API_KEY'

    # Custom JSON Serializer
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ],

        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],

        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],

        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100,
    }

    # Add global Authentication middleware
    MIDDLEWARE.append('authentication.middleware.AuthenticationAPIMiddleware')

    # Add API limits
    MIDDLEWARE.append('apps.billing.middleware.APIBillingUserPlanMiddleware')

    AUTHENTICATION_BACKENDS = [
        'authentication.backends.APIAuthBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

# -------------------------------------------------------------------------
# Dashboard settings only if dashboard is enabled
# -------------------------------------------------------------------------
if ENABLE_DASHBOARD:

    INSTALLED_APPS += [
        'django_extensions',

        'crispy_forms',
        'crispy_bootstrap5',

        # Allauth
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.github'
    ]

    MIDDLEWARE += [
        # API

        # Local middlewares
        # 'apps.tracking.middlewares.user_activity.TrackingUserActivityMiddleware',

        # Allauth
        "allauth.account.middleware.AccountMiddleware"
    ]

    SOCIALACCOUNT_PROVIDERS = {
        'github': {
            'SCOPE': [
                'user',
            ],
        }
    }

    ACCOUNT_EMAIL_VERIFICATION = 'none'
    SOCIALACCOUNT_AUTO_SIGNUP = True
    SOCIALACCOUNT_LOGIN_ON_GET = True
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
    # ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
    SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
    SOCIALACCOUNT_EMAIL_REQUIRED = True
    SOCIALACCOUNT_ADAPTER = 'authentication.social_adapter.ODSAccountAdapter'

    CONTACT_EMAIL = 'contact@open-data-spain.io'

    AUTHENTICATION_BACKENDS = [
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by email
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    LOGIN_REDIRECT_URL = reverse_lazy('dashboard-home:home')
    LOGOUT_REDIRECT_URL = reverse_lazy('dashboard-home:home')
    LOGIN_URL = reverse_lazy('dashboard-login:login')

    # -------------------------------------------------------------------------
    # Crispy forms
    # -------------------------------------------------------------------------
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

    # -------------------------------------------------------------------------
    # Bootstrap 5
    # -------------------------------------------------------------------------
    MESSAGE_TAGS = {
        messages.SUCCESS: 'alert alert-success',
        messages.ERROR: 'alert alert-danger',
        messages.WARNING: 'alert alert-warning',
        messages.INFO: 'alert alert-info',
    }
