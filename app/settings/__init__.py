import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# ✅ Environment flag
ENV = config('ENV', default='production')

# ✅ Load correct settings module
if ENV == 'test':
    from settings_test import APP_SETTINGS
else:
    from settings_prod import APP_SETTINGS

# ✅ Twilio credentials via .env (wrapped for test safety)
TWILIO_SID = config('TWILIO_SID', default=None)
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default=None)
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER', default=None)

if TWILIO_SID and TWILIO_AUTH_TOKEN:
    from twilio.rest import Client
    TWILIO_CLIENT = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
else:
    TWILIO_CLIENT = None

# ✅ Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# ✅ Installed apps
INSTALLED_APPS = [
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dash_board',
]

# ✅ Middleware
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

# ✅ Root URLs & WSGI
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

# ✅ Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'dashboard' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dash_board.context_processors.employee_context',
                'dash_board.context_processors.user_permissions_context',
            ],
        },
    },
]

# ✅ Database
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# ✅ Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Accra'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ✅ Static files for Heroku
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Authentication backends
AUTHENTICATION_BACKENDS = [
    'dash_board.auth_backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ✅ Login redirect
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# ✅ Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ Email dispatch flag
EMAIL_DISPATCH_ENABLED = os.getenv("EMAIL_DISPATCH_ENABLED", "False") == "True"

# ✅ Exported settings
__all__ = ['APP_SETTINGS']


