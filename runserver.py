import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Reserv_hotel.settings")
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv) 