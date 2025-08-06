from django.core.management.base import BaseCommand
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Send password reset emails to staff with valid email addresses and flag placeholders.'

    def handle(self, *args, **options):
        valid_staff = User.objects.filter(is_staff=True).exclude(email__icontains='placeholder')
        placeholder_staff = User.objects.filter(is_staff=True, email__icontains='placeholder')

        sent_count = 0
        failed_count = 0

        self.stdout.write(self.style.SUCCESS('Starting password reset email dispatch...\n'))

        # Send reset emails to valid staff
        for user in valid_staff:
            form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                try:
                    form.save(
                        request=None,
                        use_https=True,
                        from_email='your-email@example.com',
                        email_template_name='registration/password_reset_email.html',
                    )
                    sent_count += 1
                    self.stdout.write(f"✅ Sent to: {user.username} ({user.email})")
                except Exception as e:
                    failed_count += 1
                    self.stdout.write(self.style.WARNING(f"⚠️ Failed for: {user.username} - {str(e)}"))

        # Log users with placeholder emails
        self.stdout.write(self.style.NOTICE(f"\n🚫 Placeholder emails detected for the following users:\n"))
        for user in placeholder_staff:
            self.stdout.write(f"- {user.username} ({user.email})")

        # Final summary
        total_staff = valid_staff.count()
        self.stdout.write(self.style.SUCCESS(f"\n📬 Emails sent: {sent_count}/{total_staff}"))
        self.stdout.write(self.style.WARNING(f"❌ Failed emails: {failed_count}"))
        self.stdout.write(self.style.NOTICE(f"👥 Placeholder accounts flagged: {placeholder_staff.count()}"))
