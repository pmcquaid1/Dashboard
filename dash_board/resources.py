import random
import string

from import_export import resources
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from dash_board.models import Employee


def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))


class EmployeeResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        try:
            # ✅ Handle missing or malformed email
            email = row.get('email', '').strip()
            if not email:
                fname = row.get('first_name', 'unknown').strip().lower()
                lname = row.get('last_name', 'unknown').strip().lower()
                email = f"{fname}.{lname}.{random.randint(1000,9999)}@placeholder.local"
                row['email'] = email

            if '@' not in email or '.' not in email.split('@')[-1]:
                raise ValidationError(f"Row rejected: invalid email format — {email}")

            if User.objects.filter(email=email).exists():
                raise ValidationError(f"Row rejected: user with this email already exists — {email}")

            # ✅ Normalize Ghana phone numbers
            phone = row.get('phone', '').strip()
            if len(phone) == 10 and phone.startswith('0'):
                phone = '+233' + phone[1:]
            elif len(phone) == 9 and phone.isdigit():
                phone = '+233' + phone
            elif phone.startswith('+233') and len(phone.replace('+', '')) == 12:
                pass  # already valid
            else:
                raise ValidationError(f"Row rejected: invalid Ghana phone format — {phone}")

            row['phone'] = phone

            # ✅ Create linked User account
            password = generate_random_password()
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=password
            )
            row['user'] = user.pk

        except Exception as e:
            raise ValidationError(f"Row import failed: {str(e)}")

    class Meta:
        model = Employee
        fields = (
            'user', 'first_name', 'last_name', 'email',
            'department', 'position', 'location',
            'company', 'phone'
        )
        import_id_fields = ['email']  # ✅ New entry only
        skip_unchanged = True
        report_skipped = True







