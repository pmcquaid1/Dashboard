from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os

CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, "logs", "generated_credentials.txt")
LOGIN_URL = "https://yourapp.com/login"  # 🔁 Update with your actual login URL

class Command(BaseCommand):
    help = "Send login credentials to staff via email"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview email sending without actually sending messages'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if not os.path.exists(CREDENTIALS_PATH):
            self.stdout.write(self.style.ERROR(f"🚫 Credentials file not found at {CREDENTIALS_PATH}"))
            return

        with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            try:
                email, password = line.strip().split(",")
                subject = "Your SLLHub Login Credentials"
                body = (
                    f"Hello,\n\n"
                    f"Your login credentials for SLLHub:\n"
                    f"Email: {email}\n"
                    f"Password: {password}\n\n"
                    f"Please log in at {LOGIN_URL} and change your password immediately.\n\n"
                    f"Regards,\nSLLHub Team"
                )

                if dry_run:
                    self.stdout.write(self.style.WARNING(f"🔍 Dry run — would send email to {email}"))
                else:
                    msg = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [email])
                    msg.send()
                    self.stdout.write(self.style.SUCCESS(f"✅ Sent email to {email}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to process {line.strip()} — {e}"))
