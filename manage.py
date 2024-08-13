#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
# Get the PORT from the environment variable
    port = os.environ.get('PORT', '8000')  # Default to port 8000 for local development

# #     # Run the development server on 0.0.0.0 and the specified port
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:' + port])

if __name__ == '__main__':
    main()


#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()