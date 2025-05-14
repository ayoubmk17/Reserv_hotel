from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, register_view, logout_view

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='users')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
] + router.urls