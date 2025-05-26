import os
import sys
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Reserv_hotel.settings")
    
    # Configuration pour HTTPS
    sys.argv = [
        'manage.py',
        'runserver_plus',
        '--cert-file',
        'Reserv_hotel/ssl/certificate.crt',
        '--key-file',
        'Reserv_hotel/ssl/private.key',
        '0.0.0.0:8000'
    ]
    
    execute_from_command_line(sys.argv) 