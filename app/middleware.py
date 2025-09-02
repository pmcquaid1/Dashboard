import logging
import json
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class BaseTestMiddleware:
    """Reusable base for test-only middleware with audit logging."""
    def __init__(self, get_response: callable):
        self.get_response = get_response
        self.enabled = getattr(settings, 'ENV', '') == 'test'
        self.dry_run = getattr(settings, 'DRY_RUN_MODE', False)

    def log_event(self, event_type: str, request: HttpRequest, details: dict):
        """Emit structured audit log."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "path": request.path,
            "ip": request.META.get("REMOTE_ADDR"),
            "dry_run": self.dry_run,
            "details": details,
        }
        logger.info(f"[AUDIT] {json.dumps(payload)}")


class TestModeMiddleware(BaseTestMiddleware):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.enabled:
            self.log_event("test_mode_active", request, {"note": "Injecting test mode header"})
            request.APP_MODE = "test"

        response = self.get_response(request)

        if self.enabled:
            response['X-App-Mode'] = 'test'

        return response


class ThirdPartyAuthMiddleware(BaseTestMiddleware):
    def __init__(self, get_response: callable):
        super().__init__(get_response)
        self.token_map = getattr(settings, 'VENDOR_CONTACT_TOKENS', {}) or {}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.enabled and request.path.startswith('/api/test/'):
            if self.dry_run:
                self.log_event("dry_run_skip_auth", request, {"note": "Bypassing token check"})
                return self.get_response(request)

            email = request.headers.get('X-Contact-Email', '').strip()
            token = request.headers.get('X-Access-Token', '').strip()

            if not email or not token:
                self.log_event("auth_failed_missing_headers", request, {"email": email, "token": token})
                response = HttpResponseForbidden("Missing credentials")
                response['X-Auth-Status'] = 'denied'
                return response

            expected_token = self.token_map.get(email)
            if expected_token != token:
                self.log_event("auth_failed_invalid_token", request, {
                    "email": email,
                    "provided_token": token,
                    "expected_token": expected_token
                })
                response = HttpResponseForbidden("Invalid or mismatched token")
                response['X-Auth-Status'] = 'denied'
                return response

            self.log_event("auth_success", request, {"email": email})
            request.vendor_contact = email

            response = self.get_response(request)
            response['X-Vendor-Contact'] = email
            response['X-Auth-Status'] = 'granted'
            return response

        return self.get_response(request)


