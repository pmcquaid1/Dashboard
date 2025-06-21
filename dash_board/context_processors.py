# dash_board/context_processors.py
from .models import Employee

def employee_context(request):
    """
    Adds the logged-in user's Employee instance to the template context.
    """
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            return {'employee': employee}
        except Employee.DoesNotExist:
            return {'employee': None}
    return {'employee': None}

def user_permissions_context(request):
    """
    Adds the user's permissions as a set to the template context.
    """
    if request.user.is_authenticated:
        permissions = request.user.get_all_permissions()
        return {'user_permissions': permissions}
    return {'user_permissions': set()}
