import logging
from django.conf import settings
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

class TestModeMiddleware:
    def __init__(self, get_response: callable):
        self.get_response = get_response
        self.enabled = getattr(settings, 'APP_MODE', '') == 'test'
        logger.debug("✅ TestModeMiddleware initialized")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.enabled:
            logger.debug("✅ TestModeMiddleware called")
            request.APP_MODE = "test"
        response = self.get_response(request)
        if self.enabled:
            response['X-App-Mode'] = 'test'
        return response


class ThirdPartyAuthMiddleware:
    def __init__(self, get_response: callable):
        self.get_response = get_response
        self.enabled = getattr(settings, 'ENV', '') == 'test'
        self.token_map = getattr(settings, 'VENDOR_CONTACT_TOKENS', {}) or {}
        self.dry_run = getattr(settings, 'DRY_RUN_MODE', False)
        logger.debug("✅ ThirdPartyAuthMiddleware initialized")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.enabled and request.path.startswith('/api/test/'):
            if self.dry_run:
                logger.debug("🧪 Dry-run mode active — skipping token check")
                return self.get_response(request)

            email = request.headers.get('X-Contact-Email', '').strip()
            token = request.headers.get('X-Access-Token', '').strip()

            if not email or not token:
                logger.warning("❌ Missing authentication headers")
                return HttpResponseForbidden("Missing credentials")

            expected_token = self.token_map.get(email)
            if expected_token != token:
                logger.warning(f"❌ Unauthorized access attempt from {email} with token {token}")
                return HttpResponseForbidden("Invalid or mismatched token")

            logger.info(f"✅ Access granted to {email} from IP {request.META.get('REMOTE_ADDR')}")
            request.vendor_contact = email  # Optional: attach for downstream use

        return self.get_response(request)


