from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Removes a user from one or more groups'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('groups', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        group_names = kwargs['groups']

        try:
            user = User.objects.get(username=username)
            for group_name in group_names:
                try:
                    group = Group.objects.get(name=group_name)
                    user.groups.remove(group)
                    self.stdout.write(self.style.SUCCESS(f'User "{username}" removed from group "{group_name}".'))
                except Group.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Group "{group_name}" does not exist.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
