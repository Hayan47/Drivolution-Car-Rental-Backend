from .base import *

SECRET_KEY = config('SECRET_KEY')

# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', '0.0.0.0']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

# Security settings
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Production email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True

# Static files configuration
STATIC_ROOT = '/app/static'
STATIC_URL = '/static/'

# Media files configuration
MEDIA_ROOT = '/app/media'
MEDIA_URL = '/media/'
