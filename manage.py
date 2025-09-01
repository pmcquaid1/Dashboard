#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Use Heroku config var if set, otherwise default to test
    settings_module = os.getenv('DJANGO_SETTINGS_MODULE') or 'app.settings_test'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    # Enforce production settings only if HEROKU_APP_NAME indicates prod
    heroku_app = os.getenv('HEROKU_APP_NAME', '')
    if heroku_app.endswith('-prod') and settings_module != 'app.settings.prod':
        raise RuntimeError(
            f"App '{heroku_app}' must use 'app.settings.prod', but got '{settings_module}'"
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


