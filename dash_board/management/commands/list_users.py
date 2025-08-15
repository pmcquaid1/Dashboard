from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "List all users with username, email, is_active, is_staff, is_superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all().order_by('username')

        if not users:
            self.stdout.write("No users found.")
            return

        self.stdout.write(f"{'Username':<20} {'Email':<30} {'Active':<8} {'Staff':<8} {'Superuser':<10}")
        self.stdout.write("-" * 80)

        for user in users:
            self.stdout.write(f"{user.username:<20} {user.email:<30} {str(user.is_active):<8} {str(user.is_staff):<8} {str(user.is_superuser):<10}")
