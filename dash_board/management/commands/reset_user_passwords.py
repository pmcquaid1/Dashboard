import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = "Reset all user passwords in development and log credentials"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which users would be updated'
        )
        parser.add_argument(
            '--default-password',
            type=str,
            default=None,
            help='Set a fixed password for all users (optional)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='generated_credentials.txt',
            help='Path to output file for new credentials'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        default_password = options['default_password']
        output_path = options['output']
        users = User.objects.exclude(is_superuser=True)
        updated = 0
        lines = []

        for user in users:
            new_password = default_password or get_random_string(10)
            if dry_run:
                self.stdout.write(f"[DRY RUN] Would reset password for {user.email} → {new_password}")
            else:
                user.set_password(new_password)
                user.save(update_fields=['password'])
                lines.append(f"{user.username},{user.email},{new_password}")
                self.stdout.write(f"Reset password for {user.email} → {new_password}")
            updated += 1

        if not dry_run:
            with open(output_path, 'w') as f:
                f.write("username,email,new_password\n")
                f.write("\n".join(lines))
            self.stdout.write(self.style.SUCCESS(f"Credentials written to {output_path}"))

        self.stdout.write(self.style.WARNING(f"{updated} users processed{' (dry-run)' if dry_run else ''}."))
