import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Reserv_hotel.settings')
django.setup()

from django.conf import settings
from hotel_app.models import Hotel, RoomType, Room
from users_app.models import User

def run():
    owner = User.objects.get(id=1)
    images_dir = os.path.join(settings.MEDIA_ROOT, 'hotels')
    images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

    hotel_data = [
        # name, description, address, city, country, email, phone, base_price
        ("Riad Bahia Salam", "Un magnifique riad au cœur de la médina.", "123 rue de la Médina", "Marrakech", "Maroc", "riad.bahia@example.com", "+212600000001", 120.00),
        ("Nordic", "Hôtel moderne avec vue sur la mer.", "456 avenue du Nord", "Stockholm", "Suède", "nordic@example.com", "+4680000002", 150.00),
        ("Golden Lotus", "Un hôtel de luxe au centre-ville.", "789 rue Lotus", "Bangkok", "Thaïlande", "golden.lotus@example.com", "+6620000003", 180.00),
        ("Fernhill Lodge", "Lodge paisible entouré de nature.", "12 Fernhill Road", "Queenstown", "Nouvelle-Zélande", "fernhill@example.com", "+6430000004", 110.00),
        ("Baobab", "Hôtel écologique sous les baobabs.", "Route du Baobab", "Dakar", "Sénégal", "baobab@example.com", "+2210000005", 90.00),
        ("Estancia del Cielo", "Hacienda traditionnelle argentine.", "Camino del Cielo", "Salta", "Argentine", "estancia@example.com", "+5400000006", 130.00),
        ("Hôtel Parc", "Hôtel familial près du parc.", "Parc Central", "Paris", "France", "parc@example.com", "+3310000007", 140.00),
        ("Hôtel Parc 2", "Deuxième hôtel du parc.", "Parc Central", "Paris", "France", "parc2@example.com", "+3310000008", 135.00),
        ("Hôtel 582852843", "Hôtel générique.", "Adresse inconnue", "Ville", "Pays", "hotel582@example.com", "+3300000009", 100.00),
        ("Hôtel 551615244", "Hôtel générique.", "Adresse inconnue", "Ville", "Pays", "hotel551@example.com", "+3300000010", 100.00),
    ]

    for i, image in enumerate(images):
        if i >= len(hotel_data):
            break
        name, description, address, city, country, email, phone, base_price = hotel_data[i]
        image_path = os.path.join('hotels', image)
        hotel, created = Hotel.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'address': address,
                'city': city,
                'country': country,
                'email': email,
                'phone': phone,
                'image': image_path,
                'base_price': base_price,
                'owner': owner,
            }
        )
        if created:
            print(f"Hôtel créé : {hotel.name}")
        else:
            print(f"Hôtel déjà existant : {hotel.name}")
        # Créer un RoomType
        room_type, _ = RoomType.objects.get_or_create(
            hotel=hotel,
            name='standard',
            defaults={
                'description': 'Chambre standard confortable.',
                'base_price': base_price,
                'capacity': 2,
                'amenities': 'WiFi, TV, Climatisation',
            }
        )
        # Créer une Room
        Room.objects.get_or_create(
            hotel=hotel,
            room_type=room_type,
            room_number=f"{i+1}01",
            floor=i+1,
            defaults={
                'is_available': True
            }
        )
        print(f"Chambre ajoutée à l'hôtel {hotel.name}")

if __name__ == "__main__":
    run() 