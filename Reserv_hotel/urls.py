from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    # API URLs
    path('api/users/', include('users_app.urls')),
    path('api/hotels/', include('hotel_app.urls')),
    path('api/reservations/', include('reservations_app.urls')),
    path('api/reviews/', include('reviews_app.urls')),
    path('api/promotions/', include('promotions_app.urls')),
    # Application URLs
    path('', include('hotel_app.urls')),
    path('', include('users_app.urls')),  # URLs d'authentification
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)