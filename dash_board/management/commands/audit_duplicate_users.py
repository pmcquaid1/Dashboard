from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count

class Command(BaseCommand):
    help = "Audit duplicate users by email"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show duplicates, no changes made')

    def handle(self, *args, **options):
        duplicates = (
            User.objects
            .values('email')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        if not duplicates:
            self.stdout.write(self.style.SUCCESS("✅ No duplicate emails found."))
            return

        self.stdout.write(self.style.WARNING(f"⚠️ Found {len(duplicates)} duplicate email(s):"))
        for dup in duplicates:
            email = dup['email']
            users = User.objects.filter(email=email)
            self.stdout.write(f"\n📧 Email: {email} — {users.count()} users")
            for user in users:
                self.stdout.write(f"   - ID: {user.id}, Username: {user.username}, Active: {user.is_active}")

        if options['dry_run']:
            self.stdout.write(self.style.NOTICE("\nDry run complete. No changes made."))
