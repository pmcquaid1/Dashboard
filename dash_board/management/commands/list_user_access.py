from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Lists all permissions and groups assigned to a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        self.stdout.write(self.style.SUCCESS(f'\nAccess details for user: {username}'))

        # List groups
        groups = user.groups.all()
        if groups:
            self.stdout.write('\nGroups:')
            for group in groups:
                self.stdout.write(f' - {group.name}')
        else:
            self.stdout.write('\nNo groups assigned.')

        # List permissions
        permissions = user.get_user_permissions()
        if permissions:
            self.stdout.write('\nPermissions:')
            for perm in sorted(permissions):
                self.stdout.write(f' - {perm}')
        else:
            self.stdout.write('\nNo permissions assigned.')
