from import_export import resources
from django.core.exceptions import ValidationError

from dash_board.models import Employee
from django.contrib.auth.models import User
from dash_board.models import Category

class EmployeeResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        required_fields = [
            'first_name', 'last_name', 'email',
            'department', 'position', 'location',
            'company', 'phone'
        ]

        missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
        if missing_fields:
            raise ValidationError(
                f"Row rejected — missing required fields: {', '.join(missing_fields)}"
            )

        # Extract and sanitize data
        first_name = row['first_name'].strip()
        last_name = row['last_name'].strip()
        email = row['email'].strip()
        department = row['department'].strip()
        position = row['position'].strip()
        location = row['location'].strip()
        company = row['company'].strip()
        phone = row['phone'].strip()

        # Validate email format
        if '@' not in email:
            raise ValidationError(f"Invalid email format: {email}")

        # Prevent duplicate email entries
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Email already exists: {email}")

         # Safe username fallback
        username = email.split('@')[0]
        

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': User.objects.make_random_password(),
            }
        )

        row['user'] = user.pk
        row['department'] = department
        row['position'] = position
        row['location'] = location
        row['company'] = company
        row['phone'] = phone

    class Meta:
        model = Employee
        fields = ('user', 'department', 'position', 'location', 'company', 'phone')



