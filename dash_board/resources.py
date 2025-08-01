import random
import string
import logging
import sys
import re
from import_export import resources
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dash_board.models import Employee, Shipment
import os
from django.conf import settings  # <-- for fallback path

# 🔧 Logging Configuration
logger = logging.getLogger("import_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(handler)

# 🔢 Helper Functions
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))

def validate_email_format(email):
    return "@" in email and "." in email

def format_ghana_number(raw):
    return raw.strip()

def validate_phone_format(phone):
    return phone.startswith("+233") and len(phone) >= 12

def generate_placeholder_email(row):
    name = row.get("first_name", "user").replace(" ", "").lower()
    return f"{name}{random.randint(1000, 9999)}@placeholder.local"




# 👤 Employee Resource
class EmployeeResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_success = 0
        self.row_skipped = 0
        self.row_failed = 0


    def before_import_row(self, row, **kwargs):
        row_number = kwargs.get("row_number", "unknown")
        email = row.get("email", "").strip()
        logger.info(f"⚙️ Processing row {row_number}")
        try:
            if not email:
                email = generate_placeholder_email(row)
                row["email"] = email
                logger.info(f"ℹ️ Generated placeholder email — {email}")

            if not validate_email_format(email):
                logger.info(f"❌ Invalid email format — {email}")
                self.row_skipped += 1
                raise ValidationError("Invalid email format")

            if User.objects.filter(email=email).only("id").exists():
                logger.info(f"❌ Email already exists — {email}")
                self.row_skipped += 1
                raise ValidationError("User already exists")

            phone = format_ghana_number(row.get("phone", ""))
            if not validate_phone_format(phone):
                logger.info(f"❌ Invalid phone format — {phone}")
                self.row_skipped += 1
                raise ValidationError("Invalid phone number")

            row["phone"] = phone
            password = generate_random_password()

            user = User.objects.create_user(
                username=email.split("@")[0],
                email=email,
                password=password
            )
            row["user"] = user.pk

            # 🔒 Safe credential path setup
            fallback_path = os.path.join(settings.BASE_DIR, "logs", "generated_credentials.txt")
            default_path = "/tmp/generated_credentials.txt"

            creds_path = default_path
            if not os.access(os.path.dirname(default_path), os.W_OK):
                creds_path = fallback_path

            os.makedirs(os.path.dirname(creds_path), exist_ok=True)

            try:
                with open(creds_path, "a", encoding="utf-8") as cred_file:
                    cred_file.write(f"{email},{password}\n")
            except Exception as cred_err:
                logger.info(f"⚠️ Failed to store credentials — {cred_err}")

            logger.info(f"✅ Created user for {email}")
            self.row_success += 1

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"🔥 Unexpected error for {email} — {str(e)}", exc_info=True)
            self.row_failed += 1
            raise ValidationError(f"Critical error: {str(e)}")


        def save_instance(self, instance, is_create, row, **kwargs):
            logger.info(f"➡️ Attempting to save: {instance.__dict__}")
            try:
                super().save_instance(instance, is_create, row, **kwargs)
                persisted = Employee.objects.filter(email=instance.email).first()
                if persisted:
                    logger.info(f"✅ DB Save confirmed: {persisted.pk} — {persisted.email}")
                else:
                    logger.warning(f"⚠️ Save skipped — no record found for {instance.email}")
            except Exception as e:
                logger.error(f"❌ Save failed: {e}", exc_info=True)
                raise

        def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
            logger.info("📦 Import Summary")
            logger.info(f"✅ Success: {self.row_success} rows")
            logger.info(f"❌ Skipped: {self.row_skipped} rows")
            logger.info(f"🔥 Failed: {self.row_failed} rows")

        class Meta:
            model = Employee
            fields = (
                "first_name", "last_name", "email",
                "department", "position", "location", "company", "phone", "date_joined"
            )
            import_id_fields = ["email"]
            skip_unchanged = True
            report_skipped = True
            use_bulk = True
            use_transactions = False

# 🚚 Shipment Resource
class ShipmentResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row_number = kwargs.get("row_number", "unknown")
        fk_email = row.get("employee_email")
        if not Employee.objects.filter(email=fk_email).exists():
            logger.warning(f"🚫 Row {row_number}: No Employee found for email: {fk_email}")
            raise ValidationError(f"Missing Employee with email: {fk_email}")

    def save_instance(self, instance, is_create, row, **kwargs):
        logger.info(f"📦 Attempting to save Shipment: {instance.__dict__}")
        try:
            super().save_instance(instance, is_create, row, **kwargs)
            persisted = Shipment.objects.filter(id=instance.id).first()
            if persisted:
                logger.info(f"✅ Shipment saved: {persisted}")
            else:
                logger.warning(f"⚠️ Shipment record not found after save")
        except Exception as e:
            logger.error(f"❌ Shipment save failed: {e}", exc_info=True)
            raise

    class Meta:
        model = Shipment
        fields = "__all__"
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        use_transactions = False

