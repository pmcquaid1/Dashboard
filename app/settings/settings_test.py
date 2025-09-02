from . import *
from decouple import config
from pathlib import Path
import logging

from app.settings.constants import TEMPLATES, LOGGING, WSGI_APPLICATION

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ✅ Explicit environment flag
ENV = config('ENV', default='test')
assert ENV == 'test', "settings_test.py should only be used in test mode"

# ✅ Debug mode for test visibility
DEBUG = False

# ✅ Allow all hosts for Heroku test environment
ALLOWED_HOSTS = [
    'sllhub-test-f6581ed38b5d.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

# ✅ Use console email backend to avoid sending real emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ✅ Optional: Use SQLite for isolated testing (or set a test DATABASE_URL in Heroku)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# ✅ Twilio safety wrap
TWILIO_SID = config('TWILIO_SID', default=None)
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default=None)
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER', default=None)

if TWILIO_SID and TWILIO_AUTH_TOKEN:
    from twilio.rest import Client
    TWILIO_CLIENT = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
else:
    TWILIO_CLIENT = None

# ✅ Configurable dry-run flag
DRY_RUN_MODE = config('DRY_RUN_MODE', default='false').lower() == 'true'

# ✅ Static file handling for Heroku
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ✅ Override root URLs and WSGI if needed
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

# ✅ Template discovery for app-specific views
TEMPLATES[0]['DIRS'] += [BASE_DIR / 'dash_board' / 'templates']

# ✅ Verbose logging for audit visibility
LOGGING['handlers']['console']['level'] = 'DEBUG'

# ✅ Local definition of base middleware (no broken import)
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

# ✅ Add test-only middleware safely
if ENV == 'test':
    MIDDLEWARE += [
        'app.middleware.TestModeMiddleware',
        'app.middleware.ThirdPartyAuthMiddleware',
    ]

# ✅ Log settings confirmation
logger = logging.getLogger(__name__)
logger.info("✅ Loaded settings_test.py with test-only middleware and dry-run mode: %s", DRY_RUN_MODE)

# ✅ Vendor token mapping for scoped access
VENDOR_CONTACT_TOKENS = {
    config('VENDOR_CONTACT_1_EMAIL'): config('VENDOR_CONTACT_1_TOKEN'),
    config('VENDOR_CONTACT_2_EMAIL'): config('VENDOR_CONTACT_2_TOKEN'),
    config('VENDOR_CONTACT_3_EMAIL'): config('VENDOR_CONTACT_3_TOKEN'),
}



