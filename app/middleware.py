import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TestModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'APP_MODE', '') == 'test'
        logger.debug("✅ TestModeMiddleware initialized")

    def __call__(self, request):
        if self.enabled:
            logger.debug("✅ TestModeMiddleware called")
            request.APP_MODE = "test"
        response = self.get_response(request)
        if self.enabled:
            response['X-App-Mode'] = 'test'
        return response
