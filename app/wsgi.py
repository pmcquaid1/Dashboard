import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings_test')

logger.info("🚀 WSGI loaded successfully")
logger.info(f"📦 DJANGO_SETTINGS_MODULE = {os.environ['DJANGO_SETTINGS_MODULE']}")

application = get_wsgi_application()


