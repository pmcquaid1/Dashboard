# imports
import random, string, logging, sys, re, os
from import_export import resources
from import_export.formats.base_formats import CSV
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from dash_board.models import Employee, Shipment
import logging
logger = logging.getLogger(__name__)

# 🔧 Logging Configuration
logger.info("🧪 Running local resources.py")
logger = logging.getLogger("import_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
logger.addHandler(handler)

# 🔧 Helper Functions
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))

def validate_email_format(email):
    return "@" in email and "." in email

def format_ghana_number(raw):
    try:
        if raw is None or str(raw).strip() == "":
            return ""

        phone_str = str(raw).strip()

        # Convert scientific notation manually
        sci_match = re.match(r"^(\d+)(?:\.(\d+))?[eE]\+?(\d+)$", phone_str)
        if sci_match:
            int_part, frac_part, exponent = sci_match.groups()
            frac_part = frac_part or ""
            total_digits = int_part + frac_part
            phone_str = total_digits.ljust(int(exponent) + 1, "0")


        # Remove non-digit characters
        digits_only = re.sub(r"\D", "", phone_str)

        # Format Ghana number
        if len(digits_only) >= 12 and digits_only.startswith("233"):
            return "+233" + digits_only[3:12]
        elif len(digits_only) == 10 and digits_only.startswith("0"):
            return "+233" + digits_only[1:]
        elif len(digits_only) == 9:
            return "+233" + digits_only
        else:
            return ""
    except Exception as e:
        logger.warning(f"⚠️ Failed to format phone number: {raw} — {e}")
        return ""

def validate_phone_format(phone):
    return phone.startswith("+233") and len(phone) == 13 and phone[1:].isdigit()

def generate_placeholder_email(row):
    name = row.get("first_name", "user").replace(" ", "").lower()
    return f"{name}{random.randint(1000, 9999)}@placeholder.local"


EMAIL_DISPATCH_ENABLED = getattr(settings, "EMAIL_DISPATCH_ENABLED", False)


def send_login_email(email, password, first_name):
    logger.info(f"📧 Dispatch triggered for: {email} | Password: {password}")
    if not EMAIL_DISPATCH_ENABLED:
        logger.info(f"📧 [Simulated] Would send login email to: {email} with password: {password}")
        return

    subject = "Welcome to SLLHub – Your Login Details"
    message = f"""Hi {first_name},

Welcome to SLLHub! This resource centre will give you access to information to assist you
with your daily work as well as provide HR Support.

Your login credentials have been created:

🔐 Email: {email}
🔐 Temporary Password: {password}

👉 Please log in at https://sllhub.com and change your password immediately to keep your account secure.

If you have any questions, feel free to reach out.

Best regards,  
SLLHub Team
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)



# 👤 Employee Resource
class EmployeeResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_success = 0
        self.row_skipped = 0
        self.row_failed = 0
        self.creds_path = os.path.join(settings.BASE_DIR, "logs", "generated_credentials.txt")
        os.makedirs(os.path.dirname(self.creds_path), exist_ok=True)
        logger.info(f"📝 Credential log path initialized: {self.creds_path}")

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
                logger.warning(f"❌ Row {row_number} skipped: invalid email format ({email})")
                self.row_skipped += 1
                raise ValidationError("Invalid email format")

            phone = format_ghana_number(row.get("phone", ""))
            logger.info(f"📞 Raw phone: {row.get('phone')} → Formatted: {phone}")

            if not validate_phone_format(phone):
                logger.warning(f"❌ Row {row_number} skipped: invalid phone format ({phone})")
                self.row_skipped += 1
                raise ValidationError("Invalid phone number")

            row["phone"] = phone
            password = generate_random_password()

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                logger.info(f"🔄 Email exists — updating password for {email}")
                existing_user.set_password(password)
                existing_user.save()
                row["user"] = existing_user

            else:
                user = User.objects.create_user(
                    username=email.split("@")[0],
                    email=email,
                    password=password
                )
                row["user"] = user


            self.row_success += 1

            # ✉️ Credential Logging + Email Dispatch
            logger.info(f"📋 Attempting credential write for: {email} | Password: {password}")
            try:
                with open(self.creds_path, "a", encoding="utf-8") as cred_file:
                    cred_file.write(f"{email},{password}\n")
            except Exception as e:
                logger.warning(f"⚠️ Failed to write credentials for {email}: {e}")

            try:
                send_login_email(email, password)
                logger.info(f"📧 Sent login email to {email}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to send email to {email}: {e}")

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"🔥 Unexpected error for row {row_number} — {email} — {str(e)}", exc_info=True)
            self.row_failed += 1
            raise ValidationError(f"Critical error: {str(e)}")

    def save_instance(self, instance, is_create, row, **kwargs):
        logger.info(f"➡️ Attempting to save: {instance.__dict__}")
        try:
            instance.user = row.get("user")  # 👈 Add this line
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
        print("\n📊 Debug Summary")
        print(f"✅ Successful rows: {self.row_success}")
        print(f"❌ Skipped rows: {self.row_skipped}")
        print(f"🔥 Failed rows: {self.row_failed}")

    class Meta:
        model = Employee
        fields = (
            "first_name", "last_name", "email", "department", "position",
            "location", "company", "phone", "date_joined"
        )
        import_id_fields = ["email"]
        skip_unchanged = True
        report_skipped = True
        use_bulk = False
        use_transactions = False

# 🚚 Shipment Resource (unchanged)
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
                logger.warning("⚠️ Shipment record not found after save")
        except Exception as e:
            logger.error(f"❌ Shipment save failed: {e}", exc_info=True)
            raise

    class Meta:
        model = Shipment
        fields = "__all__"
        skip_unchanged = True
        report_skipped = True
        use_bulk = False
        use_transactions = False

