from django.core.management.base import BaseCommand
from dash_board.models import Employee
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes duplicate placeholder employees based on name, keeping one per person'

    def handle(self, *args, **kwargs):
        placeholder_suffix = "@placeholder.local"
        duplicates = {}

        # Step 1: Find all placeholder employees
        placeholder_employees = Employee.objects.filter(email__endswith=placeholder_suffix)

        # Step 2: Group by full name
        for emp in placeholder_employees:
            key = f"{emp.first_name.strip().lower()}_{emp.last_name.strip().lower()}"
            duplicates.setdefault(key, []).append(emp)

        # Step 3: Delete all but one per name group
        for name_key, records in duplicates.items():
            if len(records) > 1:
                for emp in records[1:]:
                    user = emp.user
                    self.stdout.write(f"🗑️ Deleting duplicate: {emp.email}")
                    emp.delete()
                    if user:
                        user.delete()

        self.stdout.write(self.style.SUCCESS("✅ Duplicate cleanup complete."))
