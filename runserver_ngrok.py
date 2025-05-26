import os
import sys
from pyngrok import ngrok
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Reserv_hotel.settings")
    
    # Démarrer ngrok
    http_tunnel = ngrok.connect(8000)
    print(f"\nNgrok tunnel URL: {http_tunnel.public_url}\n")
    
    # Démarrer le serveur Django
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv) 