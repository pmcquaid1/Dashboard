from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from dash_board.models import Contact  # Replace with your actual model

class Command(BaseCommand):
    help = 'Assigns a specific permission to a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('permission_codename', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        permission_codename = kwargs['permission_codename']

        try:
            user = User.objects.get(username=username)
            content_type = ContentType.objects.get_for_model(Contact)
            permission = Permission.objects.get(codename=permission_codename, content_type=content_type)
            user.user_permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f'Permission "{permission_codename}" assigned to user "{username}".'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))

