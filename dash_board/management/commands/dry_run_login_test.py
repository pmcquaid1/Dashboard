from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class Command(BaseCommand):
    help = "Dry-run login test for staff users using email and username"

    def handle(self, *args, **options):
        staff_users = User.objects.filter(is_staff=True)
        self.stdout.write(f"🔍 Testing {staff_users.count()} staff users...\n")

        for user in staff_users:
            identifier = user.email or user.username
            password = "test_password"  # Replace with known test password or fetch securely

            # Try email login
            email_result = authenticate(username=identifier, password=password)
            if email_result:
                logger.info(f"[DRY-RUN SUCCESS] {identifier} via email")
                self.stdout.write(f"✅ {identifier} authenticated via email\n")
            else:
                logger.warning(f"[DRY-RUN FAIL] {identifier} via email")
                self.stdout.write(f"❌ {identifier} failed via email\n")

            # Try username login if different
            if user.username != identifier:
                username_result = authenticate(username=user.username, password=password)
                if username_result:
                    logger.info(f"[DRY-RUN SUCCESS] {user.username} via username")
                    self.stdout.write(f"✅ {user.username} authenticated via username\n")
                else:
                    logger.warning(f"[DRY-RUN FAIL] {user.username} via username")
                    self.stdout.write(f"❌ {user.username} failed via username\n")
