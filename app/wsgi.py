import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'app.settings_test')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

logger.info("🚀 WSGI loaded successfully")
logger.info(f"📦 DJANGO_SETTINGS_MODULE = {settings_module}")

application = get_wsgi_application()

