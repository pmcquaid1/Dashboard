import logging
from functools import wraps
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def log_test_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        logger.info(
            "TEST ACCESS: path=%s, method=%s, IP=%s, contact=%s, token=%s",
            request.path,
            request.method,
            request.META.get('REMOTE_ADDR'),
            request.headers.get('X-Contact-Email'),
            request.headers.get('X-Access-Token'),
        )
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def dry_run_safe(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('X-Dry-Run', '').lower() == 'true':
            logger.info("DRY-RUN: Skipping execution for %s", request.path)
            return JsonResponse({'status': 'dry-run', 'path': request.path})
        return view_func(request, *args, **kwargs)
    return _wrapped_view
