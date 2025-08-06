from django.core.management.base import BaseCommand
from dash_board.resources import EmployeeResource
from django.conf import settings
import os
import tablib

class Command(BaseCommand):
    help = "Run a dry import using EmployeeResource without shell input"

    def handle(self, *args, **options):
        resource = EmployeeResource()

        # ✅ Use actual file path (outside project folder)
        file_path = r'c:/projects documents/employee_contacts_v3.csv'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"❌ Import file not found at: {file_path}"))
            return

        # ✅ Read file with tablib
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()

        dataset = tablib.Dataset().load(raw_data, format='csv')

        result = resource.import_data(dataset, dry_run=True, raise_errors=False)

        # ✅ Report results row-by-row
        for i, row_result in enumerate(result.row_results):
            self.stdout.write(f"\n🔢 Row {i+1}")
            if row_result.errors:
                self.stdout.write(self.style.WARNING(f"⚠️ Errors: {row_result.errors}"))
            if row_result.import_type:
                self.stdout.write(self.style.SUCCESS(f"✅ Import type: {row_result.import_type}"))
            if row_result.validation_error:
                self.stdout.write(self.style.ERROR(f"❌ Validation Error: {row_result.validation_error}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n📊 Dry import complete — {len(result.row_results)} rows processed."
        ))
