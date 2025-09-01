from . import *
from decouple import config
from pathlib import Path
from . import TEMPLATES, LOGGING, MIDDLEWARE

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = config('ENV', default='production')

DEBUG = False
ALLOWED_HOSTS = ['sllhub.herokuapp.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
