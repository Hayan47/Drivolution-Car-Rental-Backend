from .base import *
import os

DEBUG = True
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drivolution',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Development-specific settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development logging
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
        'level': 'DEBUG',
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}