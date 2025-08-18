from .settings import *

# ✅ Debug mode for test visibility
DEBUG = True

# ✅ Allow all hosts for Heroku test environment
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*").split(",")



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

# ✅ Optional dry-run flag for safe testing
DRY_RUN_MODE = True

# ✅ Static file handling for Heroku
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# ✅ Verbose logging for audit visibility
LOGGING['handlers']['console']['level'] = 'DEBUG'

