import random
import string

from import_export import resources
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from dash_board.models import Employee

# ✅ Random password generator
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))


class EmployeeResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        # ✅ Sanitize and validate email
        email = row.get('email', '').strip()
        if not email:
            raise ValidationError("Missing required field: email")

        if '@' not in email or '.' not in email.split('@')[-1]:
            raise ValidationError(f"Invalid email format: {email}")

        if User.objects.filter(email=email).exists():
            raise ValidationError(f"A user with this email already exists: {email}")

        # ✅ Create user with generated password
        password = generate_random_password()
        user = User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password=password
        )

        row['user'] = user.pk  # ✅ Link user to Employee record

    class Meta:
        model = Employee
        fields = (
            'user', 'first_name', 'last_name', 'email',
            'department', 'position', 'location',
            'company', 'phone'
        )
        import_id_fields = []            # ✅ Forces create-only mode
        skip_unchanged = True
        report_skipped = True










