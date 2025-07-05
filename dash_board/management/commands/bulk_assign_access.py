import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from dash_board.models import Contact  # Replace with your actual app and model

class Command(BaseCommand):
    help = 'Bulk assigns users to groups and permissions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    username = row['username']
                    groups = row['groups'].split()
                    permissions = row['permissions'].split()

                    try:
                        user = User.objects.get(username=username)

                        # Assign groups
                        for group_name in groups:
                            group, _ = Group.objects.get_or_create(name=group_name)
                            user.groups.add(group)

                        # Assign permissions
                        content_type = ContentType.objects.get_for_model(Contact)
                        for perm_codename in permissions:
                            try:
                                permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                                user.user_permissions.add(permission)
                            except Permission.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f'Permission "{perm_codename}" not found.'))

                        self.stdout.write(self.style.SUCCESS(f'Updated access for user "{username}".'))

                    except User.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'User "{username}" not found.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{csv_file}" not found.'))
