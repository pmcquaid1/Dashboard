import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from dash_board.models import Contact  # Replace with your actual app and model

class Command(BaseCommand):
    help = 'Bulk assigns users to groups and permissions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--dry-run', action='store_true', help='Simulate changes without applying them')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        dry_run = kwargs['dry_run']
        updated = 0
        skipped = 0

        try:
            with open(csv_file, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    email = row.get('email', '').strip()
                    department = row.get('department', '').strip()
                    permissions = row.get('permissions', '').split() if row.get('permissions') else []

                    if not email:
                        self.stdout.write(self.style.WARNING('Missing email in row. Skipping.'))
                        skipped += 1
                        continue

                    try:
                        user = User.objects.get(email=email)

                        # Replace group memberships
                        if dry_run:
                            self.stdout.write(f"[DRY-RUN] Would assign group '{department}' to {email}")
                        else:
                            user.groups.clear()
                            if department:
                                group, _ = Group.objects.get_or_create(name=department)
                                user.groups.add(group)

                        # Assign permissions
                        content_type = ContentType.objects.get_for_model(Contact)
                        for perm_codename in permissions:
                            try:
                                permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                                if not dry_run:
                                    user.user_permissions.add(permission)
                            except Permission.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f'Permission "{perm_codename}" not found.'))

                        self.stdout.write(self.style.SUCCESS(
                            f'{"[DRY-RUN] " if dry_run else ""}Updated access for user "{email}".'
                        ))
                        updated += 1

                    except User.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'User with email "{email}" not found.'))
                        skipped += 1

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{csv_file}" not found.'))
            return

        self.stdout.write(self.style.NOTICE(f'\nSummary: {updated} updated, {skipped} skipped.'))

