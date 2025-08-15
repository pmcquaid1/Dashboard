import csv
from django.core.management.base import BaseCommand
from dash_board.models import Employee
print("✅ audit_import_mismatches.py loaded")

class Command(BaseCommand):
    help = "Audit CSV records that were not imported into the Employee model"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the original CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        try:
            with open(csv_file, newline="") as file:
                reader = csv.DictReader(file)
                csv_emails = {row["email"].strip().lower() for row in reader}

            db_emails = {e.email.strip().lower() for e in Employee.objects.all()}
            missing = csv_emails - db_emails

            if missing:
                self.stdout.write("📋 Emails in CSV but missing from DB:")
                for email in sorted(missing):
                    self.stdout.write(f"❌ {email}")
                self.stdout.write(f"\nTotal missing: {len(missing)}")
            else:
                self.stdout.write("✅ All CSV records are present in the database.")

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
