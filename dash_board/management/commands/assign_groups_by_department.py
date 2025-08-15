from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from dash_board.models import Employee
import logging

logger = logging.getLogger("import_logger")

GROUP_MAP = {
    "Transport": "Transport",
    "Finance": "Finance",
    "Warehouse": "Warehouse",
    "C&F": "C&F",
    "Documentation": "Documentation",
    "RevOps": "RevOps",
    "QHSE": "QHSE",
    "Admin": "Admin",
    "HR": "HR",
    "General": "General",
    # Add more mappings as needed
}

class Command(BaseCommand):
    help = "Assign users to groups based on their department"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview group assignments without saving changes"
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated = 0
        skipped = 0

        employees = Employee.objects.select_related("user").all()

        for employee in employees:
            user = employee.user
            dept = employee.department
            group_name = GROUP_MAP.get(dept)

            if user and group_name:
                group, _ = Group.objects.get_or_create(name=group_name)
                if dry_run:
                    logger.info(f"[DRY RUN] Would assign {user.username} to '{group_name}' (Dept: {dept})")
                else:
                    user.groups.add(group)
                    logger.info(f"✅ {user.username} assigned to '{group_name}' (Dept: {dept})")
                updated += 1
            else:
                logger.warning(f"⚠️ Skipped: {employee.email} — No user or group mapping for dept '{dept}'")
                skipped += 1

        logger.info("📊 Assignment Summary")
        logger.info(f"✅ Updated: {updated}")
        logger.info(f"⚠️ Skipped: {skipped}")
