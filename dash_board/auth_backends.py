# app/auth_backends.py
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get('email')
        user = User.objects.filter(email__iexact=identifier).first()
        if user and user.check_password(password):
            logger.info(f"[AUTH SUCCESS] identifier={identifier}")
            return user
        logger.warning(f"[AUTH FAIL] identifier={identifier}, reason=Invalid credentials")
        return None

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()
