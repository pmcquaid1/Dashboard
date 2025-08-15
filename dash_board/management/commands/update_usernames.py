from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Update usernames to match email addresses"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without saving them'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        users = User.objects.exclude(email__isnull=True)
        updated = 0

        for user in users:
            if user.username != user.email:
                self.stdout.write(f"User ID {user.id}: '{user.username}' → '{user.email}'")
                updated += 1
                if not dry_run:
                    user.username = user.email
                    user.save(update_fields=['username'])

        if dry_run:
            self.stdout.write(self.style.WARNING(f"[DRY RUN] {updated} usernames would be updated."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated {updated} usernames."))

