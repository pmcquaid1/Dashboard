from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Assigns a user to one or more groups'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('groups', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        group_names = kwargs['groups']

        try:
            user = User.objects.get(username=username)
            for group_name in group_names:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'User \"{username}\" added to group \"{group_name}\".'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
