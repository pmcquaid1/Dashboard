from import_export import resources
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from dash_board.models import Employee

class EmployeeResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        # ✅ Basic required field check
        required_fields = ['email']
        missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
        if missing_fields:
            raise ValidationError(f"Missing required field(s): {', '.join(missing_fields)}")

        # ✅ Sanitize email and validate format
        email = row.get('email', '').strip()
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise ValidationError(f"Invalid email format: {email}")

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"A user with email {email} already exists.")

        # ✅ Create User and link to row
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password=password
        )
        row['user'] = user.pk

    class Meta:
        model = Employee
        fields = (
            'user', 'first_name', 'last_name', 'email',
            'department', 'position', 'location',
            'company', 'phone'
        )







